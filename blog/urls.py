from django.urls import path

from blog.views import (
    post_list_view, post_detail_view,
    PostListView, post_share_view,
)

app_name = 'blog'

urlpatterns = [
    # path('', post_list_view, name='list'),
    path('', PostListView.as_view(), name='list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail_view, name='detail'),
    path('<int:post_id>/share/', post_share_view, name='share'),
]
