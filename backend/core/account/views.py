from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions
from django.contrib.auth.models import User 
from .serializers import ResgisterSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie
class RegisterView(APIView):
    
    def post(self,request):
        data = request.data 
        serializer = ResgisterSerializer(data=data)
        if serializer.is_valid():
            user= serializer.save()
            return Response({
                "message":"user is created successfully",
                "status":True,
                "data":serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self,request):
        data = request.data 
        print(data)
        username=data.get('username')
        password=data.get('password')
        user= User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh =RefreshToken.for_user(user)
            return Response({"access_token":str(refresh.access_token),
                             "Refresh_token":str(refresh)})
        return Response({"message":"Invaild credentials"},status=status.HTTP_400_BAD_REQUEST)
    

class ProfileView(APIView):
    permission_classes=[IsAuthenticated]
    @method_decorator(cache_page(3))
    @method_decorator(vary_on_cookie)
    def get(self,request):
        user = request.user 
        serialiers= ResgisterSerializer(user) 
        return Response(serialiers.data)