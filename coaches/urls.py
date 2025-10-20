from django.urls import path

from .views import (
    BecomeCoachView, MyCoachProfileView, PublicCoachDetailView,
    SessionRequestCreateView, MyIncomingSessionRequestsView,
    MyOutgoingSessionRequestsView, SessionRequestStatusView
)



urlpatterns = [
    # coach profile
    path("coaches/become/", BecomeCoachView.as_view(), name="coach_become"),
    path("coaches/me/", MyCoachProfileView.as_view(), name="coach_me"),
    path("coaches/<int:user_id>/detail/", PublicCoachDetailView.as_view(), name="coach_public_detail"),

    # session requests
    path("coaches/session-requests/send/", SessionRequestCreateView.as_view(), name="session_request_send"),
    path("coaches/session-requests/incoming/", MyIncomingSessionRequestsView.as_view(), name="session_requests_incoming"),
    path("coaches/session-requests/outgoing/", MyOutgoingSessionRequestsView.as_view(), name="session_requests_outgoing"),
    path("coaches/session-requests/<int:pk>/status/", SessionRequestStatusView.as_view(), name="session_request_status"),
]
