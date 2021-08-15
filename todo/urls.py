# have to create this urls.py file manually

from django.urls import path

from todo.views import index, detail, createlist, createitem,item,view

app_name='todo'
urlpatterns = [
    path('', index, name='index'),
    path('view/', view, name='view'),
    path('<int:list_id>/', detail, name='list_details'),
    path('createlist/', createlist, name='list_create'),
    path('createitem/', createitem, name='item_create'),
    path('<int:list_id>/<int:item_id>/',item,name='item_details'),
    path('<int:list_id>/createitem/',createitem,name='item_create')
]