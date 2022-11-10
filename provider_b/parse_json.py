import json
from schemas import *
from datetime import datetime as dt

def search_in_trip(trip: dict, query: SearchSchema):
    """
    if first dep is my home airport
    if any arr that is not last arr is my tartget airport
    if last arr is my home airport
    """
    home_airport_is_first = trip[0].get('segments')[0]\
        .get('dep').get('airport') == query.from_.airport.value
    dep_time_from_home = dt.strptime(trip[0].get('segments')[0]\
        .get('dep').get('at'), '%Y-%m-%dT%H:%M:%S').date() == query.from_.at.date()
    home_airport_is_last = trip[-1].get('segments')[-1]\
        .get('arr').get('airport') == query.from_.airport.value

    arr_to_target_airport = False
    correct_return_time_and_airport = False
    airports = set()
    for i in trip:
        for j in i.get('segments'):
            airports.add(j.get('dep').get('airport'))
            airports.add(j.get('arr').get('airport'))
            if j.get('arr').get('airport') == query.to.airport.value:
                arr_to_target_airport = True
            if j.get('dep').get('airport') == query.to.airport.value and dt.strptime(j.get('dep').get('at'), '%Y-%m-%dT%H:%M:%S').date() == query.to.at.date():
                correct_return_time_and_airport = True

    return all([home_airport_is_first, dep_time_from_home, home_airport_is_last, correct_return_time_and_airport, arr_to_target_airport])


async def search_in_files(query: SearchSchema):
    search_results = []
    with open('provider_a/response_a.json', 'r') as f:
        data = json.load(f)
        for trip in data:
            if search_in_trip(trip.get('flights'), query):
                search_results.append(trip)
    return search_results
