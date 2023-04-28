#views.py
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Addresses
from .serializers import AddressesSerializer
from rest_framework.parsers import JSONParser
import os
import requests

from django.db import models
# Create your views here.


@csrf_exempt
def address_list(request):
    if request.method == 'GET':
        query_set = Addresses.objects.all()
        serializer = AddressesSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AddressesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def address(request, pk):

    obj = Addresses.objects.get(pk=pk)

    if request.method == 'GET':
        serializer = AddressesSerializer(obj)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AddressesSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return HttpResponse(status=204)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        search_name = data['name']
        obj = Addresses.objects.get(name=search_name)

        if data['phone_number'] == obj.phone_number:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

@csrf_exempt
def stability(request):

    if request.method == 'GET':
        api_host = os.getenv('API_HOST', 'https://api.stability.ai')
        url = f"{api_host}/v1/user/balance"

        api_key = "sk-3M0ODX6JIqf3XppYKn8U0rZsNbfxirtZzkjuc5Z2Mm5bvC4J"
        if api_key is None:
            raise Exception("Missing Stability API key.")

        response = requests.get(url, headers={
            "Authorization": f"Bearer {api_key}"
        })

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        # Do something with the payload...
        payload = response.json()
        print(payload)
        return JsonResponse(payload, safe=False)



