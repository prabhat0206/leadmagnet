from rest_framework import generics
from .serializer import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from config.decorators import allowed_users
from django.core.mail import send_mail
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class LoginToken(ObtainAuthToken):

    def post(self, request):
        serialized = self.serializer_class(data=request.data, context={'request': request})
        if serialized.is_valid():
            user = serialized.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            serialized_user = UserSerializer(user).data
            del serialized_user['password']
            return Response({"Success": True, "token": token.key, "user": serialized_user})
        return Response({"Success": False, "Error": "Invalid login credentials"})


@method_decorator(allowed_users(allowed_roles = ["admin"]), name = "post")
class RegisterView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        try:
            exist_user_check = self.get_queryset().filter(email=request.data.get('email')).first()
            if exist_user_check:
                return Response({"error": "Email already in use"})
            new_user = self.serializer_class(data = request.data)

            if new_user.is_valid():
                user = new_user.save()
                permissions = request.data["permissions"]
                for permission in permissions:
                    group = Group.objects.get(name = permission)
                    group.user_set.add(user)
                email_plain_text_message = f"Login Details for Leadmagnet Vendor : {request.data.get('username')}\n\nemail : {request.data.get('email')}\npassword : {request.data.get('password')}"
                send_mail(
                    # title:
                    "Leadmagnet Login Details",
                    # message:
                    email_plain_text_message,
                    # from:
                    "noreplyleadmagnet@sanganastery.live",
                    # to:
                    [request.data.get('email')]
                )
                return Response({"Success": True})
            else:
                return Response({"Success": new_user.is_valid(), "Error": new_user.error})
        except:
            return Response({"Success": False, "msg": "something went wrong, try again"})   


@method_decorator(allowed_users(allowed_roles = ["admin", "vendor", "callcenter", "operations", "reception", "counselor"]), name = "get")
@method_decorator(allowed_users(allowed_roles = ["admin"]), name = "post")
@method_decorator(allowed_users(allowed_roles = ["admin", "vendor", "callcenter", "operations", "reception", "counselor"]), name = "put")
class VendorUser(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, id = None):
        try:
            user = self.get_queryset().filter(id = id).first() if id else request.user
            userData = self.serializer_class(user, many = False).data
            
            permissions = dict()
            [permissions.update({group.name: False}) for group in Group.objects.exclude(name = "admin")]
            for group in userData["groups"]:
                groupName = Group.objects.filter(id = group).first().name
                permissions[groupName] = True
                
            userData["groups"] = permissions    
            return Response({"Success": True, "user": userData})
        except:
            return Response({"Success": False, "msg": f"something went wrong, try again"})    
    

    def put(self, request):
        try:
            data = request.data
            user = request.user
            
            updates = []
            for field in data:
                if field in ["address", "phone", "first_name", "last_name"]:
                    setattr(user, field, data[field])
                    updates.append(field)
                else:
                    return Response({"Success": False, "msg": "not allowed to change these fields"})    
            
            user.save(update_fields = updates)
            return Response({"Success": True, "msg": "user updated"})
        except:
            return Response({"Success": False, "msg": "something went wrong, try again"})    


@method_decorator(allowed_users(allowed_roles = ["admin"]), name = "get")
class GetVendors(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects
    serializer_class = UserSerializer
    
    def get(self, request):
        try:
            data = self.get_queryset().filter(is_superuser=False).order_by("-id")
            serialized = self.serializer_class(data, many = True)
            return Response({"Success": True, "list": serialized.data})
        except:
            return Response({"Success": False, "msg": "something went wrong, try again"})
        