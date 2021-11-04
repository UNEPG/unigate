from django.urls import path, include
import adapter.views as azt_views

urlpatterns = [
    path('', azt_views.CheckConnectionView.as_view(), name='check_view'),

    path('now/', azt_views.GetCurrentTimeView.as_view(), name='time_view'),

    path('system/', azt_views.SystemDataView.as_view({'get': 'list'}), name="system_view"),
    path('system/last/', azt_views.SystemDataView.as_view({'get': 'retrieve'}), name="system_last_view"),

    path('bme/', azt_views.BmeDataView.as_view({'get': 'list'}), name="bme_view"),
    path('bme/last/', azt_views.BmeDataView.as_view({'get': 'retrieve'}), name="bme_last_view"),

    path('bno/', azt_views.BnoDataView.as_view({'get': 'list'}), name="bno_view"),
    path('bno/last/', azt_views.BnoDataView.as_view({'get': 'retrieve'}), name="bno_last_view"),

    path('si/', azt_views.SiDataView.as_view({'get': 'list'}), name="si_view"),
    path('si/last/', azt_views.SiDataView.as_view({'get': 'retrieve'}), name="si_last_view"),

    path('camera/', azt_views.CameraDataView.as_view({'get': 'list'}), name="camera_view"),
    path('camera/last/', azt_views.CameraDataView.as_view({'get': 'retrieve'}), name="camera_last_view"),
]
