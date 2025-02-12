
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from departments.models import Department
from subjects.models import Subject
from departments.base_models import BaseModel
from django.core.validators import RegexValidator


phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Enter a valid Uzbekistan phone number in the format: +998XXXXXXXXX (9 digits after +998)."
)


class Teacher(BaseModel):

    EMPLOYMENT_TYPE_CHOICES = [
        ('full', 'Full Time'),
        ('part', 'Part Time'),
        ('contract', 'Contract'),
    ]

    STATUS_CHOICES = [
        ('ac', 'Active'),
        ('in', 'Inactive'),
        ('pd', 'Pending'),
    ]
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    qualification = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=13,
        validators=[phone_regex],
        help_text="Enter a valid Uzbekistan phone number (e.g., +998901234567)."
    )
    address = models.TextField()
    join_date = models.DateField()
    slug = models.SlugField(unique=True, blank=True)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='teachers/')
    employment_type = models.CharField(max_length=8, choices=EMPLOYMENT_TYPE_CHOICES)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='in')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers', null=True, blank=True)
    subjects = models.ManyToManyField(Subject, related_name='teachers', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_detail_url(self):
        return reverse('teachers:detail', args=[
            self.created_at.year,
            self.created_at.month,
            self.created_at.day,
            self.slug
        ])

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.first_name}-{self.last_name}")
            self.slug = base_slug
            counter = 1
            while Teacher.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def get_update_url(self):
        return reverse('teachers:update', args=[self.pk])

    def get_delete_url(self):
        return reverse('teachers:delete', args=[self.pk])
