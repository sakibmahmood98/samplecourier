from django.db import models

# Create your models here.

PLACE_CHOICES = (
    ('DH', 'Dhaka'),
    ('DD', 'Division_of_dhaka'),
    ('OD', 'Outside_of_dhaka')
)
PRODUCT_TYPE = (
    ('FR', 'Fragile'),
    ('LQ', 'Liquid')
)

class Register(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    usertype = models.CharField(max_length=20)
    address = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Orders(models.Model):
    invoice_id = models.CharField(max_length=10)

  ##  parcel_height = models.CharField(max_length=10)
  ##  parcel_width = models.CharField(max_length=10)
  ##  parcel_length = models.CharField(max_length=10)
    parcel_product_type = models.CharField(max_length=20)
    parcel_weight = models.CharField(max_length=10)
    parcel_dest_choice = models.CharField(max_length=20)
    parcel_dest = models.CharField(max_length=10)
    total_price = models.CharField(max_length=10)

    sender_name = models.CharField(max_length=150)
    sender_phone = models.CharField(max_length=20)

    receiver_name = models.CharField(max_length=150)
    receiver_phone = models.CharField(max_length=20)

 ##   pickup_address = models.CharField(max_length=120)
    deliver_address = models.CharField(max_length=120)

    marchant_name = models.CharField(max_length=150)
    marchant_phone = models.CharField(max_length=20)
  ##  deliver_address = models.CharField(max_length=120)

    order_status = models.CharField(max_length=20, default='default')


    def __str__(self):
        return self.invoice_id