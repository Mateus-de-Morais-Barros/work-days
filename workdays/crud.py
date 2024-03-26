from workdays.db import get_db
from flask import session

def get_group():
    # returns all groups of the logged user
    user_id = session['user_id']
    conn = get_db()
    allrows = conn.execute('''
                 SELECT * FROM groups WHERE user_id=?''', (user_id,)).fetchall()
    return allrows

def get_group_names():
    # returns a list of groups names
    allrows = get_group()
    group_name = [row[1] for row in allrows]
    return group_name

