from flask import Blueprint, request, redirect, render_template, url_for, jsonify
from flask.views import MethodView
from core.models import User, Group, FriendRequest, Status
from core import flask_bcrypt

core = Blueprint('admin', __name__, template_folder='templates')

from twilio.rest import TwilioRestClient
import twilio.twiml



class TwilioView(MethodView):

	def post(self):
		resp = twilio.twiml.Response()
		resp.redirect("http://afternoon-fjord-7983.herokuapp.com/update")
		return str(resp)


class StatusView(MethodView):

	def post(self):
		# get username from post request
		#TODO : Hardcoded for now
		username = "phouse512"
		# get group id from post request
		group_id = '54bb45eb7ad44d6f2a58efa6'
		# get status from post request
		status = False
		new_status = not bool(status)
		user = User.objects(phone='4403343916')
		group = Group.objects(id=group_id).first()

		new_status = Status(user=user, available=new_status, group=group)

		new_status.save()

		ACCOUNT_SID = "ACf2b361a5b8be85173d9db27f45cfb5d2" 
		AUTH_TOKEN = "4b6edb9fb0efffc0fa1a3c293b8e16c4" 
 
		client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 

		for member in group.members:
			member_groups = Group.objects(owner=member)
			for sub_group in member_groups
				if user in sub_group.members:
					member_status = Status.objects(user=member, group=sub_group).order_by('-created_at')
					if len(member_status) < 1:
						check = False
					else:
						check = member_status[0].available

					if check:
						string = "%s %s is free!" % (user.first_name, user.last_name)
						client.messages.create(
							to=member.phone, 
							from_="+12015747526", 
							body=string,  
						)

		return jsonify(current_status=new_status.available)

class UserStatusView(MethodView):

	def get(self, user_id):
		user = User.objects(id=user_id)
		status = Status.objects(user=user[0]).order_by('-created_at')[0]
		return jsonify(status=status, user=user)

class RegisterUserView(MethodView):

	def post(self):
		data = request.get_json(force=True)
		password = flask_bcrypt.generate_password_hash(data['password'])

		new_user = User(first_name=data['firstName'],last_name=data['lastName'],phone=data['number'], hashed_pw=password)
		new_user.save()

		return jsonify(status='success', token=str(new_user.id))

class LoginUserView(MethodView):

	def post(self):
		data = request.get_json(force=True)

		user = User.objects(phone=data['number'])
		if len(user) > 0:
			if flask_bcrypt.check_password_hash(user[0].hashed_pw, data['password']):
				return jsonify(status='success', token=str(user[0].id))
			else:
				return jsonify(status='failure', message='Incorrect login credentials.')
		else:
			return jsonify(status='failure', message='User not found.')

class GatherFriendsView(MethodView):

	def get(self):
		user_id = request.args.get("user_id")
		all_users = set(User.objects.all())
		user = User.objects(id=user_id).first()
		friends = set(list(user.friends) + list(user))

		difference = list(all_users - friends)
		return jsonify(users=difference)

class UserGroupsView(MethodView):

	def get(self):
		user_id = request.args.get("user_id")
		user = User.objects(id=user_id).first()
		groups_owned_by = Group.objects(owner=user).all()
		return jsonify(groups=groups_owned_by)

class GroupMemberView(MethodView):

	def get(self):
		group_id = request.args.get("group_id")
		members = Group.objects(id=group_id).first().members
		return jsonify(members=members)


# Register the urls
core.add_url_rule('/twilio', view_func=TwilioView.as_view('twilio'))
core.add_url_rule('/update', view_func=StatusView.as_view('list'))
core.add_url_rule('/status/<user_id>/', view_func=UserStatusView.as_view('status'))
core.add_url_rule('/register', view_func=RegisterUserView.as_view('register'))
core.add_url_rule('/login', view_func=LoginUserView.as_view('login'))
core.add_url_rule('/possiblefriends', view_func=GatherFriendsView.as_view('possiblefriends'))
core.add_url_rule('/groups', view_func=UserGroupsView.as_view('groups'))
core.add_url_rule('/members', view_func=GroupMemberView.as_view('members'))


