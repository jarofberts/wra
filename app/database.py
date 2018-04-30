import configparser
import os
from datetime import date
from enum import Enum

from wra.app.data_model import unpack_typing
from wra.app.data_model.client import Client

import sqlite3

CONFIG_PATH = 'app.conf'


def sqlite_column_type(obj: type):
    if obj == bytes:
        column_type = 'blob'
    elif obj == str:
        column_type = 'text'
    elif type(obj) == type(Enum) or obj in (int, date, bool):
        column_type = 'integer'
    else:
        raise NotImplementedError
    return column_type


def sqlite_object_table_schema(obj: type):
    column_defs = []
    for member_name, member_type in dict(obj.__annotations__).items():
        type_details = unpack_typing(member_type)
        column_type = sqlite_column_type(type_details['of'] if type_details['of'] else type_details['type'])
        column_defs.append('%s %s' % (member_name, column_type))
    return column_defs


def sqlite_table_def(obj: type, table_name: str):
    columns = ',\n  '.join(sqlite_object_table_schema(obj))
    table_sql = 'create table if not exists %s (\n  %s\n);' % (table_name, columns)
    return table_sql


def get_config_path(path: str=None):
    if not path:
        path = os.path.join(os.path.split(__file__)[0], globals()['CONFIG_PATH'])
    return path


def get_config(path: str):
    path = get_config_path(path)
    cp = configparser.ConfigParser()
    cp.read(path)
    return cp


def config_to_dict(path: str):
    cp = get_config(path)
    return {name: dict(cp.items(section=name)) for name in dict(cp.items()).keys()}


def db_path(config_path=None):
    config = config_to_dict(config_path)
    return os.path.abspath(os.path.join(os.path.split(os.path.abspath(get_config_path(config_path)))[0],
                                        config[config['DEFAULT']['database_type']]['location']))


def get_object_table(obj:type, config_path=None):
    config = config_to_dict(config_path)
    return config['tables'][obj.__name__.lower()]


def set_object_table(obj: type, table_name, path=None):
    path = get_config_path(path)
    cp = configparser.ConfigParser()
    cp.read(path)
    try:
        cp.add_section('tables')
    except configparser.DuplicateSectionError:
        # tables already exists
        pass
    cp.set('tables', obj.__name__.lower(), table_name)
    with open(path, 'w') as fp:
        cp.write(fp)


def save(obj, table_name: str=None, db=None):
    if not table_name:
        table_name = get_object_table(type(obj))
    columns = []
    values = []
    for field, field_type in dict(obj.__annotations__).items():
        columns.append(field)
        value = obj.__getattribute__(field)
        type_info = unpack_typing(field_type)
        column_type = sqlite_column_type(type_info['of'] if type_info['of'] else field_type)
        if column_type == 'text':
            if type(value) == list:
                value = '\n'.join(value)
            else:
                value = str(value) if value else ''
        elif column_type == 'integer':
            if type(type(value)) == type(Enum):
                value = [member for member in type(value).__members__.values() if value == member][0].value
            elif type(value) == date:
                value = value.toordinal()
            else:
                value = int(value) if value else 0
        elif column_type == 'data':
            value = sqlite3.Binary(value)
        values.append(value)
    command = 'insert into {table} ({columns}) values ({values});'.format(
        table=table_name, columns=','.join(columns), values=','.join(['?']*len(columns)))
    if not db:
        db = get_db()
    db.row_factory = sqlite3.Row
    db.execute(command, values)
    db.commit()


def get_db(config_path: str=None):
    config = config_to_dict(config_path)
    path2db = db_path(config_path)
    if config['DEFAULT']['database_type'].lower()[:6] == 'sqlite':
        os.makedirs(os.path.split(path2db)[0], exist_ok=True)
        db = sqlite3.connect(os.path.relpath(path2db))
        return db


def create_table(table_name, obj: type, db=None):
    """Create the database."""
    if not db:
        db = get_db()
    db.row_factory = sqlite3.Row
    db.executescript(sqlite_table_def(obj, table_name))
    db.commit()
    set_object_table(obj, table_name)
    print('Initialized the database.')


if __name__ == '__main__':
    create_table(table_name='clients', obj=Client)
