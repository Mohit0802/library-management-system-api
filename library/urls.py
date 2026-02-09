from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *


urlpatterns = [
    # Auth (JWT)
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # Books
    path("books/", BookListCreateView.as_view(), name="book-list-create"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    
    # Authors & Genres
    path("authors/", AuthorListCreateView.as_view(), name="author-list-create"),
    path("genres/", GenreListCreateView.as_view(), name="genre-list-create"),
    
    # Borrow Requests
    path("borrow/", BorrowRequestCreateView.as_view(), name="borrow-create"),
    path("borrow/list/", BorrowRequestListView.as_view(), name="borrow-list"),
    path("borrow/<int:pk>/approve/", ApproveBorrowRequestView.as_view(), name="borrow-approve"),
    path("borrow/<int:pk>/reject/", RejectBorrowRequestView.as_view(), name="borrow-reject"),
    path("borrow/<int:pk>/return/", ReturnBorrowRequestView.as_view(), name="borrow-return"),
    
    # Reviews
    path("books/<int:pk>/reviews/", BookReviewListView.as_view(), name="book-review-list"),
    path("books/<int:pk>/reviews/add/", BookReviewCreateView.as_view(), name="book-review-create"),
]
