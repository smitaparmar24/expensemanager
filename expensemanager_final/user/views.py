from typing import Any
from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import User
from .forms import ManagerRegistrationForm, ClientRegistrationForm
# import settings.py
from django.conf import settings
# send_mail is built-in function in django
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from expense.models import Expense
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class ManagerRegisterView(CreateView):
    template_name = 'user/manager_register.html'
    model = User
    form_class = ManagerRegistrationForm
    success_url = '/login/'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        # print("email....",email)
        if sendMail(email):
            print("Mail sent successfully")
            return super().form_valid(form)
        else:
            return super().form_valid(form)


class ClientRegisterView(CreateView):
    template_name = 'user/client_register.html'
    model = User
    form_class = ClientRegistrationForm
    success_url = '/user/login/'


def sendMail(to):
    subject = 'Welcome to PMS24'
    message = 'Hope you are enjoying your Django Tutorials'
    # recepientList = ["samir.vithlani83955@gmail.com"]
    recepientList = [to]
    EMAIL_FROM = settings.EMAIL_HOST_USER
    send_mail(subject, message, EMAIL_FROM, recepientList)
    # attach file
    # html
    return True


class UserLoginView(LoginView):
    template_name = 'user/login.html'
    model = User

    def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_manager:
                return '/user/manager-dashboard/'
            else:
                return '/user/client-dashboard/'


class ManagerDashboardView(ListView):

    def get(self, request, *args, **kwargs):
        # logic to get all the projects
        print("ManagerDashboardView")
        expenses = Expense.objects.all()  # select * from project
        print(".............................................", expenses)
        return render(request, 'user/manager_dashboard.html', {"expenses": expenses})

    template_name = 'user/manager_dashboard.html'


# class ClientDashboardView(ListView):

#     # def get(self, request, *args, **kwargs):
#     #     # logic to get all the projects
#     #     print("ClientDashboardView")
#     #     expenses = Expense.objects.all()  # select * from project
#     #     print(".............................................", expenses)
#     #     return render(request, 'user/client_dashboard.html', {"expenses": expenses})

#     # template_name = 'user/client_dashboard.html'

#     def get_queryset(self):
#         # Get the logged-in user
#         user = self.request.user
#         # Filter expenses based on the logged-in user
#         queryset = super().get_queryset().filter(user=user)
#         return queryset


class ClientDashboardView(LoginRequiredMixin, ListView):
    # template_name = 'user/client_dashboard.html'
    # model = Expense
    # context_object_name = 'expenses'

    def get_queryset(self):
        # Get the logged-in user
        user = self.request.user
        # Filter expenses based on the logged-in user
        queryset = Expense.objects.filter(user=user)
        return queryset

    def get(self, request, *args, **kwargs):
        # Get the logged-in user
        user = self.request.user
        # Filter expenses based on the logged-in user
        queryset = Expense.objects.filter(user=user)

        labels = []
        data = []

    # Get the logged-in user
        user = request.user

        queryset = Expense.objects.filter(user=user).order_by('-amount')[:5]
        print(queryset)

        for expense in queryset:
            labels.append(expense.category.name)
        # Accessing the categoryName through the ForeignKey
            print(labels)
            data.append(expense.amount)

        return render(request, "user/client_dashboard.html", {
            "labels": labels,
            "data": data,
            "expenses": queryset
        })
