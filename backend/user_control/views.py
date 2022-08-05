from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import authenticate

from datetime import datetime

from .serializers import CreateUserSerializer, LoginSerializer, UpdatePasswordSerializer, CustomUserSerializer, UserActivitiesSerializer
from .models import CustomUser, UserActivities
from core.utils import get_access_token
from core.custom_method import IsAuthenticatedCustom


def add_user_activity(user, action):
    UserActivities.objects.create(
        user_id=user.id,
        email=user.email,
        fullname=user.fullname,
        action=action
    )
    

class CreateUserView(ModelViewSet):
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (IsAuthenticatedCustom, )
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        CustomUser.objects.create(**serializer.validated_data)
        
        add_user_activity(request.user, "added new user");
        
        return Response({"success": "User created successfully"}, status=status.HTTP_201_CREATED)
    
    
class LoginView(ModelViewSet):
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        new_user = serializer.validated_data["is_new_user"]
        
        if new_user:
            user = CustomUser.objects.filter(
                email=serializer.validated_data["email"]
            )
            if user:
                user = user[0]
                if not user.password:
                    return Response({'user_id': user.id})
                else:
                  raise Exception("User has password already")
            else:
                raise Exception("User with email not found")  
        
        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data.get("password", None)
        )
        
        if not user:
            return Response(
                {"error": "Invalid email or password"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        access = get_access_token({"user_id": user.id}, 1)
        user.last_login = datetime.now()
        user.save()
        
        add_user_activity(user, "logged in");
        
        return Response({"access": access})
    

class UpdatePasswordView(ModelViewSet):
    serializer_class = UpdatePasswordSerializer
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
             
        user = CustomUser.objects.filter(id=serializer.validated_data["user_id"]) 
        
        if not user:
            raise Exception("User with id not found!")
        
        user = user[0]
        user.set_password(serializer.validated_data["password"])  
        user.save()
        
        add_user_activity(request.user, "updated password");
        
        return Response({"success": "User password updated"}) 
    

class MeView(ModelViewSet):
    http_method_names = ["get"]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticatedCustom, )
    
    def list(self, request):
        data = self.serializer_class(request.user)
        return Response(data)
    

class UserActivitiesView(ModelViewSet):
    http_method_names = ["get"]
    serializer_class = UserActivitiesSerializer
    queryset = UserActivities.objects.all()
    permission_classes = (IsAuthenticatedCustom, )
    

class UsersView(ModelViewSet):
    http_method_names = ["get"]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticatedCustom, )
    
    def list(self, request):
        users = self.queryset().filter(is_superuser=False)
        data = self.serializer_class(users, many=True).data
        return Response(data)