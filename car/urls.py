from django.contrib import admin
from django.urls import path,include
from car_prediction.views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('CarApi', CarView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homePage, name='homePage'),
    path('api/', include(router.urls)),
    path('data/', data, name='data'),
    path('add_data/', add_data, name='add_data'),
    path('export_data/', export_data, name='export_data'),
    path('predict_data/', predict_data, name='predict_data'),
    path('data/change/<int:id_car>', edit_data, name='edit_data'),
    path('data/delete/<int:id_car>', delete_data, name='delete_data'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]