from . import views
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('register/',views.register.as_view(),name="register"),
    path('login/',views.login.as_view(),name="login"),
    path('logout/', views.logout.as_view(), name="logout"),
]