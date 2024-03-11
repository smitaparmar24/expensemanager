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
class ExpenseListView(ListView):
    template_name = 'expense/list.html'
    model = Expense
    context_object_name = 'expenses'

    def get_queryset(self):
        # Get the logged-in user
        user = self.request.user
        # Filter expenses based on the logged-in user
        queryset = super().get_queryset().filter(user=user)
        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_amount = self.get_queryset().aggregate(Sum('amount'))['amount__sum']
        context['total_amount'] = total_amount if total_amount else 0
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
    return render(request, 'total_amount.html', {'total_amount': total_amount})

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
    
    