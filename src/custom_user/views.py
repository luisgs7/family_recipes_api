from rest_framework import viewsets
from custom_user.models import User
from custom_user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserSerializer
