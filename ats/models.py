from django.db import models
from django.forms import ModelForm, CheckboxSelectMultiple, fields_for_model, MultiValueField
from django.contrib.auth.models import User
import json, datetime
from django.http import HttpResponse

#here is what im thinking:
#	-interview class
#		-job		(one to many?)
#		-candidate  (one to one?)
#		-stage		char ex. first/second/final/HR
#		-location   phone/codetest/onsite
#		-time		date time
#		-outcome    unscheduled/failed/passed
#
#NEXT:
#   under each job on the candidate page, we need to list all the interviews for that role
#	under each job detail page, we need to list each candidate and their interview stage
## BUG when remaking the database, instances of Tag.objects.all() do not allow creation, comment these out before remaking the db
##
##LAST I WAS DOING: error when trying to add tagtype via admin
#http://stackoverflow.com/questions/38031772/exception-type-operationalerror-exception-value-no-such-column-blog-article



class TagType(models.Model):
	TagType_CHOICES 	= (  ('LANG', 'Language'), ('DB', 'Database'), ('FUNC', 'Function'), ('TECH', 'Technology'), ('MISC', 'Miscellaneous') )
	name 				= models.CharField(max_length=10, choices=TagType_CHOICES, default=None, null=False)

	def __unicode__(self):
		return self.verbosename

	def __str__(self):
		return self.name

class Tag(models.Model):
	name 				= models.CharField(max_length=20, default=None, null=False)
	tagtype 			= models.ForeignKey(to=TagType, related_name="tag_TagType", null=False, blank=False, default='1')

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name


class Recruiter(models.Model):
	user				= models.ForeignKey(User, default=None, null=False)
	linkedin 			= models.CharField('Linkedin', max_length=40, default=None, null=False)
	phone				= models.CharField('phone', max_length=15, default=None, null=False)
	base_url			= '/recruiter/'

	def __str__(self):
		return self.user.first_name + ' ' + self.user.last_name





class Job(models.Model):
#opportunity to look at different data structures (Tree?) that might better
#represent the corporate structure of a company:
#then you can have a single company page that will show the job openings
	title 				= models.CharField(max_length=100)
	description			= models.TextField(max_length=10000)
	#hiring_manager		= models.CharField(max_length=100)
	#salary 			= models.
	#parent				= modles.
	currently_open		= models.BooleanField(default=False)
	company 			= models.CharField(max_length=100) #should this be another obj?
	pub_date 			= models.DateTimeField('date published')
	tags 				= models.ManyToManyField(Tag)
	base_url 			= '/job/'

	def __unicode__(self):
		return "%s > %s" % (self.title, self.company)

	def get_candidates(self):
		#returns all the candidates in process, with their interviews
		candidates = []
		for candidate in Candidate.objects.filter(jobs__pk=self.id):
			candidates.append(dict({
				'first_name' : candidate.first_name,
				'last_name' : candidate.last_name,
				'url' : candidate.get_url(),
				'interviews' : Interview.objects.filter(
						candidate=Candidate.objects.filter(pk=candidate.id),
					job=Job.objects.filter(id=self.pk))
			}))
		return candidates

	def get_tags(self):
		return self.tags.values()

	def get_interviews(self, candidate):
		return Interview.objects.filter(candidate_id=candidate.id).filter(job_id=self.id)

	def get_fields(self):
		#doesnt return writeup, that is seperate for rendering purposes
		to_return = []
		for field in Job._meta.fields:
			if field.name != 'description':
				to_return.append([field.verbose_name, field.value_to_string(self)])
		return to_return


