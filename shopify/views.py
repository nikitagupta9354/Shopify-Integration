from django.shortcuts import render
from django.http import HttpResponse
from .fr import fetch_backup_data,restore_data
import json

# Create your views here.

def fetch_backup_object(request):
    fetch_backup_data('products')
    res={'Message':'Data has been backed up'}
    json_data=json.dumps(res)
    return HttpResponse(json_data,content_type='application/json')

def restore_object(request,uuid):
    restore_data('customers',uuid)
    res={'Message':'Data restored'}
    json_data=json.dumps(res)
    return HttpResponse(json_data,content_type='application/json')


