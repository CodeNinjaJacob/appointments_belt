from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from datetime import datetime
import bcrypt


def index(request):
    return render(request, 'belt_sec_try/index.html')


def success(request):
    if not request.session['user_id']:
        return redirect('/')
    else:
        context = {}
        current_user = User.objects.get(id=request.session['user_id'])
        today = datetime.today().date()
        current_appointments = Appointment.objects.filter(user = current_user , date = today).order_by('time')
        other_appointments = Appointment.objects.filter(user = current_user).exclude(date = today).order_by('date')
        context = {
            'today': today,
            'user': current_user,
            'current_appointments': current_appointments,
            'other_appointments': other_appointments
        }
    return render(request, 'belt_sec_try/home.html', context)


def register(request):
    result = User.objects.validate_reg(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/success')


def login(request):
    result = User.objects.validate_log(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully logged in!")
    return redirect('/success')


def logout(request):
    request.session.clear()
    return redirect('/')

def makeedit(request, number):
    current_user = User.objects.get(id = request.session['user_id'])
    this_appointment = Appointment.objects.get(id = number)
    # result = Appointment.objects.validate_appointment(request.POST)
    # if type(result) == list:
    #     for err in result:
    #         messages.error(request, err)
    #     return redirect('/success')
    # else:
    date = request.POST['date']
    time = request.POST['time']
    status = request.POST['status']
    task = request.POST['task']

    this_appointment.date = date
    this_appointment.time = time
    this_appointment.status = status
    this_appointment.task = task
    this_appointment.save()
    return redirect('/success')

def showedit(request, number):
    this_appointment = Appointment.objects.get(id = number)
    context = {}
    context = {
        'this_appointment': this_appointment
    }
    return render(request, 'belt_sec_try/edit.html', context)

def add(request):
    current_user = User.objects.get(id = request.session['user_id'])
    date = request.POST['date']
    time = request.POST['time']
    task = request.POST['task']
    Appointment.objects.create(date = date , time = time , status = 'Pending' , task = task , user = current_user)
    return redirect('/success')

def delete(request, number):
    current_user = User.objects.get(id = request.session['user_id'])
    this_appointment = Appointment.objects.get(id = number)
    this_appointment.delete()
    pass
    return redirect('/success')