from django.contrib import admin
from .models import Assignment,Groups, College, Files, courseTopic, course, grades, myAssignment, myFiles, mytopics, mycourses, courseUnit, myCourseUnit, Profile

# Register your models here.

admin.site.register(course)
admin.site.register(courseTopic)
admin.site.register(courseUnit)
admin.site.register(Assignment)

admin.site.register(mycourses)
admin.site.register(Groups)
admin.site.register(mytopics)
admin.site.register(myCourseUnit)
admin.site.register(myAssignment)
admin.site.register(grades)
admin.site.register(College)
admin.site.register(Files)
admin.site.register(myFiles)

admin.site.register(Profile)
