from django.urls import path
from .views import *

urlpatterns = [
    path('all', AllCallerView.as_view(), name='all_call' ),
    path('today', TodayCalls.as_view(), name='today'),
    path('reception', HandsOverToRecp.as_view(), name='reception'),
    path('add', AddCalls.as_view(), name='add'),
    path('update/<int:id>', UpdateCalls.as_view(), name='update'),
    path('uploadfiles', UploadFiles.as_view(), name='uploadfiles'),
    path('calls_at_counselor', CallsAtCounselor.as_view(), name='call'),
    path('discarded_calls', DiscardedCallsAtRec.as_view(), name='discarded_calls'),
    path('latest_call_at_recp', NewCallsAtRecp.as_view(), name='latest'),
    path('latest_call_at_coun', NeedConc.as_view(), name='latest_call_at_coun'),
    path('registered', RegisteredCalls.as_view(), name='registered'),
    path('calls_at_opt', CallsAtOpterator.as_view(), name='calls_at_opt'),
    path('stats', StatsView.as_view(), name='stats'),
    path('needs_to_follow', NeedsFollowUp.as_view() , name='needs_to_follow')
]

