from django import forms
from .models import Orders
PLACE_CHOICES = (
    ('DH', 'Dhaka'),
    ('DD', 'Division_of_dhaka'),
    ('OD', 'Outside_of_dhaka')
)
PRODUCT_TYPE = (
    ('FR', 'Fragile'),
    ('LQ', 'Liquid')
)

class OrdersForm(forms.ModelForm):
    parcel_product_type = forms.CharField(label='What is your favorite fruit?', widget=forms.Select(choices=PLACE_CHOICES))




