from django.urls import path, re_path
from bboard.views import (
    index, by_rubric, BbCreateView,
    select_columns, exclude_values,
    bb_list, bb_detail, bb_delete,
    UserListView, UserDetailView
)

urlpatterns = [
    path('', index, name='index'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('select_columns/', select_columns, name='select_columns'),
    path('exclude_values/', exclude_values, name='exclude_values'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),

    path('bbs/', bb_list, name='bb_list'),
    path('bb/<int:id>/', bb_detail, name='bb_detail'),
    path('bb/<int:id>/delete/', bb_delete, name='bb_delete'),

    path('users/', UserListView.as_view(), name='users_list'),
    path('user/', UserDetailView.as_view(), name='user_detail'),

    re_path(r'^rubric/(?P<rubric_id>\d+)/$', by_rubric, name='rubric_regex'),
    re_path(r'^bb/(?P<id>\d+)/$', bb_detail, name='bb_detail_regex'),
    re_path(r'^bb/(?P<id>\d+)/delete/$', bb_delete, name='bb_delete_regex'),
]