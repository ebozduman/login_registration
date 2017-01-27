from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .models import Quote
from .models import Favorite

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
        return redirect('/show_home/')
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
        user = User.objects.get(id=request.session['id'])
        quotes = Quote.objects.all()
        print user.first_name
        print quotes
        context = {
            'user' : User.objects.get(id=request.session['id']),
            'quotes' : Quote.objects.all()
        }
        print "==========>", context['user']
        return render(request, 'login_reg/show_home.html', context)
    else:
        print "else"
        return redirect('/')

def add_quote(request):
    print "Entered add_quote"
    postData = {
        'quote' : request.POST['quote_textarea'],
        'quoted_by' : request.POST['quoted_by'],
        'user_id' : request.session['id']
    }
    ret = Quote.objects.add(postData)
    if not ret['success']:
        for msg in ret['msg_list']:
            messages.error(request, msg)
    return redirect('/show_home')

def add_show_my_favorites(request, id):
    print "Entered show_my_favorites"
    postData={
        'user_id' : request.session['id'],
        'quote_id' : id
    }
    ret = Favorite.objects.add_fav(postData)
    favorites_list = Favorite.objects.all()
    for f in favorites_list:
        print f.quote_id.quoted_by
        print f.quote_id.quote_text
    context = {
        'favorites_list': favorites_list
    }
    return redirect('/show_home')

def logout(request):
    print "logout"
    request.session.flush()
    return index(request)
