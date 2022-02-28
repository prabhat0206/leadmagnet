from rest_framework import generics
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from config.decorators import allowed_users

@method_decorator(allowed_users(allowed_roles = {"admin"}), name = "post")
class RegisterView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        exist_user_check = self.get_queryset().filter(email=request.data.get('email')).first()
        if exist_user_check:
            return Response({"error": "Email already in use"})
        new_user = self.serializer_class(data = request.data)
        
        if new_user.is_valid():
            user = new_user.save()
            group = Group.objects.filter(name = "vendor").first()
            group.user_set.add(user)
            return Response({"success": True})
        else:
            return Response({"success": new_user.is_valid()})

@method_decorator(allowed_users(allowed_roles = {"admin"}), name = "post")
class AddPermissions(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        try:
            data = request.data
            current_user = self.get_queryset().get(id = data["id"])
            permissions = data["permissions"]

            for permission in permissions:
                group = Group.objects.get(name = permission)
                group.user_set.add(current_user)    
            
            return Response({"success": True, "msg": "permissions updated"})    
        except:
            return Response({"success": False, "msg": "something went wrong, try again"})

 
# TODO: VENDOR DETAILS API