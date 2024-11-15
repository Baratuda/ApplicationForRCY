
from sqlalchemy.ext.declarative import declarative_base
from config import engine
from sqlalchemy import  Integer, String, Column, ForeignKey

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

class LocalityClass(Base):
    __tablename__ = 'localityClass'
    __table_args__ = {'extend_existing': True}
    localityClassId = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    shortName = Column(String(200), nullable=False)
 
class Localities(Base):
    __tablename__ = 'localities'
    __table_args__ = {'extend_existing': True}
    localityId = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    localityClass_id = Column(Integer, ForeignKey('localityClass.localityClassId'))

class Sectors(Base):
    __tablename__ = 'sectors'
    __table_args__ = {'extend_existing': True}
    sectorID = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    locality_id = Column(Integer, ForeignKey('localities.localityId'))

class LocalityTowns(Base):
    __tablename__ = 'localityTowns'
    __table_args__ = {'extend_existing': True}
    localityTownId = Column(Integer, primary_key=True)
    numberHouseTo = Column(Integer, nullable=False)
    umberHouseDo = Column(Integer, nullable=False)
    street = Column(String(200), nullable=False)
    sector_id = Column(Integer, ForeignKey('sectors.sectorID'))

  