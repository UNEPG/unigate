import json

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import adapter.satellite_models as azt_satellite_models
import adapter.utils as azt_view_utils
import adapter.models as azt_models
import adapter.filters as azt_filters
import adapter.serializers as azt_serializers
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser, FormParser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
import pytz

# Create your views here.

UTC_TZ = pytz.utc


class CheckConnectionView(APIView):
    serializer_class = azt_serializers.SimpleMessageSerializer

    def get(self, request):

        azt_view_utils.check_auth(request)

        json_response = azt_view_utils.send_request_to_unisat('get', '', )
        if not json_response or json_response.get('detail', "") == 'Not Found':
            return Response("No connection", status.HTTP_503_SERVICE_UNAVAILABLE)
        serializer = self.serializer_class(json_response)
        return Response(serializer.data, status.HTTP_200_OK)

    msg_config = openapi.Parameter(f'msg', in_=openapi.IN_QUERY, description=f'say ping', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[msg_config], )
    def post(self, request):
        azt_view_utils.check_auth(request)

        param = request.GET.get(f'msg')
        if param == 'ping':
            json_response = azt_view_utils.send_request_to_unisat(method='post', url='', json_class=None,
                                                                  params=['msg', param])
            if not json_response or json_response.get('detail', "") == 'Not Found':
                return Response("No connection", status.HTTP_503_SERVICE_UNAVAILABLE)
            serializer = self.serializer_class(json_response)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response("Input parameter in url ?msg=ping", status.HTTP_400_BAD_REQUEST)


class GetCurrentTimeView(APIView):
    serializer_class = azt_serializers.CurrentTimeSerializer

    def get(self, request):
        azt_view_utils.check_auth(request)

        json_response = azt_view_utils.send_request_to_unisat('get', 'now', None, None)
        if not json_response or json_response.get('detail', "") == 'Not Found':
            return Response("No connection", status.HTTP_503_SERVICE_UNAVAILABLE)
        serializer = self.serializer_class(json_response)
        return Response(serializer.data, status.HTTP_200_OK)


class SystemDataView(azt_view_utils.AztViewMixin):
    queryset = azt_models.SystemData.objects.all()
    serializer_class = azt_serializers.VcmdSchemaBaseSerializer
    model = 'SystemData'
    sub_model = 'VcmdSchemaBase'
    obj = 'system_data'
    json_class = "VcmdSchema"
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    lookup_field = "id"
    filter_class = azt_filters.SystemDataFilterSet
    filter_fields = []
    search_fields = ['unisat_data__updated', ]
    ordering_fields = ['id', 'date_of_update', "date_of_add"]

    def get_unisat_data(self, last_object: azt_satellite_models.VcmdSchema):
        vcmd_obj = azt_models.VcmdSchemaBase.objects.create(unisat_id=last_object.id,
                                                            updated=last_object.updated,
                                                            cam_supported=last_object.cam_supported,
                                                            cam_detected=last_object.cam_detected,
                                                            state=last_object.state,
                                                            temperature=last_object.temperature,
                                                            arm_clock=last_object.arm_clock,
                                                            core_clock=last_object.core_clock,
                                                            serial_clock=last_object.serial_clock,
                                                            storage_clock=last_object.storage_clock,
                                                            voltage=last_object.voltage,
                                                            otp=json.dumps(last_object.otp),
                                                            config=json.dumps(last_object.config),
                                                            memory=json.dumps(last_object.memory),
                                                            space=json.dumps(last_object.space),
                                                            cpu_memory=last_object.cpu_memory,
                                                            gpu_memory=last_object.gpu_memory)

        system_data = azt_models.SystemData.objects.create(unisat_data=vcmd_obj)
        system_data.expire_date = system_data.date_of_update + datetime.timedelta(minutes=10)
        system_data.save()

        return vcmd_obj


class BmeDataView(azt_view_utils.AztViewMixin):
    queryset = azt_models.BmeData.objects.all()
    serializer_class = azt_serializers.BmeDataBaseSerializer
    sub_model = 'BmeDataBase'
    model = 'BmeData'
    obj = 'bme_data'
    json_class = "BmeDataBaseTime"
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    lookup_field = "id"
    filter_class = azt_filters.BmeDataFilterSet
    filter_fields = []
    search_fields = ['unisat_data__updated', ]
    ordering_fields = ['id', 'date_of_update', "date_of_add"]

    def get_unisat_data(self, last_object: azt_satellite_models.BmeDataBaseTime):
        bme_obj = azt_models.BmeDataBase.objects.create(unisat_id=last_object.id,
                                                        updated=last_object.updated,
                                                        temperature=last_object.temperature,
                                                        pressure=last_object.pressure,
                                                        humidity=last_object.humidity, )

        bme_data = azt_models.BmeData.objects.create(unisat_data=bme_obj)
        bme_data.expire_date = bme_data.date_of_update + datetime.timedelta(minutes=10)
        bme_data.save()

        return bme_obj


