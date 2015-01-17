from flask import Blueprint, request, redirect, render_template, url_for, jsonify
from flask.views import MethodView
from core.models import User, Group, FriendRequest, Status
from core import flask_bcrypt

core = Blueprint('admin', __name__, template_folder='templates')


class StatusView(MethodView):

	def post(self):
		# get username from post request
		#TODO : Hardcoded for now
		username = "phouse512"
		# get group id from post request
		group_id = '54baba611f9f8061147cdc66'
		# get status from post request
		status = False
		new_status = not bool(status)
		user = User.objects(username=username)
		group = Group.objects(id=group_id)

		new_status = Status(user=user, available=new_status, group=group)

		new_status.save()

		return jsonify(current_status=new_status.available)

class UserStatusView(MethodView):

	def get(self, user_id):
		user = User.objects(id=user_id)
		status = Status.objects(user=user[0]).order_by('-created_at')[0]
		return jsonify(status=status, user=user)

class RegisterUser(MethodView):

	def post(self):
		try:
			first_name = request.form['firstName']
			last_name = request.form['lastName']
			number = request.form['number']
			password = flask_bcrypt.generate_password_hash(request.form['password'])

			new_user = User(first_name=first_name,last_name=last_name,phone=number,hashed_pw=password)
			new_user.save()

			print new_user.id

			return jsonify(status='success', token=str(new_user.id))
		except Exception as e:
			return jsonify(status=str(e))



# Register the urls
core.add_url_rule('/update', view_func=StatusView.as_view('list'))
core.add_url_rule('/status/<user_id>/', view_func=UserStatusView.as_view('status'))
core.add_url_rule('/register', view_func=RegisterUser.as_view('register'))


