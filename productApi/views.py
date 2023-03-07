from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.http import Http404
from .simpledata import data as simpledata
from rest_framework import generics
from rest_framework.views import APIView, Response
from rest_framework import status


def home(request):
    return HttpResponse("Welcome our site")


def get_data(request, name):
    data = []
    for pro in simpledata:
        if name in pro['productname']:
            data.append(pro)
    return JsonResponse({"numberOf": len(data), "data": data})


def get_data_dict(name):
    data = []
    for pro in simpledata:
        if name in pro['productname']:
            data.append(pro)
    return {"numberOf": len(data), "data": data}


def get_data_webview(request, name):
    return render(request, "api/webview.html", get_data_dict(name))


class ProductListApi(APIView):
    def get(self, request):
        return Response(get_data_dict(), status.HTTP_200_OK)

# def data_get(request, productname):
#     try:
#         try:
#             for i in simpledata:
#                 if i['productName'] == productname:
#                     data = i
#             data = json.dumps({"data": data})
#         except Exception as e:
#             data = ""
#             for i in simpledata:
#                 data += i['productName'] + ","
#             data = json.dumps({"slimily product name is": data})
#             print(e)
#         print(data)
#         return HttpResponse({data})
#     except Http404:
#         # return HttpResponse({"error":"please enter the product name {0}".format(data)})
#         print(e)
