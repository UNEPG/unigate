from django_filters import CharFilter
from django_filters.rest_framework import FilterSet


class SystemDataFilterSet(FilterSet):
    state = CharFilter(field_name="unisat_data__state")
    expired = CharFilter(field_name="is_expired")

    class Meta:
        fields = ['expired', 'state']


class BmeDataFilterSet(FilterSet):
    expired = CharFilter(field_name="is_expired")

    class Meta:
        fields = ['expired', ]


class BnoDataFilterSet(FilterSet):
    expired = CharFilter(field_name="is_expired")

    class Meta:
        fields = ['expired', ]


class SiDataFilterSet(FilterSet):
    expired = CharFilter(field_name="is_expired")

    class Meta:
        fields = ['expired', ]
