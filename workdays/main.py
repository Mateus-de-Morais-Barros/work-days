from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from workdays.auth import login_required
from workdays.crud import load_groups, select_group, stringfy_list 

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('/index.html')

@bp.route('/group_selection')
@login_required
def group_selection():
    groups = load_groups()
    return render_template('/groups/group_selection.html', groups=groups)


@bp.route('/g_create', methods=('GET','POST'))
@login_required
def g_create():
    # data gathering
    group_id = request.args.get("group_id")

    group = select_group(group_id)
    
    print(group)
    members = []
    # creates new group if clicked "+"
    if group == "New Group":
        group = {"name":"New Group"}
        return render_template('/groups/g_create.html', group=group, members=members)

    # populates list of members
    if group:
        for member in group["members"]:
            member['days_list'] = stringfy_list(member['days'])
            member['preference_list'] = stringfy_list(member['preference'])
            members.append(member)
        
    if request.method == "POST":
        members = []
        try:
            item = 0
            while True:
                member_name = request.form[f"member_name_{item}"]
                member_days = request.form[f"member_days_{item}"]
                member_pref = request.form[f"member_pref_{item}"]
                members.append({"name":member_name, "days":member_days, "preference":member_pref})
        except:
            print("error")
            
        print(members)
    #     # create member list in groups with members from the POST
    #     request.form.get("name")
    #     for member in members:
    #         m = {
    #             "name": member[f"'{member}'_name"],
    #             "days": member[f"'{member}'_days"],
    #             "preference": member[f"'{member}'_pref"]
    #             }
    #         group["members"].append(m)
        
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



@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
    if request.method == "POST":
        print(request.form)
