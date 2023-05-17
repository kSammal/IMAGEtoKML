import os
import subprocess

# Get the current working directory
current_directory = os.getcwd()

# Change directory command
change_directory_cmd = f'cd /d {current_directory}'

# Run the change directory command
subprocess.run(change_directory_cmd, shell=True)

# Command to create KML file using Exiftool
exiftool_cmd = 'exiftool -E -p kml.fmt Images > test.kml'

# Run the Exiftool command to create the KML file
subprocess.run(exiftool_cmd, shell=True)

# Command to extract GPS coordinates using Exiftool and output formatted coordinates to a text file
extract_coordinates_cmd = 'exiftool -T -c "%.6f" -p "${Filepath};${GPSLatitude};${GPSLongitude};${GPSAltitude}" Images > coordinates.csv'

# Run the command to extract GPS coordinates and save them to a text file
subprocess.run(extract_coordinates_cmd, shell=True)

# Read the contents of the CSV file
with open('coordinates.csv', 'r') as file:
    lines = file.readlines()

# Process each line and remove 'N' from Latitude and 'E' from Longitude
for i in range(1, len(lines)):
    parts = lines[i].split(';')
    latitude = parts[1].replace(' N', '')
    longitude = parts[2].replace(' E', '')
    lines[i] = f'{parts[0]};{latitude};{longitude};{parts[3]}'

# Write the updated lines back to the TXT file
with open('coordinates.txt', 'w') as file:
    file.writelines(lines)
