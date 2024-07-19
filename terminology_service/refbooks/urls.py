from django.urls import path
from .views import RefbookListView, RefbookElementListView, CheckElementView

urlpatterns = [
    path('refbooks/', RefbookListView.as_view(), name='refbook-list'),
    path('refbooks/<int:id>/elements/', RefbookElementListView.as_view(), name='refbook-element-list'),
    path('refbooks/<int:id>/check_element/', CheckElementView.as_view(), name='refbook-check-element'),
]
