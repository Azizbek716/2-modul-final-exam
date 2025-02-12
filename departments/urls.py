from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('list/', views.DepartmentsListView.as_view(), name='depart_list'),
    path('create/', views.DepartmentsCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.DepartmentsUpdateView.as_view(), name='update'),
    path('detail/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.DepartmentsDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', views.DepartmentsDeleteView.as_view(), name='delete'),
]