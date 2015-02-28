import datetime
from haystack import indexes
from positioningservice.models import Position, Coffee


# class PositionIndex(indexes.SearchIndex, indexes.Indexable):
# text = indexes.CharField(document=True)
#     name = indexes.CharField(model_attr='name')
#     address = indexes.CharField(model_attr='address')
#     location = indexes.LocationField()
#     created_at = indexes.DateTimeField(model_attr='created_at')
#
#     def get_model(self):
#         return Position
#
#     def prepare_location(self, obj):
#         # If you're just storing the floats...
#         return "%s,%s" % (obj.latitude, obj.longitude)
#
#     def index_queryset(self, using=None):
#         """Used when the entire index for model is updated."""
#         return self.get_model().objects.filter(created_at__lte=datetime.datetime.now())


class CoffeeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, boost=.5)
    rating = indexes.FloatField(model_attr='rating', boost=1.5)
    name = indexes.CharField(model_attr='name')
    # position = indexes.CharField(model_attr='position__name')
    location = indexes.LocationField(model_attr='get_location')
    #reviews = indexes.MultiValueField(boost=1.5)
    created_at = indexes.DateTimeField(model_attr='created_at')

    def get_model(self):
        return Coffee

    def prepare_rating(self, obj):
        return obj.rating

    #def prepare_reviews(self, obj):
    #    return [p.rating for p in obj.reviews.all()]

    def prepare_location(self, obj):
        # If you're just storing the floats...
        return "%s,%s" % (obj.position.latitude, obj.position.longitude)
