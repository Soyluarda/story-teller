from sqlalchemy import Column, DateTime, MetaData, Sequence, Table
from sqlalchemy.sql.sqltypes import Integer, String

metadata = MetaData()


users = Table(
    "users",
    metadata,
    Column("id", Integer, Sequence("user_id_seq"), primary_key=True),
    Column("email", String(100)),
    Column("password", String(100)),
    Column("username", String(50)),
    Column("created_at", DateTime),
    Column("status", String(1)),
)
