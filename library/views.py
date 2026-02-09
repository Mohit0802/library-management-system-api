from time import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Author, Genre, Book, BorrowRequest, BookReview
from .serializers import RegisterSerializer, AuthorSerializer, GenreSerializer, BookSerializer, BookCreateSerializer, BorrowRequestSerializer, BookReviewSerializer
from .permissions import IsLibrarian, IsStudent

# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    filterset_fields = ["author", "genres"]
    search_fields = ["title"]
    ordering_fields = ["title", "available_copies", "total_copies"]

    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookCreateSerializer
        return BookSerializer
    
    def perform_create(self, serializer):
        if self.request.user.role != User.Roles.LIBRARIAN:
            return Response({"detail": "Only librarians can add books"}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
    

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return BookCreateSerializer
        return BookSerializer
    
    def perform_update(self, serializer):
        if self.request.user.role != User.Roles.LIBRARIAN:
            raise PermissionError("Only librarians can edit books")
        serializer.save()
    
    def perform_destroy(self, instance):
        if self.request.user.role != User.Roles.LIBRARIAN:
            raise PermissionError("Only librarians can delete books")
        instance.delete()


class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != User.Roles.LIBRARIAN:
            return Response({"detail": "Only librarians can create authors"}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()


class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != User.Roles.LIBRARIAN:
            return Response({"detail": "Only librarians can create genres"}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()


class BorrowRequestCreateView(generics.CreateAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BorrowRequestListView(generics.ListAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BorrowRequest.objects.filter(user=self.request.user)


class ApproveBorrowRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsLibrarian]

    def patch(self, request, pk):
        try:
            req = BorrowRequest.objects.get(id=pk)
        except BorrowRequest.DoesNotExist:
            return Response({"detail": "Request not found"}, status=status.HTTP_404_NOT_FOUND)

        req.status = BorrowRequest.Status.APPROVED
        req.approved_at = timezone.now()
        req.save()
        return Response({"message": "Borrow request approved"})

class RejectBorrowRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsLibrarian]
    
    def patch(self, request, pk):
        try:
            req = BorrowRequest.objects.get(id=pk)
        except BorrowRequest.DoesNotExist:
            return Response({"detail": "Request not found"}, status=status.HTTP_404_NOT_FOUND)

        req.status = BorrowRequest.Status.REJECTED
        req.save()
        return Response({"message": "Borrow request rejected"})


class ReturnBorrowRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsLibrarian]
    
    def patch(self, request, pk):
        try:
            req = BorrowRequest.objects.get(id=pk)
        except BorrowRequest.DoesNotExist:
            return Response({"detail": "Request not found"}, status=status.HTTP_404_NOT_FOUND)

        req.status = BorrowRequest.Status.RETURNED
        req.returned_at = timezone.now()
        req.save()
        return Response({"message": "Book returned"})


class BookReviewCreateView(generics.CreateAPIView):
    serializer_class = BookReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
            serializer.save(
                user=self.request.user,
                book_id=self.kwargs["pk"]
            )

class BookReviewListView(generics.ListAPIView):
    serializer_class = BookReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BookReview.objects.filter(book_id=self.kwargs["pk"])