from PIL.ExifTags import GPSTAGS


def convert_gps_to_decimal(coords, ref):
    degrees = coords[0][0] / coords[0][1]
    minutes = coords[1][0] / coords[1][1]
    seconds = coords[2][0] / coords[2][1]

    decimal = degrees + (minutes / 60) + (seconds / 3600)

    if ref in ["S", "W"]:
        decimal *= -1

    return decimal


def extract_gps(gps_info):
    gps_data = {}

    for key, value in gps_info.items():
        decoded = GPSTAGS.get(key, key)
        gps_data[decoded] = value

    if (
        "GPSLatitude" in gps_data
        and "GPSLatitudeRef" in gps_data
        and "GPSLongitude" in gps_data
        and "GPSLongitudeRef" in gps_data
    ):
        lat = convert_gps_to_decimal(
            gps_data["GPSLatitude"], gps_data["GPSLatitudeRef"]
        )

        lon = convert_gps_to_decimal(
            gps_data["GPSLongitude"], gps_data["GPSLongitudeRef"]
        )
        return {"latitude": lat, "longitude": lon}
    return None
