from django.urls import path
from . import views

app_name = 'mealsite'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('list/<str:category>/', views.CategoryListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.MealDetail.as_view(), name='detail')
]
