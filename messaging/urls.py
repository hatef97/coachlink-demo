from django.urls import path

from .views import SendMessageView, InboxListView, MessageDetailView



urlpatterns = [
    path("messages/send/", SendMessageView.as_view(), name="msg_send"),
    path("messages/", InboxListView.as_view(), name="msg_list"),
    path("messages/<int:pk>/", MessageDetailView.as_view(), name="msg_detail"),
]
