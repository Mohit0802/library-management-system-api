from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import BorrowRequest, Book


@receiver(post_save, sender=BorrowRequest)
def update_book_copies(sender, instance, created, **kwargs):
    book = instance.book

    # Auto decrement on approval
    if instance.status == BorrowRequest.Status.APPROVED:
        if book.available_copies > 0:
            book.available_copies -= 1
            book.save()

    # Auto increment on return
    if instance.status == BorrowRequest.Status.RETURNED:
        book.available_copies += 1
        book.save()
