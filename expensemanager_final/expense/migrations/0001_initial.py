# Generated by Django 5.0.1 on 2024-02-20 04:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense.category')),
            ],
            options={
                'db_table': 'subcategory',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('expDateTime', models.DateField()),
                ('paymentMethod', models.CharField(choices=[('Cash', 'Cash'), ('Cheque', 'Cheque'), ('CreditCard', 'CreditCard')], max_length=100)),
                ('status', models.CharField(choices=[('Cleared', 'Cleared'), ('Uncleared', 'Uncleared'), ('Void', 'Void')], max_length=100)),
                ('description', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense.category')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense.subcategory')),
            ],
            options={
                'db_table': 'expense',
            },
        ),
    ]