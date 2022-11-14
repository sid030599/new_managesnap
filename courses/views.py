import os
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import userform
from .models import Assignment,Profile, College, Files, course, courseTopic, myAssignment, myFiles, mycourses, mytopics, courseUnit, myCourseUnit, Groups, grades as marks
from django.http import JsonResponse
from django.db.models import Q


# Create your views here.
def home(request):

    college_choices = College.objects.all()

    if request.user.is_authenticated:
        if request.user.profile.status == 'p':
            college = request.user.profile.college
            courses = course.objects.filter(created_by__profile__college=college)
            return render(request, 'index.html', {'teachers': User.objects.filter(profile__status='t', profile__college=college), 'courses': courses, 'students': User.objects.filter(profile__status='s', profile__college=college)})

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
    print(request.user)
    courses , _ = mycourses.objects.get_or_create(user=request.user)
    courses = courses.courses.all()
    if request.user.profile.status == 't':
        courses = course.objects.filter(created_by=request.user)
        return render(request, 'index2.html', {'courses': courses, 'user':request.user})

    return render(request, 'mycourses.html', {'courses': courses, 'user':request.user})


def topic_detail(request, topicid):
    if request.user.profile.status == 't':
        topic = courseTopic.objects.get(id=topicid)
        courseid = topic.course.id
        is_unit = courseUnit.objects.filter(course__id=courseid, topics__in=[topic], name="Unit Lessons").exists()
        
        links = []
        if topic.link:
            links = topic.link.split(",")


        return render(request, 'view.html', {'topic': topic, 'status': 't', 'links': links, 'is_unit': is_unit})

    topic = mytopics.objects.get(id=topicid)

    links = []
    if topic.coursetopic.link:
        links = topic.coursetopic.link.split(",")

    courseid = topic.coursetopic.course.id
    is_unit = courseUnit.objects.filter(course__id=courseid, topics__in=[topic.coursetopic], name="Unit Lessons").exists()

    return render(request, 'topic_detail.html', {'topic': topic, 'status': 's', 'is_unit': is_unit,  'links': links})

def release_topic(request, topicid):
    
    topic = courseTopic.objects.get(id=topicid)
    topic.released = True
    print(topic)
    topic.save()
    courseid = topic.course.id
    is_unit = courseUnit.objects.filter(course__id=courseid, topics__in=[topic], name="Unit Lessons").exists()

    links = []
    if topic.link:
        links = topic.link.split(",")


    return render(request, 'view.html', {'topic': topic, 'status': 't', 'links': links, 'is_unit': is_unit})

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
    


def delete_file(request, documentid, topicid):
    Files.objects.filter(id=documentid).delete()

    return redirect('topic-detail', topicid=topicid)

def delete_assignment_file(request, documentid, assignmentid):
    Files.objects.filter(id=documentid).delete()

    return redirect('assignment-detail', assignmentid=assignmentid)


def assignment_detail(request, assignmentid):

    if request.user.profile.status == 't':
        assignment = Assignment.objects.get(id=assignmentid)
        links = []

        if assignment.link :
            links = assignment.link.split(",")

        submissions = myAssignment.objects.filter(assignment=assignment)
        for document in assignment.documents.all():
            print(document.document.name)

        return render(request, 'assignment_view.html', {'assignment': assignment, 'submissions': submissions, 'links': links})
    links = []
    assignment = myAssignment.objects.get(id=assignmentid)
    if assignment.assignment.link :
        links = assignment.assignment.link.split(",")

    return render(request, 'assignment_detail.html', {'assignment': assignment, 'links': links})

def release_assignment(request, assignmentid):
    
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

        return render(request, 'assignment_view.html', {'assignment': assignment, 'submissions': submissions, 'links': links})

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


def topic_delete(request, topicid):
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


def group_student(request,pk):
    
    # created_default_groups = Groups.objects.filter(created_by__profile__college=college, status='d', created_by=request.user)
    default_groups_students = Groups.objects.get(id=pk)

    students = default_groups_students.students.all()
    return render(request, 'students.html', {'students':students})

def profile(request,pk):
    print(pk)
    # created_default_groups = Groups.objects.filter(created_by__profile__college=college, status='d', created_by=request.user)
    
    profile = Profile.objects.get(id=pk)
    print(profile)
    
    
    return render(request, 'profile.html', {'students':profile})

