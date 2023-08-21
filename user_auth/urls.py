from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('patient/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('create/', views.create_blog, name='create_blog'),
    path('update/<str:slug>', views.update_blog, name= 'update_blog'),
    path('blog_detail/<str:slug>', views.blog_detail, name = 'blog_detail'),
    path('',views.home, name='home'),
    path('category', views.category, name='category'),
    path('self_blog', views.self_blogs, name = 'self_blog')
]
