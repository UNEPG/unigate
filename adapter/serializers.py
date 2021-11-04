from abc import ABC

from rest_framework import serializers
import adapter.models as azt_models
import json


class VcmdSchemaBaseSerializer(serializers.ModelSerializer):
    otp = serializers.SerializerMethodField()
    config = serializers.SerializerMethodField()
    space = serializers.SerializerMethodField()
    memory = serializers.SerializerMethodField()

    @staticmethod
    def get_otp(obj):
        try:
            return json.loads(obj.otp)
        except AttributeError:
            return obj['otp']

    @staticmethod
    def get_config(obj):
        try:
            return json.loads(obj.config)
        except AttributeError:
            return obj['config']

    @staticmethod
    def get_space(obj):
        try:
            return json.loads(obj.space)
        except AttributeError:
            return obj['space']

    @staticmethod
    def get_memory(obj):
        try:
            return json.loads(obj.memory)
        except AttributeError:
            return obj['memory']

    class Meta:
        model = azt_models.VcmdSchemaBase
        exclude = ("id", )


class SystemDataSerializer(serializers.ModelSerializer):
    unisat_data = VcmdSchemaBaseSerializer(many=False)

    class Meta:
        model = azt_models.SystemData
        exclude = ("is_expired", "expire_date", "date_of_add", "date_of_update")


class BmeDataBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = azt_models.BmeDataBase
        exclude = ("id", )


class BmeDataSerializer(serializers.ModelSerializer):
    unisat_data = BmeDataBaseSerializer(many=False)

    class Meta:
        model = azt_models.BmeData
        exclude = ("is_expired", "expire_date", "date_of_add", "date_of_update")


class BnoDataBaseSerializer(serializers.ModelSerializer):
    acceleration = serializers.SerializerMethodField()
    magnetic = serializers.SerializerMethodField()
    gyro = serializers.SerializerMethodField()
    euler = serializers.SerializerMethodField()
    quaternion = serializers.SerializerMethodField()
    linear_acceleration = serializers.SerializerMethodField()
    gravity = serializers.SerializerMethodField()

    @staticmethod
    def get_acceleration(obj):
        try:
            return json.loads(obj.acceleration)
        except AttributeError:
            return obj['acceleration']

    @staticmethod
    def get_magnetic(obj):
        try:
            return json.loads(obj.magnetic)
        except AttributeError:
            return obj['magnetic']

    @staticmethod
    def get_gyro(obj):
        try:
            return json.loads(obj.gyro)
        except AttributeError:
            return obj['gyro']

    @staticmethod
    def get_euler(obj):
        try:
            return json.loads(obj.euler)
        except AttributeError:
            return obj['euler']

    @staticmethod
    def get_quaternion(obj):
        try:
            return json.loads(obj.quaternion)
        except AttributeError:
            return obj['quaternion']

    @staticmethod
    def get_linear_acceleration(obj):
        try:
            return json.loads(obj.linear_acceleration)
        except AttributeError:
            return obj['linear_acceleration']

    @staticmethod
    def get_gravity(obj):
        try:
            return json.loads(obj.gravity)
        except AttributeError:
            return obj['gravity']

    class Meta:
        model = azt_models.BnoDataBase
        exclude = ("id",)


class BnoDataSerializer(serializers.ModelSerializer):
    unisat_data = BnoDataBaseSerializer(many=False)

    class Meta:
        model = azt_models.BnoData
        exclude = ("is_expired", "expire_date", "date_of_add", "date_of_update")


class SiDataBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = azt_models.SiDataBase
        fields = ("__all__")


class SiDataSerializer(serializers.ModelSerializer):
    unisat_data = SiDataBaseSerializer(many=False)

    class Meta:
        model = azt_models.SiData
        exclude = ("is_expired", "expire_date", "date_of_add", "date_of_update")


class SimpleMessageSerializer(serializers.Serializer):
    msg = serializers.CharField(max_length=50)


class CurrentTimeSerializer(serializers.Serializer):
    now = serializers.DateTimeField()


class CameraDataBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = azt_models.CameraDataBase
        fields = ("__all__")


class CameraDataSerializer(serializers.ModelSerializer):
    unisat_data = CameraDataBaseSerializer(many=False)

    class Meta:
        model = azt_models.CameraData
        exclude = ("is_expired", "expire_date", "date_of_add", "date_of_update")
