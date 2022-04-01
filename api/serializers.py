from rest_framework import serializers
from authentication.models import Lead, Remark, SalesUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesUser
        fields = [
            "first_name",
            "last_name",
            "user_type",
            "user_bio",
            "username",
            "email",
        ]


class LeadSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()

    class Meta:
        model = Lead
        fields = [
            "id",
            "state",
            "name",
            "phone_number",
            "email",
            "user_id",
            "created",
        ]


class RemarkSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    lead = LeadSerializer()

    class Meta:
        model = Remark
        fields = [
            "remark",
            "user",
            "lead",
            "created",
            "updated",
        ]


class NewRemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remark
        fields = [
            "remark",
            "user",
            "lead",
        ]
