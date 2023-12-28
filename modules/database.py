import json
from PyQt6.QtWidgets import QMessageBox

from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase, JSONField

db = SqliteExtDatabase('./database/pw.db', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


class ListControlModel(BaseModel):
    id = PrimaryKeyField(null=False)
    telegram = CharField(max_length=100, null=False)
    date_telegram = DateField()
    date_deadline = DateField()
    description = TextField(null=True)
    number_lk = CharField(max_length=10, null=True)
    answer_telegram = CharField(max_length=100, null=True)
    date_answer = DateField(null=True)
    specialties_for_exec = JSONField()
    planes_for_exec = JSONField()
    planes_on_create = JSONField()
    complete_flag = BooleanField(default=False)

    class Meta:
        db_table = 'list_control'


class UnitModel(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=30)
    performs_work = BooleanField(default=True)

    class Meta:
        db_table = 'units'


class SubunitModel(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=30)

    class Meta:
        db_table = 'subunits'


class PlaneTypeModel(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=30)

    class Meta:
        db_table = 'plane_types'


class PlaneModel(BaseModel):
    id = PrimaryKeyField(null=False)
    tail_number = CharField(max_length=10)
    factory_number = CharField(max_length=30, null=True)
    unit = ForeignKeyField(UnitModel.id, backref='units', on_delete='cascade')
    plane_type = ForeignKeyField(PlaneTypeModel.id, backref='plane_types', on_delete='cascade')

    class Meta:
        db_table = 'planes'


class CheckModel(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=30)
    period = CharField(max_length=30)
    last_check = DateField()

    class Meta:
        db_table = 'checks'


class CompleteListModel(BaseModel):
    id_list = ForeignKeyField(ListControlModel, backref='completes', on_delete='cascade')
    id_plane = ForeignKeyField(PlaneModel, backref='planes', on_delete='cascade')
    id_subunit = ForeignKeyField(SubunitModel, backref='subunits', on_delete='cascade')

    class Meta:
        db_table = 'complete_list'
        primary_key = CompositeKey('id_list', 'id_plane', 'id_subunit')


def create_tables():
    with db:
        db.create_tables(
            [
                PlaneModel, PlaneTypeModel, UnitModel,
                SubunitModel, ListControlModel, CompleteListModel,
                CheckModel
            ]
        )

