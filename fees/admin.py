from django.contrib import admin
from .models import FeeStructure, FeePayment

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ['year', 'semester', 'tuition_fee', 'total_fee']
    list_filter = ['year', 'semester']

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount_paid', 'payment_date', 'status', 'receipt_number']
    list_filter = ['status', 'payment_date', 'payment_method']
    search_fields = ['student__roll_number', 'receipt_number', 'transaction_id']