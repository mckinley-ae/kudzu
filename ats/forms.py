from django.db import models
from django.forms import ModelForm, MultiValueField, MultipleChoiceField
from .models import Candidate, Job, Interview, Tag, TagType
from datetimewidget.widgets import DateTimeWidget
from django import forms
from django.forms.widgets import RadioSelect


class CandidateSearchForm(forms.Form):
	keywords = forms.CharField(required=False)
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)
	recruiter = forms.MultipleChoiceField(required=False)

	class Meta:
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(CandidateSearchForm, self).__init__(*args, **kwargs)
		#add fields
		for tag_field_pair in add_tag_fields_to_form(self):
			self.fields[tag_field_pair[0]] = tag_field_pair[1]

class JobSearchForm(forms.Form):
	keywords = forms.CharField(required=False)
	title = forms.CharField(required=False)
	company = forms.CharField(required=False)
	recruiter = forms.MultipleChoiceField(required=False)

	class Meta:
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(JobSearchForm, self).__init__(*args, **kwargs)
		#add fields
		for tag_field_pair in add_tag_fields_to_form(self):
			self.fields[tag_field_pair[0]] = tag_field_pair[1]

class NewCandidateForm(ModelForm):
	class Meta:
		model = Candidate
		exclude = ['pub_date', 'jobs', 'change_log', 'tags']

	def __init__(self, *args, **kwargs):
		super(NewCandidateForm, self).__init__(*args, **kwargs)
		#add fields
		for tag_field_pair in add_tag_fields_to_form(self):
			self.fields[tag_field_pair[0]] = tag_field_pair[1]


class NewJobForm(ModelForm):
	class Meta:
		model = Job
		exclude = ['pub_date', 'currently_open', 'tags']

	def __init__(self, *args, **kwargs):
		super(NewJobForm, self).__init__(*args, **kwargs)
		#add fields
		for tag_field_pair in add_tag_fields_to_form(self):
			self.fields[tag_field_pair[0]] = tag_field_pair[1]


class SubmitCandidateForm(ModelForm):
	class Meta:
		model = Candidate
		job = forms.ModelMultipleChoiceField(queryset=Job.objects.all())
		fields = '__all__'

class InterviewAddForm(ModelForm):
	class Meta:
		model = Interview
		job = forms.ModelMultipleChoiceField(queryset=Job.objects.all(), required=True)
		fields = ['interview_type', 'job' ]

class UploadResumeForm(forms.Form):
	resume = forms.FileField(required=True)

	class Meta:
		fields = '__all__'

class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())





##		HELPER FUNCTIONS

def get_tag_options(tag_type):
	#accepts parameter for tag_type
	tag_options = []
	if tag_type == None:     #returns all
		for tag in Tag.objects.all():
			tag_options.append([tag.pk, tag.name])
	else:
		for tag in Tag.objects.filter(tagtype = TagType.objects.filter(name = tag_type)):
			tag_options.append([tag.pk, tag.name])
	return tag_options

def add_tag_fields_to_form(self):
	tag_field_pairs = [
		['tags_languages', forms.MultipleChoiceField(label='Language', required=False, choices=get_tag_options('LANG'))],
		['tags_function', forms.MultipleChoiceField(label='Function',required=False, choices=get_tag_options('FUNC'))],
		['tags_database', forms.MultipleChoiceField(label='Database',required=False, choices=get_tag_options('DB'))],
		['tags_technology', forms.MultipleChoiceField(label='Technology',required=False, choices=get_tag_options('TECH'))],
		['tags_miscellaneous', forms.MultipleChoiceField(label='Miscellaneous',required=False, choices=get_tag_options('MISC'))]
	]
	return tag_field_pairs
