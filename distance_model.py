from init_config import db


class Distance(db.Document):
    source = db.StringField()
    destination = db.StringField()
    distance_in_km = db.FloatField()
    hits = db.IntField(default=0)

    # Order json of the object
    def get_with_hits_as_json(self):
        return {"source": self.source, "destination": self.destination, "hits": self.hits}

    def get_with_distance_as_json(self):
        return {"source": self.source, "destination": self.destination, "distance": self.distance_in_km}