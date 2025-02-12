from django import forms
from .models import Subject


class SubjectForm(forms.ModelForm):
    prerequisites = forms.MultipleChoiceField(
        choices=Subject.PREREQUISITE_CHOICES,
        widget=forms.SelectMultiple(attrs={
            'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
        })
    )
    class Meta:
        model = Subject
        fields = ('name', 'department', 'description', 'credit_hours', 'status', 'grade_level', 'prerequisites')

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter subject name',
            }),
            'department': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 4,
            }),
            'credit_hours': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
            'grade_level': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError("Subject name must be at least 2 characters long.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise forms.ValidationError("Description must be at least 10 characters long.")
        return description

    def clean_credit_hours(self):
        credit_hours = self.cleaned_data.get('credit_hours')
        if credit_hours is None or credit_hours <= 0:
            raise forms.ValidationError("Credit hours must be a positive number.")
        return credit_hours

    def clean_prerequisites(self):
        prerequisites = self.cleaned_data.get('prerequisites')
        if not prerequisites:
            raise forms.ValidationError("Please select prerequisites.")
        return prerequisites
