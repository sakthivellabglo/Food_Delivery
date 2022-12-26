from ast import FloorDiv
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.db.models import Sum ,F

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.models import Token

from delivery_app.utils import get_tokens_for_user


from .models import Cart, Profile, Restaurant, Food, Order
from .serializers import (
    AdminApproveSerializer,
    CartSerializer,
    ChangePasswordSerializer,
    ManagerSerializer,
    UserSerializer,
    LoginSerializer,
    RestaurantSerializer,
    CreateRestaurantSerializer,
    FoodSerializer,
    PlaceOrderSerializer,
    CancellOrderSerializer,
    ApproveDeliveredOrderSerializer,
    AcceptOrderSerializer,
)
from .permissions import (
    IsUserOrReadonly,
    ManagerPermission,
    HasRestaurant,
    IsFoodOwner,
    CustomerCancellOrderPermission,
    IsCustomerOfOrder,
    CustomerApproveDeliveredOrderPermission,
    IsManagerOfOrder,
    ManagerCancellAcceptOrderPermission,
)


class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        a = request.data
        if 'username' not in a or 'password' not in a:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        username = a['username']
        password = a['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(user)
            return Response({**auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class Register(generics.CreateAPIView):
    """
    Register a new account.
    """
    serializer_class = UserSerializer

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MangerRegister(generics.CreateAPIView):
    """
    Register a new account.
    """
    serializer_class = ManagerSerializer


class UserList(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
        IsUserOrReadonly,
        )
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfile(viewsets.ModelViewSet):
    """
    User profile to be retrieved, updated or destroyed.
    """

    permission_classes = (IsAuthenticated,IsUserOrReadonly)
    serializer_class = UserSerializer
    queryset = User.objects.all()
   
class RestaurantList(viewsets.ReadOnlyModelViewSet):
    """
    List of all restaurants.
    """
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

class FoodList(viewsets.ReadOnlyModelViewSet):
    """
    List of all restaurants.
    """
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
    permission_classes = (IsAuthenticated,)

class CreateRestaurant(viewsets.ModelViewSet):
    """
    Create a restaurant by manager.
    """
    queryset = Restaurant.objects.all()
    serializer_class = CreateRestaurantSerializer
    permission_classes = [
        IsAuthenticated,
        ManagerPermission,
    ]
    http_method_names = [ 'post']
    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)


class ManagerFoodCreate(viewsets.ModelViewSet):
    """
    Create food for restaurant by manager and update the old foods
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = (
       IsAuthenticated,
          ManagerPermission,
          HasRestaurant,
        )
    def get_queryset(self):
        restaurant = Restaurant.objects.filter(manager=self.request.user.id).first()
        return Food.objects.filter(restaurant=restaurant)

    def perform_create(self, serializer):
        restaurant = Restaurant.objects.filter(manager=self.request.user.id).first()
        serializer.save(restaurant=restaurant)

class CreateCart(viewsets.ModelViewSet):
    """
    Add to Cart.
    """

    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    def perform_create(self, serializer):
        food_price = Food.objects.filter(id=self.request.data["food"]).aggregate(
            total=Sum(F('price')))['total']*int(self.request.data["quantity"])
        serializer.save(customer=self.request.user,price = food_price)
        
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        instance = self.get_object()
        f_price = Food.objects.get(id = instance.food.id).price
        price=int(f_price) * int(instance.quantity)
        instance.price =price
        instance.save()
        return Response(CartSerializer(instance).data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(customer=request.user)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CreateOrder(viewsets.ModelViewSet):
    """
    Place an Order.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    http_method_names = ["post"]
    def perform_create(self, serializer):
        ids =dict(self.request.data)
        food_price = Cart.objects.filter(id__in=ids["cart"]).aggregate(Sum("price"))['price__sum']
        serializer.save(customer=self.request.user,total_price = food_price)



class CustomerActiveOrderList(generics.ListAPIView):
    """
    List of all active orders which are not cancelled or delivered.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(
            customer=self.request.user.id, is_delivered=False ,is_cancelled =False
        )
        


class CustomerCancelledOrderList(generics.ListAPIView):
    """
    List of customer's cancelled orders.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.id, is_cancelled=True)


class CustomerDeliveredOrderList(generics.ListAPIView):
    """
    List of customer's delivered orders.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.id, is_delivered=True)


class CustomerCancellOrder(generics.UpdateAPIView):
    """
    Cancell order if has permission to.
    """

    serializer_class = CancellOrderSerializer
    permission_classes = (
        IsAuthenticated,
        IsCustomerOfOrder,
        CustomerCancellOrderPermission,
    )
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        serializer.save(cancell_datetime=timezone.now())


class CustomerAprroveDeliveredOrder(generics.UpdateAPIView):
    """
    Aprrove that order has been delivered.
    """

    serializer_class = ApproveDeliveredOrderSerializer
    permission_classes = (
        IsAuthenticated,
        IsCustomerOfOrder,
        CustomerApproveDeliveredOrderPermission,
    )
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        serializer.save(delivered_datetime=timezone.now())


class ManagerActiveOrderList(generics.ListAPIView):
    """
    List of manager's restaurant active orders.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (
        IsAuthenticated,
        ManagerPermission,
        HasRestaurant,
    )

    def get_queryset(self):
        restaurant = Restaurant.objects.filter(manager=self.request.user.id).first()
        cart = Cart.objects.filter(food__restaurant=restaurant).values_list("id")
        orders = Order.objects.filter(
            cart__in=cart, is_delivered=False
        )
        return orders


class ManagerCancelledOrderList(generics.ListAPIView):
    """
    List of manager's restaurant cancelled orders.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (
        IsAuthenticated,
        ManagerPermission,
        HasRestaurant,
    )

    def get_queryset(self):
        restaurant = Restaurant.objects.filter(manager=self.request.user.id).first()
        foods = Cart.objects.filter(food__restaurant=restaurant.id).values_list("id")
        orders = Order.objects.filter(
            cart__in=foods, is_cancelled=False
        )
        return orders


class ManagerDeliveredOrderList(generics.ListAPIView):
    """
    List of manager's restaurant delivered orders.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (
        IsAuthenticated,
        ManagerPermission,
        HasRestaurant,
    )

    def get_queryset(self):
        restaurant = Restaurant.objects.filter(manager=self.request.user.id).first()
        foods = Cart.objects.filter(food__restaurant=restaurant.id).values_list("id")
        print(foods)
        orders = Order.objects.filter(
            cart__in=foods, is_delivered=True
        )
        return orders

class CartList(viewsets.ModelViewSet):
    """
    Add to Cart.
    """

    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    


class ManagerCancellOrder(generics.UpdateAPIView):
    """
    Cancell order if has permission to.
    """

    serializer_class = CancellOrderSerializer
    permission_classes = (
        IsAuthenticated,
        IsManagerOfOrder,
        ManagerCancellAcceptOrderPermission,
    )
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        serializer.save(cancell_datetime=timezone.now())


class ManagerAcceptOrder(generics.UpdateAPIView):
    """
    Accept order if has permission to.
    """

    serializer_class = AcceptOrderSerializer
    permission_classes = (
        IsAuthenticated,
        IsManagerOfOrder,
        ManagerCancellAcceptOrderPermission,
    )
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        serializer.save(accept_datetime=timezone.now())

class AdminApproveManager(generics.UpdateAPIView):
    """
    Accept  Manager if has permission to.
    """

    serializer_class = AdminApproveSerializer
    permission_classes = (
        IsAdminUser,
    )
    queryset = Profile.objects.all()

