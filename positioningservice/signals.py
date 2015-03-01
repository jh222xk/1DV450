from pyelasticsearch import ElasticSearch


def update_index(sender, created, **kwargs):
    """
    A signal for indexing new coffeehouses
    upon creation
    """
    es = ElasticSearch()
    if created:
        m = sender.objects.last()
        es.bulk([
            es.index_op({
                "pk": m.pk,
                "name": m.name,
                "rating": m.rating,
                "location": {
                    "lon": m.position.longitude,
                    "lat": m.position.latitude
                }
            }),
            ],
            doc_type="place",
            index="toerh_coffee")
