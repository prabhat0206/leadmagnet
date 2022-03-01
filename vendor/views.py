from rest_framework import generics
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from config.decorators import allowed_users
from django.core.mail import send_mail
import os

@method_decorator(allowed_users(allowed_roles = ["admin"]), name = "post")
class RegisterView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        try:
            print(request.data)
            exist_user_check = self.get_queryset().filter(email=request.data.get('email')).first()
            if exist_user_check:
                return Response({"error": "Email already in use"})
            new_user = self.serializer_class(data = request.data)

            if new_user.is_valid():
                user = new_user.save()
                group = Group.objects.filter(name = "vendor").first()
                group.user_set.add(user)

                email_plaintext_message = f"Login Details for Leadmagnet Vendor : {request.data.get('username')}\n\nemail : {request.data.get('email')}\npassword : {request.data.get('password')}"

                send_mail(
                    # title:
                    "Leadmagnet Login Details",
                    # message:
                    email_plaintext_message,
                    # from:
                    os.environ.get("EMAIL"),
                    # to:
                    [request.data.get('email')]
                )
                return Response({"success": True})
            else:
                return Response({"success": new_user.is_valid()})
        except:
            return Response({"success": False, "msg": "something went wrong, try again"})    
@method_decorator(allowed_users(allowed_roles = ["admin", "vendor", "callcenter", "operations", "reception", "counselor"]), name = "get")
@method_decorator(allowed_users(allowed_roles = ["admin"]), name = "post")
@method_decorator(allowed_users(allowed_roles = ["vendor", "callcenter", "operations", "reception", "counselor"]), name = "put")
class VendorUser(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, id):
        try:
            user = self.get_queryset().filter(id = id).first()
            userData = self.serializer_class(user, many = False).data
            
            permissions = dict()
            [permissions.update({group.name: False}) for group in Group.objects.exclude(name = "admin")]
            for group in userData["groups"]:
                groupName = Group.objects.filter(id = group).first().name
                permissions[groupName] = True
                
            userData["groups"] = permissions    
            return Response({"success": True, "user": userData})
        except:
            return Response({"success": False, "msg": f"something went wrong, try again"})    
    
    def post(self, request, id):
        try:
            data = request.data
            current_user = self.get_queryset().get(id = id)
            permissions = data["permissions"]

            for permission in permissions:
                group = Group.objects.get(name = permission)
                group.user_set.add(current_user)    
            
            return Response({"success": True, "msg": "permissions updated"})    
        except:
            return Response({"success": False, "msg": "something went wrong, try again"})

    def put(self, request, id):
        try:
            data = request.data
            user = self.get_queryset().filter(id = id).first()
            
            updates = []
            for field in data:
                if field in ["address", "phone", "first_name", "last_name"]:
                    setattr(user, field, data[field])
                    updates.append(field)
                else:
                    return Response({"success": False, "msg": "not allowed to change these fields"})    
            
            user.save(update_fields = updates)
            return Response({"success": True, "msg": "user updated"})
        except:
            return Response({"success": False, "msg": "something went wrong, try again"})    

@method_decorator(allowed_users(allowed_roles = ["admin"]), name = "get")
class GetVendors(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects
    serializer_class = UserSerializer
    
    def get(self, request):
        try:
            data = self.get_queryset().filter(groups__name = "vendor").order_by("-id")
            serialized = self.serializer_class(data, many = True)
            return Response({"sucess": True, "list": serialized.data})
        except:
            return Response({"success": False, "msg": "something went wrong, try again"})
        