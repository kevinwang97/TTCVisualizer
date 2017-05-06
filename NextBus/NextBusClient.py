import requests


endpoint = "http://webservices.nextbus.com/service/publicJSONFeed"


class NextBusClient:
    def __init__(self):
        pass

    def get_request(self, payload):
        r = requests.get(endpoint, params=payload)

        if r.status_code != 200:
            raise Exception("Request failed with error {}".format(r.status_code))

        return r.json()

    def agencies(self):
        return self.get_request({'command': 'agencyList'})

    def route_list(self, agency_tag):
        return self.get_request({'command': 'routeList', 'a': agency_tag})

    def route_config(self, agency_tag, route_tag):
        return self.get_request({'command': 'routeConfig', 'a': agency_tag, 'r': route_tag})

    def predictions(self, agency_tag, route_tag, stop_tag):
        return self.get_request({'command': 'predictions', 'a': agency_tag, 'r': route_tag, 's': stop_tag})

    def schedule(self, agency_tag, route_tag):
        return self.get_request({'command': 'schedule', 'a': agency_tag, 'r': route_tag})

    def vehicle_locations(self, agency_tag, time, route_tag=None):
        payload = {'command': 'vehicleLocations', 'a': agency_tag, 't': time}
        if route_tag:
            payload['r'] = route_tag
        return self.get_request(payload)