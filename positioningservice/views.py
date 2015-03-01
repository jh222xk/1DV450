from django.contrib.auth.models import User

from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet
from rest_framework.decorators import detail_route, list_route

from .models import Position, Tag, Coffee, Review
from .authentications import SafeTokenAuthentication, UnsafeJSONWebTokenAuthentication, IsOwner, IsLoggedInAs, \
    SafeTokenUserCreationAuthentication
from .indexes import SearchIndex
from .serializers import PositionSerializer, TagSerializer, CoffeeSerializer, UserSerializer, \
    ReviewSerializer, NestedReviewSerializer


class CoffeeViewSet(ReadOnlyModelViewSet):
    serializer_class = CoffeeSerializer
    authentication_classes = (SafeTokenAuthentication, UnsafeJSONWebTokenAuthentication)

    def get_queryset(self):
        index = 'toerh_coffee'
        es = SearchIndex(model=Coffee)

        try:
            pk = self.kwargs['pk']
        except KeyError:
            pk = None
        if pk is None:
            try:
                latitude = float(self.request.query_params.get('latitude'))
                longitude = float(self.request.query_params.get('longitude'))
            except TypeError:
                longitude = None
                latitude = None

            query = self.request.query_params.get('query', "")

            # Call on our elasticsearch's search
            results = es.search(index=index, question=query, longitude=longitude, latitude=latitude, size=50)

            hits = results['hits']['hits']

            # Query the database after the search result
            queryset = list(Coffee.objects.filter(pk__in=[r['_source']['pk'] for r in hits]))

            # SORT IT
            queryset.sort(key=lambda t: [int(r['_source']['pk']) for r in hits].index(t.pk))

            return queryset
        else:
            coffee = Coffee.objects.filter(pk=pk)
            return coffee


class PositionViewSet(ReadOnlyModelViewSet):
    """
    Returns a list of all positions
    """
    authentication_classes = (SafeTokenAuthentication, UnsafeJSONWebTokenAuthentication)
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ('address', 'created_at',)


class TagViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwner)
    authentication_classes = (SafeTokenAuthentication, UnsafeJSONWebTokenAuthentication)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ('name', 'created_at')

    @detail_route()
    def coffeehouses(self, request, pk):
        queryset = Coffee.objects.filter(tags__pk=pk)

        serializer = CoffeeSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserViewSet(CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    authentication_classes = (
        SafeTokenAuthentication, SafeTokenUserCreationAuthentication, UnsafeJSONWebTokenAuthentication
    )
    permission_classes = (IsLoggedInAs,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ('username', 'email', 'date_joined', 'last_login', 'is_active')

    @detail_route()
    def reviews(self, request, pk):
        reviews = Review.objects.filter(user=pk)

        serializer = NestedReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)

    @list_route()
    def active(self, request):
        users = User.objects.filter(is_active=True)

        serializer = UserSerializer(users, many=True, context={'request': request})

        return Response(serializer.data)

    @list_route()
    def un_active(self, request):
        users = User.objects.filter(is_active=False)

        serializer = UserSerializer(users, many=True, context={'request': request})

        return Response(serializer.data)


class ReviewViewSet(ModelViewSet):
    """
    Returns a list of all events
    """
    authentication_classes = (SafeTokenAuthentication, UnsafeJSONWebTokenAuthentication)
    permission_classes = (IsOwner,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ('rating', 'description', 'coffee', 'created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)