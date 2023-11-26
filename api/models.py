from sqlalchemy import Table, Column, String, Integer, DateTime, Boolean, MetaData, ForeignKey, Sequence

metadata = MetaData()

users = Table(
    "py_users",
    metadata,
    Column("id", Integer, Sequence('user_id_seq'), primary_key=True),
    Column("email", String(100)),
    Column("password", String(100)),
    Column("username", String(50)),
    Column("created_at", DateTime),
    Column("status", String(1)),

)