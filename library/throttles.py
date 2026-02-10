from rest_framework.throttling import UserRateThrottle

class BorrowRequestThrottle(UserRateThrottle):
    rate = "7/day"  # Limit to 5 borrow requests per day per user
