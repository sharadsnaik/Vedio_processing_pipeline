from temporalio import activity
from DB.clickhouse import connect_client

@activity.defn
async def store_events(video_id: str, events: list[dict]):
    client = connect_client()

    rows = [
        (
            video_id,
            e["timestamp"],
            e["event_type"],
            e["confidence"],
        )
        for e in events
    ]

    client.insert(
        table="video_events",
        data=rows,
        column_names=[
            "video_id",
            "timestamp",
            "event_type",
            "confidence",
        ],
    )

    return len(rows)
