from workdays.db import get_db
from flask import session, request

# returns all groups of the logged user
def get_group():
    user_id = session['user_id']
    conn = get_db()
    allrows = conn.execute('''
                 SELECT * FROM groups WHERE user_id=?''', (user_id,)).fetchall()
    return allrows

# returns a list of groups names
def get_group_names():
    allrows = get_group()
    group_name = [row[1] for row in allrows]
    return group_name

# returns a list of member id's
def get_member_ids(group_name):
    user_id = session['user_id']
    
    conn = get_db()
    members_id = conn.execute('''
                 SELECT members_id FROM groups WHERE user_id=? AND group_name=?''', (user_id, group_name,)).fetchone()
    try:
        members_id = [int(x) for x in members_id[0].split(',')]
    except:
        members_id = []
        
    return members_id

def update_member_ids():
    pass

# returns a list of member names
def get_member_names(group_name):
    members_id = get_member_ids(group_name)
    m_id_list = []
    for m_id in members_id:
        conn = get_db()
        try:
            row = conn.execute('''
                        SELECT * FROM members WHERE id=?''', (m_id,)).fetchone()
            m_id_list.append(row[1])
        except:
            continue
    print(m_id_list)
    return m_id_list

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
    
    
    