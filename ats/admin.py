from django.contrib import admin
from .models import Candidate, Job, Recruiter, Tag, TagType

admin.site.register(Job)
admin.site.register(Candidate)
admin.site.register(Recruiter)
admin.site.register(Tag)
admin.site.register(TagType)
