from django.shortcuts import render
import os
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from courses.forms import userform,LessonForm,LessonFileForm
from courses.models import Assignment,Payment, Files, course, courseTopic, myAssignment, myFiles, mycourses, mytopics, courseUnit, myCourseUnit, Groups, Unit,Lesson,Lesson,LessonFile,MyUnit,MyLesson, grades as marks
from django.http import JsonResponse
from django.db.models import Q
from account.models import *

import razorpay
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


# Create your views here.
def handlesignup(request):
    if request.method == 'POST':
        print(request.POST)
        # Get the Post parametres
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['pass2']
         


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
def handleteachersignup(request):
    if request.method == 'POST':
        # Get the Post parametres
        print(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['pass2']

        if request.user.profile.status == 's' or request.user.profile.status == 't':
            print('studk')
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
            print('check')
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
