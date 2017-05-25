from django.http import HttpResponse
from django.views import generic
from .models import * #Candidate, Job, Interview, Tag, Recruiter, User, TagType
from .forms import * # NewCandidateForm, NewJobForm, SubmitCandidateForm, InterviewAddForm, CandidateSearchForm, JobSearchForm, UploadResumeForm
from django.views.generic import TemplateView, FormView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django import forms
import json, os, datetime
from ats.parse import *



##
##
## TODO
## 	define workflow
##
##
##
##
##
##  current: better search results handling
##     how to display every result with the same html template?
##
##  hyperlink the job tags to a list of all jobs by that tag
##  clean up files a bit?
##  figure out proper place for resume parser
##  change color of interview depending on outcome of the interview
##  revamp job page to look presentable
##  add titles to each page through title content
##
## color coding scheme for each tag that is uniform
## upload resume to create candidate?
## reporting information
## quota system
## recruiter page [flush out]
## fix keyword search function
##      add a "todo" function in the index
##         [X] unscheduled interviews
## 		   [ ] what other info??
##
##
## ideas:
##      add company object - maybe we can create data sctructure for org chart
##      popup for add interview
## bugs:
##		error when adding interview and no job selected
##		redirect to candidate detail after submit candidate to job
##      edit interviews




def login_user(request):
	context = {
		'page_title' : 'Login',
		'errors' : None,
		'form' : LoginForm
	}
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return render(request, 'ats/index.html', context)
			# Redirect to a success page.
		else:
			context['errors'] = 'Incorrect login information'
			# Return an 'invalid login' error message.
	return render(request, 'ats/login.html', context)

@login_required
def logout_user(request):
	logout(request)
	#TODO logout page?
	return render(request, 'ats/login.html')



@login_required
def index(request):
	context = {
		'latest_candidate_list': Candidate.objects.order_by('-pub_date')[:10],
		'latest_job_list' : Job.objects.order_by('-pub_date')[:5],
		'unscheduled_list' : Interview.objects.filter(date_time=None)
	}
	return render(request, 'ats/index.html', context)

@login_required
def recruiter(request, user_username):
	r = Recruiter.objects.get(user = User.objects.get(username = user_username))
	context = {
		'recruiter_info' : r
	}
	if request.POST:
		print(request)
	return render(request, 'ats/recruiter.html', context)


@login_required
def search(request):
	#allows searching for candidate/job
	context = {
		'candidate_search_form' : CandidateSearchForm,
		'job_search_form' : JobSearchForm,
		'results'  : None
	}
	if request.method == 'POST':
		results = set()
		if 'submit_candidate_search_form' in request.POST:
			form = CandidateSearchForm(request.POST)
			if form.is_valid():
				search = form.cleaned_data
				if search['first_name']:
					results.update(Candidate.objects.filter(first_name = search['first_name']))
				if search['last_name']:
					results.update(Candidate.objects.filter(last_name = search['last_name']))
				if search['tags']:
					for tag in search['tags']:
						results.update(Candidate.objects.filter(tags = Tag.objects.filter(pk=tag)))
				context['results'] = (results)
		if 'submit_job_search_form' in request.POST:
			form = JobSearchForm(request.POST)
			if form.is_valid():
				search = form.cleaned_data
				if search['keywords']:
					print('this')
					#results.update(Job.objects.filter(keywords = search['keywords']))
				if search['title']:
					results.update(Job.objects.filter(title = search['title']))
				if search['company']:
					results.update(Job.objects.filter(company = search['company']))
				if search['tags']:
					for tag in search['tags']:
						results.update(Job.objects.filter(tags = Tag.objects.filter(pk=tag)))
				context['results'] = (results)
	return render(request, 'ats/search.html', context)

@login_required
def search_results(request):
	#allows searching for candidate/job
	context = {
		'page_title' : 'Search Results',
		'search_params' : None,
		'results_table_header' : [],
		'results'  : set()
	}
	#if request.method == 'POST':
	context['search_params'] = request.POST
	context['results_table_header'] = ['name', 'phone', 'email', 'other']
	context['results'].update(Candidate.objects.all())
	return render(request, 'ats/search_results.html', context)

@login_required
def calendar(request):
	#https://fullcalendar.io/docs/usage/
	##LAST I WAS DOING
	##creating a way to pass interviews into context for the caldner.html template
	events = []
	context = {
		'no_panel_content' : True,
		'events' : json.dumps([interview.calendar_display() for interview in Interview.objects.all()])
	}
	return render(request, 'ats/calendar.html', context)







