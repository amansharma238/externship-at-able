from rest_framework.decorators import api_view
from rest_framework.response import Response
from authentication.models import Lead, Remark, SalesUser
from .serializers import LeadSerializer, UserSerializer, RemarkSerializer
import django_filters
from django_filters.utils import translate_validation
from rest_framework.pagination import PageNumberPagination


class LeadFilter(django_filters.FilterSet):
    class Meta:
        model = Lead
        fields = ["state", "name", "created"]


# class RemarkFilter(django_filters.FilterSet):
#     useremail = django_filters.ModelChoiceFilter(
#         field_name="email", queryset=Lead.objects.all()
#     )

#     class Meta:
#         model = Remark
#         fields = ["user","lead"]


@api_view(["GET"])
def lead_list(request):
    if request.method == "GET":
        paginator = PageNumberPagination()
        paginator.page_size = 10
        filterset = LeadFilter(request.GET, queryset=Lead.objects.all())
        if not filterset.is_valid():
            raise translate_validation(filterset.errors)
        queryset = paginator.paginate_queryset(filterset.qs, request)
        serializer = LeadSerializer(queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def user_list(request):
    if request.method == "GET":
        salesuser = SalesUser.objects.all()
        serializer = UserSerializer(salesuser, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def user_detail(request, email):
    if request.method == "GET":
        salesuser = SalesUser.objects.get(email=email)
        serializer = UserSerializer(salesuser)
        return Response(serializer.data)


@api_view(["GET"])
def remark_list(request):
    if request.method == "GET":
        queryset = Remark.objects.all()
        # filterset = RemarkFilter(request.GET, queryset=queryset)
        # if filterset.is_valid():
        #     queryset = filterset.qs
        serializer = RemarkSerializer(queryset, many=True)
        # serializer = RemarkSerializer(filterset, many=True)

        return Response(serializer.data)


@api_view(["GET"])
def remark_detail(request, email, id):
    if request.method == "GET":
        leadremark = Remark.objects.filter(user__email=email, lead__id=id)
        serializer = RemarkSerializer(leadremark, many=True)
        return Response(serializer.data)
