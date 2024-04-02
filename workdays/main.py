from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from workdays.auth import login_required
from workdays.crud import load_groups, delete_group, delete_member, select_group, stringfy_list 

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('/index.html')

@bp.route('/group_selection')
@login_required
def group_selection():
    dict_list = load_groups()
    group_names = [name['name'] for name in dict_list]
    
    return render_template('/groups/group_selection.html', group_names=group_names)


@bp.route('/g_create', methods=('GET','POST'))
@login_required
def g_create():
    # data gathering
    group_name = request.args.get("resource")
    group = select_group(group_name)
    
    members = []
    for member in group["members"]:
        member['days_list'] = stringfy_list(member['days'])
        member['preference_list'] = stringfy_list(member['preference'])
        members.append(member)

    
    
    if group_name == "New Group":
        members = []
        return render_template('/groups/g_create.html', group_name=group_name, members=members)

    # members = get_member_names(group_name)
    return render_template('/groups/g_create.html', group_name=group_name, members=members)


@bp.route('/m_create', methods=('GET','POST'))
@login_required
def m_create():
    # data gathering
    group_name = request.args.get("resource")
    members = []

    if group_name == "New Group":
        members = []
        return render_template('/groups/m_create.html', group_name=group_name, members=members)
    
    
    # members = get_member_names(group_name)
    return render_template('/groups/m_create.html', group_name=group_name, members=members)


@bp.route('/g_delete', methods=('GET','POST'))
@login_required
def g_delete():
    # data gathering
    resource = request.args.get("resource")
    mode = request.args.get("mode")
    
    if mode == "group":
        delete_group(resource)
        return group_selection()
    
    if mode == "member":
        delete_member(resource)
        return g_create()

# logic    ----------------------------------------------

# def get_groups_names():
#     db = get_db()
#     user_id = session['user_id']
#     data = db.execute("SELECT * FROM groups WHERE user_id=?", (user_id,)).fetchall()
    
#     name_list = []
#     for row in data:
#         blob = json.loads(row[2])
#         group_name = blob["g_name"]
#         name_list.append(group_name)
#     return name_list


# def get_group(user_id, group_name):
#     data = get_db().execute(
#         'SELECT *'
#         ' FROM groups'
#         ' WHERE user_id = ?',
#         (user_id,)
#     ).fetchall()

#     for row in data:
#         blob = json.loads(row[2])
#         group = {}
#         if blob['g_name'] == group_name:
#             group['g_id'] = row[0]
#             group['user_id'] = row[1]
#             group['g_name'] = blob['g_name']
#             group['g_members'] = list(blob['g_members'].keys())
#             group['member_list'] = ', '.join([x for x in group['g_members']])

#             return group

# def group_data():
#     group = get_group()
#     g_id = group['g_id']
#     g_user_id = group['user_id']
#     g_name = list(group['g_data'].keys())[0]
#     g_members = [x for x in group['g_data']]
#     # if check_author and post['author_id'] != g.user['id']:
#     #     abort(403)
#     {
#     "g_name": "grupo_1",
#     "g_members": {
#         "breno": {
#             "days": [
#                 "18/02/2024",
#                 "16/02/2024",
#                 "20/02/2024"
#             ],
#             "preferred": [
#                 "any"
#             ]
#             }}}

# def create():
#     db = get_db()
#     db.execute("")
'''
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('main.index'))

    return render_template('main/create.html')

'''
'''
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('main.index'))

    return render_template('main/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('main.index'))
    
    '''