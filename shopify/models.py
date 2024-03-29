from django.contrib import admin
from django.db import models
from django.utils import timezone
import uuid

OBJECT_TYPE_CHOICES = (
    ('products', 'Product'),
    ('customers', 'Customer'),
    ('orders', 'Order'),
    # Add more choices as needed
)
class Store(models.Model):
    store_id=models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    Organization_name=models.CharField(max_length=100)
    store_url=models.URLField()

class Object(models.Model):
    store= models.ForeignKey(Store,on_delete=models.CASCADE)
    object_type=models.CharField(max_length=100,choices=OBJECT_TYPE_CHOICES)
    data = models.JSONField()  # Field to store JSON data
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)  # Character field
    backup_date = models.DateTimeField(default=timezone.now)  # Current date/time

    # def __str__(self):
    #     return self.id

    # restore/<id>/
    #backup/<store_id>/?object_type=''