#### START DETAILS #####
@login_required
def job_detail(request, job_pk):
	j = Job.objects.get(pk=job_pk)
	context = {
		'page_title' : j.title + ' l ' + j.company,
		'job_details' : j.get_fields(),
		'job_tags' : j.tags.all(),
		'description' : j.description,
		'candidates_on_jobs' : j.get_candidates()
	}
	return render(request, 'ats/job_detail.html', context)

@login_required
def candidate_detail(request, candidate_pk):
	#displays candidate information
	c = Candidate.objects.get(pk=candidate_pk)
	context = {
		'page_title' : c.first_name + ' ' + c.last_name,
		'candidate_tags' : c.tags.all(),
		'candidate_fields' : c.get_fields(),
		'candidate_resume' : c.get_resume_url(),
		'candidate_writeup' : c.writeup,
		'candidate_jobs' :	c.jobs.all(),
		'interview_add_form' : InterviewAddForm,
		'candidate_name' : c.first_name + ' ' + c.last_name,
		'candidate_recruiter' : c.recruiter
	}
	# allows editing of interview schedules
	if request.method == 'POST':
		if 'delete_interview' in request.POST:
			#delete_interview is tagged on submit button
			i = Interview.objects.filter(pk=request.POST['delete_interview'])
			i.delete()
		elif 'add_interview' in request.POST:
			#add_interview is tagged on submit button
			i = InterviewAddForm(request.POST)
			if i.is_valid():
				#manually add data from form to interview object
				new_interview = i.save(commit=False)
				for job in Job.objects.filter(pk=request.POST['job_id']):
					new_interview.job = job
				interview_date = request.POST['date']
				interview_time = request.POST['time']
				if not (interview_date or interview_time) :
					new_interview.date_time = None
				else:
					new_interview.date_time = datetime.datetime.strptime(
									interview_date + " " +
									interview_time, "%m/%d/%Y %I:%M %p")
				new_interview.interview_type = request.POST['interview_type']
				#SLOPPY!
				new_interview.candidate = Candidate.objects.filter(pk=candidate_pk)[0]
				new_interview.save()
			else:
				print('error saving')
				print(i.errors)
	#attach interviews to context
	for job in context['candidate_jobs']:
		job.interviews = Interview.objects.filter(candidate_id=c.id).filter(
									job_id=job.id)
	return render(request, 'ats/candidate_detail.html', context)

###### END DETAILS ######
###### START NEW ######
@login_required
def new_candidate(request):
	context = {
		'page_title' : 'New Candidate',
		'form' : NewCandidateForm,
		'errors' : None
	}
	if request.method == 'POST':
		c = NewCandidateForm(request.POST, request.FILES)
		if c.is_valid():
			new_candidate = c.save(commit=False)
			new_candidate.pub_date = datetime.datetime.today()
			# implement login here
			#TODO - catch if no recruiter assigned
			new_candidate.recruiter = Recruiter.objects.get(user = request.user)
			new_candidate.save()
			new_candidate.change_log = []
			new_candidate.tags = get_tags_from_multiple_input_fields(request.POST)
			c.save_m2m()
		else:
			print('error saving')
			context['errors'] = c.errors
	return render(request, 'ats/new_candidate.html', context)
@login_required
def new_job(request):
	context = {
		'page_title' : 'New Job',
		'form' : NewJobForm,
		'errors' : None
	}
	if request.method == 'POST':
		j = NewJobForm(request.POST)
		if j.is_valid():
			job_tags = set()
			new_job = j.save(commit=False)
			new_job.pub_date = datetime.datetime.today()
			new_job.save()
			new_job.tags = get_tags_from_multiple_input_fields(request.POST)
			j.save_m2m()
		else:
			print('error saving')
			context['errors'] = j.errors
	return render(request, 'ats/new_job.html', context)

