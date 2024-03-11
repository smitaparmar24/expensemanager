from django.db import models
from user.models import User
from django.utils.timezone import now

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = "subcategory"

    def __str__(self):
        return self.name


paymentMethod = (
    ("Cash", "Cash"),
    ("Cheque", "Cheque"),
    ("CreditCard", "CreditCard"),
)

status = (
    ("Cleared", "Cleared"),
    ("Uncleared", "Uncleared"),
    ("Void", "Void"),
)


class Expense(models.Model):
    amount = models.FloatField()
    expDateTime = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    paymentMethod = models.CharField(max_length=100, choices=paymentMethod)
    status = models.CharField(max_length=100, choices=status)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "expense"


class Receipts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    receiptImage = models.ImageField(upload_to="uploads/")

    class Meta:
        db_table = "receipts"

    def __str__(self):
        return self.name