class Candidate(models.Model):
	#to figure out where candidats are coming from, look at pub date vs source
	I9_CHOICES 			= ( ('UNK', 'Unknown'), ('USC', 'US Citizen/Greencard'), ('H1B', 'H1B'), ('OPT', 'OPT') )
	SOURCE_CHOICES 		= ( ('LIM', 'Linkedin Message'), ('REF', 'Referral'), ('NET', 'Networking Event'), ('LIP', 'Linkedin Posting'), ('CJP','Community Job Posting'))
	#CORE VALUES (null=False)
	first_name 			= models.CharField('first name', max_length=20, default=None, null=False)
	last_name 			= models.CharField('last name', max_length=20, default=None, null=False)
	phone 				= models.CharField('phone', max_length=15, default=None, null=False)
	email_address 		= models.EmailField('email', max_length=40, default=None, null=False)
	tags 				= models.ManyToManyField(Tag, default=None)
	zip_code 			= models.CharField('zip code', max_length=6, default=None, null=False)
	source 				= models.CharField('source', max_length=20, choices=SOURCE_CHOICES, default=None, null=False)
	#SECONDARY VALUES (blank=True)
	linkedin 			= models.URLField('linkedin', default=None, null=True, blank=True)
	resume 				= models.FileField('resume', upload_to='resumes/', default=None, null=True, blank=True)
	writeup 			= models.TextField('writeup', max_length=4000, default=None, null=True, blank=True)
	salary_base 		= models.IntegerField('base', default=100, null=True, blank=True)
	salary_bonus 		= models.IntegerField('bonus', default=20, null=True, blank=True)
	i9_status 			= models.CharField('i9 status', max_length=3,choices=I9_CHOICES, default='UNK', null=True)
	pub_date 			= models.DateTimeField('date published')
	jobs 				= models.ManyToManyField(Job, blank=True)
	#interviews			= models.OneToManyField(Interview, blank=True)
	#languages
	recruiter			= models.ForeignKey(Recruiter, on_delete=models.CASCADE, default=None, null=True, blank=True)
	base_url 			= '/candidate/'
	#note - need provisions for what happens when max_length is exceeded
	change_log			= models.CharField(null=True, blank=True, max_length=4000)

	def get_fields(self):
		to_return = []
		for field in Candidate._meta.fields:
			if field.verbose_name not in { 'writeup' , 'recruiter', 'resume'}:
				to_return.append((
					field.verbose_name,
					field.value_to_string(self),
					field.name
				))
		return to_return

	def get_resume_url(self):
		#returns an array, first index is url, second is text for resume link
		print(self.resume)
		if self.resume:
			return  ["/download/resume/" + str(self.pk), 'DOWNLOAD RESUME']
		else:
			return ["edit" , "UPLOAD RESUME"]

	def get_jobs(self):
		return self.jobs

	def get_url(self):
		return self.base_url+str(self.pk)

	def get_interviews(self, job):
		return Interviews.objects.filter(candidate=self, job=job)

	def timestamp_change(self, recruiter):
		self.change_log.append([datetime.now, recruiter])




class Interview(models.Model):
	REVIEW				= 'REVIEW'
	TECH_PHONE			= 'TECH_PHONE'
	CODE_TEST			= 'TEST'
	ONSITE				= 'ONSITE'
	INTRO				= 'INTRO'
	HR					= 'HR'
	REJECT 				= 'REJECT'
	PASS				= 'PASS'
	FAIL				= 'FAIL'
	NONE				= 'NONE'
	OUTCOME				= ( (PASS, 'Pass'), (FAIL, 'Fail'), (NONE, 'Unknown') )
	INTERVIEW_STAGE		= (
							(REVIEW, 'Submit/Review'), (TECH_PHONE, 'Technical Phone'), (CODE_TEST, 'Codetest'),
							(ONSITE, 'Onsite'), (INTRO, 'Intro Call'), (HR, 'HR Call'), (REJECT, 'Reject')
						)
	job 				= models.ForeignKey(to=Job, related_name="interviews_job", null=True, blank=True)
	candidate 			= models.ForeignKey(to=Candidate, related_name="interviews_candidate", null=True, blank=True)
	interview_type		= models.CharField('interview type', max_length=11, choices=INTERVIEW_STAGE, default=TECH_PHONE, null=True)
	date_time			= models.DateTimeField('interview date/time',blank=True, null=True)
	outcome				= models.CharField('interview type', max_length=5, choices=OUTCOME, default=NONE)

	def label_from_instance(self, obj):
		return obj.name

	def calendar_display(self):
		##data is rendered on line 7430 of the fullcalendar
		#duraton is encoded in end time in the event below
		title = self.candidate.first_name + " " + self.candidate.last_name + ' / ' + self.interview_type
		return dict(
		 	id = self.pk,
		    title = title,
		    start = self.date_time.isoformat(),
			end = (self.date_time + datetime.timedelta(hours=1)).isoformat(),
		    allDay = False,
			url = self.candidate.get_url(),
			data = dict(
				job = self.job.title,
				company = self.job.company
				)
			)
