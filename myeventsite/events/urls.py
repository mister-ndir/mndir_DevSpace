from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/export/csv/', views.export_events_csv, name='export_events_csv'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-subscriptions/', views.my_subscriptions, name='my_subscriptions'),
    
    # Admin pages
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/event/create/', views.admin_event_create, name='admin_event_create'),
    path('admin-dashboard/event/<int:event_id>/edit/', views.admin_event_edit, name='admin_event_edit'),
    path('admin-dashboard/event/<int:event_id>/delete/', views.admin_event_delete, name='admin_event_delete'),
]

handler404 = 'events.views.handler404'