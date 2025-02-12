
from django.urls import path
from . import views


app_name = 'students'


urlpatterns = [
    path('list/', views.StudentListView.as_view(), name='student_list'),
    path('create/', views.StudentCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.StudentUpdateView.as_view(), name='update'),
    path('detail/<int:year>/<int:month>/<int:day>/<slug:slug>', views.StudentDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', views.StudentDeleteView.as_view(), name='delete'),
]
