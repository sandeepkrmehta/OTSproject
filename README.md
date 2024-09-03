-------------------  Ajenda Of Project  ---------------


(1) Project Statement

    Online Testing System(Exam):
    User can see a welcome page(Landing page) , from where he/she can read all needful
    details of OTS and link to create an account, and a link to login for registered users.
    Once loggedin, user can see home page from where he/she can select a test paper from the 
    list of test papers.
    Once the test paper is selected user can see test page where a list of questions with options 
    to select as answer. Finally submit the test and result page will appear
    On the home page user can also see a log of previous attempts of textpapers and their result.

(2) Navigation Diagram



(3) Database

Tables
Candidate : username(Primary_key), password, name, test_attempt, points(0-10)
Questions : q_id(Primary_key), que, option(a, b, c, d), ans
Result    : result_id(primary_key), username, date, time, attempt, right, wrong, points


Step 1:
(i) DOWNLOAD PYTHON : 
 -->Window User: https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe

(ii) Install PIP file
command   

 --> PIP INSTALL DJANGO

(iii) Create Project
 --> django-admin startproject myproject
 --> cd myproject

(iv) Create App
 --> python manage.py startapp OTS

(v) Create templates and static directory

(vi) update settings.py

(vii) Define modules

(viii) make migration and migrate

(iX) views

Welcome()
candidateRegistrationForm()
CandidateRegistration()
login view()
CandidateHome()
testPaper()
calculateTestResult()
testResult()
testResultHistory()
ShowTestResult()
Logoutview()

(x) Define templates

(xi) Set Urls

--------------------------------------------------

* Fist of all creates models:
      after that run command:
< python manage.py makemigrations OTS>
< python manage.py migrate OTS>


  
