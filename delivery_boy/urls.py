from rest_framework .routers import DefaultRouter
from django.urls import path,include
from delivery_boy.views import FoodList, LoginView, MenuList, OrderList, Register, ResList


router = DefaultRouter()

router.register('register', Register)
router.register('menu', MenuList)
router.register('food', FoodList)
router.register('res', ResList)
router.register('order', OrderList)

urlpatterns = [
    path('',include(router.urls)),
    path('login/', LoginView.as_view(), name = 'login'),]