from rest_framework.throttling import UserRateThrottle



class InteractionThrottle(UserRateThrottle):
    rate = '100/day'