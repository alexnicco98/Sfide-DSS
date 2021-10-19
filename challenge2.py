from PIL import Image
import os
import pyexiv2
from os.path import join
import exifread
import simplekml


def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None


def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


def get_exif_location(exif_data):
    """
    Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
    """
    lat = None
    lon = None

    gps_latitude = _get_if_exist(exif_data, 'GPS GPSLatitude')
    gps_latitude_ref = _get_if_exist(exif_data, 'GPS GPSLatitudeRef')
    gps_longitude = _get_if_exist(exif_data, 'GPS GPSLongitude')
    gps_longitude_ref = _get_if_exist(exif_data, 'GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degress(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = 0 - lat

        lon = _convert_to_degress(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = 0 - lon

    return lat, lon


def is_jpg(filename):
    try:
        i = Image.open(filename)
        return i.format == 'JPEG'
    except IOError:
        return False


def search_jpg(path):
    f = []
    for subdir, dirs, files in os.walk(path):
        for file in files:
            if is_jpg(join(subdir, file)):
                f.append(join(subdir, file))
    return f

def get_exif_data(image_file):
    with open(image_file, 'rb') as f:
        exif_tags = exifread.process_file(f)
    return exif_tags


mypath = "F:"
file_jpg = search_jpg(mypath)
kml = simplekml.Kml()
for i in file_jpg:
    img = pyexiv2.Image(i)
    exif_info = img.read_exif()
    if not len(exif_info) == 0:
        lat, long = get_exif_location(get_exif_data(i))
        print(lat, long)
        kml.newpoint(name=i, coords=[(long, lat)])
        kml.save("./prova.kml")
        # Construct the Google Maps query and open it.
        #query = "http://maps.google.com/maps?q=loc:%.6f,%.6f" % (lat, long)
        #subprocess.call(['open', query])
