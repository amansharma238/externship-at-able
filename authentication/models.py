from django.db import models
from django.contrib.auth.models import AbstractUser

# import uuid


class SalesUser(AbstractUser):
    # user_id = models.UUIDField(
    #     primary_key=True, default=uuid.uuid4, editable=False)
    USERTYPE = (
        ("none", "None"),
        ("admin", "sales_admin"),
        ("representative", "sales_representative"),
    )
    username = models.CharField(
        max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField("email address", unique=True)
    phone_number = models.CharField(max_length=10)
    user_type = models.CharField(
        max_length=32, choices=USERTYPE, default="none")
    user_bio = models.CharField(max_length=200, null=True, blank=True)
    profile = models.ImageField(
        default='default.jpg', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]
    manager_id = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.email}"


class Lead(models.Model):
    state = (
        ("Hot Lead", "Hot Lead"),
        ("Grey Lead", "Cold Lead"),
        ("Med Lead", "Med Lead"),
        ("Success", "Sold"),
        ("New Lead", "New Lead"),
    )

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone_number = models.IntegerField()
    state = models.CharField(default="New Lead", choices=state, max_length=100)
    user_id = models.ForeignKey(SalesUser, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Remark(models.Model):
    user = models.ForeignKey(SalesUser, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    remark = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "created"]

    def __str__(self):
        return self.remark[0:50]