class BnoDataView(azt_view_utils.AztViewMixin):
    queryset = azt_models.BnoData.objects.all()
    serializer_class = azt_serializers.BnoDataBaseSerializer
    model = 'BnoData'
    sub_model = "BnoDataBase"
    obj = 'bno_data'
    json_class = "BnoDataBaseTime"
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    lookup_field = "id"
    filter_class = azt_filters.BnoDataFilterSet
    filter_fields = []
    search_fields = ['unisat_data__updated', ]
    ordering_fields = ['id', 'date_of_update', "date_of_add"]

    def get_unisat_data(self, last_object: azt_satellite_models.BnoDataBaseTime):
        bno_obj = azt_models.BnoDataBase.objects.create(unisat_id=last_object.id,
                                                        temperature=last_object.temperature,
                                                        updated=last_object.updated,
                                                        acceleration=json.dumps(last_object.acceleration),
                                                        magnetic=json.dumps(last_object.magnetic),
                                                        gyro=json.dumps(last_object.gyro),
                                                        euler=json.dumps(last_object.euler),
                                                        quaternion=json.dumps(last_object.quaternion),
                                                        linear_acceleration=json.dumps(last_object.linear_acceleration),
                                                        gravity=json.dumps(last_object.gravity),

                                                        )

        bno_data = azt_models.BnoData.objects.create(unisat_data=bno_obj)
        bno_data.expire_date = bno_data.date_of_update + datetime.timedelta(minutes=10)
        bno_data.save()

        return bno_obj


class SiDataView(azt_view_utils.AztViewMixin):
    queryset = azt_models.SiData.objects.all()
    serializer_class = azt_serializers.SiDataBaseSerializer
    sub_model = 'SiDataBase'
    model = 'SiData'
    obj = 'si_data'
    json_class = "SiDataBaseTime"
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    lookup_field = "id"
    filter_class = azt_filters.SiDataFilterSet
    filter_fields = []
    search_fields = ['unisat_data__updated', ]
    ordering_fields = ['id', 'date_of_update', "date_of_add"]

    def get_unisat_data(self, last_object: azt_satellite_models.SiDataBaseTime):
        si_obj = azt_models.SiDataBase.objects.create(unisat_id=last_object.id,
                                                      updated=last_object.updated,
                                                      vis=last_object.vis,
                                                      ir=last_object.ir,
                                                      uv=last_object.uv)

        si_data = azt_models.SiData.objects.create(unisat_data=si_obj)
        si_data.expire_date = si_data.date_of_update + datetime.timedelta(minutes=10)
        si_data.save()

        return si_obj


class CameraDataView(azt_view_utils.AztViewMixin):
    queryset = azt_models.CameraData.objects.all()
    serializer_class = azt_serializers.CameraDataBaseSerializer
    model = 'CameraData'
    sub_model = 'CameraDataBase'
    obj = 'camera_data'
    json_class = "CameraSchema"
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    lookup_field = "id"
    params = 'cam_num'
    filter_class = azt_filters.SiDataFilterSet
    filter_fields = []
    search_fields = ['unisat_data__updated', ]
    ordering_fields = ['id', 'date_of_update', "date_of_add"]

    def get_unisat_data(self, last_object: azt_satellite_models.CameraSchema):
        camera_obj = azt_models.CameraDataBase.objects.create(unisat_id=last_object.id,
                                                              updated=last_object.updated,
                                                              cam_num=last_object.cam_num,
                                                              path=last_object.path)

        camera_data = azt_models.CameraData.objects.create(unisat_data=camera_obj)
        camera_data.expire_date = camera_data.date_of_update + datetime.timedelta(minutes=10)
        camera_data.save()

        return camera_obj

    def check_last_obj(self):
        param = self.get_param()
        if not param:
            param = 0

        obj = azt_view_utils.str_to_class(self.model).objects.filter(unisat_data__cam_num=param).first()
        path = str(self.request.path).replace("/adapter/", "")

        if obj:

            if not obj.is_expired:
                now = azt_view_utils.timezone.now()
                if now.replace(tzinfo=datetime.timezone.utc) > obj.expire_date:
                    obj.is_expired = True
                    obj.save()
                else:
                    return obj.unisat_data

        last_object = azt_view_utils.send_request_to_unisat(method='get', url=path, json_class=self.json_class,
                                                            params=[self.params, param])

        if not last_object and obj:
            return obj.unisat_data
        elif not last_object and not obj:
            return Response("Unisat didn't answer and no object in db. Try later", status.HTTP_503_SERVICE_UNAVAILABLE)

        return self.get_unisat_data(last_object)
