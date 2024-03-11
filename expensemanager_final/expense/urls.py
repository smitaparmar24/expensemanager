from django.contrib import admin
from django.urls import path, include
from .views import ExpenseCreationView, ExpenseListView, ExpenseDetailView, ExpenseDeleteView, ExpenseUpdateView, ReceiptCreateView
from .import views
urlpatterns = [
    path("add/", ExpenseCreationView.as_view(), name="expense_add"),
    path("list/", ExpenseListView.as_view(), name="expense_list"),
    path("detail/<int:pk>/", ExpenseDetailView.as_view(), name="detail_expense"),
    path("delete/<int:pk>/", ExpenseDeleteView.as_view(), name="delete_expense"),
    path("edit/<int:pk>/", ExpenseUpdateView.as_view(), name="edit_expense"),
    path("chart/", views.pieChart, name="chart"),
    path("receipt_create/", ReceiptCreateView.as_view(), name="receipt_create"),
    path("receipt_list/", views.ReceiptListView.as_view(), name="receipt_list"),
    path("total_amount/", views.total_amount, name="total_amount"),
]
