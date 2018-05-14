from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from models import * 

def index(request):
	return render(request, "test_app/index.html")

def signin(request):
	return render(request, "test_app/signin.html")

def register(request):
	return render(request, "test_app/register.html")

def new(request):
	return render(request, "test_app/add_new.html")

def edit(request, user_id):
	user = User.objects.get(id=user_id)
	context = { "user": user }
	return render(request, "test_app/edit.html", context)

def dashboard(request):
	context = {"users": User.objects.all()}
	try:
		id = request.session['user_id']
		user = User.objects.get(id = id)
		return render(request, "test_app/dashboard.html", context)
	except:
		return redirect('/')

def admin_dashboard(request):
	context = {"users": User.objects.all()}
	try:
		id = request.session['user_id']
		user = User.objects.get(id = id)
		return render(request, "test_app/admin_dashboard.html", context)
	except:
		return redirect('/')

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
			return redirect('/dashboard/admin')
		else:
			request.session['user_id'] = result.id
			return redirect('/dashboard')

def profile(request, user_id):
	user = User.objects.get(id=user_id)
	context = { "user": user, "authors": User.objects.all() }
	return render(request, "test_app/profile.html", context)

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

def destroy(request, user_id):
	User.objects.get(id=user_id).delete()
	return redirect('/dashboard/admin')

def post_message(request, user_id):
	print "Hello!"
	result = Message.objects.message_validator(request.POST)
	if type(result) == list:
		for error in result:
			messages.error(request, error)
		return redirect('show', user_id=user_id)
		# return redirect('show', user_id=user_id)
	else:
		return redirect('show', user_id=user_id)

def logoff(request):
	request.session.clear()
	return redirect('/')
