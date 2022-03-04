from django.db import models
from django.contrib.auth.models import AbstractUser


class SalesUser(AbstractUser):
    USERTYPE = (
        ('none', 'None'),
        ('admin', 'sales_admin'),
        ('representative', 'sales_representative')
    )
    username = models.CharField(
        max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField('email address', unique=True)
    phone_number = models.CharField(max_length=10)
    user_type = models.CharField(
        max_length=32, choices=USERTYPE, default="none")
    user_bio = models.CharField(max_length=200, null=True, blank=True)
    # profile_image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    manager_id = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.email}"


class Lead(models.Model):
    state = (
        ('hot', 'Hot Lead'),
        ('cold', 'Cold Lead'),
        ('med', 'Med Lead'),
        ('sold', 'Sold'),
        ('new', 'New')
    )

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone_number = models.IntegerField()
    state = models.CharField(default='new', choices=state, max_length=100)
    user_id = models.ForeignKey(SalesUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Remark(models.Model):
    user = models.ForeignKey(SalesUser, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    remark = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', 'created']

    def __str__(self):
        return self.remark[0:50]
