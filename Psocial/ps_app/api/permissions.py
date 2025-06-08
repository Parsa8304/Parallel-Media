from rest_framework import permissions

class IsUniverseMemberOrPublic(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        return obj.persona.universe == request.user.persona.universe