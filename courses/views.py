import os
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm  

from django.contrib.auth import authenticate, login, logout
from .forms import userform,LessonForm,LessonFileForm, ManagerNotificationForm,NewsFeedForm,ManagerEventForm

from .models import Assignment,Payment, Files, course, courseTopic, myAssignment, myFiles, mycourses, mytopics, courseUnit, myCourseUnit, Groups, Unit,Lesson,Lesson,LessonFile,MyUnit,Manager_Eveng,MyLesson, grades as marks
from django.http import JsonResponse
from django.db.models import Q
from account.models import *
from account.forms import *
import razorpay
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import json
import requests
razorpay_client= razorpay.Client(
                        auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))

def payment1(request,courseid):
    
    
    profile = Profile.objects.get(user=request.user)
    user = profile
    course_name = course.objects.get(pk=courseid)
    
    bill_amount = (course_name.course_price)
    
    if bill_amount == 'FREE':
        bill_amount = "200"
    bill_amount = int(bill_amount)
    lessons = Lesson.objects.filter(unit__course=course_name)

    razorpay_payment = razorpay_client.order.create(
        dict(amount=(bill_amount), currency='INR'))

    order_id = razorpay_payment['id']
    order_status = razorpay_payment['status']
    data = {
        
        'title': course_name.title,
        'img': course_name.image,
        'lessons': len(lessons),
        'price': bill_amount,
        'razorpay_price':bill_amount

    }
    
    return render(request, "payment.html",{'course' : course_name,'id':order_id,'status':order_status,"data":data})


