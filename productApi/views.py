from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework import status
from authenticationApi.utils import check_user
from .utils import get_data_dict


def home(request):
    """Home page In a html format view for browser"""
    return render(request, "productApi/endpoints.html", {})


def get_data_webview(request, name):
    return render(request, "api/webview.html", get_data_dict(name))


class ProductListApi(APIView):
    """Product api is a get the data from database and send to the user as a json file format.the search query variable and default value:
    {
        "search_name": search_name, 
        "product_length": product_length, 
        "data": search_data,
        "based_price": search_price,
        "all": False
    }
    """
    def get(self, request, token, password):
        data = check_user(token, password)
        try:
            if data[0] == "Done":
                
                search_name = self.request.query_params.get('q')
                if search_name == None:
                    search_name = "iphone"
                    
                product_length = int(self.request.query_params.get('value'))
                if product_length == None:
                    product_length = 10
                    
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
        except Exception as e:
            print(e)
            data_want = ("search_name", "product_length", "data", "based_price", "all (default=Flase)")
            return Response({"msg": data[0], "error_msg":f"check the token or query variables, query variable are {data_want}, search_name and value must be given"}, status.HTTP_400_BAD_REQUEST)
