import sgp4
import numpy as np



def generate_tle(satellite_name, line_1, line_2):
  """Generates a TLE as a function of time for the given satellite name, line 1 and line 2 of the TLE.

  Args:
    satellite_name: The name of the satellite.
    line_1: The first line of the TLE.
    line_2: The second line of the TLE.

  Returns:
    A list of TLEs, one for each time step.
  """
  from sgp4 import Satrec
  # Create a satellite object from the TLE.
  satellite = sgp4.Satrec()
  satellite.twoline2rv(line_1, line_2)

  # Create a list of times.
  times = np.linspace(0, 3600, 100)

  # Generate TLEs for each time step.
  tle_list = []
  for time in times:
    tle_list.append(satellite.sgp4(time))

  return tle_list

# Get the satellite name, line 1 and line 2 of the TLE.
satellite_name = "ISS"
line_1 = "1 25544U 98067A 18135.61844383 .00002728 00000-0 48567-4 0 9998"
line_2 = "2 25544 51.6402 181.0633 0004018 88.8954 22.2246 15.54059185113452"

# Generate TLEs for the given satellite.
tle_list = generate_tle(satellite_name, line_1, line_2)

# Print the first TLE.
print(tle_list[0])

