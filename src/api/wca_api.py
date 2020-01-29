import urllib.request
import json
import logging

logger = logging.getLogger('spam_application')

base_url = "https://www.worldcubeassociation.org/api/v0"

delegates_endpoint = "/delegates"


def get_delegates():
    url = base_url + delegates_endpoint
    print("Fetching data from WCA")
    print("url:", url)

    with urllib.request.urlopen(url) as request:
        data = json.loads(request.read().decode())
        return data
