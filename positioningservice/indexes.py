from pyelasticsearch import ElasticSearch, IndexAlreadyExistsError


class SearchIndex(object):
    def __init__(self, model):
        self.es = ElasticSearch()
        self.model = model

    def put_mapping(self, index, doc_type):
        mapping = {
            doc_type: {
                "properties": {
                    "location": {
                        "type": "geo_point"
                    },
                }
            }
        }
        self.es.put_mapping(index=index, doc_type=doc_type, mapping=mapping)

    def bulk_items(self, index, doc_type):
        for m in self.model.objects.all():
            self.es.bulk([
                self.es.index_op({
                    "pk": m.pk,
                    "name": m.name,
                    "rating": m.rating,
                    "address": m.address,
                    "description": m.description,
                    "location": {
                        "lon": m.position.longitude,
                        "lat": m.position.latitude
                    }
                }),
                ],
                doc_type=doc_type,
                index=index)

    def search(self, index, question, longitude, latitude, size=10):
        #self.es.delete_index(index)
        try:
            self.es.create_index(index)
            self.put_mapping(index, "place")
            self.bulk_items(index, "place")
        except IndexAlreadyExistsError:
            pass

        query = {
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "should": [
                                {"match": {"name": question}},
                                {"match": {"_all": {
                                    "query": question,
                                    "operator": "or",
                                    "fuzziness": "auto",
                                    "zero_terms_query": "all"
                                    }}}
                                ]
                            }
                        },
                    "functions": [
                        {"exp": {"rating": {"origin": 5, "scale": 1, "offset": 0.1}}},
                    ]
                    }
                }
            }

        if longitude and longitude is not None:
            query['query']['function_score']['functions'] = [
                {'gauss': {
                    "location": {"origin": {"lat": latitude, "lon": longitude}, "offset": "550m", "scale": "1km"}
                    }},
                {'gauss': {
                    "location": {"origin": {"lat": latitude, "lon": longitude}, "offset": "500m", "scale": "2km"}
                    }},
            ]

        results = self.es.search(query, index=index, size=size)

        self.es.refresh()

        return results
