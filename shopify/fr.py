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
    #print(data)
    s=Store.objects.get(Organization_name='Trial')
    o = Object()
    o.store=s
    o.object_type=object
    o.data = json.dumps(data)
    o.save()
    return data


def create_product(data):
    url = f'https://trialproject12.myshopify.com/admin/api/2024-01/products.json'
    headers = {
        "X-Shopify-Access-Token":'' ,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers)

    print(response.status_code)
    print(response.json())


def restore_shopify_data(resource, data):
    url = f'https://trialproject12.myshopify.com/admin/api/2024-01/products/{data["product"]["id"]}.json'
    headers = {
        'X-Shopify-Access-Token':'' ,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))

    return response

def restore_data(uuid):
    url = f'https://trialproject12.myshopify.com/admin/api/2024-01/products.json'
    headers = {
        'X-Shopify-Access-Token': '',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    o=Object.objects.get(id=uuid)
    products=o.data
    for product in products['products']:
        response=restore_shopify_data('products',{'product':product})

    if response.status_code!=200:
        print('creating product')
        create_product({'product':product})
















