from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .forms import ExpenseCreationForm, ReceiptCreationForm
from .models import Expense
from .models import Category, Receipts
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import ExtractMonth
import calendar
# Create your views here.


class ExpenseCreationView(CreateView):
    template_name = 'expense/add.html'
    model = Expense
    form_class = ExpenseCreationForm
    success_url = '/expense/list/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ExpenseListView(LoginRequiredMixin, ListView):
    template_name = 'expense/list.html'
    model = Expense
    context_object_name = 'expenses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the logged-in user
        user = self.request.user
        # Regular expenses
        context['expenses'] = Expense.objects.filter(user=user)
        # Monthly expenses
        monthly_expenses = (
            Expense.objects
            .filter(user=user)
            .annotate(month=ExtractMonth('expDateTime'))
            .values('month')
            .annotate(total_amount=Sum('amount'))
            .order_by('month')  # Order by month in ascending order
        )
        # Convert month number to month name
        for expense in monthly_expenses:
            month_number = expense['month']
            expense['month'] = calendar.month_name[month_number]
        context['monthly_expenses'] = monthly_expenses
        return context

class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseCreationForm
    success_url = "/expense/list/"
    template_name = "expense/expense_edit_form.html"


class ExpenseDetailView(DetailView):
    model = Expense
    context_object_name = "expense"
    template_name = "expense/expense_detail.html"


class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = "expense/expense_delete.html"
    success_url = "/expense/list/"


def total_amount(request):
    # Get the logged-in user
    user = request.user
    total_amount = Expense.objects.filter(
        user=user).aggregate(Sum('amount'))['amount__sum']
    # If no expenses are found, set total_amount to 0
    total_amount = total_amount if total_amount else 0
    print(total_amount)
    return render(request, 'client_dashboard.html',  {'total_amount': total_amount})


def pieChart(request):
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

    return render(request, 'expense/pie_chart.html', {
        'labels': labels,
        'data': data
    })
    

@login_required
def monthly_expense_chart(request):
    # Get the logged-in user
    user = request.user
    # Monthly expenses
    monthly_expenses = (
        Expense.objects
        .filter(user=user)
        .annotate(month=ExtractMonth('expDateTime'))
        .values('month')
        .annotate(total_amount=Sum('amount'))
        .order_by('month')  # Order by month in ascending order
    )
    # Convert month number to month name
    month_names = [calendar.month_name[expense['month']]
                   for expense in monthly_expenses]
    total_amounts = [expense['total_amount'] for expense in monthly_expenses]
    return render(request, 'expense/monthly_expense_chart.html', {
        'month_names': month_names,
        'total_amounts': total_amounts,
    })


class ReceiptCreateView(LoginRequiredMixin, CreateView):
    model = Receipts
    template_name = 'expense/create_receipt.html'
    success_url = '/expense/list/'
    form_class = ReceiptCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReceiptListView(LoginRequiredMixin, ListView):
    template_name = 'expense/receipt_list.html'
    model = Receipts
    context_object_name = 'receipts'

    def get_queryset(self):
        # Filter receipts based on the logged-in user
        return Receipts.objects.filter(user=self.request.user)


def about_app(request):
    return render(request, 'expense/about_app.html')


def contact_us(request):
    return render(request, 'expense/contact_us.html')


def calculate_savings(request):
    # Get the logged-in user
    user = request.user
    # Define the income
    income = 30000  # You can adjust this value as needed
    # Get the total expenses for each month
    monthly_expenses = []
    for month in range(1, 13):  # Loop through each month
        expenses = Expense.objects.filter(
            user=user, expDateTime__month=month).aggregate(Sum('amount'))['amount__sum']
        total_expenses = expenses if expenses else 0
        monthly_expenses.append(total_expenses)

    # Calculate savings for each month
    savings = [income - expense for expense in monthly_expenses]

    # Prepare data for rendering
    month_names = [calendar.month_name[i] for i in range(1, 13)]

    # Combine month names with savings data
    savings_data = zip(month_names, savings)

    return render(request, 'expense/savings.html', {'savings_data': savings_data})
