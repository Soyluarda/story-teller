from api.users import schema
from api.utils.database import database


def find_exist_user(email: str):
    query = "SELECT * from users WHERE status='1' and email = :email"
    return database.fetch_one(query=query, values={"email": email})

    # query = users.select().where(users.c.email == email)
    # return await database.fetch_one(query)


def find_exists_user(email: str):
    query = "SELECT * FROM users WHERE status='1' and email = :email"
    return database.fetch_one(query=query, values={"email": email})

    # query = users.select().where(users.c.email == email)
    # return await database.fetch_one(query)


def save_user(user: schema.UserCreate):
    query = "INSERT INTO users VALUES (nextval('user_id_seq'), :email, :password, :username, now() at time zone 'UTC', '1')"
    return database.execute(
        query=query,
        values={
            "email": user.email,
            "password": user.password,
            "username": user.username,
        },
    )
