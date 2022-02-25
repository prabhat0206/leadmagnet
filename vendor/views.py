from rest_framework import generics
from .serializer import *


class RegisterApi(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer



