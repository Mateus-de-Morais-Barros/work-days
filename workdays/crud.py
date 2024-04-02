from workdays.db import get_db
from flask import session, request
import json

# returns all groups of the logged user
def get_groups():
    user_id = session['user_id']
    conn = get_db()
    allrows = conn.execute('''
                 SELECT * FROM groups WHERE user_id=?''', (user_id,)).fetchall()
    return allrows

# returns a blob string from a row
def load_blob(row):
    blob = json.loads(row[2])
    return blob

# returns a list of dicts
def load_groups():
    allrows = get_groups()
    dict_list = []
    for row in allrows:
        dict_list.append(load_blob(row))
    return dict_list 

# returns only the selected group
def select_group(group_name):
    groups = load_groups()
    for group in groups:
        if group["name"] == group_name:
            print(group)
            return group

def stringfy_list(mylist):
    string = ','.join(mylist)
    return string



    
    
# deletes a group and its members
def delete_group(resource):
    conn = get_db()
    print("deleting " + resource)
    user_id = session['user_id']
    
    # deletes all members
    member_ids = get_member_ids(resource)
    for m_id in member_ids:
        conn.execute("""
                DELETE FROM members WHERE id=?""", (m_id,))
    # deletes the group
    conn.execute("""
                DELETE FROM groups WHERE user_id=? AND group_name=?""", (user_id, resource,))
    
    conn.commit()

# deletes a member
def delete_member(resource):
    conn = get_db()
    # deletes a member
    conn.execute("""
                DELETE FROM members WHERE name=?""", (resource,))
    conn.commit()
    