import datetime
from datetime import date

import pydantic
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import generics, status
from unigate.settings import UNISAT_DOMAIN
import adapter.models as azt_models
import adapter.satellite_models as azt_satellite_models
from django.utils import timezone
from django.urls import reverse
import requests
import inspect
import json
import os


def send_request_to_unisat(method, url, json_class=None, params=None):
    request_url = f'{UNISAT_DOMAIN}{url}'

    if not params:
        params = [None, None]

    if params[1]:
        request_url = request_url + f'?{params[0]}={params[1]}'
    try:
        json_data = getattr(requests, f"{method}")(request_url).json()

        if json_class:
            try:
                json_data = getattr(azt_satellite_models, json_class)(**json_data)
            except pydantic.error_wrappers.ValidationError:
                return False
    except Exception as e:
        return False

    return json_data


def get_last_object(file_name, json_class):
    with open(f'{os.getcwd()}/adapter/data/{file_name}.txt', 'r') as f:
        json_txt = (f.read())
    json_data = json.loads(json_txt)

    last_object = getattr(azt_satellite_models, json_class)(**json_data)
    return last_object


def check_auth(request):
    if not request.user.is_authenticated:
        raise PermissionDenied()


def str_to_class(classname):
    return getattr(azt_models, classname)


class ViewSerializerMixin:
    list_serializer_class = None

    @staticmethod
    def get_caller_name():
        current_frame = inspect.currentframe()
        call_frame = inspect.getouterframes(current_frame, 2)
        return call_frame[2][3]

    def get_serializer(self, *args, **kwargs):
        caller = self.get_caller_name()
        serializer_class = self.get_serializer_class()

        if caller == 'list':
            serializer_class = self.list_serializer_class
        elif caller == 'retrieve':
            serializer_class = self.serializer_class

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class ListObjectsMixin(generics.ListAPIView):

    serializer_class = None
    filter_backends = (DjangoFilterBackend,)
    permission_classes = []
    model = None
    sub_model = None
    user_private = None
    filter_fields = []
    search_fields = []

    def list(self, request, *args, **kwargs):
        try:
            class_name = str_to_class(self.sub_model)

            objects = class_name.objects.all()

            objects = self.filter_queryset(objects)

            page = self.paginate_queryset(objects)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(objects, many=True)

            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error, wrong data: {str(e)}",  status.HTTP_400_BAD_REQUEST)


class RetrieveObjectsMixin(generics.RetrieveAPIView):
    serializer_class = None
    filter_backends = (DjangoFilterBackend,)
    permission_classes = []
    obj = None
    model = None
    sub_model = None
    json_class = None
    user_private = None
    params = None
    lookup_field = 'id'

    def get_param(self):
        return self.request.GET.get(self.params, None)

    def check_last_obj(self):
        obj = str_to_class(self.model).objects.first()
        path = str(self.request.path).replace("/unigate/", "")
        param = self.get_param()

        if obj:
            if not obj.is_expired:
                now = timezone.now()
                if now.replace(tzinfo=datetime.timezone.utc) > obj.expire_date:
                    obj.is_expired = True
                    obj.save()
                else:
                    return obj.unisat_data

        last_object = send_request_to_unisat(method='get', url=path, json_class=self.json_class, params=[self.params,
                                                                                                         param])
        if not last_object and obj:
            return obj.unisat_data
        elif not last_object and not obj:
            return Response("Unisat didn't answer and no object in db. Try later", status.HTTP_503_SERVICE_UNAVAILABLE)

        return self.get_unisat_data(last_object)

    def get_unisat_data(self, last_object):
        pass

    def retrieve(self, request, *args, **kwargs):
        class_name = str_to_class(self.model)
        try:
            obj = self.check_last_obj()
            serializer = self.serializer_class(obj)
            return Response(serializer.data, status.HTTP_200_OK)
        except class_name.DoesNotExist:
            return Response(f'DoesNotExist. {self.obj} does not exist in {self.model}', status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"Error, wrong data: {str(e)}",  status.HTTP_400_BAD_REQUEST)


class AztViewMixin(ListObjectsMixin, RetrieveObjectsMixin, GenericViewSet):
    pass
