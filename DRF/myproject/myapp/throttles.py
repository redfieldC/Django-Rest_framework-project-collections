from rest_framework.throttling import UserRateThrottle

class CustomUserThrottle(UserRateThrottle):
    scope='custom_user'