from django_filters.rest_framework import filters


class IsIndicatedQuizFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)
