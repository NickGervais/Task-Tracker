from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib import auth, messages

from datetime import datetime
import os
import pyrebase
import random
import time

# Create your views here.
config = {
    'apiKey': "AIzaSyBMLYGNME-or2S4CzeAuVqq5aOfgZcqMBM",
    'authDomain': "task-tracker-a37dd.firebaseapp.com",
    'databaseURL': "https://task-tracker-a37dd.firebaseio.com",
    'projectId': "task-tracker-a37dd",
    'storageBucket': "task-tracker-a37dd.appspot.com",
    'messagingSenderId': "418470831758",
    'serviceAccount': str(os.getcwd()) + "/tasktracker/serviceAccount/serviceAccountCredentials.json",
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

def signIn(request):
    return render(request, 'tasktracker/signIn.html')

def home(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = authe.sign_in_with_email_and_password(email,password)
        except Exception as e:
            message = 'Invalid Credentials'
            return redirect('/',{"message":message})
        session_id = user['idToken']
        request.session['uid'] = str(session_id)
    elif request.method == 'GET' and request.session['uid']:
        user = authe.get_account_info(str(request.session['uid']))['users'][0]
        email = user['email']
    
    # Get Users to do Lists
    todoLists_obj = database.child('users').child(user['localId']).child('todoLists').get()
    if todoLists_obj.each():
        todoLists_keys = []
        for todolist in todoLists_obj.each():
            todoLists_keys.append(todolist.val())
        todoLists = []
        for key in todoLists_keys:
            print('key is:', key)
            td_list = database.child('todoLists').child(key).get()
            if td_list.val():
                print(td_list.val(), td_list.key())
                todoLists.append({'name':td_list.val()['list_name'], 'list_id':td_list.key()})
            
    else:
        todoLists = None

    # Get User's Shared lists
    shared_lists_obj = database.child('users').child(user['localId']).child('shared_lists').get()
    if shared_lists_obj.each():
        shared_lists_keys = []
        for shared_list in shared_lists_obj.each():
            shared_lists_keys.append(shared_list.val())
        shared_lists = []
        for key in shared_lists_keys:
            cur_list = database.child('todoLists').child(key).get()
            if cur_list.val():
                shared_lists.append({'name':s_list.val()['list_name'], 'list_id':s_list.key()})
    else:
        shared_lists = None
    
    context = {
        'email': email,
        'todoLists': todoLists,
        'shared_lists': shared_lists
    }
    return render(request, 'tasktracker/home.html', context)

def todoList(request, list_id):
    user = authe.get_account_info(str(request.session['uid']))['users'][0]
    list_obj = database.child('todoLists').child(list_id).get()
    list_name = list_obj.val().get('list_name')
    tasks_obj = list_obj.val().get('tasks')
    if tasks_obj:
        tasks = []
        for t_key, t_val in tasks_obj.items():
            tasks.append({'key':t_key, 'val':t_val})
    else:
        tasks = None
    context = {
        'list_name':list_name,
        'list_id': list_id,
        'tasks': tasks
    }
    return render(request, 'tasktracker/toDoList.html', context)

def logout(request):
    auth.logout(request)
    return redirect('/')

def signUp(request):

    return render(request, 'tasktracker/signUp.html')

def postsignUp(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = authe.create_user_with_email_and_password(email, password)
    except Exception as e:
        return redirect('/signUp/', {'message':str(e)})
    uid = user['localId']
    data = {
        'name':name, 
        'email':email
    }

    database.child("users").child(uid).set(data)
    return redirect('/')
    
def create_todoList(request):
    return render(request, 'tasktracker/create_todoList.html')

def post_create_todoList(request):
    list_name = request.POST.get('list_name')
    user = get_user_info(request)
    localId = user['localId']

    data = {
        'list_name': list_name
    }
    
    new_list = database.child('todoLists').push(data)
    database.child('users').child(localId).child('todoLists').push(new_list['name'])
    return redirect('/home/')

def create_task(request, list_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        state = request.POST.get('state')
        time_start = request.POST.get('time_start') if request.POST.get('time_start') else None
        if time_start:
            time_length = request.POST.get('time_length') 
            time_length = time_length if time_length else '1'
        else:
            state = 'todo'
            time_length=None
        # date_create = datetime.datetime.now()
        
        data = {
            'title':title,
            'description':description,
            'state':state,
            'time_start':time_start,
            'time_length':time_length
        }
        
        database.child('todoLists').child(list_id).child('tasks').push(data)
        return redirect('/todoList/' + list_id + '/')
    elif request.method == 'GET':
        list_obj = database.child('todoLists').child(list_id).get()
        list_name = list_obj.val()['list_name']
        context = {
            'list_name': list_name,
            'list_id': list_id,
            'time_slot_range': range(1, 25),
            'time_length_range': range(1, 9)
        }
        return render(request, 'tasktracker/create_task.html', context)

def edit_task(request, list_id, task_id):
    task_obj = database.child('todoLists').child(list_id).child('tasks').child(task_id).get()
    context = {
        'list_id': list_id,
        'task_id': task_id,
        'task': task_obj.val(),
        'time_slot_range': range(1, 25),
        'time_length_range': range(1, 9)
    }
    return render(request, 'tasktracker/edit_task.html', context)    

def post_edit_task(request, list_id, task_id):
    title = request.POST.get('title')
    description = request.POST.get('description')
    state = request.POST.get('state')
    time_start = request.POST.get('time_start')
    time_length = request.POST.get('time_length')

    data = {
        'title':title,
        'description':description,
        'state':state,
        'time_start':time_start,
        'time_length':time_length
    }

    task_id = request.POST.get('task_id')
    database.child('todoLists').child(list_id).child('tasks').child(task_id).update(data)

    return redirect('/todoList/' + list_id + '/')

def share_list(request, list_id):
    return render(request, 'tasktracker/share.html', {'list_id':list_id})

def post_share_list(request, list_id):
    if request.method == 'POST':
        share_with_email = request.POST.get('email')
        share_user = database.child('users').order_by_child('email').equal_to(share_with_email).get()
        print(list(share_user.val().items()))
        share_user = list(share_user.val().items())[0]
        current_user = get_user_info(request)
        if share_with_email != current_user['email'] and share_user:
            database.child('users').child(share_user[0]).child('shared_lists').push(list_id)
        elif not share_user.key():
            # user doesn't exist
            pass

    return redirect('/todoList/' + list_id + '/')

def delete_task(request, list_id, task_id):
    try:
        database.child('todoLists').child(list_id).child('tasks').child(task_id).remove()
    except:
        #delete didn't work
        pass
    return redirect('/todoList/'+list_id+'/')

def delete_list(request, list_id):
    try:
        database.child('todoLists').child(list_id).remove()
    except:
        # delete didn't work
        pass
    return redirect('/home/')

def search_task(request, list_id):
    if request.method == 'GET':
        search_str = request.GET.get('search_str')
        result_tasks_obj = database.child('todoLists').child(list_id).child('tasks').order_by_child('title').equal_to(search_str).get()
        if result_tasks_obj.each():
            result_tasks = []
            for task in result_tasks_obj.each():
                result_tasks.append({'key':task.key(), 'val':task.val()})
        else:
            result_tasks = None
    
        context = {
            'list_id': list_id,
            'result_tasks': result_tasks
        }
        return render(request, 'tasktracker/search_results.html', context)

def get_user_info(request):
    return authe.get_account_info(str(request.session['uid']))['users'][0]
