from django_filters import FilterSet, CharFilter
from django.db.models import Q
from .models import Book


class BookFilter(FilterSet):
    """filters for books"""

    # General search term
    search = CharFilter(method='get_search')

    def get_search(self, queryset, name, value):
        """Allow filter by title OR description OR author"""

        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value) | Q(
                authors__full_name__icontains=value)
        )

    class Meta:
        model = Book

        # Enable filter by title
        fields = {'title': ['icontains']}