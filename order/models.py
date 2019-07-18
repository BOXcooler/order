import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MinValueValidator


class Order(models.Model):
    order_item = models.CharField(max_length=200, unique=False, error_messages={'required': 'It is required field'})
    slug = models.SlugField(max_length=50, unique=True, default=uuid.uuid1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_name')
    created_on = models.DateTimeField(default=now)
    cost = models.FloatField(default=0, validators=[MinValueValidator(0.01)])
    comment = models.TextField()

    def __str__(self):
        return self.order_item
