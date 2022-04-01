from rest_framework.decorators import api_view
from rest_framework.response import Response
from authentication.models import Lead, Remark, SalesUser
from .serializers import (
    LeadSerializer,
    NewRemarkSerializer,
    UserSerializer,
    RemarkSerializer,
)
import django_filters
from django_filters.utils import translate_validation
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


class LeadFilter(django_filters.FilterSet):
    class Meta:
        model = Lead
        fields = ["state", "name", "created"]


@api_view(["GET"])
def lead_list(request):
    if request.method == "GET":
        paginator = PageNumberPagination()
        paginator.page_size = 2
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


@api_view(["GET", "POST"])
def remark_list(request):
    if request.method == "GET":
        queryset = Remark.objects.all().order_by("-created")
        serializer = RemarkSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        # Remark.objects.create(
        #     user=request.user, lead=mark.lead, remark=request.POST.get("remark")
        # )
        request.data.update({"user": request.user.id})
        # print(request.data)
        serializer = NewRemarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def remark_detail(request, email, id):
    if request.method == "GET":
        leadremark = Remark.objects.filter(user__email=email, lead__id=id).order_by(
            "created"
        )
        serializer = RemarkSerializer(leadremark, many=True)
        return Response(serializer.data)
