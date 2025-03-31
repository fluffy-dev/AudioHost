import asyncio

from typer import Option, Typer
from sqlalchemy.exc import IntegrityError


from src.apps.user.entity import UserEntity
from src.apps.user.models.user import UserModel
from src.apps.user.dto import UserDTO

from src.config.database.engine import db_helper

from src.libs.exceptions import AlreadyExistError

app = Typer()

async def create_user(user_entity: UserEntity):
    async with db_helper.get_session() as session:
        user = UserModel(**user_entity.__dict__)
        session.add(user)
        try:
            await session.commit()
            print(f"{user.name} {user.email} successfully created")
        except IntegrityError:
            raise AlreadyExistError(f"{user.email} is already exist")


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command(help="Create a new admin user")
def createsuperuser(
    name: str = Option(default="admin", help="user name"),
    surname: str = Option(default="admin", help="user surname"),
    email: str = Option("admin@example.com", help="user email"),
    password: str = Option("admin", prompt="user password", hide_input=True),
):
    dto = UserDTO(
        name=name,
        surname=surname,
        email=email,
        password=password,
        is_admin=True
    )
    user_entity = UserEntity(**dto.model_dump())

    asyncio.run(create_user(user_entity))


if __name__ == "__main__":
    app()
