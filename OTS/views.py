from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from OTS.models import *
import random


# welcome function is used to render the welcome.html page

def welcome(request):
    template=loader.get_template('welcome.html')
    return HttpResponse(template.render())
def candidateRegistrationForm(request):
    res=render(request,'registration_form.html')
    return res

# candidateRegistration function is used to register the candidate and store the details in the database

def candidateRegistration(request):
    if request.method=='POST':
        username=request.POST['username']
        #Check if the username already exists
        if(len(Candidate.objects.filter(username=username))):
            userStatus=1
        else:
            candidate=Candidate()
            candidate.username=username
            candidate.password=request.POST['password']
            candidate.name=request.POST['name']
            candidate.save()
            userStatus=2
    else:
        userStatus=3 #requset method is not POST
    context={
        'userStatus':userStatus
    }
    res=render(request,'registration.html',context)
    return res

# loginView function is used to render the login.html page and to check the username and password entered by the user

def loginView(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        candidate= Candidate.objects.filter(username=username,password=password)
        if len(candidate)==0:
            loginError="Invalid username or password"
            res=render(request,'login.html',{'loginError':loginError})
        else:
            #login sucessful
            request.session['username']=candidate[0].username
            request.session['name']=candidate[0].name
            res=HttpResponseRedirect("home")
    else:
        res=render(request,'login.html')
    return res


# codidateHome function is used to render the home.html page if the user is logged in

def condidateHome(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect("login")
    else:
        res=render(request, 'home.html')
    return res

# testPaper function is used to render the test_paper.html page

def testPaper(request):
        if 'name' not in request.session.keys():
            res=HttpResponseRedirect("login")  
#=======================fetch question from database=======================
        n=int(request.GET['n'])
        question_pool=list(Question.objects.all())
        random.shuffle(question_pool)
        questions_list=question_pool[:n]
        context={'questions':questions_list}
        res=render(request,'test_paper.html',context)
        return res

def calculateTestResult(request):
    pass
def testResultHistory(request):
    pass
def showTestResult(request):
    pass

# logoutView function is used to logout the user and render the login.html page

def logoutView(request):
    if 'name' in request.session.keys():
        del request.session['username']
        del request.session['name']
    return HttpResponseRedirect("login")
