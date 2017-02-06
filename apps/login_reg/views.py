from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import User
from .models import Appointment
from pytz import timezone

def index(request):
    return render(request, 'login_reg/index.html')

def register_process(request):
    postData = {
        'name' : request.POST['name'],
        'email' : request.POST['email'],
        'password' : request.POST['password'],
        'conf_pwd' : request.POST['conf_pwd']
    }
    ret = User.objects.register(postData)
    if ret['success']:
        id = User.objects.get(email=postData['email']).id
        request.session['id'] = id
        return redirect('/show_home')
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
        return redirect('/show_home')
    else:
        for msg in ret['msg_list']:
            messages.error(request, msg)
        return redirect('/')

def show_home(request):
    print "Entered show_home"
    if 'id' in request.session:
        user_id = request.session['id']
        user = User.objects.get(id=user_id)
        todays_date = datetime.now(timezone('US/Pacific')).date()
        time_now = datetime.now(timezone('US/Pacific')).time()
        todays_appt_list = Appointment.objects.filter(user__id = user_id, date = todays_date)
        print "todays_date", todays_date
        appointments_list = Appointment.objects.filter(user__id = user_id, date__gt = todays_date)
        for i in appointments_list:
            print i.task, i.date, i.time, i.status

        context = {
            'user': user,
            'todays_date':todays_date,
            'todays_appt_list': todays_appt_list,
            'appointments_list': appointments_list,
        }
        return render(request, 'login_reg/show_home.html', context)
    else:
        print "else"
        return redirect('/')

def add_appt(request):
    print "Entered add_appt"
    print "request.POST['date'] = ", request.POST['date']
    print "request.POST['time'] = ", request.POST['time']
    print "request.POST['task'] = ", request.POST['task']
    postData={
        'user_id': request.session['id'],
        'date': request.POST['date'],
        'time': request.POST['time'],
        'task': request.POST['task']
    }
    ret = Appointment.objects.add_appt(postData)
    if not ret['success']:
        for msg in ret['msg_list']:
            messages.error(request, msg)
    return redirect('/show_home')

def delete_appt(request, appt_id):
    print "Entered delete_appt"
    postData={
        'user_id': request.session['id'],
        'appt_id': appt_id
    }
    Appointment.objects.delete_appt(postData)
    print "returned from model"
    return redirect('/show_home')

def edit_appt(request, appt_id):
    appt = Appointment.objects.get(id=appt_id)
    task = appt.task
    print "appt.task", task
    status = appt.status
    print "appt.status", status
    print "appt.date", appt.date
    date = appt.date.strftime('%Y-%m-%d')
    print "reformatted appt.date", date
    print "appt.time", appt.time
    time = str(appt.time).split(':')
    seq = time[0], time[1]
    time = ':'.join(seq)
    print "reformatted appt.time", time
    context = {
        'appt_id': appt_id,
        'task': task,
        'status': status,
        'date': date,
        'time': time
    }
    return render(request, 'login_reg/edit_appt.html', context)

def update_appt(request, appt_id):
    print "request",request
    new_task = request.POST['task']
    new_status = request.POST['status']
    new_date = request.POST['date']
    new_time = request.POST['time']
    postData={
        'appt_id': appt_id,
        'new_task': new_task,
        'new_status': new_status,
        'new_date': new_date,
        'new_time': new_time,
    }
    Appointment.objects.update_appt(postData)
    return redirect('/edit_appt/' + appt_id)

def logout(request):
    print "logout"
    request.session.flush()
    return index(request)
