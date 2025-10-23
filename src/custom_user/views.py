from custom_user.permissions.custom_user_permissions import SuperUserPermission
from rest_framework import viewsets
from custom_user.models import User
from custom_user.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [SuperUserPermission]
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserSerializer

    @action(detail=False, methods=["GET", "PATCH"], permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "PATCH":
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                password = request.data.get("password") or None
                if password:
                    request.user.set_password(password)
                serializer.save(partial=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
