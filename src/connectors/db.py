from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


def create_session():
    engine = create_engine("mysql+pymysql://root:1q2w3e@localhost:3306/people-api")
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
