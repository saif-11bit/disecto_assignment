from rest_framework.permissions import BasePermission
from authentication.models import Visitor, Consultant

class OnlyVisitor(BasePermission):
    def has_permission(self, request, view):
        is_visitor = Visitor.objects.filter(user_id=request.user.id).first()
        return True if is_visitor else False


class OnlyConsultant(BasePermission):
    def has_permission(self, request, view):
        is_consultant = Consultant.objects.filter(user_id=request.user.id).first()
        return True if is_consultant else False
    