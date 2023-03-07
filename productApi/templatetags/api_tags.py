from django.template import Library

register = Library()


def dict_link(value):
    return value["detaillink"]

register.filter("link", dict_link)