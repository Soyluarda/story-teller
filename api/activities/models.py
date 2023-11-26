from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import String, Text

metadata = MetaData()


activities = Table(
    "activities",
    metadata,
    Column("id", String(50), primary_key=True),
    Column("title", String(100)),
    Column("story", Text),
)
