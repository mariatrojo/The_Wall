from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import * 

def index(request):
	return render(request, "test_app/index.html")

def signin(request):
	return render(request, "test_app/signin.html")

def register(request):
	return render(request, "test_app/register.html")

def new(request):
	if 'user_id' in request.session:
		return render(request, "test_app/add_new.html")
	else:
		return redirect('/signin')

def edit(request, user_id):
	if 'user_id' in request.session:
		user = User.objects.get(id=user_id)
		context = { "user": user }
		return render(request, "test_app/edit.html", context)
	else:
		return redirect('/signin')

def dashboard(request):
	if 'user_id' in request.session:
		context = {"users": User.objects.all()}
		try:
			id = request.session['user_id']
			user = User.objects.get(id = id)
			return render(request, "test_app/dashboard.html", context)
		except:
			return redirect('/')
	else:
		return redirect('/signin')

def admin_dashboard(request):
	context = {"users": User.objects.all()}
	if 'user_id' in request.session:
		try:
			id = request.session['user_id']
			user = User.objects.get(id = id)
			return render(request, "test_app/admin_dashboard.html", context)
		except:
			return redirect('/')
	else:
		return redirect('/signin')


def signin_form(request):
	result = User.objects.login_validator(request.POST)
	if type(result) == list:
		for error in result:
			messages.error(request, error)
		return redirect('/signin')
	else:
		if result.user_level == 1:
			request.session['user_id'] = result.id
			return redirect('/dashboard')
		else:
			request.session['user_id'] = result.id
			return redirect('/dashboard/admin')

def register_form(request):
	result = User.objects.register_validator(request.POST)
	if type(result) == list:
		for error in result:
			messages.error(request, error)
		return redirect('/register')
	else:
		if result.user_level == 1:
			request.session['user_id'] = result.id
			return redirect('/dashboard')
		elif result.user_level == 9:
			request.session['user_id'] = result.id
			return redirect('/dashboard/admin')

def profile(request, user_id):
	if 'user_id' in request.session:
		user = User.objects.get(id=user_id)
		authors = User.objects.all()
		user_messages = Message.objects.order_by('-created_at')
		comments = Comment.objects.all()
		print comments
		context = { 
			"user": user, 
			"authors": authors, 
			"user_messages": user_messages, 
			"comments": comments,
		}
		return render(request, "test_app/profile.html", context)
	else:
		return redirect('/signin')

def admin_register(request):
	result = User.objects.register_validator(request.POST)
	if type(result) == list:
		for error in result:
			messages.error(request, error)
		return redirect('/users/new')
	else:
		return redirect('/dashboard/admin')

def edit_info(request, user_id):
	result = User.objects.edit_validator(request.POST)
	if type(result) == list:
		for error in result:
			messages.error(request, error)
		return redirect('edit', user_id=user_id)
	else:
		return redirect('/dashboard/admin')

def edit_pw(request, user_id):
	result = User.objects.edit_pw_validator(request.POST)
	if type(result) == list:
		for error in result:
			messages.error(request, error)
		return redirect('edit', user_id=user_id)
	else:
		return redirect('/dashboard/admin')

def edit_desc(request, user_id):
	result = User.objects.edit_desc_validator(request.POST)
	if type(result) == list:
		for error in result:
			messages.error(request, error)
		return redirect('edit', user_id=user_id)
	else:
		return redirect('show', user_id=user_id)

def destroy(request, user_id):
	try:
		Message.objects.get(author_id=user_id).delete()
		Comment.objects.get(commenter_id=user_id).delete()
		User.objects.get(id=user_id).delete()
	except:
		User.objects.get(id=user_id).delete()

	return redirect('/dashboard/admin')

def post_message(request, user_id):
	result = Message.objects.message_validator(request.POST)
	if type(result) == list:
		for error in result:
			messages.error(request, error)
		return redirect('show', user_id=user_id)
		# return redirect('show', user_id=user_id)
	else:
		return redirect('show', user_id=user_id)

def post_comment(request, user_id):
	result = Comment.objects.comment_validator(request.POST)
	if type(result) == list:
		for error in result:
			comment_messages = messages.error(request, error)
		return redirect('show', user_id=user_id)
		# return redirect('show', user_id=user_id)
	else:
		return redirect('show', user_id=user_id)

def logoff(request):
	request.session.clear()
	return redirect('/')
