from utils import dist

# Python is annoying when it comes from importing from parent folder so, intead of a model folder
# we create a Model file.


class Competition:
    id = None
    location = (None, None)
    date = None

    def set_location(self, lat, long):
        self.location = (lat, long)

    def distance(self, other):
        return dist(self.location[0], self.location[1], other.location[0], other.location[1])

    # Sorting competitions by date
    def __lt__(self, other):
        return self.date < other.date
