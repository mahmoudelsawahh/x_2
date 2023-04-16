from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from car_prediction.models import Car
from car_prediction.forms import FormCar
from django.contrib import messages
from .resources import CarResource
from django.http import HttpResponse
from tablib import Dataset

from .serializers import CarSerializers 
from rest_framework import viewsets, permissions

import pickle
import numpy as np 
import pandas as pd
import traceback
import json

class CarView(viewsets.ModelViewSet): 
    queryset = Car.objects.all() 
    serializer_class = CarSerializers
    permission_classes = [permissions.IsAuthenticated]

@login_required(login_url=settings.LOGIN_URL)
def data(request):
    cars = Car.objects.all()

    context = {
        'cars': cars,
    }

    return render(request, 'data.html', context)

@login_required(login_url=settings.LOGIN_URL)
def add_data(request):
    if request.POST:
        form = FormCar(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = FormCar()
            message = "Data Saved Successfully"

            context = {
                'form': form,
                'message': message,
            }
            return render(request, 'add_data.html', context)
    else:
        form = FormCar()

        context = {
            'form': form,
        }

    return render(request, 'add_data.html', context)

@login_required(login_url=settings.LOGIN_URL)
def edit_data(request, id_car):
    car = Car.objects.get(id=id_car)
    template = 'edit_data.html'
    if request.POST:
        form = FormCar(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, "Data has been successfully changed!")
            return redirect('edit_data', id_car=id_car)
    else:
        form = FormCar(instance=car)
        konteks = {
            'form':form,
            'car':car,
        }
    return render(request, template, konteks)

@login_required(login_url=settings.LOGIN_URL)
def delete_data(request, id_car):
    car = Car.objects.filter(id=id_car)
    car.delete()

    messages.success(request, "Data Deleted Successfully!")
    return redirect('data')

@login_required(login_url=settings.LOGIN_URL)
def predict_data(request):
    if request.POST:
        form = FormCar(request.POST, request.FILES)
        if form.is_valid():
            Model = form.cleaned_data['model']
            Year = form.cleaned_data['year']
            Transmission = form.cleaned_data['transmission']
            Mileage = form.cleaned_data['mileage']
            FuelType = form.cleaned_data['fuel_type']
            Tax = form.cleaned_data['tax']
            Mpg = form.cleaned_data['mpg']
            EngineSize = form.cleaned_data['engine_size']

            df = pd.DataFrame({'model':[Model], 'year':[Year], 'transmission':[Transmission], 'mileage':[Mileage], 'fuelType':[FuelType], 'tax':[Tax], 'mpg':[Mpg], 'engineSize':[EngineSize]})
            result = price_prediction(df)
            instance = form.save(commit=False)
            instance.price = result
            form.save()
            form = FormCar()
            message = "Data Saved Successfully"
            
            context = {
                'form': form,
                'message': message,
                'result': result,
            }

            return render(request, 'predict_data.html', context)
    else:
        form = FormCar()

        context = {
            'form': form,
        }

    return render(request, 'predict_data.html', context)

def price_prediction(df):
    try:
        final_pipe=pickle.load(open("/home/elsawah/Documents/portfolio/Web_App_Car_Price_Prediction_-master/car_prediction/final_pipe.sav", 'rb'))
        y_pred = final_pipe.predict(df)
        result = int(y_pred)
        return result 
    except ValueError as e:
        trace_back = traceback.format_exc()
        message = str(e)+ " " + str(trace_back) + str(df)
        return message

@login_required(login_url=settings.LOGIN_URL)
def export_data(request):
    if request.POST:
        # Get selected option from form
        file_format = request.POST['file-format']
        car_resource = CarResource()
        dataset = car_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response        
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response   

    return render(request, 'export.html')
    
def homePage(request):
    return render(request, 'index.html') 