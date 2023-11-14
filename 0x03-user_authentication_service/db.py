#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User

class DB:
    """DB class for interacting with the database
    """

    def __init__(self) -> None:
        """Initialize a new DB instance and create database tables if they do not exist
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object for interacting with the database
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Create a User object and save it to the database
        Args:
            email (str): user's email address
            hashed_password (str): password hashed by bcrypt's hashpw
        Return:
            Newly created User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Return a user who has an attribute matching the attributes passed as arguments
        Args:
            kwargs (dict): a dictionary of attributes to match the user
        Return:
            matching user or raise NoResultFound error
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found with the specified attributes")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes
        Args:
            user_id (int): user's id
            kwargs (dict): dict of key, value pairs representing the attributes to update and the values to update them with
        Return:
            No return value
        """
        try:
            user = self._session.query(User).filter_by(id=user_id).one()
            for attr, value in kwargs.items():
                setattr(user, attr, value)
            self._session.commit()
        except NoResultFound:
            raise ValueError("No user found with the specified user_id")
