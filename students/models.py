
from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse
from groups.models import Group
from departments.base_models import BaseModel
from django.core.validators import RegexValidator


phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Enter a valid Uzbekistan phone number in the format: +998XXXXXXXXX (9 digits after +998)."
)


class Student(BaseModel):

    SELECT_GENDER = [
        ('mal', 'Male'),
        ('fem', 'Female'),
    ]

    GRADE_CHOICES = [
        ('1', 'Grade 1'),
        ('2', 'Grade 2'),
        ('3', 'Grade 3'),
        ('4', 'Grade 4'),
        ('5', 'Grade 5'),
        ('6', 'Grade 6'),
        ('7', 'Grade 7'),
        ('8', 'Grade 8'),
        ('9', 'Grade 9'),
        ('10', 'Grade 10'),
        ('11', 'Grade 11'),
    ]

    STATUS_CHOICES = [
        ('ac', 'Active'),
        ('in', 'Inactive'),
        ('pd', 'Pending'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    phone_number = models.CharField(
        max_length=13,
        validators=[phone_regex],
        help_text="Enter a valid Uzbekistan phone number (e.g., +998901234567)."
    )
    image = models.ImageField(upload_to='images/')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students', blank=True)
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, blank=True)
    gender = models.CharField(max_length=50, choices=SELECT_GENDER, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='ac')
    address = models.TextField()
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=13)
    guardian_email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.first_name}-{self.last_name}")
            unique_slug = base_slug
            counter = 1
            while Student.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_detail_url(self):
        return reverse('students:detail', args=[
            self.created_at.year,
            self.created_at.month,
            self.created_at.day,
            self.slug
        ])

    def get_update_url(self):
        return reverse('students:update', args=[self.pk])

    def get_delete_url(self):
        return reverse('students:delete', args=[self.pk])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
