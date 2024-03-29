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

    response = requests.post(url, data=data, headers=headers)

    print(response.status_code)
    print(response.json())


def restore_shopify_data(data):
    print(json.loads(data))
    d=json.loads(data)
    idval=d.get('product',{}).get('id')
    print(idval)
    url = f'https://trialproject12.myshopify.com/admin/api/2024-01/products/{idval}.json'
    headers = {
        'X-Shopify-Access-Token':'' ,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.put(url, headers=headers, data=data)

    return response

def restore_data(uuid):
    url = f'https://trialproject12.myshopify.com/admin/api/2024-01/products.json'
    headers = {
        'X-Shopify-Access-Token': '',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    o=Object.objects.get(id=uuid)
    products=json.loads(o.data)
    print(products.get("products", [])[0] )
    num_parts = len(products.get("products", []))
    print(num_parts)
    for i in range(0,num_parts):
        p=products.get("products", [])[i]

        print({'product':p})
        data={'product': p}


        response = restore_shopify_data(json.dumps(p))

    if response.status_code != 200:
        print('creating product')
        create_product(json.dumps(data))
        print(json.dumps(data))


    # for product in products['products']:
    #     response=restore_shopify_data('products',{'product',product})
    #     print()
    # if response.status_code!=200:
    #     print('creating product')
    #     create_product({'product':product})