import json
from PyQt6.QtWidgets import QMessageBox
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase, JSONField

db = SqliteExtDatabase('./database/pw.db', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


class ListControlM(BaseModel):
    id = PrimaryKeyField(null=False)
    telegram = CharField(max_length=100, null=False)
    date_telegram = DateField()
    date_deadline = DateField()
    description = TextField(null=True)
    number_lk = CharField(max_length=10, null=True)
    answer = CharField(max_length=100, null=True)
    answer_date = DateField(null=True)
    specialties_for_exec = JSONField()
    planes_for_exec = JSONField()
    planes_on_create = JSONField()
    complete_flag = BooleanField(default=False)

    class Meta:
        db_table = 'list_control'


class UnitM(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=30, unique=True)
    performs_work = BooleanField(default=True)

    class Meta:
        db_table = 'units'


class PlaneTypeM(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'plane_types'


class SubunitM(BaseModel):
    id = PrimaryKeyField(null=False)
    plane_type = ForeignKeyField(PlaneTypeM, backref='planes', on_delete='cascade')
    name = CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'subunits'


class PlaneM(BaseModel):
    id = PrimaryKeyField(null=False)
    tail_number = CharField(max_length=10)
    factory_number = CharField(max_length=30, null=True)
    unit = ForeignKeyField(UnitM, backref='planes', on_delete='cascade')
    plane_type = ForeignKeyField(PlaneTypeM, backref='planes', on_delete='cascade')
    deleted = BooleanField(default=False)

    class Meta:
        db_table = 'planes'


class CheckM(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=30, unique=True)
    period = CharField(max_length=30)
    last_check = DateField()

    class Meta:
        db_table = 'checks'


class CompleteLM(BaseModel):
    id_list = ForeignKeyField(ListControlM, backref='completes', on_delete='cascade')
    id_plane = ForeignKeyField(PlaneM, backref='planes', on_delete='cascade')
    id_subunit = ForeignKeyField(SubunitM, backref='subunits', on_delete='cascade')

    class Meta:
        db_table = 'complete_list'
        primary_key = CompositeKey('id_list', 'id_plane', 'id_subunit')


class SystemM(BaseModel):
    id = PrimaryKeyField(null=False)
    subunit_type = ForeignKeyField(SubunitM, backref='subunits', on_delete='cascade')
    plane_type = ForeignKeyField(PlaneTypeM, backref='systems', on_delete='cascade')
    name = CharField(max_length=30, null=False)


class AgregateM(BaseModel):
    id = PrimaryKeyField(null=False)
    id_system = ForeignKeyField(SystemM, backref='agregates', on_delete='cascade')
    name = CharField(max_length=30, null=False)
    amount = IntegerField(default=1)


class RemovedM(BaseModel):
    id = PrimaryKeyField(null=False)
    id_plane = ForeignKeyField(PlaneM, backref='removes', on_delete='cascade')
    id_agregate = ForeignKeyField(AgregateM, backref='agregates', on_delete='cascade')
    agr_number = CharField(max_length=30)
    note = CharField(max_length=100)


class DefectiveM(BaseModel):
    id = PrimaryKeyField(null=False)
    id_plane = ForeignKeyField(PlaneM, backref='defectives', on_delete='cascade')
    id_agregate = ForeignKeyField(AgregateM, backref='agregates', on_delete='cascade')
    agr_number = CharField(max_length=30, null=True)


def create_tables():
    with db:
        db.create_tables(
            [
                PlaneM, PlaneTypeM, UnitM,
                SubunitM, ListControlM, CompleteLM,
                CheckM, SystemM, AgregateM,
                RemovedM, DefectiveM
            ]
        )
