from sqlalchemy import create_engine, Column, Integer, String, Date, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

engine = create_engine('sqlite:///alphawolf.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    points = Column(Integer, default=0)
    last_claim_date = Column(Date)

Base.metadata.create_all(engine)

# Initialize DB
def init_db():
    Base.metadata.create_all(engine)

# Add a new user
def add_user(telegram_id, username, referrer=None):
    user = User(telegram_id=telegram_id, username=username)
    session.add(user)
    session.commit()

    # Handle referral points
    if referrer:
        referred_user = session.query(User).filter_by(telegram_id=referrer).first()
        if referred_user:
            user.points += 50  # Points for being referred
            referred_user.points += 50  # Points for referrer
            session.commit()

# Get user points
def get_user_points(telegram_id):
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if user:
        return user.points
    return 0

# Update user points
def update_user_points(telegram_id, points):
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if user:
        user.points += points
        session.commit()
