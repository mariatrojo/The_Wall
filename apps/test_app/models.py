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
		print userLevel
		# normal = postData['normal']
		# admin = postData['admin']

		if not email and not fname and not lname:
			errors.append("All fields cannot be empty")
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
				user = User.objects.get(id = user_id)
				user.email = email
				user.save()
			if fname:
				user = User.objects.get(id = user_id)
				user.first_name = fname
				user.save()
			if lname:
				user = User.objects.get(id = user_id)
				user.last_name = lname
				user.save()
			if userLevel == "1":
				user = User.objects.get(id = user_id)
				user.user_level = 1
				user.save()
			if userLevel == "2":
				user = User.objects.get(id = user_id)
				user.user_level = 9
				user.save()
			print user.user_level
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

	def message_validator(self, postData):
		errors = []
		msg = postData['message']
		user_id = postData['id']
		author = postData['logged_in_user']

		if not msg:
			errors.append("Message cannot be empty")
		elif len(msg) < 8:
			errors.append("Message must be 8 characters or longer")

		if not errors:
			if msg:
				user = User.objects.get(id = user_id)
				author = User.objects.get(id = author)
				return Message.objects.create(text=msg, user=user, author=author)

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
