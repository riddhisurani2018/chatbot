from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('InquiryForm/', views.AskConsultant, name="inquiryForm"),
    path('InquiryForm1/', views.AskConsultant_arabic, name="inquiryForm1"),
    path('queryForm/', views.manualResponse, name="queryForm"),
    path('queryForm1/', views.manualResponse_arabic, name="queryForm1"),
]