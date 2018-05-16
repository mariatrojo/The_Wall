from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.index),
	url(r'^signin$', views.signin),
	url(r'^signin_form$', views.signin_form),
	url(r'^register$', views.register),
	url(r'^register_form$', views.register_form),
	url(r'^dashboard/admin$', views.admin_dashboard),
	url(r'^dashboard$', views.dashboard),
	url(r'^users/new$', views.new),
	url(r'^users/show/(?P<user_id>\d+)$', views.profile, name='show'),
	url(r'^users/admin_register$', views.admin_register),
	url(r'^users/edit/(?P<user_id>\d+)$', views.edit, name='edit'),
	url(r'^users/edit_info/(?P<user_id>\d+)$', views.edit_info),
	url(r'^users/edit_pw/(?P<user_id>\d+)$', views.edit_pw),
	url(r'^users/edit_desc/(?P<user_id>\d+)$', views.edit_desc),
	url(r'^users/(?P<user_id>\d+)/destroy$', views.destroy),
	url(r'^users/post_message/(?P<user_id>\d+)$', views.post_message),
	url(r'^users/post_comment/(?P<user_id>\d+)$', views.post_comment),
	url(r'^logoff$', views.logoff)
]