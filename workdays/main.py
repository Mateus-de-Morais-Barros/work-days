from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from workdays.auth import login_required
from workdays.crud import create_and_update, delete_group, group_id_lst, listify, load_groups, select_group, stringfy_list

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('/index.html')

#tela de seleção de grupos
@bp.route('/group_selection')
@login_required
def group_selection():
    groups = load_groups()
    return render_template('/groups/group_selection.html', groups=groups)

#tela de CRUD de membros e nome do grupo
@bp.route('/g_create', methods=('GET','POST'))
@login_required
def g_create():
    
    if request.method == "POST":
        members = []
        try:
            item = 0
            while True:
                member_name = request.form[f"member_name_{item}"]
                member_days = request.form[f"member_days_{item}"]
                member_pref = request.form[f"member_pref_{item}"]
                members.append({"name":member_name, "days":listify(member_days), "preference":listify(member_pref)})
                item += 1
        except:
            print("There are no members to go through\n")
            
        group = {}
        group["id"] = int(request.form["id"])
        group["name"] = request.form["group_name"]
        group["user_id"] = session["user_id"]
        group["members"] = members
 
        create_and_update(group)
        
        return group_selection()
                    
    else:
        # creates new group if clicked "+"
        # if request.args.get('group') == "New Group":
        #     group = {"name":"New Group", "user_id":f"{session['user_id']}", "members":[]}
        #     return render_template('/groups/g_create.html', group=group, members=members)
        
        # data gathering
        group_id = request.args.get("group_id")
        group = select_group(group_id)
        members = []
        

        # populates list of members
        if group:
            for member in group["members"]:
                member['days_list'] = stringfy_list(member['days'])
                member['preference_list'] = stringfy_list(member['preference'])
                members.append(member)

        return render_template('/groups/g_create.html', group=group, members=members)


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


@bp.route('/g_delete')
@login_required
def g_delete():
    # data gathering
    g_id = request.args.get("id")
    
    delete_group(g_id)
    
    return group_selection()
    



@bp.route('/new_group', methods=('GET','POST'))
@login_required
def new_group():
    id_lst = group_id_lst() 
    next_id = id_lst[-1] + 1
    
    group = {'id': next_id, 'name':'New Group', 'members':[]}
    group["user_id"] = session["user_id"]
    create_and_update(group)
    return redirect('/group_selection')
