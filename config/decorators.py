from rest_framework.response import Response

def allowed_users(allowed_roles = set):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            userGroups = dict()
            if request.user.groups.exists():
                [userGroups.update({group.name: True}) for group in request.user.groups.all()]
            
            for role in allowed_roles:
                if userGroups.get(role) and role != "vendor":    
                    return view_func(request, *args, **kwargs)
            
            return Response("You are not authorized to view this page")
        
        return wrapper_func
    
    return decorator        