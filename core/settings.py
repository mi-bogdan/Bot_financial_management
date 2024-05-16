from dataclasses import dataclass

from environs import Env


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class DataBaseConfig:
    db_url: str


@dataclass
class Settings:
    bots: Bots
    database: DataBaseConfig


def get_settings(path: str) -> Settings:
    env = Env()
    env.read_env(path)
    return Settings(
        bots=Bots(bot_token=env.str("TOKEN_API"), admin_id=env.int("ADMIN_ID")),
        database=DataBaseConfig(
            db_url=f'postgresql+asyncpg://{env.str("DB_USER")}:{env.str("DB_PASSWORD")}@{env.str("DB_HOST")}:{env.str("DB_PORT")}/{env.str("DB_NAME")}'
        ),
    )


config = get_settings("env")
