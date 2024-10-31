from django.contrib import admin
from .models import Candidate
from .models import Question
from .models import Result


# # Register your models here.
admin.site.register(Candidate)
admin.site.register(Question)
admin.site.register(Result)

