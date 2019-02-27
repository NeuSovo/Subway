from django.urls import path
from .views import *

app_name = "system"
urlpatterns = [
     path('set_text', SetSystemTextItem, name='set_text'),
     path('set_img', SetSystemImgItem, name='set_img'),


     path('set_qr', SetQrcodeView.as_view(), name='set_qr'),
     path('set_backend', SetBackendView.as_view(), name='set_backend'),
     path('set_mobile', SetMobileView.as_view(), name='set_mobile'),
]