import os
import exifread

# Header
header = 'Failinimi;Laiuskraad;Pikkuskraad;Kõrgus'

# Get the current working directory
current_directory = os.getcwd()

# Path to the Images directory
images_directory = os.path.join(current_directory, 'Images')

# List to store the extracted coordinates
coordinates = []

# Iterate over the image files in the directory
for filename in os.listdir(images_directory):
    if filename.endswith('.jpg') or filename.endswith('.jpeg'):
        filepath = os.path.join(images_directory, filename)

        # Open the image file
        with open(filepath, 'rb') as file:
            # Read the EXIF tags using exifread
            tags = exifread.process_file(file, details=False)

            # Extract the required GPS tags
            latitude = tags.get('GPS GPSLatitude')
            longitude = tags.get('GPS GPSLongitude')
            altitude = tags.get('GPS GPSAltitude')

            # Check if the required GPS tags are present
            if latitude and longitude and altitude:
                # Format the coordinates
                latitude_ref = str(tags.get('GPS GPSLatitudeRef'))
                longitude_ref = str(tags.get('GPS GPSLongitudeRef'))
                altitude_ref = str(tags.get('GPS GPSAltitudeRef'))

                latitude_values = [float(x.num) / float(x.den) for x in latitude.values]
                longitude_values = [float(x.num) / float(x.den) for x in longitude.values]

                latitude_formatted = sum(latitude_values[i] / 60 ** i for i in range(3))
                longitude_formatted = sum(longitude_values[i] / 60 ** i for i in range(3))
                altitude_formatted = float(altitude.values[0].num) / float(altitude.values[0].den)

                if latitude_ref == 'S':
                    latitude_formatted *= -1
                if longitude_ref == 'W':
                    longitude_formatted *= -1
                if altitude_ref == 'BelowSeaLevel':
                    altitude_formatted *= -1

                # Add the formatted coordinates to the list
                coordinates.append(
                    f'{filename};{latitude_formatted:.6f};{longitude_formatted:.6f};{altitude_formatted:.6f}')

# Sort the coordinates based on the filename
coordinates.sort()

# Insert the header at the beginning of the list
coordinates.insert(0, header)

# Write the coordinates to the file
with open('coordinates.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(coordinates))

print("Coordinates extracted and written to coordinates.txt successfully.")
