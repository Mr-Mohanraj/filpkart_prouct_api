from django.shortcuts import render
from django.http import HttpResponse
import json
from django.http import Http404
from .simpledata import data as simpledata


def home(request):
    return HttpResponse("Welcome our site")


def data_get(request, productname):
    try:
        try:
            for i in simpledata:
                if i['productName'] == productname:
                    data = i
            data = json.dumps({"data": data})
        except Exception as e:
            data = ""
            for i in simpledata:
                data += i['productName'] + ","
            data = json.dumps({"slimily product name is": data})
            print(e)
        print(data)
        return HttpResponse({data})
    except Http404:
        # return HttpResponse({"error":"please enter the product name {0}".format(data)})
        print(e)
