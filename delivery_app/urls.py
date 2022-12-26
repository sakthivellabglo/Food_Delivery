
from django.urls import path,include

from delivery_app import views
from rest_framework .routers import DefaultRouter


router = DefaultRouter()
router.register('users', views.UserList,)
router.register('cart', views.CreateCart,)
router.register('profile', views.UserProfile,basename='user-detail')
router.register('restaurant', views.RestaurantList,basename="Restaurant")
router.register('food', views.FoodList,basename="foods-list")
router.register('manager/newrestaurant', views.CreateRestaurant,)
router.register('manager/foods', views.ManagerFoodCreate,basename="food-list",)
router.register('customer/neworder', views.CreateOrder,)
router.register('cartlist', views.CartList,basename="cartlist-list")
urlpatterns = [

    # rest_framework Authentication
    path('api/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('',include(router.urls)),


    # General API URI
    path("register/", views.Register.as_view(),name="register"),
     path("manager/register/", views.MangerRegister.as_view(),name="MangerRegister"),
    path("login/", views.LoginAPIView.as_view(),name="login"),

    # Managers API URI
    path("manager/activeorders/", views.ManagerActiveOrderList.as_view(),name="mamactive"),
    path("manager/cancelledorders/",views.ManagerCancelledOrderList.as_view(),name="cancelledorders"),
    path("manager/deliveredorders/",views.ManagerDeliveredOrderList.as_view(),name="deliveredorders"),
    path("manager/cancell/<int:pk>/", views.ManagerCancellOrder.as_view(),name="cancell"),
    path("manager/accept/<int:pk>/", views.ManagerAcceptOrder.as_view(),name="accept"),
    path("Admin/Approve/<int:pk>/", views.AdminApproveManager.as_view(),name="accept"),


    # Customers API URI
    path("customer/activeorders/", views.CustomerActiveOrderList.as_view(), name="activeorders"),
    path("customer/cancelledorders/",views.CustomerCancelledOrderList.as_view(),name="cancelledorders"),
    path("customer/deliveredorders/",views.CustomerDeliveredOrderList.as_view(),name="deliveredorders"),
    path("customer/cancell/<int:pk>/", views.CustomerCancellOrder.as_view(),name="CustomerCancellOrder"),
    path("customer/approvedelivered/<int:pk>/",views.CustomerAprroveDeliveredOrder.as_view(),name="CustomerAprroveDeliveredOrder"),
]
