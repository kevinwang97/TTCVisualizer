CREATE TABLE ttc_bus_data.vehicle_locations(
  id INT,
  longitude DECIMAL(16,14),
  latitude DECIMAL(16,14),
  route_number INT,
  direction INT,
  updated_at TIMESTAMP,
  PRIMARY KEY (id)
)