##### END NEW ######
##### START EDIT #####
@login_required
def edit_candidate(request, candidate_pk):
	c = Candidate.objects.get(pk=candidate_pk)
	if request.method == 'POST':
		for field in request.POST:
			if field not in ['csrfmiddlewaretoken', 'tags', 'recruiter']:
				setattr(c, field, request.POST[field])
		for field in request.FILES:
			setattr(c, field, request.FILES[field])
		#START procedure for setting tags
		setattr(c, 'tags', get_tags_from_multiple_input_fields(request.POST))
		#START procedure for setting recruiter
		setattr(c, 'recruiter', Recruiter.objects.get(pk=request.POST['recruiter']))
		#START add
		c.save()
	context = {
		'page_title' : 'Edit Candidate',
		'type' : 'Candidate',
		'form': NewCandidateForm(instance=c, initial={
								'tags_languages' : get_tag_id_by_tag_type(c, 'LANG'),
								'tags_function' : get_tag_id_by_tag_type(c, 'FUNC'),
								'tags_database' : get_tag_id_by_tag_type(c, 'DB'),
								'tags_technology' : get_tag_id_by_tag_type(c, 'TECH'),
								'tags_miscellaneous' : get_tag_id_by_tag_type(c, 'MISC')
													})
	}
	return render(request, 'ats/edit_object.html', context)

@login_required
def edit_job(request, job_pk):
	j = Job.objects.get(pk=job_pk)
	if request.method == 'POST':
		for field in request.POST:
			if field not in ['csrfmiddlewaretoken', 'tags', 'recruiter']:
				setattr(j, field, request.POST[field])
		for field in request.FILES:
			setattr(j, field, request.FILES[field])
		#START procedure for setting tags
		setattr(j, 'tags', get_tags_from_multiple_input_fields(request.POST))
		#START procedure for setting recruiter
		#setattr(j, 'recruiter', Recruiter.objects.get(pk=request.POST['recruiter']))
		#START add
		j.save()
	context = {
		'page_title' : 'Edit Job',
		'type' : 'Job',
		'form': NewJobForm(instance=j, initial={
								'tags_languages' : get_tag_id_by_tag_type(j, 'LANG'),
								'tags_function' : get_tag_id_by_tag_type(j, 'FUNC'),
								'tags_database' : get_tag_id_by_tag_type(j, 'DB'),
								'tags_technology' : get_tag_id_by_tag_type(j, 'TECH'),
								'tags_miscellaneous' : get_tag_id_by_tag_type(j, 'MISC')
													})
	}
	return render(request, 'ats/edit_object.html', context)

@login_required
def submit_candidate(request, candidate_pk):
	c = Candidate.objects.get(pk=candidate_pk)
	#ALERT: might be messy at scale
	global_jobs = Job.objects.all()
	if request.method == 'POST':
		arr = request.POST.getlist('jobs')
		for i in range(0,len(arr)):
			for job in Job.objects.filter(pk=arr[i]):
				c.jobs.add(job)
	context = { 'formset' : global_jobs }
	return render(request, 'ats/submit_candidate.html', context)




@login_required
def download(request, type, pk):
	if type == 'resume':
		c = Candidate.objects.get(pk=pk)
		file_path = 'media/' + str(c.resume)
		print(os.path.basename(file_path))
		if os.path.exists(file_path):
			with open(file_path, 'rb') as fh:
				response = HttpResponse(fh.read())
				response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
				return response


@login_required
def upload_resume(request):
	context = {
		'form' : UploadResumeForm,
		'errors' : None,
		'resume_text' : None
	}
	if request.method == 'POST':
		r = UploadResumeForm(request.POST, request.FILES)
		res = request.FILES

		context['resume_text'] = strip_text(pdf_to_text(res['resume']))
		#if r.is_valid():
			#r.fields['resume'])
			#new_resume = r.save(commit=False)
			#new_candidate.pub_date = datetime.datetime.today()
			# implement login here
			#TODO - catch if no recruiter assigned
			#new_candidate.recruiter = Recruiter.objects.get(user = request.user)
			#new_candidate.save()
			#new_candidate.change_log = []
			#new_candidate.tags = get_tags_from_multiple_input_fields(request.POST)
			#c.save_m2m()
		#else:
		#	print('error saving')
		#	context['errors'] = c.errors
	return render(request, 'ats/upload_resume.html', context)







###### HELPER FUNCTIONS ########

def get_tags_from_multiple_input_fields(req):
	#accepts: request.POST,
	#returns: a set of the tags contained within
	set_of_tags = set()
	for field in req:
		if field.startswith('tags_'):
			for tag in req.getlist(field):
				set_of_tags.update(Tag.objects.filter(pk=tag))
	return set_of_tags
	#https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method


def get_tag_id_by_tag_type(model_object, tag_type):
	#accepts: candidate/job, tag_type
	#returns: list of tag.id for which the candidate/job is tagged
	tags = [tag.id for tag in model_object.tags.filter(tagtype = TagType.objects.filter(name = tag_type))]
	return tags
