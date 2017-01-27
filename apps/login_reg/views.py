from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def index(request):
    return render(request, 'login_reg/index.html')

def register_process(request):
    postData = {
        'first_name' : request.POST['first_name'],
        'last_name' : request.POST['last_name'],
        'email' : request.POST['email'],
        'password' : request.POST['password'],
        'conf_pwd' : request.POST['conf_pwd']
    }
    ret = User.objects.register(postData)
    if ret['success']:
        id = User.objects.get(email=postData['email']).id
        request.session['id'] = id
        return redirect('/show_home/'+str(id))
    else:
        for msg in ret['msg_list']:
            messages.error(request, msg)
        return redirect('/')

def login_process(request):
    postData = {
        'email' : request.POST['email'],
        'password' : request.POST['password']
    }
    ret = User.objects.login(postData)
    if ret['success']:
        id = User.objects.get(email=postData['email']).id
        request.session['id'] = id
        return redirect('/show_home/'+str(id))
    else:
        for msg in ret['msg_list']:
            messages.error(request, msg)
        return redirect('/')

def show_home(request, id):
    print "Entered show_home"
    print "Passed into method ==>", id
    print "session-id ==>", request.session['id']
    if str(request.session['id']) == id.encode():
        context = {
            'user' : User.objects.get(id=id)
        }
        print "==========>", context['user']
        return render(request, 'login_reg/show_home.html', context)
    else:
        print "else"
        return redirect('/')

def logout(request):
    print "logout"
    request.session.flush()
    return index(request)
