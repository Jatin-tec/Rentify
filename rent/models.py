from django.db import models
from authentication.models import Profile

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('condo', 'Condo'),
        ('townhouse', 'Townhouse'),
        ('villa', 'Villa'),
    ]

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    area = models.IntegerField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    nearby_hospitals = models.CharField(max_length=255, blank=True, null=True)
    nearby_colleges = models.CharField(max_length=255, blank=True, null=True)
    images = models.ImageField(upload_to='media/properties/')

    def __str__(self):
        return self.title

from django.utils import timezone

class Notification(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    viewed_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='viewed_by', blank=True, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.first_name} - {self.message}'