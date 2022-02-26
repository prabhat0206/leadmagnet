from rest_framework.response import Response

def allowed_users(allowed_roles = set):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            userGroups = set()
            if request.user.groups.exists():
                [userGroups.add(group.name) for group in request.user.groups.all()]
            
            if userGroups.issubset(allowed_roles) or allowed_roles.issubset(userGroups):
                return view_func(request, *args, **kwargs)
            
            else:
                return Response("You are not authorized to view this page")
        
        return wrapper_func
    
    return decorator        