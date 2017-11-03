# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.db import models
from django.utils import timezone
email_regex=re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
# Create your models here.

class UsersManager(models.Manager):
    def validator(self,postData):
        errors={}
        if len(postData['name'])<3:
            errors['last_name']="Your name must be at least 3 characters"
        if len(postData['username'])<3:
            errors['email']="Your username must be at least 3 characters"
        if len(postData['pw'])<8:
            errors['pw']="Your password must be at least 8 characters"
        if postData['pw']!=postData['pw_c']:
            errors['pw_c']="Your passwords do not match"
        return errors

class PlansManager(models.Manager):
    def validator(self,postData):
        errors={}
        if len(postData['destination'])<1:
            errors['last_name']="You must have a destination for your trip"
        if len(postData['desc'])<1:
            errors['desc']="You must have a description for your trip"
        if len(postData['travel_start'])<1:
            errors['travel_start']="You must have a travel start date"
        if postData['travel_end']<postData['travel_start']:
            errors['pw_c']="Your travel must start before it ends! Check the dates of your trip again"
        return errors

class Users(models.Model):
    name=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    pw=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UsersManager()


class Plans(models.Model):
    destination=models.CharField(max_length=255)
    travel_start=models.DateField()
    travel_end=models.DateField()
    desc=models.CharField(max_length=255)
    creator=models.ForeignKey(Users,related_name="plans")
    members=models.ManyToManyField(Users,related_name="schedules")
    objects=PlansManager()
