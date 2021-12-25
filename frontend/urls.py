from django.urls import path,re_path
from .views import index  # the view responsible for the frontend

urlpatterns = [
    path('', index,name='index'),  # add the view to the url
    re_path(r'^.*$', index,name='index'), # saved my day

]