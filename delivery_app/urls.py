
from django.urls import path,include

from delivery_app import views
from rest_framework .routers import DefaultRouter


router = DefaultRouter()
router.register('users', views.UserList,)
router.register('profile', views.UserProfile,basename='user-detail')
router.register('restaurant', views.RestaurantList,basename="Restaurant")
router.register('manager/newrestaurant', views.CreateRestaurant,)
router.register('manager/foods', views.ManagerFoodListCreate,)
router.register('manager/updatefood', views.UpdateFood,)
router.register('customer/neworder/', views.CreateOrder,)
urlpatterns = [
    # rest_framework Authentication
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('',include(router.urls)),
    # General API URI
    path("register/", views.Register.as_view()),
    path("login/", views.api_login.as_view()),
    # Managers API URI
    path("manager/activeorders/", views.ManagerActiveOrderList.as_view()),
    path("manager/cancelledorders/",views.ManagerCancelledOrderList.as_view(),),
    path("manager/deliveredorders/",views.ManagerDeliveredOrderList.as_view(),),
    path("manager/cancell/<int:id>/", views.ManagerCancellOrder.as_view()),
    path("manager/accept/<int:id>/", views.ManagerAcceptOrder.as_view()),
    # Customers API URI
    path("customer/activeorders/", views.CustomerActiveOrderList.as_view()),
    path("customer/cancelledorders/",views.CustomerCancelledOrderList.as_view(),),
    path("customer/deliveredorders/",views.CustomerDeliveredOrderList.as_view(),),
    path("customer/cancell/<int:id>/", views.CustomerCancellOrder.as_view()),
    path("customer/approvedelivered/<int:id>/",views.CustomerAprroveDeliveredOrder.as_view(),),
]