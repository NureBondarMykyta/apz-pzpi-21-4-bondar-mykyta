from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer, IsAdminOrSelf


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminOrSelf]
        elif self.action == 'create':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super(UsersViewSet, self).get_permissions()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def set_staff(self, request, pk=None):
        user = self.get_object()
        user.is_staff = True
        user.save()
        return Response({'status': 'staff status set'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def set_superuser(self, request, pk=None):
        user = self.get_object()
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return Response({'status': 'superuser status set'}, status=status.HTTP_200_OK)