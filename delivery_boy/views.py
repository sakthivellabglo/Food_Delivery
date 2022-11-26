from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Sum


from delivery_boy.models import FoodItem, Menu, Order, Restaurant
from delivery_boy.serializers import CreateuserSerializers, Foodserializer, Loginserializer, Menuserializer, Orderserializer, Resserializer

class Register(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = CreateuserSerializers

    
class LoginView(generics.GenericAPIView):
    serializer_class = Loginserializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'})
        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid Credentials'})
        login(request, user)
        token, li = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    
class MenuList(viewsets.ModelViewSet):
     queryset = Menu.objects.all()
     serializer_class = Menuserializer

class FoodList(viewsets.ModelViewSet):
     queryset = FoodItem.objects.all()
     serializer_class = Foodserializer

class ResList(viewsets.ModelViewSet):
     queryset = Restaurant.objects.all()
     serializer_class = Resserializer

class OrderList(viewsets.ModelViewSet):
     queryset = Order.objects.all()
     serializer_class = Orderserializer

     def perform_create(self, serializer):
        print("it's work")
        print(self.request.data['order_item'])
        price = FoodItem.objects.filter(id=self.request.data['order_item']).aggregate(Sum('price'))['price__sum']
        print(price)
        quvantity=int(self.request.data['quantity'])
        price =int(price)*quvantity
        serializer.save(user=self.request.user,price = price)

     def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)
        print("queryset of list", queryset)
        page = self.paginate_queryset(queryset)
        print("return the iteralble queryset", page)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)