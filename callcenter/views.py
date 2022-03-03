from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializer import *
from .forms import *
from datetime import date
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import  IsAuthenticated
from django.utils.decorators import method_decorator
from config.decorators import allowed_users


class StatsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects.all()
    serializer_class = CallerSerializer

    def get(self, request):
        
        today = date.today()
        vendor = request.user
        today_calls = self.get_queryset().filter(vendor=vendor, datetime__year=today.year, datetime__month=today.month, datetime__day=today.day).order_by('-id')
        calls_at_recp = self.get_queryset().filter(vendor=vendor, at_reception=True)
        calls_at_counselor = self.get_queryset().filter(vendor=vendor, at_counselor=True).order_by("-id")
        discarded_calls = self.get_queryset().filter(vendor=vendor, isCallDiscard=True).order_by('-id')
        new_calls_at_recp = self.get_queryset()\
            .filter(vendor=vendor, isCallDiscard=False, needsToFollow=False, at_reception=True, at_counselor=False, at_operations=False, isRegistered=False, isDocumentMissing=False)
        need_counselling = self.get_queryset()\
            .filter(vendor=vendor, isCallDiscard=False, needsToFollow=False, at_counselor=True, at_operations=False, isRegistered=False, isDocumentMissing=False)
        calls_at_opterator = self.get_queryset().filter(vendor=vendor, at_operations=True)
        registered_calls = self.get_queryset().filter(vendor=vendor, isRegistered=True)
        needs_follow_up = self.get_queryset().filter(vendor=vendor, at_operations=True, isRegistered=False)
        return Response({
            "latest_total": today_calls.count(), 
            "total_calls":self.get_queryset().all().count(), 
            "total_recp": self.get_queryset().filter(at_reception=True).count(),
            "calls_at_counselor": calls_at_counselor.count(),
            "calls_at_recp": calls_at_recp.count(),
            "discarded_calls": discarded_calls.count(),
            "new_calls_at_recp": new_calls_at_recp.count(),
            "calls_at_opterator": calls_at_opterator.count(),
            "registered_calls": registered_calls.count(),
            "need_counselling": need_counselling.count(),
            "needs_follow_up": needs_follow_up.count()
        })


@method_decorator(allowed_users(allowed_roles = ["admin", "vendor", "callcenter"]), name = "get")
class AllCallerView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        call_center = self.get_queryset().filter(vendor=request.user).order_by('-id')
        all_calls = CallerSerializer(call_center, many=True)
        paginated = self.paginate_queryset(all_calls.data)
        return self.get_paginated_response(paginated)


@method_decorator(allowed_users(allowed_roles = ["admin", "vendor", "callcenter"]), name = "get")
class TodayCalls(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        today = date.today()
        today_calls = self.get_queryset().filter(vendor=request.user, datetime__year=today.year, datetime__month=today.month, datetime__day=today.day).order_by('-id')
        today_date = CallerSerializer(today_calls, many=True)
        return Response(today_date.data)


@method_decorator(allowed_users(allowed_roles = ["admin", "vendor", "callcenter", "reception"]), name = "get")
class HandsOverToRecp(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        calls = self.get_queryset().filter(vendor=request.user, at_reception=True).order_by('-id')
        serialized = self.serializer_class(calls, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)


@method_decorator(allowed_users(allowed_roles = ["admin", "vendor", "callcenter"]), name = "post")
class AddCalls(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    parser_classes = (MultiPartParser, FormParser, )

    def post(self, request):
        new_Data = request._request.POST.dict()
        new_Data['vendor'] = request.user.id
        data = CallerForm(new_Data, request._request.FILES)
        if data.is_valid():
            data.save()
            return Response({"Success": True})
        
        return {"Success": False, "Error": "Something went wrong"}


@method_decorator(allowed_users(allowed_roles = ["admin", "vendor"]), name = "update")
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


@method_decorator(allowed_users(allowed_roles = ["admin", "vendor", "counselor", "operations"]), name = "post")
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


@method_decorator(allowed_users(allowed_roles = ["admin", "vendor", "counselor", "reception"]), name = "get")
class CallsAtCounselor(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        data = self.get_queryset().filter(vendor=request.user, at_counselor=True).order_by("-id")
        serialized = self.serializer_class(data, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)


@method_decorator(allowed_users(allowed_roles = ["admin", "vendor", "reception"]), name = "get")
class DiscardedCallsAtRec(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        data = self.get_queryset().filter(vendor=request.user, isCallDiscard=True).order_by('-id')
        serialized = self.serializer_class(data, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)


@method_decorator(allowed_users(allowed_roles = ["admin", "vendor", "reception"]), name = "get")
class NewCallsAtRecp(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        data = self.get_queryset().filter(
            vendor=request.user,
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


@method_decorator(allowed_users(allowed_roles = ["admin", "vendor", "counselor"]), name = "get")
class NeedConc(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        data = self.get_queryset().filter(
            vendor=request.user,
            isCallDiscard=False, 
            needsToFollow=False, 
            at_counselor=True, 
            at_operations=False, 
            isRegistered=False, 
            isDocumentMissing=False
        ).order_by('-id')
        serialized = self.serializer_class(data, many=True)
        return Response(serialized.data)


@method_decorator(allowed_users(allowed_roles = ["admin", "vendor", "operations"]), name = "get")
class RegisteredCalls(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        data = self.get_queryset().filter(vendor=request.user, isRegistered=True).order_by('-id')
        serialized = self.serializer_class(data, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)


@method_decorator(allowed_users(allowed_roles = ["admin", "vendor", "operations", "reception"]), name = "get")
class CallsAtOpterator(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        data = self.get_queryset().filter(vendor=request.user, needsToFollow=True).order_by('-id')
        serialized = self.serializer_class(data, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)


@method_decorator(allowed_users(allowed_roles = ["admin", "vendor", "operations", "reception"]), name = "get")
class NeedsFollowUp(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Caller.objects
    serializer_class = CallerSerializer

    def get(self, request):
        data = self.get_queryset().filter(vendor=request.user, at_operations=True, isRegistered=False).order_by('-id')
        serialized = self.serializer_class(data, many=True)
        paginated = self.paginate_queryset(serialized.data)
        return self.get_paginated_response(paginated)

