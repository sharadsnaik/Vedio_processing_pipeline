import clickhouse_connect

def connect_client():
    return clickhouse_connect.get_client(
        host="localhost",
        port=8123,          # HTTP port (default)
        username="default",
        password="",
        database="video_db",
    )
    # client.command("""
    #     CREATE TABLE IF NOT EXISTS video_metadata (
    #         video_id String,
    #         url String,
    #         path String,
    #         created_at DateTime DEFAULT now()
    #     ) ENGINE = MergeTree
    #     ORDER BY video_id
    # """)

    # client.insert(
    #     "video_metadata",
    #     [(video_id, url, path)],
    #     column_names=["video_id", "url", "path"],
    # )

    # return "inserted"