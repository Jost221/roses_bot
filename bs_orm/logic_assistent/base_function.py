from .. import db_settings
from . import composit_function
import sqlite3


def serach(table_search: object, **qwargs) -> list:
    conn = sqlite3.connect(db_settings.path)
    cur = conn.cursor()
    request  = f'SELECT * FROM [{table_search.__name__}]'
    if qwargs != {}:
        request+=' WHERE'
        for atr, val in qwargs.items():
            if table_search.__dict__[atr].type_r != type(val):
                table_search.__dict__[atr].type_r(val)
            request+= f' {atr} = {val} AND'
        request = request[:-4]
    cur.execute(request)
    conn.commit()
    values = cur.fetchall()
    returned = []
    obj = {}
    from ..DataTypes import Table

    for line in values:
        column_names = iter(cur.description)
        for val in line:
            if val != None:
                atr = next(column_names)[0]
                col, val = table_search.__convert_of_read__(atr, val)
            else:
                col, val = next(column_names)[0], None
            obj[col] = val
        returned.append(type(table_search.__name__, (Table,), obj))
    conn.commit()
    conn.close()
    return returned

def update(objects, **qwargs):
    request=''
    for cls in objects:
        request+= f'UPDATE {cls.__name__} SET '
        new_flag = True
        for i in [qwargs, composit_function.clear_default(cls)]:
            flag = False
            for key, value in i.items():
                key, value = cls.__convert_to_write__(key, value)
                if value != 'NULL':
                    request += f'{key} = {value} AND '
                flag=True
            if flag:
                request = request[:-4]+' '
            if new_flag:    
                request = request.replace(' AND', ',')
                new_flag = False
            request += 'WHERE '
        request = request[:-6]
        request+=';\n'
        for k, v in qwargs.items():
            setattr(cls, k, v)
    conn = sqlite3.connect(db_settings.path)
    cur = conn.cursor()
    cur.executescript(request)
    conn.commit()
    conn.close()
    return True

def save(cls) -> bool:
    conn = sqlite3.connect(db_settings.path)
    cur = conn.cursor()
    try:
        cls_value = composit_function.clear_default(cls)
        request = f'INSERT INTO [{cls.__name__}] ('
        values = 'VALUES ('
        for k, v in cls_value.items():
            k, v = cls.__convert_to_write__(k, v)
            request+=f'{k}, '
            values+=f'{v}, '
        request = request[:-2] + ')'
        values = values[:-2] + ')'
        cur.execute(request+values)
        conn.commit()
        conn.close()
        return True
    except Exception as ex:
        raise Exception(
            f'well congratulations your father goes fucking you with a chair on the head with these words: {ex}')
    
def execute(cls, execut: str) -> list[any]:
    conn = sqlite3.connect(db_settings.path)
    cur = conn.cursor()
    cur.execute(execut)
    conn.commit()
    conn.close()
    return cur.fetchall()

def add_if_not_exist(cls, **qwargs) -> bool:
    if len(cls.search(**qwargs)) != 0:
        return False
    obj = qwargs
    from ..DataTypes import Table
    new_cls = type(cls.__name__, (Table,), obj)
    return new_cls.save()

def add(cls, **qwargs) -> bool:
    obj = qwargs
    from ..DataTypes import Table
    new_cls = type(cls.__name__, (Table,), obj)
    new_cls.save()

def create(cls, **qwargs):
    obj = qwargs
    from ..DataTypes import Table
    new_cls = type(cls.__name__, (Table,), obj)
    return new_cls