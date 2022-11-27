
from django.urls import path,include

from delivery_app import views
from rest_framework .routers import DefaultRouter


router = DefaultRouter()
router.register('users', views.UserList,)
router.register('profile', views.UserProfile,basename='user-detail')
urlpatterns = [
    # rest_framework Authentication
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('',include(router.urls)),
    # General API URI
    path("register/", views.Register.as_view()),
    path("login/", views.api_login.as_view()),
    path("restaurants/", views.RestaurantList.as_view()),
    # Managers API URI
    path("manager/newrestaurant/", views.CreateRestaurant.as_view()),
    path("manager/foods/", views.ManagerFoodListCreate.as_view()),
    path("manager/updatefood/<int:pk>/", views.UpdateFood.as_view()),
    path("manager/activeorders/", views.ManagerActiveOrderList.as_view()),
    path("manager/cancelledorders/",views.ManagerCancelledOrderList.as_view(),),
    path("manager/deliveredorders/",views.ManagerDeliveredOrderList.as_view(),),
    path("manager/cancell/<int:pk>/", views.ManagerCancellOrder.as_view()),
    path("manager/accept/<int:pk>/", views.ManagerAcceptOrder.as_view()),
    # Customers API URI
    path("customer/neworder/", views.CreateOrder.as_view()),
    path("customer/activeorders/", views.CustomerActiveOrderList.as_view()),
    path("customer/cancelledorders/",views.CustomerCancelledOrderList.as_view(),),
    path("customer/deliveredorders/",views.CustomerDeliveredOrderList.as_view(),),
    path("customer/cancell/<int:pk>/", views.CustomerCancellOrder.as_view()),
    path("customer/approvedelivered/<int:pk>/",views.CustomerAprroveDeliveredOrder.as_view(),),
]
