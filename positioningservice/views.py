from django.contrib.auth.models import User

from pyelasticsearch import ElasticSearch, ElasticHttpNotFoundError
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import detail_route

from .models import Position, Tag, Coffee, Review
from .authentications import SafeTokenAuthentication, UnsafeJSONWebTokenAuthentication, IsOwner

from .serializers import PositionSerializer, TagSerializer, CoffeeSerializer, UserSerializer, \
    ReviewSerializer, NestedReviewSerializer, ReviewCoffee


class CoffeeViewSet(ModelViewSet):
    serializer_class = CoffeeSerializer
    authentication_classes = (SafeTokenAuthentication, UnsafeJSONWebTokenAuthentication)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('name', 'address', 'created_at')


    def search(self, question, longitude, latitude):
        index = 'toerh_coffee'
        es = ElasticSearch()
        try:
            es.delete_index(index)
        except (AttributeError, ElasticHttpNotFoundError):
            pass

        mapping = {
            "place": {
                "properties": {
                    "location": {
                        "type": "geo_point",
                        #"lat_lon": True
                    },
                }
            }
        }

        es.create_index(index)
        es.put_mapping(index, "place", mapping)
        for c in Coffee.objects.all():
            es.bulk([
                    es.index_op({
                        'pk': c.pk,
                        'name': c.name,
                        'rating': c.rating,
                        'location': {
                            'lon': c.position.longitude,
                            'lat': c.position.latitude
                        }
                    }),
                    ],
                    doc_type='place',
                    index=index)

        query = {
            'query': {
                'function_score': {
                    'query': {
                        'bool': {
                            'should': [
                                {'match': {'name': question}},
                                {'match': {'_all': {
                                    'query': question,
                                    'operator': 'or',
                                    'fuzziness': 'auto',
                                    'zero_terms_query': 'all'
                                }}}
                            ]
                        }
                    },
                    'functions': [
                        {'exp': {'rating': {'origin': 5, 'scale': 1, 'offset': 0.1}}},
                    ]
                }
            }
        }

        if longitude and longitude is not None:
            query['query']['function_score']['functions'] = [
                #{'exp': {'rating': {'origin': 5, 'scale': 1, 'offset': 0.1}}},
                #{'gauss': {'location': {'origin': 'location', 'scale': '250m', 'offset': '50m'}}},
                {'gauss': {
                        "location": {"origin": {"lat": latitude, "lon": longitude}, "offset": "50m",
                                     "scale": "250m"}
                        }},
                {'gauss': {
                        "location": {"origin": {"lat": latitude, "lon": longitude}, "offset": "50m",
                                     "scale": "500m"}
                        },
                },
                ]

        # print(query)

        es.refresh()

        results = es.search(query, index=index)

        return results

    def get_queryset(self):
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

            # use LONGITUDE, LATITUDE
            results = self.search(question=query, longitude=longitude, latitude=latitude)

            hits = results['hits']['hits']

            # print(hits)

            # for x in hits:
            # print(x['_source'])

            # {'_score': 0.79549515, '_type': 'place', '_id': '3eVjFTuQQ3yxtSiOXjB7MQ', '_index': 'toerh_coffee',
            # '_source': {'name': 'Espresso House', 'location': {'lat': 16.326955, 'lon': 56.6874601}}}

            queryset = list(Coffee.objects.filter(id__in=[r['_source']['pk'] for r in hits]))

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
    ordering_fields = ('name', 'address', 'created_at',)


class TagViewSet(ModelViewSet):
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


class UserViewSet(ModelViewSet):
    authentication_classes = (SafeTokenAuthentication, UnsafeJSONWebTokenAuthentication)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ('username', 'email', 'date_joined', 'last_login', 'is_active')

    @detail_route()
    def reviews(self, request, pk):
        reviews = Review.objects.filter(user=pk)

        serializer = NestedReviewSerializer(reviews, many=True, context={'request': request})
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
    ordering_fields = ('rating', 'description', 'coffee', )


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)