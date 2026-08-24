from aiokafka import AIOKafkaConsumer
import json
from app.core.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_POLICY_PROPOSED_TOPIC
from app.db.database import SessionLocal
from app.schemas.events import PolicyProposedEvent
from app.services.logical_task_service import process_policy_proposed

async def consume_policy_proposed():
    consumer = AIOKafkaConsumer(
        KAFKA_POLICY_PROPOSED_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="ms-p04-logical-task-management-test",
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        ),
    )

    await consumer.start()

    try:
        async for message in consumer:

            db = SessionLocal()

            try:
                event = PolicyProposedEvent.model_validate(
                    message.value
                )

                task = process_policy_proposed(
                    db=db,
                    event=event,
                )

                print(
                    f"Logical task created: {task.task_id}"
                )

                await consumer.commit()

            except Exception as error:
                db.rollback()

                print(
                    f"Failed processing POLICY_PROPOSED: {error}"
                )

            finally:
                db.close()

    finally:
        await consumer.stop()
        