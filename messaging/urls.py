from django.urls import path

from .views import SendMessageView, InboxListView, MessageDetailView, ThreadListView, ThreadMessagesView



urlpatterns = [
    path("messages/send/", SendMessageView.as_view(), name="msg_send"),
    path("messages/", InboxListView.as_view(), name="msg_list"),
    path("messages/<int:pk>/", MessageDetailView.as_view(), name="msg_detail"),
    path("threads/", ThreadListView.as_view(), name="chat_threads"),
    path("threads/<int:thread_id>/messages/", ThreadMessagesView.as_view(), name="chat_thread_messages"),    
]
