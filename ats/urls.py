from django.conf.urls import url
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
	#Add Django site authentication urls (for login, logout, password management)
#	url('^accounts/', include('django.contrib.auth.urls')),

	#ex: /
	url(r'^$', views.index, name='index'),

	#ex: /login/
	url(r'^login/', views.login_user, name='login_user'),
	#ex: /logout/
	url(r'^logout/', views.logout_user, name='logout_user'),

	#ex: /recruiter/mothra
	url(r'^recruiter/(?P<user_username>\w+)', views.recruiter, name='recruiter'),

	#ex: /new_candidate/
	url(r'^new_candidate/', views.new_candidate, name='new_candidate'),

	#ex: /search/{search_params}
	url(r'^search/$', views.search, name='search'),

	#ex: /new_job/
	url(r'^new_job/', views.new_job, name='new_job'),

	#ex: /candidate/5
	url(r'^candidate/(?P<candidate_pk>[0-9]+)/$', views.candidate_detail, name='candidate_detail'),

	#ex: /candidate/5/submit
	url(r'^candidate/(?P<candidate_pk>[0-9]+)/submit$', views.submit_candidate, name='submit_candidate'),

	#ex: /candidate/5/edit
	url(r'^candidate/(?P<candidate_pk>[0-9]+)/edit$', views.edit_candidate, name='edit_candidate'),

	#ex: /job/5
	url(r'^job/(?P<job_pk>[0-9]+)/$', views.job_detail, name='job_detail'),

	#ex: /calendar
	url(r'^calendar/$', views.calendar, name='calendar'),

	#ex: /download/resume/5
	url(r'^download/(?P<type>[A-z]+)/(?P<pk>[0-9]+)/$', views.download, name='download')
]