def all_annoucements(reques,pk):
    pass

def groups(request):

    if (not request.user.is_authenticated) or (request.user.profile.status != 't'):
        return HttpResponse("You don't have permission to perform this action")
    college = request.user.profile.college

    # created_default_groups = Groups.objects.filter(created_by__profile__college=college, status='d', created_by=request.user)
    default_groups = Groups.objects.filter(created_by__profile__college=college, status='d')
    custom_groups = Groups.objects.filter(created_by=request.user, status='c')

    return render(request, 'groups.html', {'default_groups': default_groups, 'custom_groups': custom_groups})
    

def enrollstudents(request, courseid):
    coursedet = course.objects.get(id=courseid)

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
    print(studentid)
    student = User.objects.get(id=studentid)
    print(student)
    addcourse = course.objects.get(id=courseid)
    mycourse,_ = mycourses.objects.get_or_create(user=student)
    mycourse.courses.add(addcourse)
    mycourse.save()

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
        mycourse = mycourses.objects.get(user=student)

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

    messages.success(request, "student unenrolled successfully")
    return redirect('enroll-students', courseid=courseid)
        


def courseDetail(request, courseid):

    if request.user.profile.status == 't':
        coursedet = course.objects.get(id=courseid)
        courseunits = courseUnit.objects.filter(course__id = courseid)
        return render(request, 'course-content-detail.html', {'courseunits': courseunits, 'course': coursedet})

    mycourseunits = myCourseUnit.objects.filter(user=request.user, courseunit__course__id=courseid)
    return render(request, 'course-detail.html', {'mycourseunits': mycourseunits})

def assignDetail(request,obj):
    print(obj)
    if request.user.profile.status == 't':
        coursedet = course.objects.all()
        print(coursedet)
        for i in coursedet:
            print(i.title)
        courseunits = courseUnit.objects.all()
        return render(request, 'assignment.html', {'courseunits': courseunits, 'course': coursedet,"obj":obj})

    mycourseunits = myCourseUnit.objects.filter(user=request.user)
    return render(request, 'course-detail.html', {'mycourseunits': mycourseunits})

def announceDetail(request,obj):
    
    if obj=='Timetable':
        obj='Time Table'
    if obj=='Unit':
        obj='Unit Lessons'
    print(obj)
    if request.user.profile.status == 't':
        coursedet = course.objects.all()
        print(coursedet)
        for i in coursedet:
            print(i.title)
        courseunits = courseUnit.objects.all()
        return render(request, 'announcements.html', {'courseunits': courseunits, 'course': coursedet,"obj":obj})

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
        return redirect('home')

    if request.method == 'POST':
        print("SDF",request.POST)
        title = request.POST['title']
        next = request.POST.get('next', '/')
        category = request.POST['category']
        image = request.FILES['image']
        
        instance = course(title=title, category=category, created_by=user, image=image)
        # instance.image = image
        print(instance)
        instance.save()

        messages.success(request, "Your course has been created.")
        return HttpResponseRedirect(next)
    
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


def create_topic(request):

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
 
            
            instance.save()

            courseunit.topics.add(instance)
            courseunit.save()

            messages.success(request, "Your topic to the unit has been added.")
            return redirect("courseDetail", courseid=courseunit.course.id)

        max_grades = request.POST['grades']
        deadline = request.POST['deadline']

        print(deadline)

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
        
        instance.save()
        courseunit.assignments.add(instance)
        courseunit.save()

        messages.success(request, "Your Work to the unit has been added.")
        return redirect("courseDetail", courseid=courseunit.course.id)

    
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


def handlesignup(request):
    if request.method == 'POST':
        # Get the Post parametres
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['pass2']
        college = request.POST['college']


        # check for errorneous input
        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters")
            return redirect('home')

        if " " in username:
            messages.error(request, "Username cannot contain spaces")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Uername already exists. Choose unique username")
            return redirect('home')
        if User.objects.filter(email=email).exists():
            messages.error(request, "email already exists. Please Log in")
            return redirect('home')

        # Create the user
        form1 = userform(request.POST)

        if form1.is_valid():
            form1.save()

            user = User.objects.get(username=username)
            user.profile.college = college
            user.save()

            messages.success(request, "Your account has created.")
            return redirect('home')

        else:
            form1 = userform()


    return HttpResponse("404 - Not Found")


