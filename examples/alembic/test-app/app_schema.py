from sqlalchemy import Column, Integer, MetaData, String, Table, Integer
import sqlalchemy_postgresql_audit.event_listeners.sqlalchemy

metadata = MetaData()

t = Table(
    "test",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("name", String, nullable=False),
    Column("external_id", Integer, nullable=False),
    info={
        "audit.options": {
            "enabled": True,
            "session_settings": [
                Column("username", String, nullable=False),
            ],
        }
    },
    schema="public",
)
