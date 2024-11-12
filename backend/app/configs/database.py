import databases
import sqlalchemy

from app.configs.environs import config

metadata = sqlalchemy.MetaData()

post_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("image", sqlalchemy.String),
)

connect_args = (
    {} if "postgresql" in config.DATABASE_URL else {"check_same_thread": False}
)
engine = sqlalchemy.create_engine(config.DATABASE_URL, connect_args=connect_args)

metadata.create_all(engine)
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)
