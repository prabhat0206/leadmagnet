from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializer import *
from .forms import *
from datetime import date
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.decorators import method_decorator
from config.decorators import allowed_users



@method_decorator(allowed_users(allowed_roles = ["vendor", "callcenter"]), name = "get")
class AllCallerView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        call_center = self.get_queryset().order_by('-id')
        all_calls = CallerSerializer(call_center, many=True)
        paginated = self.paginate_queryset(all_calls.data)
        return self.get_paginated_response(paginated)

@method_decorator(allowed_users(allowed_roles = ["vendor", "callcenter"]), name = "get")
class TodayCalls(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        today = date.today()
        today_calls = self.get_queryset().filter(datetime__year=today.year, datetime__month=today.month, datetime__day=today.day).order_by('-id')
        today_date = CallerSerializer(today_calls, many=True)
        return Response(today_date.data)

@method_decorator(allowed_users(allowed_roles = ["vendor", "callcenter", "reception"]), name = "get")
class HandsOverToRecp(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        calls = self.get_queryset().filter(at_reception=True).order_by('-id')
        serialized = self.serializer_class(calls, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)

@method_decorator(allowed_users(allowed_roles = ["vendor", "callcenter"]), name = "post")
class AddCalls(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    parser_classes = (MultiPartParser, FormParser, )

    def post(self, request):
        data = CallerForm(request._request.POST, request._request.FILES)
        if data.is_valid():
            data.save()
            return Response({"Success": True})
        
        return {"Success": False, "Error": str(data.errors)}

@method_decorator(allowed_users(allowed_roles = ["vendor"]), name = "update")
class UpdateCalls(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def update(self, request, id):
        instance = self.get_queryset().get(id=id)
        data_for_change = request.data
        serialized = self.serializer_class(instance, data=data_for_change, partial=True)
        if serialized.is_valid():
            self.perform_update(serialized)
            return Response({"Success": True, "data": serialized.data})
        return Response({"Success": False, "Errors": str(serialized.errors)})

@method_decorator(allowed_users(allowed_roles = ["vendor", "councelor", "operations"]), name = "post")
class UploadFiles(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Uploades.objects
    parser_classes = (MultiPartParser, FormParser, )

    def post(self, request):
        data = UploadForm(request._request.POST, request._request.FILES)
        if data.is_valid():
            data.save()
            return Response({"Success": True})
        return Response({"Success": False, "Error": str(data.errors)})

@method_decorator(allowed_users(allowed_roles = ["vendor", "councelor", "reception"]), name = "get")
class CallsAtCounselor(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        data = self.get_queryset().filter(at_counselor=True).order_by("-id")
        serialized = self.serializer_class(data, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)

@method_decorator(allowed_users(allowed_roles = ["vendor", "reception"]), name = "get")
class DiscardedCallsAtRec(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        data = self.get_queryset().filter(isCallDiscard=True).order_by('-id')
        serialized = self.serializer_class(data, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)

@method_decorator(allowed_users(allowed_roles = ["vendor", "reception"]), name = "get")
class NewCallsAtRecp(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        data = self.get_queryset().filter(
            isCallDiscard=False, 
            needsToFollow=False,
            at_reception=True, 
            at_counselor=False, 
            at_operations=False, 
            isRegistered=False, 
            isDocumentMissing=False
        ).order_by('-id')
        serialized = self.serializer_class(data, many=True)
        return Response(serialized.data)

@method_decorator(allowed_users(allowed_roles = ["vendor", "councelor"]), name = "get")
class NeedConc(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        data = self.get_queryset().filter(
            isCallDiscard=False, 
            needsToFollow=False, 
            at_counselor=True, 
            at_operations=False, 
            isRegistered=False, 
            isDocumentMissing=False
        ).order_by('-id')
        serialized = self.serializer_class(data, many=True)
        return Response(serialized.data)

@method_decorator(allowed_users(allowed_roles = ["vendor", "operations"]), name = "get")
class RegisteredCalls(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        data = self.get_queryset().filter(isRegistered=True).order_by('-id')
        serialized = self.serializer_class(data, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)

@method_decorator(allowed_users(allowed_roles = ["vendor", "operations", "reception"]), name = "get")
class CallsAtOpterator(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        data = self.get_queryset().filter(at_operations=True).order_by('-id')
        serialized = self.serializer_class(data, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)
