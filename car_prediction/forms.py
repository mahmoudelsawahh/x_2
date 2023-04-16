from django.forms import ModelForm
from django import forms
from car_prediction.models import Car

class FormCar(forms.ModelForm):
    price = forms.IntegerField(required=False)
    class Meta:
        model = Car
        fields = '__all__'

