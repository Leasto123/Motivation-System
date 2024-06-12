from django.urls import path
from .views import home, services, register, order_service, admin_services, CustomLoginView, add_review, about, user_logout

urlpatterns = [
    path('', home, name='home'),
    path('services/', services, name='services'),
    path('register/', register, name='register'),
    path('order_service/<int:service_id>/', order_service, name='order_service'),
    path('admin_services/', admin_services, name='admin_services'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('add_review/', add_review, name='add_review'),
    path('about/', about, name='about'),
    path('logout/', user_logout, name='logout'),
]
