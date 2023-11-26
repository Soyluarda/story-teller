from api.utils.db import database
from api.auth import schema

def find_exist_user(email: str):
    query = "SELECT * from py_users WHERE status='1' and email = :email"
    return database.fetch_one(query=query, values={"email": email})

    #query = users.select().where(users.c.email == email)
    #return await database.fetch_one(query)


def find_exists_user(email: str):
    query = "SELECT * FROM py_users WHERE status='1' and email = :email"
    return database.fetch_one(query=query, values={"email": email})

    #query = users.select().where(users.c.email == email)
    #return await database.fetch_one(query)


def save_user(user: schema.UserCreate):
    query = "INSERT INTO py_users VALUES (nextval('user_id_seq'), :email, :password, :username, now() at time zone 'UTC', '1')"
    return database.execute(query=query, values={"email": user.email, "password": user.password, "username": user.username})
