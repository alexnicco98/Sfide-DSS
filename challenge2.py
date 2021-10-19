import pyexiv2
from PIL import Image
from PIL.ExifTags import TAGS
import os
from os.path import join
import sys
from gensim.utils import tokenize

'''def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees'''

'''def image_coordinates(img_path):
    with open(img_path, 'rb') as src:
        img = Image(src)
    if img.has_exif:
        try:
            img.gps_longitude
            coords = (decimal_coords(img.gps_latitude,
                      img.gps_latitude_ref),
                      decimal_coords(img.gps_longitude,
                      img.gps_longitude_ref))
        except AttributeError:
            print('No Coordinates')
    else:
        print('The Image has no EXIF information')
    print(f"Image {src.name}, OS Version:{img.get('software', 'Not Known')} ------")
    print(f"Was taken: {img.datetime_original}, and has coordinates:{coords}")'''

'''def get_coordinates(info):
    for key in ['Latitude', 'Longitude']:
        if 'GPS' + key in info and 'GPS' + key + 'Ref' in info:
            e = info['GPS' + key]
            ref = info['GPS' + key + 'Ref']
            info[key] = (str(e[0][0] / e[0][1]) + '°' +
                         str(e[1][0] / e[1][1]) + '′' +
                         str(e[2][0] / e[2][1]) + '″ ' +
                         ref)

    if 'Latitude' in info and 'Longitude' in info:
        return [info['Latitude'], info['Longitude']]'''

'''def dms_to_decimal(degrees, minutes, seconds, sign=' '):
    """Convert degrees, minutes, seconds into decimal degrees.

    >>> dms_to_decimal(10, 10, 10)
    10.169444444444444
    >>> dms_to_decimal(8, 9, 10, 'S')
    -8.152777777777779
    """
    return (-1 if sign[0] in 'SWsw' else 1) * (
        float(degrees)        +
        float(minutes) / 60   +
        float(seconds) / 3600
    )


def print_gps(image_file):
    try:
        metadata = pyexiv2.metadata.ImageMetadata(image_file)
        metadata.read()
        thumb = metadata.exif_thumbnail

        try:
            latitude = metadata.__getitem__("Exif.GPSInfo.GPSLatitude")
            latitudeRef = metadata.__getitem__("Exif.GPSInfo.GPSLatitudeRef")
            longitude = metadata.__getitem__("Exif.GPSInfo.GPSLongitude")
            longitudeRef = metadata.__getitem__("Exif.GPSInfo.GPSLongitudeRef")

            latitude = str(latitude).split("=")[1][1:-1].split(" ");
            latitude = map(lambda f: str(float(Fraction(f))), latitude)
            latitude = latitude[0] + u"\u00b0" + latitude[1] + "'" + latitude[2] + '"' + " " + str(latitudeRef).split("=")[1][1:-1]

            longitude = str(longitude).split("=")[1][1:-1].split(" ");
            longitude = map(lambda f: str(float(Fraction(f))), longitude)
            longitude = longitude[0] + u"\u00b0" + longitude[1] + "'" + longitude[2] + '"' + " " + str(longitudeRef).split("=")[1][1:-1]

            latitude_value = dms_to_decimal(*metadata.__getitem__("Exif.GPSInfo.GPSLatitude").value + [metadata.__getitem__("Exif.GPSInfo.GPSLatitudeRef").value]);
            longitude_value = dms_to_decimal(*metadata.__getitem__("Exif.GPSInfo.GPSLongitude").value + [metadata.__getitem__("Exif.GPSInfo.GPSLongitudeRef").value]);

            print("--- GPS ---")
            print("Coordinates: " + latitude + ", " + longitude)
            print("Coordinates: " + str(latitude_value) + ", " + str(longitude_value))
            print("--- GPS ---")
        except Exception as e:
            print("No GPS Information!")
            #print e

        # Check for thumbnail
        if(thumb.data == ""):
            print("No thumbnail!")
    except Exception as e:
        print("Error processing image...")
        print(e)'''


# sistemare in base alla libreria pyexiv2
def dms_to_dd(gps_coords, gps_coords_ref):
    d, m, s = gps_coords
    dd = d + m / 60 + s / 3600
    if gps_coords_ref.upper() in ('S', 'W'):
        return -dd
    elif gps_coords_ref.upper() in ('N', 'E'):
        return dd
    else:
        raise RuntimeError('Incorrect gps_coords_ref {}'.format(gps_coords_ref))


def get_field(exif, field):
    for (k, v) in exif.items():
        if TAGS.get(k) == field:
            return v


def get_exif(fn):
    '''path = bytes(fn, 'utf-8')
    with open(path, 'rb') as f:
        with pyexiv2.ImageData(f.read()) as img:
            data = img.read_exif()
            if not len(data) == 0:
                ret = {}
                for tag, value in data:
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
                print(ret)'''
    img = pyexiv2.Image(fn)
    exif_info = img.read_exif()
    if not len(exif_info) == 0:
        print(exif_info)
        a = list(tokenize(exif_info['Exif.GPSInfo.GPSLatitude']))
        print(a)
        # print(exif_info['Exif.Image.ImageWidth'])
        '''
        # Read the GPS info.
        latref = exif_info['Exif.GPSInfo.GPSLatitudeRef']
        print(exif_info['Exif.GPSInfo.GPSLatitude'])
        print( float(exif_info['Exif.GPSInfo.GPSLatitude'][0]) / float(exif_info['Exif.GPSInfo.GPSLatitude'][2]))
        print(float(exif_info['Exif.GPSInfo.GPSLatitude'][4]) / float(exif_info['Exif.GPSInfo.GPSLatitude'][6]))
        #lat = [float(exif_info['Exif.GPSInfo.GPSLatitude'][0]), float(exif_info['Exif.GPSInfo.GPSLatitude'][3]), float(exif_info['Exif.GPSInfo.GPSLatitude'][6])]
        #print(lat)
        lonref = exif_info['Exif.GPSInfo.GPSLongitudeRef']
        lon = float(exif_info['Exif.GPSInfo.GPSLongitude'])


        # Convert the latitude and longitude to signed floating point values.
        latitude = float(lat[0]) + float(lat[1]) / 60 + float(lat[2]) / 3600
        longitude = float(lon[0]) + float(lon[1]) / 60 + float(lon[2]) / 3600
        if latref == 'S': latitude = -latitude
        if lonref == 'W': longitude = -longitude

        # Construct the Google Maps query and open it.
        query = "http://maps.google.com/maps?q=loc:%.6f,%.6f" % (latitude, longitude)
        subprocess.call(['open', query])'''


# print(dms_to_dd(exif_info["Exif.GPSInfo.GPSLatitude"], exif_info["Exif.GPSInfo.GPSLatitudeRef"]))
# print(dms_to_dd(exif_info["Exif.GPSInfo.GPSLongitude"], exif_info["Exif.GPSInfo.GPSLongitudeRef"]))
# print(get_coordinates(exif_info))
# print(img.read_iptc())
# print(img.read_xmp())


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


mypath = "F:"
file_jpg = search_jpg(mypath)
# print(file_jpg)
for i in file_jpg:
    get_exif(i)
    # image_coordinates(i)
    # get_coordinates(exif['GPSInfo'])

    ''''# Get the data from image file and return a dictionary
    data = gpsphoto.getGPSData(i)
    print(data['Latitude'], data['Longitude'])'''
