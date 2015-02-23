from django.contrib.gis.tests.relatedapp.models import Location
from haystack.utils.geo import Point, D
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from haystack.query import SearchQuerySet, RelatedSearchQuerySet

from .models import Position, Event, Tag, Coffee, Review

from .serializers import PositionSerializer, EventSerializer, TagSerializer, CoffeeSerializer


class PositionSearchViewSet(ModelViewSet):
    serializer_class = CoffeeSerializer

    def get_queryset(self):

        if self.request.query_params.get('q'):
            latitude = float(self.request.query_params.get('latitude'))
            longitude = float(self.request.query_params.get('longitude'))
            # location = Position.objects.get(latitude=latitude, longitude=longitude)

            # use LONGITUDE, LATITUDE
            location = Point(longitude, latitude)

            # Within a distance
            max_dist = D(km=40)

            search_q = SearchQuerySet().models(Coffee).dwithin('location', location, max_dist).load_all()
            # search_q = SearchQuerySet().dwithin('location', location, max_dist)
            #search_q = SearchQuerySet().all()
            queryset = list(Coffee.objects.filter(id__in=[r.pk for r in search_q]))

            # SORT IT BACK FFS
            queryset.sort(key=lambda t: [int(r.pk) for r in search_q].index(t.pk))

            try:
                order_by = self.request.query_params.get('order_by', None).lower()
                limit = int(self.request.query_params.get('limit', None))
            except Exception:
                order_by = None
                limit = None

            if order_by and order_by == 'desc':
                results = SearchQuerySet().order_by('-created_at')[:limit]
            elif order_by and order_by == 'asc':
                results = SearchQuerySet().order_by('created_at')[:limit]
        else:
            queryset = Coffee.objects.all()

        # Using the new input types...

        # sqs = SearchQuerySet().filter(content=AutoQuery(self.request.GET['q']), product_type=Exact('ancient book'))

        return queryset


class PositionViewSet(ReadOnlyModelViewSet):
    """
    Returns a list of all positions
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class EventViewSet(ModelViewSet):
    """
    Returns a list of all events
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class TagViewSet(ModelViewSet):
    """
    Returns a list of all tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
