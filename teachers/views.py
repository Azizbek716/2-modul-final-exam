
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from departments.models import Department
from subjects.models import Subject
from .models import Teacher
from django.urls import reverse_lazy
from .forms import TeacherForm
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import DeleteView, UpdateView


class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = 'teachers/list.html'
    context_object_name = 'teachers'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['departments'] = Department.objects.all()
        ctx['subjects'] = Subject.objects.all()
        return ctx

    def get_queryset(self):
        teachers = Teacher.objects.all()
        status = self.request.GET.get('status')
        department = self.request.GET.get('department')
        subjects = self.request.GET.get('subject')
        search_query = self.request.GET.get('search')

        if status:
            teachers = teachers.filter(status=status)
        if department:
            teachers = teachers.filter(department=department)
        if subjects:
            teachers = teachers.filter(subjects=subjects)
        if search_query:
            teachers = teachers.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
        return teachers


class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teachers/form.html'

    def get_success_url(self):
        return reverse_lazy('teachers:teacher_list')


class TeacherUpdatedView(UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teachers/form.html'
    success_url = reverse_lazy('teachers:teacher_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'teachers/detail.html'
    context_object_name = 'teacher'


class TeacherDeleteView(DeleteView):
    model = Teacher
    success_url = reverse_lazy('teachers:teacher_list')

    def dispatch(self, request, *args, **kwargs):
        group = self.get_object()
        group.delete()
        return redirect(self.success_url)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
