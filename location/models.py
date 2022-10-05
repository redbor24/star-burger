import requests
from django.conf import settings
from django.db import models
from django.utils import timezone
from geopy import distance

from star_burger.settings import GEO_ENGINE_BASE_URL


class Location(models.Model):
    address = models.CharField(max_length=100, verbose_name='Адрес', db_index=True, unique=True)
    lat = models.FloatField('Широта', db_index=True, null=True)
    lon = models.FloatField('Долгота', db_index=True, null=True)
    creation_date = models.DateField(verbose_name='Дата добавления записи', default=timezone.now, db_index=True)

    class Meta:
        verbose_name = 'Координаты заказа'
        verbose_name_plural = 'Координаты заказов'

    def __str__(self):
        return self.address


def fetch_coordinates(address):
    response = requests.get(GEO_ENGINE_BASE_URL, params={
        'geocode': address,
        'apikey': settings.YANDEX_GEOCODER_API,
        'format': 'json',
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(' ')
    return lat, lon


def get_distance(order, locations):
    order_coordinates = locations.get(order.delivery_address)
    for restaurant in order.restaurants:
        restaurant_coordinates = locations.get(restaurant.address)
        if order_coordinates and restaurant_coordinates:
            restaurant.distance_for_order = round(distance.distance(order_coordinates, restaurant_coordinates).km, 3)
    return order


def get_locations(*addresses):
    locations = {
        location.address: (location.lat, location.lon)
        for location in Location.objects.filter(address__in=addresses)
    }
    new_locations = list()
    for address in addresses:
        if address in locations.keys():
            continue
        coordinates = fetch_coordinates(address)
        if coordinates:
            lat, lon = coordinates
            location = Location(address=address, lat=lat, lon=lon)
            locations[location.address] = (location.lat, location.lon,)
            new_locations.append(location)
    Location.objects.bulk_create(new_locations)
    return locations
