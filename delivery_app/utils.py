from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    role = get_role(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user_type': str(role),
    }

def get_role(user):
    if user.profile.is_manager:
        return "manager"
    else:
        return "user"