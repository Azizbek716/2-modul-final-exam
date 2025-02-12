from django.contrib import admin
from .models import Department
from .forms import DepartmentForm


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_department', 'location', 'email', 'phone_number', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'head_department', 'location', 'email')
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    form = DepartmentForm

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(status='ac')
