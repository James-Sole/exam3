# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib import messages
from models import *
import bcrypt
def index(request):
	return render(request, "login_reg/index.html")
def login(request, methods = ['POST']):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request,error)
        return redirect('/')
    request.session['id']= User.objects.get(username = request.POST['username']).id
    request.session['status']= 'logged in'
    return redirect('/pokes')

def register(request, methods = ['POST']):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request,error)
        return redirect('/')
    password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    User.objects.create(name = request.POST['name'], username = request.POST['username'], email = request.POST['email'], password = password, birth_date = request.POST['birth_date'])
    request.session['id']= User.objects.last().id
    request.session['status']= 'registered'
    return redirect('/pokes')

def pokes(request):
    if 'id' in request.session:
        Pokes = User.objects.filter(pokes = request.session['id'])
        count_pokes = Pokes.count()
        context = {
            'username' : User.objects.get(id =request.session['id']).username,
            'pokers': Pokes,
			'other_pokers': User.objects.exclude(id = request.session['id']),
            'poke_number': count_pokes
        }
        return render(request, "login_reg/success.html", context)
    return redirect('/')
def poke(request, id):
    if 'id' in request.session:
    	#add relationship
    	user = User.objects.get( id=request.session['id'])
    	poker = User.objects.get(id = id)
    	poker.pokes.add(user)
    	return redirect('/pokes')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

# Create your views here.
