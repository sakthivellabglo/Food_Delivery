from rest_framework import permissions

from .models import Profile, Restaurant, Food, Order


class IsUserOrReadonly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        print(obj)

        return obj == request.user


class ManagerPermission(permissions.BasePermission):
    """
    Check if the user is a restaurant manager.
    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user.profile.is_manager and bool(Profile.objects.filter(is_manager = 'True',is_approved = 'A'))


class HasRestaurant(permissions.BasePermission):
    """
    Check if the manager has created a restaurant to manage.
    """

    message = "You should create a restaurant first to be able to access it's foods"

    def has_permission(self, request, view):
        return bool(Restaurant.objects.get(manager=request.user.id ))


class IsFoodOwner(permissions.BasePermission):
    """
    Check if the manager is the owner of the food which wants to edit.
    """

    message = "You are not the owner of this food restaurant"

    def has_permission(self, request, view):
        food = Food.objects.get(id=view.kwargs.get("pk", None))
        if food is None:
            return False
        return (
            Restaurant.objects.get(manager=request.user.id)
            == food.restaurant
        )


class CustomerCancellOrderPermission(permissions.BasePermission):
    """
    Check if the customer has the permission to cancell the order.
    """

    message = (
        "You don't have permission to cancell this order."
    )

    def has_permission(self, request, view):
        order = Order.objects.get(id=view.kwargs.get("pk", None))
        if order is None:
            return False
        return not order.is_cancelled


class IsCustomerOfOrder(permissions.BasePermission):
    """
    Check if the customer is the owner of order.
    """
    message = "You can't cancell this order because you are not it's owner."

    def has_permission(self, request, view):
        order = Order.objects.filter(customer=request.user.id).first()
        return order is not None


class CustomerApproveDeliveredOrderPermission(permissions.BasePermission):
    """
    Check if the customer has permission to aprrove the delivered order.
    """

    message = "You can not approve this order as delivered."

    def has_permission(self, request, view):
        order = Order.objects.get(id=view.kwargs.get("pk", None))
        if order is None:
            return False
        return order.is_accepted and not order.is_cancelled and not order.is_delivered


class IsManagerOfOrder(permissions.BasePermission):
    """
    Check if the manager is the owner of order.
    """

    message = "You are not the manager of this order."

    def has_permission(self, request, view):

        order = Order.objects.get(id=view.kwargs.get("pk", None))
        
        if order is None:
            return False
        food = order.cart.first()
        
        if order is None or food is None:
            return False
        
        return food.food.restaurant.manager.id == request.user.id


class ManagerCancellAcceptOrderPermission(permissions.BasePermission):
    """
    Check if the manager has permission to cancell the order.
    """

    message = "You don't have permission to cancell this order."

    def has_permission(self, request, view):
        order = Order.objects.get(id=view.kwargs.get("pk", None))
        if order is None:
            return False
        return not order.is_cancelled and not order.is_accepted