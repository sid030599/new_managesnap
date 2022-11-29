from django.contrib import admin
from .models import Assignment,Groups, College, Files, courseTopic, course, grades, myAssignment,MyUnit,MyLesson, myFiles, mytopics, mycourses, courseUnit, myCourseUnit, Profile,Lesson,LessonFile,Unit

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
admin.site.register(Lesson)
admin.site.register(LessonFile)
admin.site.register(Unit)
admin.site.register(MyUnit)
admin.site.register(MyLesson)

admin.site.register(Profile)
