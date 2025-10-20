from django.urls import path

from .views import NotificationListView, NotificationUnreadCountView, NotificationMarkReadView



urlpatterns = [
    path("notifications/", NotificationListView.as_view(), name="notif_list"),
    path("notifications/unread-count/", NotificationUnreadCountView.as_view(), name="notif_unread"),
    path("notifications/<int:pk>/read/", NotificationMarkReadView.as_view(), name="notif_mark_read"),
]
