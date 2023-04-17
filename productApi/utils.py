import csv
from .simpledata import data as simpledata
from django.http import JsonResponse


def get_data_dict(data_want: dict):
    print(data_want)
    length = data_want["product_length"]
    data_new = []
    if isinstance(length, int):
        data = []
        based_price = []
        for pro in simpledata:
            if data_want["search_name"] in pro['productname']:
                data.append(pro)
        if data_want["all"]:
            return {"numberOf": len(data), "product_data": simpledata}

        if length <= len(data):
            if data_want["data"]:
                data_new = data[:length]
                if data_want["based_price"]:
                    based_price = based_on_price(data_new)
            elif data_want["based_price"]:
                based_price = based_on_price(data)

            return {"numberOf": len(data), "product_data": data_new, "price based": based_price}
        else:
            return {"error - msg": f"Length must be small then {len(data)}, If you want over the and get all data use all=True in query in url bar"}
    else:
        return {"error - msg": "Input length must be an integer"}


def based_on_price(data: list):
    price_data = []
    for d in data:
        price_data.append({
            "product_name": d["productfullname"],
            "product_price": d["currentprice"]
        })
    return price_data


def based_on_review(data: list, review):
    price_data = []
    for d in data:
        if (d["review"] <= review or d["review"] >= review):
            price_data.append({
                "product_name": d["productfullname"],
                "product_price": d["review"]
            })
        else:
            continue
    return price_data


def based_on_rating_review(data: list, rating_review: dict = {"rating": 4.2, "review": 100}):
    price_data = []
    for d in data:
        if d["rating"] == rating_review[0] and d["review"] == rating_review[1]:
            price_data.append({
                "product_name": d["productfullname"],
                "product_price": d["ratingcount"]
            })
        else:
            continue
    return price_data


def based_on_rating(data: list, rating):
    price_data = []
    for d in data:
        if (d["rating"] <= rating or d["rating"] >= rating):
            price_data.append({
                "product_name": d["productfullname"],
                "product_price": d["ratingcount"]
            })
        else:
            continue
    return price_data


def csv_to_py_file(csv_file_path, py_file_path):
    """Csv and python are without extension
    like a : ./data and ./simple data"""
    with open(f"{csv_file_path}.csv", 'r') as file:
        red = csv.DictReader(file)
        with open(f"{py_file_path}.py", 'w', encoding='utf-8') as file:
            for i in red:
                file.write(f"{str(i)},\n")


# def get_data(request, name):
#     data = []
#     for pro in simpledata:
#         if name in pro['productname']:
#             data.append(pro)
#     return JsonResponse({"numberOf": len(data), "data": data})

#     path('get/<str:name>/', views.get_data, name='dataget'),