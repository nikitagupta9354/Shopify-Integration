from django.shortcuts import render
import requests
import json
from .models import Object,Store
# Create your views here.
def fetch_backup_data(object):
    url = f'https://trialproject12.myshopify.com/admin/api/2024-01/{object}.json'

    # Make the request with the access token included in the headers
    headers = {
        'X-Shopify-Access-Token': '',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    s=Store.objects.get(Organization_name='Trial')
    o = Object()
    o.store=s
    o.object_type=object
    o.data = json.dumps(data)
    o.save()





