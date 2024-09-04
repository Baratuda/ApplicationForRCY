
from sqlalchemy.ext.declarative import declarative_base
from config import engine

Base = declarative_base()
Base.metadata.reflect(engine)

class FireTruks(Base):
    __table__ = Base.metadata.tables['todo_firetruk']

class FireFighters(Base):
    __table__ = Base.metadata.tables['todo_firefigthters']

class FireDepartment(Base):
    __table__ = Base.metadata.tables['todo_firedepartment']

class DistrictDepartment(Base):
    __table__ = Base.metadata.tables['todo_districtdepartment'] 

class COU(Base):
    __table__ = Base.metadata.tables['todo_cou']  

class NotCombatVinicles(Base):
    __table__ = Base.metadata.tables['todo_notcombatvinicles']    