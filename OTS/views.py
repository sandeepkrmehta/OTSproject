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
        # else:
        #     candidate=Candidate()
        #     candidate.username=username
        #     candidate.password=request.POST['password']
        #     candidate.name=request.POST['name']
        #     candidate.save()
        #     userStatus=2


        else:
            candidate = Candidate(
                username=username,
                password=request.POST['password'],
                name=request.POST['name']
            )
            candidate.save()
            userStatus = 2  # Registration successful

    else:
        userStatus=3 #requset method is not POST
   
    context={ 'userStatus':userStatus}
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


# cadidateHome function is used to render the home.html page if the user is logged in

def candidateHome(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect("login")
    else:
        res=render(request, 'home.html')
    return res

# testPaper function is used to render the test_paper.html page

def testPaper(request):
        if 'name' not in request.session.keys():
            res=HttpResponseRedirect("login")  


        n=int(request.GET['n'])  #Get nummber of question to fetch
        question_pool=list(Question.objects.all())
        random.shuffle(question_pool)
        questions_list=question_pool[:n]
        context={'questions':questions_list}
        res=render(request,'test_paper.html',context)
        return res


def calculateTestResult(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect("login")
    total_attempt = 0
    total_right = 0
    total_wrong = 0
    qid_list=[]
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(int(request.POST[k]))
    for n in qid_list:
        question = Question.objects.get(qid=n)
        try:
            if question.ans == request.POST['q'+str(n)]:
                total_right += 1
            else:
                total_wrong += 1
            total_attempt += 1
        except:
            pass
    points = (total_right-total_wrong)/len(qid_list)*10
    #store result in store table
    result = Result()
    result.username = Candidate.objects.get(username=request.session['username'])
    result.attempt = total_attempt
    result.right = total_right
    result.wrong = total_wrong
    result.points = points
    result.save()

    #update candidate tabe
    candidate = Candidate.objects.get(username=request.session['username'])
    candidate.test_attempted += 1
    candidate.points = (candidate.points * (candidate.test_attempted - 1) + points ) / candidate.test_attempted
    candidate.save()
    return HttpResponseRedirect('result')


def testResultHistory(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect("login")
    candidate=Candidate.objects.filter(username=request.session['username'])
    results=Result.objects.filter(username_id=candidate[0].username)
    context={'candidate':candidate[0],'results':results}
    res=render(request,'candidate_history.html',context)
    return res




def showTestResult(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect("login")

    #fetch latest result from result table
    result=Result.objects.filter(resultid=Result.objects.latest('resultid').resultid,username_id=request.session['username'])
    context={'result':result}
    res=render(request,'show_result.html',context)
    return res



# logoutView function is used to logout the user and render the login.html page

def logoutView(request):
    if 'name' in request.session.keys():
        del request.session['username']
        del request.session['name']
    return HttpResponseRedirect("login")