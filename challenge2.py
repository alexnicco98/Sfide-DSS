import pyexiv2
from PIL import Image
from PIL.ExifTags import TAGS
import os
from os.path import join

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
    img = pyexiv2.Image(fn)
    exif_info = img.read_exif()
    if not len(exif_info) == 0:
        print(exif_info)
        #print(exif_info['Exif.Image.ImageWidth'])
        print(dms_to_dd(exif_info["Exif.GPSInfo.GPSLatitude"], exif_info["Exif.GPSInfo.GPSLatitudeRef"]))
        print(dms_to_dd(exif_info["Exif.GPSInfo.GPSLongitude"], exif_info["Exif.GPSInfo.GPSLongitudeRef"]))
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
print(file_jpg)
for i in file_jpg:
    get_exif(i)
    # image_coordinates(i)
# get_coordinates(exif['GPSInfo'])
