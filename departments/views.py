
from json import dumps
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.shortcuts import redirect
from .models import Department
from subjects.models import Subject
from students.models import Student
from teachers.models import Teacher
from groups.models import Group
from .forms import DepartmentForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'dashboard.html'
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['teachers'] = Teacher.objects.all()
        ctx['groups'] = Group.objects.all()
        ctx['subjects'] = Subject.objects.all()
        ctx['groups_count'] = Group.objects.filter(status='ac').count()
        ctx['subject_names'] = [subject.name for subject in Subject.objects.all()]
        ctx['subject_teachers_counts'] = [subject.teachers.count() for subject in Subject.objects.all()]
        ctx['student_count'] = Student.objects.filter(status='ac').count()

        enrollments = (
            Student.objects.filter(status='ac')
            .annotate(month=ExtractMonth('created_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        enrollment_data = {i: 0 for i in range(1, 13)}
        for enrollment in enrollments:
            enrollment_data[enrollment['month']] = enrollment['count']

        ctx['enrollment_counts'] = dumps(list(enrollment_data.values()))

        return ctx


class DepartmentsListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'departments/list.html'
    context_object_name = 'departments'


class DepartmentsCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/form.html'
    success_url = reverse_lazy('departments:depart_list')


class DepartmentsUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/form.html'
    success_url = reverse_lazy('departments:depart_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class DepartmentsDetailView(DetailView):
    model = Department
    template_name = 'departments/detail.html'
    context_object_name = 'department'


class DepartmentsDeleteView(DeleteView):
    model = Department
    success_url = reverse_lazy('departments:depart_list')

    def dispatch(self, request, *args, **kwargs):
        group = self.get_object()
        group.delete()
        return redirect(self.success_url)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
