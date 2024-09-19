from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics,status,views,permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import register_serializer,login_serializer,logout_serializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.

    
class register(generics.GenericAPIView):
    serializer_class = register_serializer 
    
    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        validated_user_data = serializer.data  
        return Response(validated_user_data, status=status.HTTP_201_CREATED)
        

class login(generics.GenericAPIView):
    
    serializer_class = login_serializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class logout(generics.GenericAPIView):
    
    serializer_class = logout_serializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
