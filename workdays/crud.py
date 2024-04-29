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
def select_group(group_id):
    conn = get_db()
    row = conn.execute('''
                 SELECT * FROM groups WHERE id=?''', (group_id,)).fetchone()
    
    group = load_blob(row)
    
    return group


def stringfy_list(mylist):

    string = ', '.join(mylist)
    return string


    
    
# # deletes a group and its members
# def delete_group(resource):
#     conn = get_db()
#     print("deleting " + resource)
#     user_id = session['user_id']
    
#     # deletes all members
#     member_ids = get_member_ids(resource)
#     for m_id in member_ids:
#         conn.execute("""
#                 DELETE FROM members WHERE id=?""", (m_id,))
#     # deletes the group
#     conn.execute("""
#                 DELETE FROM groups WHERE user_id=? AND group_name=?""", (user_id, resource,))
    
#     conn.commit()

# # deletes a member
# def delete_member(resource):
    conn = get_db()
    # deletes a member
    conn.execute("""
                DELETE FROM members WHERE name=?""", (resource,))
    conn.commit()
   
def listify(mystring):
    lst = mystring.split(", ")
    return lst
 
# returns a list with all the group ids
def group_id_lst():
    conn = get_db()
    
    id_list = conn.execute('''SELECT id FROM groups''') .fetchall()
    
    ids = [i[0] for i in id_list]
    return ids

# creates or updates a group
def create_and_update(group):
    conn = get_db()
    
    ids = group_id_lst()

        
    if group['id'] in ids:
        blob = json.dumps(group)
        conn.execute('''
                    UPDATE groups 
                    SET user_id=?, blob=? 
                    WHERE id=?
                    ''', (group['user_id'], blob, group['id']))
        conn.commit()
    
    
    else:
        group['id'] = ids[-1] + 1
        blob = json.dumps(group)

        conn.execute('''
                    INSERT INTO groups (user_id, blob)
                    VALUES (?, ?)
                    ''', (group['user_id'], blob,))
        conn.commit()


def delete_group(group_id):
    conn = get_db()
    conn.execute('''
                 DELETE FROM groups WHERE id=?''', (int(group_id),))
    conn.commit()
    
