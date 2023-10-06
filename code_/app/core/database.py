from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from flask_marshmallow import Marshmallow
from .config import config

db = SQLAlchemy(engine_options={"echo": False})
ma = Marshmallow()
migrate = Migrate()

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()
