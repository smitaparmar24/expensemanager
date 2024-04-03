from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("manager-register/", views.ManagerRegisterView.as_view(),
         name="manager-register"),
    path("client-register/", views.ClientRegisterView.as_view(),
         name="client-register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("manager-dashboard/", views.ManagerDashboardView.as_view(),
         name="manager-dashboard"),
    # path("developer-register/",views.DeveloperRegisterView.as_view(),name="developer-register"),
    path("client-dashboard/", views.ClientDashboardView.as_view(),
         name="client-dashboard"),
    path("logout/", LogoutView.as_view(next_page="/user/login"), name="logout"),

    # path("sendmail/",views.sendMail,name="sendmail"),
]
