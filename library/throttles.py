from rest_framework.throttling import UserRateThrottle

class BorrowRequestThrottle(UserRateThrottle):
    rate = "5/day"  # Limit to 5 borrow requests per day per user
