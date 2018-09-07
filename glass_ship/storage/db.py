"""  create connection to postgres, create session interface """
# engine = create_engine('postgresql://localhost/DATABASE')

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://localhost/glassship')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """
    Initializes all imported tables in the specified database
    :return: None
    """
    import application.models
    Base.metadata.create_all(bind=engine)