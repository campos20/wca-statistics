import urllib.request
import json
import logging

logger = logging.getLogger('spam_application')

base_url = "https://www.worldcubeassociation.org/api/v0"

delegates_endpoint = "/delegates"


def get_delegates():

    print("Fetching data from WCA")

    page = 1

    delegates = []
    while True:
        # json is paginated
        url = base_url + delegates_endpoint+"?page=%s" % page
        print("url:", url)

        with urllib.request.urlopen(url) as request:
            data = json.loads(request.read().decode())
            if len(data) == 0:
                break
            delegates += data
        page += 1
    return delegates
