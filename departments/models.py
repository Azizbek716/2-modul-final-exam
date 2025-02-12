from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from .base_models import BaseModel
from django.core.validators import RegexValidator


phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Enter a valid Uzbekistan phone number in the format: +998XXXXXXXXX (9 digits after +998)."
)


class Department(BaseModel):

    STATUS_CHOICES = [
        ('ac', 'Active'),
        ('in', 'Inactive'),
        ('pd', 'Pending'),
    ]
    HEAD_OF_DEPARTMENT = [
        ('js', 'Dr. Jane Smith'),
        ('jd', 'Dr. John Doe'),
        ('sj', 'Prof. Sarah Johnson'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    head_department = models.CharField(max_length=2, choices=HEAD_OF_DEPARTMENT, blank=True)
    location = models.CharField(max_length=500)
    phone_number = models.CharField(
        max_length=13,
        validators=[phone_regex],
        help_text="Enter a valid Uzbekistan phone number (e.g., +998901234567)."
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='ac')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_detail_url(self):
        return reverse('departments:detail', args=[
            self.created_at.year,
            self.created_at.month,
            self.created_at.day,
            self.slug
        ])

    def get_update_url(self):
        return reverse('departments:update', args=[self.pk])

    def get_delete_url(self):
        return reverse('departments:delete', args=[self.pk])

    def __str__(self):
        return self.name
