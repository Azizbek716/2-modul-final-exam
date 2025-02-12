
from django.core.paginator import Paginator
from django.shortcuts import redirect
from departments.models import Department
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Subject
from django.urls import reverse_lazy
from .forms import SubjectForm
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView


class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'subjects/list.html'
    context_object_name = 'subjects'
    paginate_by = 10

    def get_queryset(self):
        subjects = Subject.objects.all()
        status = self.request.GET.get('status')
        department = self.request.GET.get('department')
        grade_level = self.request.GET.get('grade_level')
        search_query = self.request.GET.get('search')

        if status:
            subjects = subjects.filter(status=status)
        if department:
            subjects = subjects.filter(department=department)
        if grade_level:
            subjects = subjects.filter(grade_level=grade_level)
        if search_query:
            subjects = subjects.filter(name__icontains=search_query)

        return subjects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        subjects_page = paginator.get_page(page)

        context['subjects'] = subjects_page
        context['paginator'] = paginator
        context['departments'] = Department.objects.all()
        return context


class SubjectCreateView(CreateView):
    model = Subject
    template_name = 'subjects/form.html'
    form_class = SubjectForm
    success_url = reverse_lazy('subjects:subject_list')

    def form_valid(self, form):
        messages.success(self.request, "Subject successfully created!")
        return super().form_valid(form)


class SubjectUpdatedView(UpdateView):
    model = Subject
    template_name = 'subjects/form.html'
    form_class = SubjectForm
    success_url = reverse_lazy('subjects:subject_list')

    def form_valid(self, form):
        messages.success(self.request, "Subject successfully updated!")
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class SubjectDetailView(DetailView):
    model = Subject
    template_name = 'subjects/detail.html'
    context_object_name = 'subject'


class SubjectDeleteView(DeleteView):
    model = Subject
    success_url = reverse_lazy('subjects:subject_list')

    def dispatch(self, request, *args, **kwargs):
        group = self.get_object()
        group.delete()
        return redirect(self.success_url)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
