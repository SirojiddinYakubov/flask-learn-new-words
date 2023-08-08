import getpass
import pathlib
from typing import Any

from . import ConfigMeta, make_attr

BASE_DIR = pathlib.Path(__file__).parents[3]

if getpass.getuser() == "yakubov":
    env_filename = ".env.dev"
else:
    env_filename = ".env.prod"

ENV_FILE_PATH = f"{BASE_DIR}/deploy/{env_filename}"


class Config(metaclass=ConfigMeta):
    """Set Flask config variables."""

    # General Config
    FLASK_ENV: str
    FLASK_APP: str
    FLASK_DEBUG: bool
    SECRET_KEY: str
    STATIC_FOLDER: str = f"{BASE_DIR}/code_/app/static"
    TEMPLATES_FOLDER: str = f'{BASE_DIR}/code_/app/templates'

    DATABASE_PORT: int
    DATABASE_PASSWORD: str
    DATABASE_USER: str
    DATABASE_NAME: str
    DATABASE_HOST: str

    # Database
    @staticmethod
    @make_attr("SQLALCHEMY_DATABASE_URI")
    def assemble_db_connection(values: dict[str, Any]) -> str:
        return "postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}".format(
            DATABASE_USER=values.get("DATABASE_USER"),
            DATABASE_PASSWORD=values.get("DATABASE_PASSWORD"),
            DATABASE_HOST=values.get("DATABASE_HOST"),
            DATABASE_PORT=values.get("DATABASE_PORT"),
            DATABASE_NAME=values.get("DATABASE_NAME"),
        )

    class Meta:
        env_file = ENV_FILE_PATH


config = Config()
