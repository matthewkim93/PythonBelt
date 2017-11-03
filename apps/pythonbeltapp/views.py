# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.shortcuts import render, redirect
from django.contrib.messages import error
from time import gmtime, strftime
import bcrypt, random

def index(request):
    return render(request,'pythonbeltapp/index.html')

def register(request):
    errors=Users.objects.validator(request.POST)
    if errors:
        for tag,err in errors.iteritems():
            error(request,err,extra_tags=tag)
        return redirect('/main')
    else:
        hash_pw=bcrypt.hashpw(request.POST['pw'].encode(),bcrypt.gensalt())
        Users.objects.create(name=request.POST['name'], username=request.POST['username'],pw=hash_pw)
        user=Users.objects.get(username=request.POST['username'])
        request.session['name']=user.name
        request.session['id']=user.id
        return redirect('/travels')

def login(request):
    errors={}
    try:
        user=Users.objects.get(username=request.POST['username'])
        if bcrypt.checkpw(request.POST['pw'].encode(),user.pw.encode())==True:
            request.session['name']=user.name
            request.session['username']=user.username
            request.session['id']=user.id
            return redirect('/travels')
        else:
            errors['loginfail']="Your password does not match the username"
            for tag,err in errors.iteritems():
                error(request,err,extra_tags=tag)
            return redirect('/main')
    except:
        errors['loginfail']="Your username does not exist in the database"
        for tag,err in errors.iteritems():
            error(request,err,extra_tags=tag)
        return redirect('/main')

def home(request):
    errors={}
    try:
        request.session['id']
        context={
            "schedule":Plans.objects.filter(creator_id=request.session['id']),
            "plans":Plans.objects.exclude(creator_id=request.session['id']).exclude(members=request.session['id']),
            "joined":Plans.objects.filter(members=request.session['id'])
        }
        return render(request,'pythonbeltapp/home.html',context)
    except:
        errors['loginfail']="You must login"
        for tag,err in errors.iteritems():
            error(request,err,extra_tags=tag)
        return redirect('/main')

def logout(request):
    try:
        del request.session['name']
        del request.session['username']
        del request.session['id']
        return redirect('/main')
    except:
        return redirect('/main')

def add(request):
        errors={}
        try:
            request.session['id']
            return render(request,"pythonbeltapp/add.html")
        except:
            errors['loginfail']="You must login"
            for tag,err in errors.iteritems():
                error(request,err,extra_tags=tag)
            return redirect('/main')

def addtrip(request):
    errors=Plans.objects.validator(request.POST)
    if errors:
        for tag,err in errors.iteritems():
            error(request,err,extra_tags=tag)
        return redirect('/travels/add')
    else:
        Plans.objects.create(destination=request.POST['destination'], desc=request.POST['desc'], travel_start=request.POST['travel_start'], travel_end=request.POST['travel_end'], creator_id=request.session['id'])
        return redirect('/travels')

def join(request):
    user=Users.objects.get(id=request.session['id'])
    plan=Plans.objects.get(id=request.POST['plan_id'])
    plan.members.add(user)
    return redirect('/travels')

def destination(request,destination_id):
    context={
        "plan":Plans.objects.get(id=destination_id),
        "members":Users.objects.filter(schedules=destination_id).exclude(id=request.session['id'])
    }
    return render(request,'pythonbeltapp/destination.html',context)
