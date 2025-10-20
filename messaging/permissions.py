from rest_framework.permissions import BasePermission



class IsParticipant(BasePermission):
    """
    Allow access only if request.user is sender or receiver of the message.
    """
    def has_object_permission(self, request, view, obj):
        return obj.sender_id == request.user.id or obj.receiver_id == request.user.id
