#!/usr/bin/env python3
""" User module
"""
import hashlib
from models.base import Base


class User(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        if pwd is None or not isinstance(pwd, str):
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd):
        if pwd is None or not isinstance(pwd, str):
            return False
        if self.password is None:
            return False
        pwd_hash = hashlib.sha256(pwd.encode()).hexdigest().lower()
        return pwd_hash == self.password

    def display_name(self):
        if self.email is None and self.first_name is None and self.last_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return self.email
        if self.last_name is None:
            return self.first_name
        if self.first_name is None:
            return self.last_name
        return f"{self.first_name} {self.last_name}"