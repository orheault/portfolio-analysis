from sqlalchemy import Integer, Column, String
from app import db  # noqa
from typing import Any


class Search(db.Model):  # type: ignore
    """Search"""

    __tablenxame__ = "doodad"

    doodad_id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    purpose = Column(String(255))

    def update(self):
        for key, val in changes.items():
            setattr(self, key, val)
        return self

