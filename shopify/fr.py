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


def fetch_backup_data_id(object,id):
    url = f'https://trialproject12.myshopify.com/admin/api/2024-01/{object}/{id}.json'

    # Make the request with the access token included in the headers
    headers = {
        'X-Shopify-Access-Token': '',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    # print(data)
    s = Store.objects.get(Organization_name='Trial')
    o = Object()
    o.store = s
    o.object_type = object
    o.data = json.dumps(data)
    o.save()





def create_object(object_type,data):
    url = f'https://trialproject12.myshopify.com/admin/api/2024-01/{object_type}.json'
    headers = {
        "X-Shopify-Access-Token":'' ,
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=data, headers=headers)

    print(response.status_code)
    print(response.json())


def restore_shopify_data(object_type,data):
    #print(json.loads(data))
    d=json.loads(data)
    id_value=d.get('product',{}).get('id')
    #print(id_value)
    url = f'https://trialproject12.myshopify.com/admin/api/2024-01/{object_type}/{id_value}.json'
    headers = {
        'X-Shopify-Access-Token':'' ,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.put(url, headers=headers, data=data)

    return response

def restore_data(object_type,uuid):
    o = Object.objects.get(id=uuid)
    object_type = o.object_type
    url = f'https://trialproject12.myshopify.com/admin/api/2024-01/{object_type}.json'
    headers = {
        'X-Shopify-Access-Token': '',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    data=json.loads(o.data)
    #print(products.get("products", [])[0] )
    num_parts = len(data.get(object_type, []))
    #print(num_parts)
    for i in range(0,num_parts):
        item=data.get(object_type, [])[i]
        # print({'product':p})
        data={object_type[:-1]: item}
        response = restore_shopify_data(object_type,json.dumps(data))
        #print(response.status_code)
        #print(response.text)
        if response.status_code != 200:
            print('creating {object_type}')
            create_object(object_type,json.dumps(data))
        #print(json.dumps(data))


    # for product in products['products']:
    #     response=restore_shopify_data('products',{'product',product})
    #     print()
    # if response.status_code!=200:
    #     print('creating product')
    #     create_product({'product':product})