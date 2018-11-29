from django.shortcuts import render
import pyrebase

# Create your views here.
config = {
    apiKey: "AIzaSyBMLYGNME-or2S4CzeAuVqq5aOfgZcqMBM",
    authDomain: "task-tracker-a37dd.firebaseapp.com",
    databaseURL: "https://task-tracker-a37dd.firebaseio.com",
    projectId: "task-tracker-a37dd",
    storageBucket: "task-tracker-a37dd.appspot.com",
    messagingSenderId: "418470831758"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

def signIn(request):
    return render(request, 'tasktracker/signIn.html')

def home(request):
    email=request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = auth.sign_in_with_email_and_password(email,passw)
    except:
        message = 'Invalid Credentials'
        return render(request,'tasktracker/signIn.html',{"message":message})
    return render(request, 'tasktracker/home.html', {'email':email})

def toDoList(request, user_id, list_id):
    return render(request, 'tasktracker/toDoList.html')
