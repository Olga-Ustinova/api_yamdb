from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .permissions import AuthorModerAdminPermission

from reviews.models import Review
from api.serializers import (CommentSerializer, ReviewSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModerAdminPermission,)

    def get_queryset(self):
        title_id = get_object_or_404(Review, pk=self.kwargs.get("title_id"))
        return title_id.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Review, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorModerAdminPermission,)

    def get_queryset(self):
        review_id = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review_id.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
