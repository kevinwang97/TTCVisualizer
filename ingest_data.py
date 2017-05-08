import os
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import sys

sys.path.insert(0, 'NextBus/')

from NextBusClient import NextBusClient

user = 'root' #os.environ['MYSQL_USER']
password = 'root' #os.environ['MYSQL_PASSWORD']
db = 'ttc_bus_data'

config = {
    'user': user,
    'password': password,
    'host': 'localhost',
    'database': 'ttc_bus_data',
    'raise_on_warnings': True,
}


def remove_old_data(db_connection):
    query = "DELETE FROM vehicle_locations WHERE updated_at < (NOW() - INTERVAL 1 MINUTE)"
    cursor = db_connection.cursor()
    cursor.execute(query)
    db_connection.commit()
    cursor.close()


def ingest_data(db_connection):
    next_bus_client = NextBusClient()

    add_vehicle_location = ("INSERT INTO vehicle_locations "
                            "(id, longitude, latitude, route_number, direction, updated_at) "
                            "VALUES (%(id)s, %(longitude)s, %(latitude)s, %(route_number)s, %(direction)s, %(updated_at)s) "
                            "ON DUPLICATE KEY UPDATE "
                            "longitude=VALUES(longitude),latitude=VALUES(latitude),route_number=VALUES(route_number),direction=VALUES(direction), updated_at=VALUES(updated_at)")

    cursor = db_connection.cursor()

    vehicles = next_bus_client.vehicle_locations('ttc', 0)['vehicle']

    for vehicle in vehicles:
        vehicle_data = {
            'id': vehicle['id'],
            'longitude': vehicle['lon'],
            'latitude': vehicle['lat'],
            'route_number': vehicle['routeTag'],
            'direction': vehicle['heading'],
            'updated_at': datetime.now()
        }
        cursor.execute(add_vehicle_location, vehicle_data)

    db_connection.commit()
    cursor.close()


def main():
    try:
        db_connection = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Incorrect username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return

    # remove_old_data(db_connection)
    ingest_data(db_connection)
    db_connection.close()


if __name__ == '__main__':
    main()