def handlelogin(request):
    if request.method == 'POST':
        # Get the Post parametres
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpassword)
        user_verify = User.objects.get(username=loginusername)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect('home')
        elif user_verify.is_active == False:
            messages.error(request, "Please verify your email first to login.")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials: Please try again")
            return redirect('home')
    return HttpResponse('404 not found')


def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
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

def add_file(request):
    if request.method == 'POST':
        document = request.FILES.getlist('document', None)
        assignmentid = request.POST['assignmentid']
        isassignment = request.POST['isassignment']

        if isassignment == 'True':
            assignment = Assignment.objects.get(id=assignmentid)
            for doc in document:
                file = Files.objects.create(document=doc)
                assignment.documents.add(file)
            assignment.save()

            messages.success(request, "You have added the file successfully")
            return redirect('assignment-detail', assignmentid=assignmentid)

        else:
            topic = courseTopic.objects.get(id=assignmentid)

            for doc in document:
                file = Files.objects.create(document=doc)
                topic.documents.add(file)

            topic.save()
            messages.success(request, "You have added the file successfully")
            return redirect('topic-detail', topicid=assignmentid)
        
    return HttpResponse("Something went wrong", status=404)


def add_link(request):
    if request.method == 'POST':
        link = request.POST['link']
        assignmentid = request.POST['assignmentid']
        isassignment = request.POST['isassignment']

        if isassignment == 'True':
            assignment = Assignment.objects.get(id=assignmentid)
            if not assignment.link :
                assignment.link = link
            else:
                assignment.link = str(assignment.link) + "," + link

            assignment.save()

            messages.success(request, "You Link have been added successfully")
            return redirect('assignment-detail', assignmentid=assignmentid)

        else:
            topic = courseTopic.objects.get(id=assignmentid)
            if not topic.link :
                topic.link = link
            else:
                topic.link = str(topic.link) + "," + link

            topic.save()
            messages.success(request, "You Link have been added successfully")
            return redirect('topic-detail', topicid=assignmentid)
        
    return HttpResponse("Something went wrong", status=404)   


def delete_link_assignment(request, assignmentid, link):
    assignment = Assignment.objects.get(id=assignmentid)
    links = assignment.link.split(",")


    links.remove(links[int(link)-1])
    
    assignment.link = ",".join(links)
    assignment.save()

    messages.success(request, "link deleted")
    return redirect('assignment-detail', assignmentid=assignmentid)


def delete_link_topic(request, topicid, link):
    topic = courseTopic.objects.get(id=topicid)
    links = topic.link.split(",")


    links.remove(links[int(link)-1])
    
    topic.link = ",".join(links)
    topic.save()

    messages.success(request, "link deleted")
    return redirect('topic-detail', topicid=topicid)





def edit_topic(request):
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
            return redirect('assignment-detail', assignmentid=assignmentid)

        else:
            courseTopic.objects.filter(id=assignmentid).update(title = title, info = info)

            messages.success(request, "Updated!!")
            return redirect('topic-detail', topicid=assignmentid)


def handleteachersignup(request):
    if request.method == 'POST':
        # Get the Post parametres
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['pass2']

        if request.user.profile.status != 'p':
            messages.error(request, "You don't have permission to add a teacher.")
            return redirect('home')

        # check for errorneous input
        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters")
            return redirect('home')

        if " " in username:
            messages.error(request, "Username cannot contain spaces")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Uername already exists. Choose unique username")
            return redirect('home')
        if User.objects.filter(email=email).exists():
            messages.error(request, "email already exists. Please Log in")
            return redirect('home')

        # Create the user
        form1 = userform(request.POST)

        if form1.is_valid():
            form1.save()

            teacher = User.objects.get(username=username)
            teacher.profile.status = 't'
            teacher.profile.college = request.user.profile.college

            teacher.save()

            messages.success(request, "Your have successfully added the teacher " + username)
            return redirect('home')

        else:
            form1 = userform()


    return HttpResponse("404 - Not Found")
