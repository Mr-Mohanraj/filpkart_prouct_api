from django.shortcuts import render
from django.http import HttpResponse
import json
from django.http import Http404
from rest_framework import generics
from rest_framework.views import APIView, Response
from rest_framework import status
from authenticationApi.utils import check_user
from .utils import get_data_dict


def home(request):
    return HttpResponse("Welcome our site")


def get_data_webview(request, name):
    return render(request, "api/webview.html", get_data_dict(name))


class ProductListApi(APIView):
    def get(self, request, token, password):
        data = check_user(token, password)
        search_name = self.request.query_params.get('q')
        product_length = int(self.request.query_params.get('value'))
        search_data = self.request.query_params.get('data') == "true"
        search_price = self.request.query_params.get('price') == "true"
        all_data = self.request.query_params.get('all') == "true"
        if search_data or search_price or all_data:
            data_want = {"search_name": search_name, "product_length": product_length, "data": search_data,
                         "based_price": search_price, "all": False, "rating_review": {"rating": 4.5, "review": 55}}
        else:
            data_want = {"search_name": search_name, "product_length": product_length, "data": False,
                         "based_price": True, "all": False, "rating_review": {"rating": 4.5, "review": 55}}
        if data[1]:
            return Response(get_data_dict(data_want), status.HTTP_200_OK)
        else:
            return Response({"msg": data[0]}, status.HTTP_400_BAD_REQUEST)