@csrf_exempt
def success(request,courseid):
    response = request.POST

    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature'],
    }

    client = razorpay.Client(
        auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
    cours = course.objects.get(pk = courseid)
    payment = Payment(student = request.user,course = cours,razorpay_order_id =response['razorpay_order_id'],razorpay_payment_id = response['razorpay_payment_id'],razorpay_signature= response['razorpay_signature'])
    payment.save()

    status = client.utility.verify_payment_signature(params_dict)
    if status:
        cours = mycourses.objects.get(user = request.user,courses__id = courseid)
        cours.paid = True
        cours.save()
        
        return redirect('home')




    return render(request, "success.html", {'status': False})

# Create your views here.
from .models import Manager_notification,News_feed
def home(request):

    college_choices = College.objects.all()

    if request.user.is_authenticated:
        if request.user.profile.status == 'p':
            college = request.user.profile.college
            courses = course.objects.filter(created_by__profile__college=college)
            return render(request, 'index.html', {'teachers': User.objects.filter(profile__status='t', profile__college=college), 'courses': courses, 'students': User.objects.filter(profile__status='s', profile__college=college)})

        if request.user.profile.status == 't' :

            courses = course.objects.filter(created_by=request.user)
            Totalcourse = len(courses)
            return render(request, 'dashboard.html', {'college_choices': college_choices,'numberofcourses':Totalcourse})

        if request.user.profile.status == 's':
            courses = mycourses.objects.get(user=request.user)
            print(courses)
            announcements = courseTopic.objects.filter(created_by = "M")
            
            notification = Manager_notification.objects.all()
            news  = News_feed.objects.all()
            all_courses = mycourses.objects.all()
            cours=courses.courses.all()
            # for i in courses:
            #     cours.append(i.courses)

            return render(request, 'student_home.html', {"announcements":announcements , 'courses': cours, 'user':request.user,'all_courses':all_courses,"news":news,"notification":notification})
        if request.user.profile.status == 'm':
            Student = Profile.objects.filter(status = "s")
            not_veri = temp_verification.objects.filter(is_varified = False,is_rejected = False)
            veri_req = temp_verification.objects.filter(is_varified = True)
            rejected = temp_verification.objects.filter(is_rejected = True)
            user_form = userform()
            # form = ManagerNotificationForm()
            # news_form = NewsFeedForm()
            
            # if request.method == "POST":
            #     if request.POST.get('announce') == 'T':
            #         print('asdf')
            #         title = request.POST['title']
            #         info = request.POST.get('info', None)
            #         document = request.FILES.getlist('document', None)
            #         link = request.POST.get('link', None)
            #         instance = courseTopic(title=title,created_by = 'M')

            #         if info:
            #             instance.info = info
            #             instance.save()
            #             if document:
            #                 for doc in document:
            #                     file = Files.objects.create(document=doc)
            #                     instance.documents.add(file)

            #             if link:
            #                 instance.link = link

            #             instance.save()
            #     if request.POST.get('notification')=='True':
                    
            #         form = ManagerNotificationForm(request.POST)
                
            #         if form.is_valid():
            #             form = form.save(commit=False)
            #             form.user = request.user
            #             form.save()
            #     elif request.POST.get('notification')=='False':
                    
            #         news_form = NewsFeedForm(request.POST)
            #         if news_form.is_valid():
            #             form = news_form.save(commit=False)
            #             form.user = request.user
            #             form.save()
            #     news_form = NewsFeedForm()
            #     form = ManagerNotificationForm()
            #     return render(request,'manager.html',{'Student':Student,'request':veri_req,"not_form":form,"news_form":news_form})

            # return render(request,'manager.html',{'Student':Student,'request':veri_req,"not_form":form,"news_form":news_form})

            
            return render(request, 'requests.html', {'Student':Student,'request':not_veri,'verified':veri_req,'rejected':rejected,"user_form":user_form})

    return render(request, 'index.html', {'college_choices': college_choices})



def coursepage(request):
    college_choices = College.objects.all()
    courses = course.objects.all()
    excluded = []
    if request.user.is_authenticated:
        excluded = mycourses.objects.get(user=request.user).courses.all()
        courses = course.objects.exclude(title__in=[ex.title for ex in excluded])
    return render(request, 'courses.html', {'courses': courses, 'excluded': excluded, 'college_choices': college_choices})

def usercourse(request):
    
    courses , _ = mycourses.objects.get_or_create(user=request.user)
    all_courses = mycourses.objects.all()
    #courses = courses.courses.all()
    if request.user.profile.status == 't':
        courses = course.objects.filter(created_by=request.user)
        choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced')]
        return render(request, 'index2.html', {'courses': courses, 'user':request.user,'choices':choices})

    return render(request, 'student_home.html', {'courses': courses, 'user':request.user,'all_courses':all_courses})



def all_courses(request):
    
    all_courses = course.objects.all()
    

    return render(request, 'all_courses.html', { 'user':request.user,'all_courses':all_courses})

def update_lesson(request,obj,lessonid, unitid,courseid):
    if request.user.profile.status == 't':
        
        if request.method == 'POST':
            unit = Unit.objects.get(id=unitid)
            lessons = Lesson.objects.filter(unit = unit)
            lesson = Lesson.objects.get(id = lessonid)
            # latest_order = Lesson.objects.filter(unit__course=unit.course).order_by('-order')
            # if latest_order:
            #     latest_order = latest_order.first().order
            # else :
            #     latest_order = 0
            
            form = LessonForm(request.POST, request.FILES,instance=lesson)
            #print(request.POST)
            if form.is_valid():
                files = request.FILES.getlist('resource')
                print(files)
                lesson = form.save(commit=False)
                lesson.unit = unit
                #lesson.order = latest_order + 1
                lesson.save()
                lesson_form = LessonForm()
                for f in files:
                    file_instance = LessonFile(lesson = lesson , file = f)
                    file_instance.save()
                return render(request, 'lesson_details.html', {'lesson_form':lesson_form,'unit': unit,'lessons':lessons, 'status': 't', 'courseid':courseid,'obj':obj})
        lesson = Lesson.objects.get(id = lessonid)     

        lesson_form = LessonForm(instance=lesson)
        unit = Unit.objects.get(id=unitid)
        
        return render(request, 'update_lesson.html', {'lesson_form':lesson_form,'lessonid':lessonid, 'unit': unit, 'status': 't', 'courseid':courseid,'obj':obj})

def delete_lesson(request,obj,lessonid, unitid,courseid):
    if request.user.profile.status == 't':
        
        
            unit = Unit.objects.get(id=unitid)
            lessons = Lesson.objects.filter(unit = unit)
            Lesson.objects.get(id = lessonid).delete()
            # latest_order = Lesson.objects.filter(unit__course=unit.course).order_by('-order')
            # if latest_order:
            #     latest_order = latest_order.first().order
            # else :
            #     latest_order = 0
            
            lesson_form = LessonForm()
            
            
            return render(request, 'lesson_details.html', {'lesson_form':lesson_form,'unit': unit,'lessons':lessons, 'status': 't', 'courseid':courseid,'obj':obj})


def unit_detail(request,obj, unitid,courseid):
    if request.user.profile.status == 't':
        
        if request.method == 'POST':
            unit = Unit.objects.get(id=unitid)
            lessons = Lesson.objects.filter(unit = unit)
            # latest_order = Lesson.objects.filter(unit__course=unit.course).order_by('-order')
            # if latest_order:
            #     latest_order = latest_order.first().order
            # else :
            #     latest_order = 0
            
            form = LessonForm(request.POST, request.FILES)
            #print(request.POST)
            if form.is_valid():
                files = request.FILES.getlist('resource')
                #print(files)
                lesson = form.save(commit=False)
                lesson.unit = unit
                # lesson.order = latest_order + 1
                lesson.save()
                lesson_form = LessonForm()
                for f in files:
                    file_instance = LessonFile(lesson = lesson , file = f)
                    file_instance.save()
                return render(request, 'lesson_details.html', {'lesson_form':lesson_form,'unit': unit,'lessons':lessons, 'status': 't', 'courseid':courseid,'obj':obj})
                return redirect('update-unit', slug=slug, unit_slug=lesson.unit.slug)
        unit = Unit.objects.get(id=unitid)
        lessons = Lesson.objects.filter(unit = unit)
        lesson_form = LessonForm()
        
        return render(request, 'lesson_details.html', {'lesson_form':lesson_form,'unit': unit,'lessons':lessons, 'status': 't', 'courseid':courseid,'obj':obj})

def show_links(request,pk):
    
        lesson = Lesson.objects.get(id = pk)
        links = (lesson.resource_link)
        if links:
            links = links.split(",")
        
        return render(request,'links.html',{'all_links':links,'obj':'document','slug':'slug'})

def show_document(request,slug):
    if request.method == 'GET':
        lesson = Lesson.objects.get(id = slug)
        print(lesson)
        documents = LessonFile.objects.filter(lesson = lesson)
        print(documents)
        return render(request,'documents.html',{'documents':documents,'obj':'document','slug':'slug'})
    
    if request.method == 'POST':
        lesson = Lesson.objects.get(id = slug)
        documents = LessonFile.objects.filter(lesson = lesson)
        return render(request,'documents.html',{'documents':documents,'obj':'document','slug':'slug'})

def lesson_detail(request, lessonid,courseid):
    if request.user.profile.status == 't':
        
        lesson = Lesson.objects.get(id=lessonid)
        #courseid = topic.course.id
        #is_unit = courseUnit.objects.filter(course__id=courseid, topics__in=[topic], name="Unit Lessons").exists()
        file = LessonFile.objects.filter(lesson = lesson)
        links = []
        if lesson.resource_link:
            links = lesson.resource_link.split(",")
        #print(file)

        return render(request, 'lesson_view.html', {'lesson': lesson, 'status': 't', 'links': links,'courseid':courseid,'file':file})


def topic_detail(request,obj, topicid,courseid):
    if request.user.profile.status == 'm':
        print('asd')
        topic = courseTopic.objects.get(id=topicid)
        links = []
        if topic.link:
            links = topic.link.split(",")
        
        return render(request, 'manager_announce_detail.html', {'course':None,'topic': topic, 'status': 'm', 'links': links, 'is_unit': None,'courseid':None,'obj':"Announcement"})

    if request.user.profile.status == 't' :
        
        
        topic = courseTopic.objects.get(id=topicid)
        courseid = topic.course.id
        course = topic.course
        is_unit = courseUnit.objects.filter(course__id=courseid, topics__in=[topic], name="Unit Lessons").exists()
        
        links = []
        if topic.link:
            links = topic.link.split(",")


        return render(request, 'view.html', {'course':course,'topic': topic, 'status': 't', 'links': links, 'is_unit': is_unit,'courseid':courseid,'obj':obj})

    topic = mytopics.objects.get(id=topicid)

    links = []
    if topic.coursetopic.link:
        links = topic.coursetopic.link.split(",")

    courseid = topic.coursetopic.course.id
    is_unit = courseUnit.objects.filter(course__id=courseid, topics__in=[topic.coursetopic], name="Unit Lessons").exists()

    return render(request, 'topic_detail.html', {'topic': topic, 'status': 's', 'is_unit': is_unit,  'links': links,'courseid':courseid})

def stu_announce_detail(request, topicid,courseid):
    

    topic = mytopics.objects.get(id=topicid)
    print(topic)
    links = []
    if topic.coursetopic.link:
        links = topic.coursetopic.link.split(",")

    courseid = topic.coursetopic.course.id
    #is_unit = courseUnit.objects.filter(course__id=courseid, topics__in=[topic.coursetopic], name="Unit Lessons").exists()

    return render(request, 'topic_detail.html', {'topic': topic, 'status': 's',  'links': links,'courseid':courseid})

def stu_topic_detail(request, id,courseid):
    
    unit = MyUnit.objects.filter(id = id)

    unit_ids = []
    for i in unit:
        unit_ids.append(i.unit.id)
    print(unit_ids)
    lessons = []
    
    
    
    lessons = MyLesson.objects.filter(unit__id__in =unit_ids)
    print(lessons)
    

    
    #is_unit = courseUnit.objects.filter(course__id=courseid, topics__in=[topic.coursetopic], name="Unit Lessons").exists()

    return render(request, 'topic_detail.html', {'topic': unit,'lessons':lessons, 'status': 's',  'courseid':courseid})

from django.http import HttpResponseRedirect

def release_topic(request,obj, topicid, courseid):
    if request.user.profile.status == 'm':
        if obj == 'Announcement':
               
            course_topic = courseTopic.objects.get(id = topicid)
            course_topic.released = True
            course_topic.save()

            links = []
            if course_topic.link:
                links = course_topic.link.split(",")
            return render(request, 'manager_announce_detail.html', {'topic': course_topic, 'status': 't','obj':"Announcement", 'links': links, 'is_unit': None,'courseid':None})
    if request.user.profile.status == 't':
        print(obj)
        if obj == 'Unit':
        
            unit = Unit.objects.get(id = topicid)
            print(unit)
            unit.released = True
            unit.save()
            print(request.path_info)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if obj == 'lesson':
           
            lesson = Lesson.objects.get(id = topicid)
            lesson.released = True
            lesson.save()

            return redirect('lesson-detail', courseid = courseid, lessonid = topicid)
       
        topic = courseTopic.objects.get(id=topicid)
        topic.released = True
        topic.save()
        
        courseid = topic.course.id
        is_unit = courseUnit.objects.filter(course__id=courseid, topics__in=[topic], name="Unit Lessons").exists()

        links = []
        if topic.link:
            links = topic.link.split(",")

        return render(request, 'view.html', {'topic': topic, 'status': 't','obj':obj, 'links': links, 'is_unit': is_unit,'courseid':courseid})

def topic_stats(request, topicid):
    my_topics = mytopics.objects.filter(coursetopic__id=topicid)
    coursetopic = courseTopic.objects.get(id=topicid)

    return render(request, "topic_stats.html", {'my_topics': my_topics, 'coursetopic': coursetopic})


def assignment_stats(request, assignmentid):
    my_topics = myAssignment.objects.filter(assignment__id=assignmentid)
    coursetopic = Assignment.objects.get(id=assignmentid)

    return render(request, "topic_stats.html", {'my_topics': my_topics, 'coursetopic': coursetopic})

def topic_unit_stats(request, topicid, documentid):
    my_topics = mytopics.objects.filter(coursetopic__id=topicid)
    coursetopic = courseTopic.objects.get(id=topicid)

    return render(request, "topic_unit_stats.html", {'my_topics': my_topics, 'documentid': documentid, 'coursetopic': coursetopic})


def course_stats(request, courseid):
    Course = course.objects.get(id=courseid)
    my_courses = Course.mycourses


    return render(request, "course_stats.html", {'course': Course, 'my_courses': my_courses})

def my_grades(request):
    if request.user.is_authenticated:
        myAssignments = myAssignment.objects.filter(user__id=request.user.id, grades__is_graded=True)

        return render(request, "my_grades.html", {'myAssignments': myAssignments})
    return redirect('home')


def rename_file(request):
    
        if request.method == 'POST':
            filename = request.POST['filename'].replace(" ", "_")
            ext = filename.split(".", 1)[1]
            filename = filename.split(".", 1)[0]
            documentid = request.POST['documentid']
            next = request.POST.get('next', '/')
            file = Files.objects.get(id=documentid)
            print(next)
            path = file.document.path.split("documents/")[0]
            #print(path)
            #print(file.document.name)
            #print(file.document.path)
            os.rename(file.document.path, path + "documents/" + filename + "." + ext)
            file.document.name = "documents/" + filename  + "." + ext
            file.save()
            #print(file.document.name)
            messages.success(request, "Filename updated")
            return HttpResponseRedirect(next)
    


def delete_file(request,obj, documentid, topicid,courseid):
    if obj == 'lesson':
        LessonFile.objects.filter(id = documentid).delete()
        return redirect('lesson-detail',courseid,topicid)

    Files.objects.filter(id=documentid).delete()

    return redirect('topic-detail',obj = obj, topicid=topicid,courseid=courseid)

def delete_assignment_file(request, documentid, assignmentid,courseid):
    Files.objects.filter(id=documentid).delete()
    assignment = Assignment.objects.get(id=assignmentid)
    submissions = myAssignment.objects.filter(assignment=assignment)
    if assignment.link :
            links = assignment.link.split(",")
    return render(request, 'assignment_view.html', {'assignment': assignment, 'submissions': submissions, 'links': links,'courseid':courseid,'obj':'Assignment'})


def assignment_detail(request,obj, assignmentid,courseid):

    if request.user.profile.status == 't':
        assignment = Assignment.objects.get(id=assignmentid)
        links = []
        cours = course.objects.get(id = courseid)
        if assignment.link :
            links = assignment.link.split(",")

        submissions = myAssignment.objects.filter(assignment=assignment)
        # for document in assignment.documents.all():
        #     print(document.document.name)

        return render(request, 'assignment_view.html', {'course':cours,'assignment': assignment, 'submissions': submissions, 'links': links,'courseid':courseid,'obj':obj})
    links = []
    assignment = myAssignment.objects.get(id=assignmentid)
    if assignment.assignment.link :
        links = assignment.assignment.link.split(",")

    return render(request, 'assignment_detail.html', {'assignment': assignment, 'links': links})

def stu_assignment_detail(request, assignmentid,courseid):
    links = []
    assignment = myAssignment.objects.get(id=assignmentid)
    if assignment.assignment.link :
        links = assignment.assignment.link.split(",")

    return render(request, 'assignment_detail.html', {'assignment': assignment, 'links': links})

def release_assignment(request,obj, assignmentid,courseid):
    
    if request.user.profile.status == 't':
        assignment = Assignment.objects.get(id=assignmentid)
        links = []
        assignment.released = True
    
        assignment.save()
        if assignment.link :
            links = assignment.link.split(",")

        submissions = myAssignment.objects.filter(assignment=assignment)
        for document in assignment.documents.all():
            print(document.document.name)

        return render(request, 'assignment_view.html', {'assignment': assignment,'obj':obj, 'submissions': submissions, 'links': links,'courseid':courseid})

def submitted(request, assignmentid):

    assignment = Assignment.objects.get(id=assignmentid)
    submissions = myAssignment.objects.filter(assignment=assignment).exclude(upload='')
    print(submissions)

    return render(request, 'submitted.html', {'submissions': submissions})

def not_submitted(request, assignmentid):

    assignment = Assignment.objects.get(id=assignmentid)
    submissions = myAssignment.objects.filter(assignment=assignment, upload='')

    return render(request, 'not_submitted.html', {'submissions': submissions})

def graded(request, assignmentid):

    assignment = Assignment.objects.get(id=assignmentid)
    submissions = myAssignment.objects.filter(assignment=assignment, grades__is_graded=True)

    return render(request, 'graded.html', {'submissions': submissions})

def not_graded(request, assignmentid):

    assignment = Assignment.objects.get(id=assignmentid)
    submissions = myAssignment.objects.filter(assignment=assignment, grades__is_graded=False).exclude(upload='')

    return render(request, 'not_graded.html', {'submissions': submissions})
    

def grades(request):

    if request.method == 'POST':
        grade = request.POST['grades']
        remark = request.POST['remark']
        assignmentid = request.POST['assignmentid']

        my_assignment = myAssignment.objects.get(id=assignmentid)
        grades = my_assignment.grades
        grades.grades = int(grade)
        grades.is_graded = True
        grades.remark = remark
        grades.save()
        my_assignment.save()

        messages.success(request, "Graded!!")
        return redirect('assignment-detail', assignmentid=my_assignment.assignment.id)
    
    messages.error(request, "Somenthing went Wrong")
    return redirect('home')


def topic_delete(request, topicid,courseid):
    topic = courseTopic.objects.get(id=topicid)
    title = topic.title
    courseid = topic.course.id
    topic.delete()
    messages.success(request ,'Your ' + title + ' is deleted')
    return redirect('courseDetail', courseid=courseid)

def assignment_delete(request, assignmentid):
    assignment = Assignment.objects.get(id=assignmentid)
    title = assignment.title
    courseid = assignment.course.id
    assignment.delete()
    messages.success(request ,'Your ' + title + ' is deleted')
    return redirect('courseDetail', courseid=courseid)

from account.forms import GroupsStudentForm



def group_student(request,pk):
    
    #created_default_groups = Groups.objects.filter(created_by__profile__college = college, status='d', created_by=request.user)
    students = Profile.objects.filter(status='s')
    default_groups_students = Groups.objects.get(id=pk)
    form = GroupsStudentForm()
    students = default_groups_students.students.all()
    
    if request.method == 'POST':
        default_groups_students.students.add(request.POST['students'])
        
        default_groups_students = Groups.objects.get(id=pk)
        
        #form = GroupsStudentForm(students)
        students = default_groups_students.students.all()
        
        return render(request, 'students.html', {'students':students,"group_name":default_groups_students,"form":form})

    return render(request, 'students.html', {'students':students,"group_name":default_groups_students,"form":form})

def profile(request,pk):
    # created_default_groups = Groups.objects.filter(created_by__profile__college=college, status='d', created_by=request.user)
    profile = Profile.objects.get(id=pk)
    #print(profile)
    
    
    return render(request, 'profile.html', {'students':profile})

def all_annoucements(reques,pk):
    pass

def groups(request):

    if (not request.user.is_authenticated) or (request.user.profile.status != 't'):
        return HttpResponse("You don't have permission to perform this action")
    college = request.user.profile.college

    #created_default_groups = Groups.objects.filter(created_by__profile__college=college, status='d', created_by=request.user)
    default_groups = Groups.objects.filter(created_by__profile__college=college, status='d')
    custom_groups = Groups.objects.filter(created_by=request.user, status='c')

    return render(request, 'groups.html', {'default_groups': default_groups, 'private_groups': custom_groups})
    

def enrollstudents(request, courseid):
    coursedet = course.objects.get(id=courseid)
    student_unit = MyUnit.objects.filter(course__id = courseid)
    students = User.objects.filter(profile__status='s', profile__college=request.user.profile.college).exclude(enrolledcourses__courses__in=[coursedet])
    enrolled_students = User.objects.filter(profile__status='s', profile__college=request.user.profile.college, enrolledcourses__courses__in=[coursedet])
    groups = Groups.objects.filter(created_by__profile__college=request.user.profile.college, status='d').exclude(enrolled_courses__in=[coursedet]) | Groups.objects.filter(created_by=request.user).exclude(enrolled_courses__in=[coursedet])
    return render(request, 'enrollstudents.html', {'course': coursedet, 'user':request.user, 'students': students, 'groups': groups, 'enrolled_students': enrolled_students, 'searched': False})

def search_students(request):
    query = request.POST['search']
    courseid = request.POST['courseid']

    coursedet = course.objects.get(id=courseid)

    if query == '':
         enrolled_students = User.objects.filter(profile__status='s', profile__college=request.user.profile.college, enrolledcourses__courses__in=[coursedet])
    else:
        enrolled_students = User.objects.filter(profile__status='s', profile__college=request.user.profile.college, enrolledcourses__courses__in=[coursedet], username__icontains=query)


    students = User.objects.filter(profile__status='s', profile__college=request.user.profile.college).exclude(enrolledcourses__courses__in=[coursedet])  
    groups = Groups.objects.filter(created_by__profile__college=request.user.profile.college, status='d').exclude(enrolled_courses__in=[coursedet]) | Groups.objects.filter(created_by=request.user).exclude(enrolled_courses__in=[coursedet])
    return render(request, 'enrollstudents.html', {'course': coursedet, 'user':request.user, 'students': students, 'groups': groups, 'enrolled_students': enrolled_students, 'searched': True, 'query': query})



def enrollcourse(request, courseid, studentid):

    if request.user.profile.status != 't':
        messages.error(request, "You are not the staff")
        return redirect('home')
    
    student = User.objects.get(id=studentid)

    addcourse = course.objects.get(id=courseid)
    mycourse,_ = mycourses.objects.get_or_create(user=student)
    mycourse.courses.add(addcourse)
    mycourse.save()
    print(courseid)

    unit = Unit.objects.filter(course = addcourse)
    print(unit)
    
    
    
    for i in unit:
        myunit= MyUnit.objects.create(user = student,unit=i,course = addcourse)
        myunit.save()
        
        lesson = Lesson.objects.filter(unit = i)
        
        for j in lesson:
            mylesson = MyLesson.objects.create(user = student,lesson=j,unit=i)
            mylesson.save()


    # topics = courseTopic.objects.filter(course = courseid)

    # # for topic in topics:
    # #     mytopics.objects.create(user=request.user, coursetopic=topic)

    units = courseUnit.objects.filter(course__id=courseid)

    for unit in units:
        myunit = myCourseUnit.objects.create(courseunit=unit, user=student)
        for topic in unit.topics.all():
            mytopic = mytopics(user=student, coursetopic=topic)
            mytopic.save()
            myunit.coursetopics.add(mytopic)
        for assignment in unit.assignments.all():
            my_assignment = myAssignment(user=student, assignment=assignment)
            my_assignment.save()
            marks.objects.create(myassignment=my_assignment)
            myunit.course_assignments.add(my_assignment)
        myunit.save()

    messages.success(request, 'course enrolled successfully')
    return redirect('enroll-students', courseid=courseid)

def enroll_group(request, courseid, groupid):

    if request.user.profile.status != 't':
        messages.error(request, "You are not the staff")
        return redirect('home')

    group = Groups.objects.get(id=groupid)
    addcourse = course.objects.get(id=courseid)
    units = courseUnit.objects.filter(course__id=courseid)

    for student in group.students.all():
        user = User.objects.get(profile = student)
        
        mycourse = mycourses.objects.get(user=user)

        if addcourse not in mycourse.courses.all():
            mycourse.courses.add(addcourse)
            mycourse.save()

            for unit in units:
                myunit = myCourseUnit.objects.create(courseunit=unit, user=student)
                for topic in unit.topics.all():
                    mytopic = mytopics(user=student, coursetopic=topic)
                    mytopic.save()
                    myunit.coursetopics.add(mytopic)
                myunit.save()
    
    group.enrolled_courses.add(addcourse)
    group.save()

    messages.success(request, 'course enrolled to group successfully')
    return redirect('enroll-students', courseid=courseid)

def unenroll_student(request, studentid, courseid):
    student = User.objects.get(id=studentid)
    Course  = course.objects.get(id=courseid)

    student.enrolledcourses.courses.remove(Course)
    student.save()
    mytopics.objects.filter(user=student, coursetopic__course=Course).delete()
    myAssignment.objects.filter(user=student, assignment__course=Course).delete()
    myCourseUnit.objects.filter(user=student, courseunit__course=Course).delete()
    MyUnit.objects.filter(user = student,course__id = courseid).delete()
    unit = Unit.objects.filter(course__id = courseid)
    unitid = []
    for i in unit:
        unitid.append(i.id)
    print(unitid)
    MyLesson.objects.filter(user= student,unit_id__in = unitid).delete()
    messages.success(request, "student unenrolled successfully")
    return redirect('enroll-students', courseid=courseid)
        


def courseDetail(request, courseid):
    
    if request.user.profile.status == 't':
        coursedet = course.objects.get(id=courseid)
        courseunits = courseUnit.objects.filter(course__id = courseid)
       
        return render(request, 'course-content-detail.html', {'courseunits': courseunits, 'course': coursedet,'courseid':courseid})

    mycourseunits = myCourseUnit.objects.filter(user=request.user, courseunit__course__id=courseid)
    
    return render(request, 'course-detail.html', {'mycourseunits': mycourseunits,'courseid':courseid})

def courseunit(request, courseid):
    
    mycourseunits = myCourseUnit.objects.filter(user=request.user, courseunit__course__id=courseid)
    
    units = MyUnit.objects.filter(user = request.user,course__id = courseid)
    #print(units)
    for i in mycourseunits:
    
        
        if i.courseunit.name == 'Announcement':
            
            assign=  i.coursetopics.all()
        
    
    
    return render(request, 'course_units.html', {'units':units,'courseid':courseid,'assignments':assign})
    
def student_learning_page(request, courseid):
    mycourseunits = myCourseUnit.objects.filter(user=request.user, courseunit__course__id=courseid)
    units = Unit.objects.filter(course__id = courseid)
    lessons = []
    for unit in units:
        lesson = unit.lessons.all()
        lessons.append(lesson)
    
    mylist = zip(units, lessons)
    

    return render(request, 'student_learning_page.html', {"units":units,"courseid":courseid,'lessons':lessons,'mylist':mylist})

def test_assign_page(request, courseid):
    mycourseunits = myCourseUnit.objects.filter(user=request.user, courseunit__course__id=courseid)
    
    for i in mycourseunits:
        
        if i.courseunit.name == 'Assignment':
            
            assign=  i.course_assignments.all()
    

    return render(request, 'test_assignment.html', {"assign":assign,"courseid":courseid})

def student_files(request, courseid):
    mycourseunits = myCourseUnit.objects.filter(user=request.user, courseunit__course__id=courseid)
    
    
    for i in mycourseunits:
        
        if i.courseunit.name == 'Assignment':
            
            assign=  i.course_assignments.all()
    

    return render(request, 'student_files.html', {"assign":assign})

def assignDetail(request,obj,courseid):
    
    if request.user.profile.status == 't':
        coursedet = course.objects.get(id=courseid)
    
        
        courseunits = courseUnit.objects.filter(course__id = courseid)
        return render(request, 'assignment.html', {'courseunits': courseunits, 'course': coursedet,"obj":obj,'courseid':courseid})

    mycourseunits = myCourseUnit.objects.filter(user=request.user)
    return render(request, 'course-detail.html', {'mycourseunits': mycourseunits})

def unitDetail(request,obj,courseid):
    if request.user.profile.status == 't':
        coursedet = course.objects.get(id=courseid)
        
       
        units = Unit.objects.filter(course__id = courseid)
        
        return render(request, 'units.html', {'units': units, 'course': coursedet,"obj":obj,'courseid':courseid})

    mycourseunits = myCourseUnit.objects.filter(user=request.user)
    units = Unit.objects.filter(course__id = courseid)
    
    return render(request, 'course-detail.html', {'mycourseunits': mycourseunits,'units':units})

def announceDetail(request,obj,courseid):
    
    if obj=='Timetable':
        obj='Time Table'
    if obj=='Unit':
        obj='Unit Lessons'

    if request.user.profile.status == 'm':
        courseunits = courseTopic.objects.filter(created_by = 'M')
        if request.method == 'POST':
            print('yes')
            if request.POST.get('announce') == 'T':
                        print('asdf')
                        title = request.POST['title']
                        info = request.POST.get('info', None)
                        document = request.FILES.getlist('document', None)
                        link = request.POST.get('link', None)
                        instance = courseTopic(title=title,created_by = 'M')

                        if info:
                            instance.info = info
                            instance.save()
                            if document:
                                for doc in document:
                                    file = Files.objects.create(document=doc)
                                    instance.documents.add(file)

                            if link:
                                instance.link = link

                        instance.save()
        return render(request, 'manager_announce.html', {'courseunits': courseunits})
        
    if request.user.profile.status == 't':
        coursedet = course.objects.get(id=courseid)
        #print(coursedet)
       
        courseunits = courseUnit.objects.filter(course__id = courseid)
        return render(request, 'announcements.html', {'courseunits': courseunits, 'course': coursedet,"obj":obj,'courseid':courseid})

    mycourseunits = myCourseUnit.objects.filter(user=request.user)
    return render(request, 'course-detail.html', {'mycourseunits': mycourseunits})

def group_detail(request, groupid):
    group = Groups.objects.get(id=groupid)

    enrolled = []
    for stu in group.students.all():
        enrolled.append(stu.username)

    students_unenrolled = User.objects.filter(profile__college=request.user.profile.college, profile__status='s').exclude(username__in=enrolled)

    if request.user.profile.status == 't':
        return render(request, 'group_detail.html', {'group': group, 'teacher': request.user, 'students_unenrolled': students_unenrolled})
    
    return HttpResponse('Something went wrong')

def create_course(request):

    user = request.user
    if(user.profile.status != 't'):
        messages.error(request, "You are not the staff so you can't create a course")
        return redirect('usercourse')

    if request.method == 'POST':
       
        title = request.POST['title']
        next = request.POST.get('next', '/')
        print(next)
        price = request.POST['price']
        level = request.POST['level']
        category = request.POST['category']
        image = request.FILES['image']
        
        instance = course(title=title, category=category, created_by=user, image=image,course_price = price, course_level = level)
        # instance.image = image
        print(instance)
        instance.save()

        messages.success(request, "Your course has been created.")
        return redirect('usercourse')
    
    #messages.error('something went wrong')
    return redirect('home')

def edit_course(request):

    user = request.user
    if(user.profile.status != 't'):
        messages.error(request, "You are not the staff so you can't edit a course")
        return redirect('home')

    if request.method == 'POST':
        title = request.POST['title']
        courseid = request.POST.get('courseid')
        category = request.POST['category']
        image = request.FILES.get('image', None)

        instance = course.objects.get(id=courseid)
        instance.title=title
        instance.category=category
        if image != None:
            instance.image=image

        instance.save()

        messages.success(request, "Your course has been Updated.")
        return redirect('courseDetail', courseid=courseid)
    
    messages.error('something went wrong')
    return redirect('home')


def delete_course(request, courseid):
    print(courseid)
    course.objects.filter(id=courseid).delete()

    messages.success(request, "Course Deleted Successfully")
    return redirect('usercourse')


def create_course_unit(request):

    user = request.user
    if(user.profile.status != 't'):
        messages.error(request, "You are not the staff so you can't create a course unit")
        return redirect('home')

    if request.method == 'POST':
        name = request.POST['name']
        courseid = request.POST['courseid']

        instance = courseUnit(name=name, course=course.objects.get(id=courseid))
        instance.save()

        messages.success(request, "Your course unit has been created.")
        return redirect("courseDetail", courseid=instance.course.id)
    
    messages.error('something went wrong')
    return redirect('home')

def create_unit(request,obj):
    
    user = request.user
    if(user.profile.status != 't'):
        messages.error(request, "You are not the staff so you can't create a course topic")
        return redirect('home')

    if request.method == 'POST':
        if obj == 'Unit':
            
            courseid = request.POST['courseunitid']
            title = request.POST['title']
            brief = request.POST.get('brief', None)
            cours = course.objects.get(id = courseid)
            due = request.POST.get('due')

            instance = Unit(title=title,brief =brief, due = due, course = cours)


            instance.save()
            return redirect("unitDetail", courseid=courseid,obj = obj )
def update_unit(request,obj,unitid):
    
    user = request.user
    if(user.profile.status != 't'):
        messages.error(request, "You are not the staff so you can't create a course topic")
        return redirect('home')

    if request.method == 'POST':
        if obj == 'Unit':
            print(unitid)
            print(request.POST)
            instance = Unit.objects.get(pk = unitid)
            print(request.POST['courseid'])
            courseid = request.POST['courseid']
            title = request.POST['title']
            brief = request.POST.get('brief', None)
            cours = course.objects.get(id = courseid)
            due = request.POST.get('due')

            instance = Unit.objects.filter(id = unitid).update(title=title,brief =brief, due = due, course = cours)
            

            
            return redirect("unitDetail", courseid=courseid,obj = obj )

        

def create_topic(request,obj):

    user = request.user
    if(user.profile.status != 't'):
        messages.error(request, "You are not the staff so you can't create a course topic")
        return redirect('home')

    

    if request.method == 'POST':
        courseunitid = request.POST['courseunitid']
        courseunit = courseUnit.objects.get(id=courseunitid)
        title = request.POST['title']
        info = request.POST.get('info', None)
        document = request.FILES.getlist('document', None)
        link = request.POST.get('link', None)
        

        if courseunit.is_assignment == False:
  

            instance = courseTopic(title=title, course=courseunit.course)

            if info:
                instance.info = info
            instance.save()
            if document:
                for doc in document:
                    file = Files.objects.create(document=doc)
                    instance.documents.add(file)

            if link:
                instance.link = link
                links = []
                links = instance.link.split(",")
            
            
            instance.save()

            courseunit.topics.add(instance)
            courseunit.save()
            is_unit = courseUnit.objects.filter(course__id=courseunit.course.id, topics__in=[instance], name="Unit Lessons").exists()

            messages.success(request, "Your topic to the unit has been added.")
            #return redirect("announceDetail", courseid=courseunit.course.id,obj = obj )
            return render(request, 'view.html', {'course':courseunit.course,'topic': instance, 'status': 't', 'links': links, 'is_unit': is_unit,'courseid':courseunit.course.id,'obj':obj})

        max_grades = request.POST['grades']
        deadline = request.POST['deadline']

        

        instance = Assignment(course=courseunit.course ,title=title, max_grades=max_grades, deadline=deadline)

        if info:
            instance.info = info

        instance.save()
            
        if document:
            for doc in document:
                file = Files.objects.create(document=doc)
                instance.documents.add(file)

        if link:
            instance.link = link
            links = []
            links = instance.link.split(",")
        
        instance.save()
        courseunit.assignments.add(instance)
        courseunit.save()
        submissions = myAssignment.objects.filter(assignment=instance)

        messages.success(request, "Your Work to the unit has been added.")
        #return redirect("assignDetail", courseid=courseunit.course.id,obj = obj)
        return render(request, 'assignment_view.html', {'course':courseunit.course,'assignment': instance, 'submissions': submissions, 'links': links,'courseid':courseunit.course.id,'obj':obj})
    
    messages.error(request, 'something went wrong')
    return redirect('home')


def submit_assignment(request):

    if request.method == 'POST':
        my_assignment = myAssignment.objects.get(id=request.POST['assignmentid'])
        document = request.FILES['document']
        assignment = my_assignment.assignment

        if(assignment.submittable() == False):
            messages.error(request, "Deadline ended you can't submit now")
            return redirect('assignment-detail', assignmentid=my_assignment.id)

        my_assignment.upload = document

        my_assignment.save()
        messages.success(request, "You have submitted your work to " + my_assignment.assignment.title)
        return redirect('assignment-detail', assignmentid=my_assignment.id)

    return HttpResponse('Something went wrong')


def create_group(request):
    if (not request.user.is_authenticated) or (request.user.profile.status != 't'):
        return HttpResponse("You don't have permission to perform this action")
    
    if request.method == 'POST':
        name = request.POST['name']
        status = request.POST['status']
        next = request.POST['next']
        user = request.user

        group = Groups(name=name, status=status, created_by=user)
        group.save()
        messages.success(request, "you have successfully added a group")
        return HttpResponseRedirect(next)
    
    messages.error(request, "Something went wrong")
    return redirect('home')


def add_student_to_group(request, studentid, groupid):
    student = User.objects.get(id=studentid)
    group = Groups.objects.get(id=groupid)

    if request.user.is_authenticated and request.user == group.created_by:
        group.students.add(student)
        group.save()
        messages.success(request, student.username + " added to this group")
        return redirect('group-detail', groupid=group.id)
    
    messages.error(request, "You can't perform this action")
    return redirect('home')

def remove_student_to_group(request, studentid, groupid):
    student = User.objects.get(id=studentid)
    group = Groups.objects.get(id=groupid)

    if request.user.is_authenticated and request.user == group.created_by:
        group.students.remove(student)
        group.save()
        messages.success(request, student.username + " removed from this group")
        return redirect('group-detail', groupid=group.id)
    
    messages.error(request, "You can't perform this action")
    return redirect('home')



def topiComp(request, coursetopic):
    Topic = mytopics.objects.get(user=request.user, id=coursetopic)
    done = True
    if(Topic.done == True):
        mytopics.objects.filter(user=request.user, id=coursetopic).update(done = False)
        done = False
    else:
       mytopics.objects.filter(user=request.user, id=coursetopic).update(done=True)
       done=True

    data = {
        'done': done,
    }

    return JsonResponse(data)

def lessonComp(request, lessonid):
    #print(lessonid)
    lesson = MyLesson.objects.get(id=lessonid)
    isdone = True
    #print(lesson)
    if(lesson.isdone == True):
        MyLesson.objects.filter(id=lessonid).update(isdone = False)
        isdone = False
    else:
       MyLesson.objects.filter(id=lessonid).update(isdone=True)
       isdone=True

    data = {
        'done': isdone,
    }

    return JsonResponse(data)


def unitTopiComp(request, documentid):
    file = myFiles.objects.get(id=documentid)
    done = True
    if(file.done == True):
        myFiles.objects.filter(id=documentid).update(done = False)
        done = False
    else:
       myFiles.objects.filter(id=documentid).update(done=True)
       done=True

    data = {
        'done': done,
    }

    return JsonResponse(data)

def assignmentComp(request, assignmentid):
    my_assignment = myAssignment.objects.get(id=assignmentid)
    done = True
    if(my_assignment.done == True):
        my_assignment.done = False
        done = False
    else:
       my_assignment.done = True
       done=True
    
    my_assignment.save()

    data = {
        'done': done,
    }

    return JsonResponse(data)

def add_file(request,courseid):
    if request.method == 'POST':
        islesson  = request.POST['islesson']
        document = request.FILES.getlist('document', None)
        assignmentid = request.POST['assignmentid']
        isassignment = request.POST['isassignment']

        if islesson == 'True':

            lesson = Lesson.objects.get(id = assignmentid)
            for doc in document:
                file = LessonFile.objects.create(file = doc,lesson = lesson)
                file.save()
            messages.success(request, "You have added the file successfully")

            return redirect('lesson-detail', courseid = courseid, lessonid = assignmentid)
        if isassignment == 'True':
            assignment = Assignment.objects.get(id=assignmentid)
            for doc in document:
                file = Files.objects.create(document=doc)
                assignment.documents.add(file)
            assignment.save()

            messages.success(request, "You have added the file successfully")
            # return redirect('assignment-detail', assignmentid=assignmentid,courseid=courseid)
            
            assignment = Assignment.objects.get(id=assignmentid)
            links = []

            if assignment.link :
                links = assignment.link.split(",")

            submissions = myAssignment.objects.filter(assignment=assignment)
        

            return render(request, 'assignment_view.html', {'assignment': assignment, 'submissions': submissions, 'links': links,'courseid':courseid,'obj':'Assignment'})
        else:
            topic = courseTopic.objects.get(id=assignmentid)

            for doc in document:
                file = Files.objects.create(document=doc)
                topic.documents.add(file)

            topic.save()
            messages.success(request, "You have added the file successfully")
            return redirect('topic-detail', topicid=assignmentid,courseid=courseid)
        
    return HttpResponse("Something went wrong", status=404)


def add_link(request,courseid):
    if request.method == 'POST':
        islesson  = request.POST['islesson']
        link = request.POST['link']
        assignmentid = request.POST['assignmentid']
        isassignment = request.POST['isassignment']

        if islesson == 'True':
            lesson = Lesson.objects.get(id = assignmentid)
            if not lesson.resource_link :
                lesson.resource_link = link
            else:
                lesson.resource_link = str(lesson.resource_link) + "," + link
            lesson.save()

            messages.success(request, "You Link have been added successfully")
            return redirect('lesson-detail', lessonid=lesson.id,courseid=courseid)

        if isassignment == 'True':
            assignment = Assignment.objects.get(id=assignmentid)
            if not assignment.link :
                assignment.link = link
            else:
                assignment.link = str(assignment.link) + "," + link

            assignment.save()

            messages.success(request, "You Link have been added successfully")
            return redirect('assignment-detail', assignmentid=assignmentid,courseid=courseid,obj='Assignment')

        else:
            topic = courseTopic.objects.get(id=assignmentid)
            if not topic.link :
                topic.link = link
            else:
                topic.link = str(topic.link) + "," + link

            topic.save()
            messages.success(request, "You Link have been added successfully")
            return redirect('topic-detail',obj = 'Announcement', topicid=assignmentid,courseid=courseid)
        
    return HttpResponse("Something went wrong", status=404)   


def delete_link_assignment(request, assignmentid, link,courseid):

    assignment = Assignment.objects.get(id=assignmentid)
    links = assignment.link.split(",")


    links.remove(links[int(link)-1])
    
    assignment.link = ",".join(links)
    assignment.save()

    messages.success(request, "link deleted")
    return redirect('assignment-detail', assignmentid=assignmentid,courseid=courseid,obj='Assignment')


def delete_link_topic(request,obj, topicid, link,courseid):
    if obj == 'topic':
        topic = courseTopic.objects.get(id=topicid)
        links = topic.link.split(",")


        links.remove(links[int(link)-1])
        
        topic.link = ",".join(links)
        topic.save()

        messages.success(request, "link deleted")
        return redirect('topic-detail',obj = 'Announcement', topicid=topicid,courseid=courseid)
    if obj == 'lesson':
        topic = Lesson.objects.get(id = topicid)
        links = topic.resource_link.split(",")
        #print(links)

        links.remove(links[int(link)-1])
        
        topic.resource_link = ",".join(links)
        topic.save()

        messages.success(request, "link deleted")
        return redirect('lesson-detail', lessonid=topic.id,courseid=courseid)
        





def edit_topic(request,courseid):
    if request.method == 'POST':
        assignmentid = request.POST['assignmentid']
        isassignment = request.POST['isassignment']
        deadline = request.POST.get('deadline')
        title = request.POST['title']
        max_grades = request.POST.get('max_grades', None)
        info = request.POST['info']

        if isassignment == 'True':
            Assignment.objects.filter(id=assignmentid).update(title = title, max_grades = max_grades, info = info, deadline=deadline)

            messages.success(request, "Updated!!")
            return redirect('assignment-detail', assignmentid=assignmentid,courseid=courseid)

        else:
            courseTopic.objects.filter(id=assignmentid).update(title = title, info = info)

            messages.success(request, "Updated!!")
            return redirect('topic-detail', topicid=assignmentid,courseid=courseid)

from account.forms import student_verificationform
def student_setting(request):
    
    student = Profile.objects.get(user = request.user)
    is_verified = False
    if student.is_verified:
        is_verified = True
    #print(student)
    form = student_verificationform()
    if request.method == "POST":
        #print(request.POST)
        form = student_verificationform(request.POST, request.FILES)
        if form.is_valid():
            mod  = form.save(commit=False)
            
            mod.user = request.user
            mod.save()
        form = student_verificationform
        return render(request,'student_setting.html' ,{"student":student,"form":form,"is_ver":is_verified})

    return render(request,'student_setting.html' ,{"student":student,"form":form,"is_ver":is_verified})

from account.serializer import temp_verification_ser

def accept_req(request,userid):
    profile  = Profile.objects.get(user_id = userid)
    data = temp_verification.objects.filter(user_id = userid).first()
    profile.section = data.section
    profile.semester = data.semester
    profile.Year = data.Year
    profile.roll_number = data.roll_number
    profile.is_verified = True
    profile.department = data.department
    profile.college = data.college

    profile.save()

    data.is_varified=True
    data.save()
    return render(request,'profile.html',{'student':profile})
    
def reject_req(request,userid):
    profile  = Profile.objects.get(user_id = userid)
    profile.is_rejected = True
    data = temp_verification.objects.filter(user_id = userid).first()
    data.is_rejected = True
    data.save()
    profile.save()
    

    return render(request,'profile.html',{'student':profile})

def manager_event(request):
    event = Manager_Eveng.objects.filter(user = request.user)
    event_form = ManagerEventForm()

    if request.method == "POST":
        if request.POST.get('events') == 'True':
            event_form = ManagerEventForm(request.POST)
            if event_form.is_valid():
                form = event_form.save(commit=False)
                form.user = request.user
                form.save() 
        event_form = ManagerEventForm()
        return render(request,'events.html',{"event_form":event_form,"events":event}) 


    return render(request,'events.html',{"event_form":event_form,"events":event})
    
def manager_noti(request):
    notifications = Manager_notification.objects.filter(user = request.user)
    news = News_feed.objects.filter(user = request.user)
    event = Manager_Eveng.objects.filter(user = request.user)
    form = ManagerNotificationForm()
    event_form = ManagerEventForm()
    news_form = NewsFeedForm()
    
    if request.method == "POST":
        
        if request.POST.get('noti')=='True':
            
            form = ManagerNotificationForm(request.POST)
        
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
        elif request.POST.get('noti')=='False':
            
            news_form = NewsFeedForm(request.POST)
            if news_form.is_valid():
                form = news_form.save(commit=False)
                form.user = request.user
                form.save()
        elif request.POST.get('events') == 'True':
            event_form = ManagerEventForm(request.POST)
            if event_form.is_valid():
                form = event_form.save(commit=False)
                form.user = request.user
                form.save()         
        
        news_form = NewsFeedForm()
        form = ManagerNotificationForm()
        event_form = ManagerEventForm()
        return render(request,'manager.html',{"not_form":form,"news_form":news_form,"notifications":notifications,"news":news,"event_form":event_form,"events":event})

    return render(request,'manager.html',{"not_form":form,"news_form":news_form,"notifications":notifications,"news":news,"event_form":event_form,"events":event})


def teacher_profile(request):
    if request.user.profile.status == 'm':
        teacher  = Profile.objects.filter(status = 't')
        teacher_form = userform()
        return render(request , 'teacher_profile.html', {'teacher':teacher,"teacher_form":teacher_form})

    if request.user.profile.status == 's':
        teacher  = Profile.objects.filter(status = 't',semester = request.user.profile.semester)

        return render(request , 'student_preference.html', {'teacher':teacher})

def update_man_not(request, obj):
    if request.user.profile.status == 'm':
        
        #print(request.POST)
        if obj == 'notification':
            id = request.POST.get('id')
           
            instance = Manager_notification.objects.get(pk = id)
            form = ManagerNotificationForm(request.POST, instance=instance)
            if form.is_valid():
                
                form.save(commit=False)
                form.user = request.user
                form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    
        if obj == 'news':
                id = request.POST.get('id')
                instance = News_feed.objects.get(pk = id)
                form = NewsFeedForm(request.POST, instance=instance)
                if form.is_valid():
                    form.save(commit=False)
                    form.user = request.user
                    form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if obj == 'events':
                id = request.POST.get('id')
                instance = Manager_Eveng.objects.get(pk = id)
                form = ManagerEventForm(request.POST, instance=instance)
                if form.is_valid():
                    print('e')
                    form.save(commit=False)
                    form.user = request.user
                    form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 


def del_man_not(request, obj, id):
    if request.user.profile.status == 'm':
        
        if obj == 'notification':
            instance = Manager_notification.objects.get(pk = id)
            instance.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    
    if obj == 'news':
            instance = News_feed.objects.get(pk = id)
            instance.delete()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if obj == 'events':
            instance = Manager_Eveng.objects.get(pk = id)
            instance.delete()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 