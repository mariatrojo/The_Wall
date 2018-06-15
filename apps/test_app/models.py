from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class BlogManager(models.Manager):
	def register_validator(self, postData):
		errors = []

		email = postData['email']
		fname = postData['first_name']
		lname = postData['last_name']
		pw = postData['password']
		conf_password = postData['confirm_password']

		if not email:
			errors.append("Email cannot be empty")
		elif not EMAIL_REGEX.match(email):
			errors.append("Invalid Email!")

		if not fname:
			errors.append("First name cannot be empty")
		elif len(fname) < 2:
			errors.append("First name must be longer than 1 character")
		elif not fname.isalpha():
			errors.append("First name can only contain letters")
		
		if not lname:
			errors.append("Last name cannot be empty")
		elif len(lname) < 2:
			errors.append("Last name must be longer than 1 character")
		elif not lname.isalpha():
			errors.append("Last name can only contain letters")

		if not pw:
			errors.append("Password cannot be empty")
		elif len(pw) < 8:
			errors.append("Password must be 8 characters or longer")
		elif pw != conf_password:
			errors.append("Passwords don't match")
		
		if not errors:
			try:
				User.objects.get(email=email)
				errors.append("Email is already used")
			except:
				hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
				return User.objects.create(email=email, first_name=fname, last_name=lname, password=hash, user_level=1)
				if User.objects.get(id=1):
					user = User.objects.get(id=1)
					user.user_level=9
					user.save()
					return user
		return errors

	def login_validator(self, postData):
		errors = []
		email = postData['email']
		pw = postData['password']

		if not email:
			errors.append("Email cannot be empty")
		elif not EMAIL_REGEX.match(email):
			errors.append("Invalid Email!")
		
		if not pw:
			errors.append("Password cannot be empty")
		elif len(pw) < 8:
			errors.append("Password must be 8 characters or longer")

		if not errors:
			try:
				user = User.objects.get(email=email)
				if bcrypt.checkpw(pw.encode(), user.password.encode()):
					return user
				else:
					errors.append("Incorrect password")
			except:
				errors.append("You aren't registered yet")

		return errors
	
	def admin_register_validator(self, postData):
		errors = []

		email = postData['email']
		fname = postData['first_name']
		lname = postData['last_name']
		pw = postData['password']
		conf_password = postData['confirm_password']

		if not email:
			errors.append("Email cannot be empty")
		elif not EMAIL_REGEX.match(email):
			errors.append("Invalid Email!")

		if not fname:
			errors.append("First name cannot be empty")
		elif len(fname) < 2:
			errors.append("First name must be longer than 1 character")
		elif not fname.isalpha():
			errors.append("First name can only contain letters")
		
		if not lname:
			errors.append("Last name cannot be empty")
		elif len(lname) < 2:
			errors.append("Last name must be longer than 1 character")
		elif not lname.isalpha():
			errors.append("Last name can only contain letters")

		if not pw:
			errors.append("Password cannot be empty")
		elif len(pw) < 8:
			errors.append("Password must be 8 characters or longer")
		elif pw != conf_password:
			errors.append("Passwords don't match")
		
		if not errors:
			try:
				User.objects.get(email=email)
				errors.append("Email is already used")
			except:
				hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
				return User.objects.create(email=email, first_name=fname, last_name=lname, password=hash, user_level=1)
				if User.objects.get(id = 1):
					user = User.objects.get(id = 1)
					user.user_level = 9
					user.save()
					return user

		return errors

	def edit_validator(self, postData):
		errors = []
		email = postData['email']
		fname = postData['first_name']
		lname = postData['last_name']
		user_id = postData['id']
		userLevel = postData['user_level']
		user = User.objects.get(id = user_id)
		# normal = postData['normal']
		# admin = postData['admin']

		if not email and not fname and not lname and not userLevel:
			errors.append("All fields cannot be empty")
		elif user.email == email and user.first_name == fname and user.last_name == lname and (user.user_level == 9 and userLevel == "2") or (user.user_level == 1 and userLevel == "1"):
			errors.append("No changes detected")
		else:
			if len(email) < 5 and len(email) > 1:
				errors.append("Email cannot be less than 5 characters")
			elif len(email) < 5 and len(email) > 1 and not EMAIL_REGEX.match(email):
				errors.append("Invalid Email!")

			if len(fname) < 2 and len(fname) > 0:
				errors.append("First name must be longer than 1 character")
			elif len(fname) > 2 and not fname.isalpha():
				errors.append("First name can only contain letters")
			
			if len(lname) < 2 and len(lname) > 0:
				errors.append("Last name must be longer than 1 character")
			elif len(lname) > 2 and not lname.isalpha():
				errors.append("Last name can only contain letters")

		if not errors:
			if email:
				user.email = email
				user.save()
			if fname:
				user.first_name = fname
				user.save()
			if lname:
				user.last_name = lname
				user.save()
			if userLevel == "1":
				user.user_level = 1
				user.save()
			if userLevel == "2":
				user.user_level = 9
				user.save()
			return user

		return errors

	def edit_pw_validator(self, postData):
		errors = []
		pw = postData['password']
		conf_password = postData['confirm_password']
		user_id = postData['id']
		hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())

		if not pw:
			errors.append("Password cannot be empty")
		elif len(pw) < 8:
			errors.append("Password must be 8 characters or longer")
		elif pw != conf_password:
			errors.append("Passwords don't match")

		if not errors:
			if pw:
				user = User.objects.get(id = user_id)
				user.password = hash
				user.save()
			return user

		return errors

	def edit_desc_validator(self, postData):
		errors = []
		desc = postData['desc']
		user_id = postData['id']
		user = User.objects.get(id = user_id)

		if not desc:
			errors.append("Description cannot be empty")
		elif len(desc) < 8:
			errors.append("Description must be 8 characters or longer")
		elif desc == user.desc:
			errors.append("No change detected")

		if not errors:
			if desc:
				user.desc = desc
				user.save()
			return user

		return errors

	def message_validator(self, postData):
		errors = []
		msg = postData['message']
		user_id = postData['id']
		author = postData['logged_in_user']
		user = User.objects.get(id = user_id)

		if not msg:
			errors.append("Message cannot be empty")
		elif len(msg) < 2:
			errors.append("Message must be 8 characters or longer")

		if not errors:
			if msg:
				author = User.objects.get(id = author)
				return Message.objects.create(text=msg, user=user, author=author)

		return errors

	def comment_validator(self, postData):
		errors = []
		comment = postData['message']
		# user_id = postData['id']
		commenter = postData['logged_in_user']
		message_post = postData['id']

		if not comment:
			errors.append("Comment cannot be empty")
		elif len(comment) < 2:
			errors.append("Commment must be 8 characters or longer")

		if not errors:
			if comment:
				message = Message.objects.get(id = message_post)
				commenter = User.objects.get(id = commenter)
				return Comment.objects.create(text=comment, message=message, commenter=commenter)

		return errors

class User(models.Model):
	email = models.CharField(max_length=255)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	user_level = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	desc = models.TextField()

	objects = BlogManager()

class Message(models.Model):
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add = True)
	user = models.ForeignKey(User, related_name="messages")
	author = models.ForeignKey(User, related_name="message_submitted")

	objects = BlogManager()

class Comment(models.Model):
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add = True)
	commenter = models.ForeignKey(User, related_name="comments")
	message = models.ForeignKey(Message, related_name="comments")

	objects = BlogManager()
