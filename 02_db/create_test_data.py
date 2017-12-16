from datetime import datetime
from dateutil.relativedelta import relativedelta

import factory
from envparse import env
from factory.compat import UTC
from factory.fuzzy import FuzzyDateTime, FuzzyText
from sqlalchemy import Column, BigInteger, Unicode, DateTime, UnicodeText, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

env.read_envfile()
engine = create_engine(env('DATABASE_URL'))
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


# declare models
class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger(), primary_key=True)
    username = Column(Unicode(50), unique=True, nullable=False)
    email = Column(Unicode(255))
    first_name = Column(Unicode(30), nullable=False)
    last_name = Column(Unicode(150), nullable=False)
    last_login_at = Column(DateTime)
    blocked_at = Column(DateTime)


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(BigInteger(), primary_key=True)
    text = Column(UnicodeText, nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)


# declare factories
class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: 'username {}'.format(n))
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    last_login_at = FuzzyDateTime(datetime(2017, 1, 1, tzinfo=UTC))

    class Meta:
        model = User
        sqlalchemy_session = session


class CommentFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    text = FuzzyText(length=100)
    user_id = factory.SubFactory(UserFactory)
    created_at = FuzzyDateTime(datetime(2017, 1, 1, tzinfo=UTC))

    class Meta:
        model = Comment
        sqlalchemy_session = session


# create test data
users = UserFactory.create_batch(100)
for user in users:
    CommentFactory.create_batch(100, user_id=user.id)

# blocked users 1 year ago and last login in last month
now = datetime.now().replace(tzinfo=UTC)
month_ago = now - relativedelta(month=1)
two_years_ago = now - relativedelta(year=2)
year_ago = now - relativedelta(year=1)

a = UserFactory.create_batch(
    100,
    blocked_at=FuzzyDateTime(two_years_ago, year_ago).fuzz(),
    last_login_at=FuzzyDateTime(month_ago).fuzz()
)

# biggest amount of daily comments
CommentFactory.create_batch(200, user_id=users[0].id, created_at=FuzzyDateTime(year_ago, year_ago).fuzz())

# blocked less than year ago
UserFactory.create_batch(100, blocked_at=FuzzyDateTime(datetime(2017, 9, 1, tzinfo=UTC)).fuzz())

# not blocked users
UserFactory.create_batch(200)

# commit session changes
session.commit()
