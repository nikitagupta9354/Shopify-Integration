from django.shortcuts import render
from django.http import HttpResponse
from .fr import fetch_backup_data
import json

# Create your views here.

def fetch_restore_product(request):
    fetch_backup_data('products')
    res={'Message':'Data has been backed up'}
    json_data=json.dumps(res)
    return HttpResponse(json_data,content_type='application/json')



