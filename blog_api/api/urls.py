from blog_api.api.views import(
    api_detail_blog_view,
    api_create_blog_view,
    api_delete_blog_view,
    api_update_blog_view,
    ApiBlogListView
) 
from django.urls import path
app_name='blog_api'

urlpatterns=[
    path('<slug>/detail',api_detail_blog_view,name='detail'),
    path('<slug>/update/',api_update_blog_view,name='update'),
    path('<slug>/delete/',api_delete_blog_view,name='delete'),
    path('create/',api_create_blog_view,name='create'),
    path('list',ApiBlogListView.as_view(),name='list'),

]