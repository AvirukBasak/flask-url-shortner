#!/bin/env python3

import sqlite3
import os

def init_db():
    if os.path.isfile('data/data.sqlite3'):
        print('database already exists')
        return
    else: os.makedirs('data', exist_ok=True)

    con = sqlite3.connect('data/data.sqlite3')
    cur = con.cursor()

    with open('dbmodels/schema_userdb.sql', 'r') as schema_userdb:
        schema = schema_userdb.read()
        cur.execute(schema)
        print('created table userdb')

    with open('dbmodels/schema_urldb.sql', 'r') as schema_urldb:
        schema = schema_urldb.read()
        cur.execute(schema)
        print('created table urldb')

    print('database initialised')
    con.close()

init_db()
