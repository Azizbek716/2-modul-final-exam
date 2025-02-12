
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from subjects.models import Subject
from teachers.models import Teacher
from departments.base_models import BaseModel


class Group(BaseModel):
    GRADE_LEVEL_CHOICES = [
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
        ('12', 'Grade 12'),
    ]

    SCHEDULE_CHOICES = [
        ('mr', 'Morning Session'),
        ('af', 'Afternoon Session'),
        ('ev', 'Evening Session'),
    ]

    STATUS_CHOICES = [
        ('ac', 'Active'),
        ('in', 'Inactive'),
        ('pd', 'Pending'),
    ]

    name = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=2, choices=GRADE_LEVEL_CHOICES)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='groups', blank=True)
    schedule = models.CharField(max_length=2, choices=SCHEDULE_CHOICES)
    academic_year = models.CharField(max_length=30)
    max_students = models.PositiveIntegerField()
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    subjects = models.ManyToManyField(Subject, related_name='groups')



    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.name}")
            self.slug = base_slug
            counter = 1
            while Group.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def get_detail_url(self):
        return reverse('groups:detail', args=[
            self.created_at.year,
            self.created_at.month,
            self.created_at.day,
            self.slug
        ])
    def get_update_url(self):
        return reverse('groups:update', args=[self.pk])

    def get_delete_url(self):
        return reverse('groups:delete', args=[self.pk])

    def __str__(self):
        return self.name
