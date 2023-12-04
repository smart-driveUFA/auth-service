from core.custom_exceptions import MethodNotAllowsError
from core.models import TPI


def mixin_tpi_model(create=False, get=False, kwargs=None):
    lat_start = kwargs.get("lat_start", None)
    lon_start = kwargs.get("lon_start", None)
    lat_end = kwargs.get("lat_end", None)
    lon_end = kwargs.get("lon_end", None)
    start = kwargs.get("start", None)
    end = kwargs.get("end", None)
    highway = kwargs.get("highway", None)
    if create:
        if all({lat_start, lon_start, start, end, highway, lat_end, lon_end}):
            TPI.objects.create(
                lat_start=lat_start,
                lon_start=lon_start,
                lon_end=lon_end,
                lat_end=lat_end,
                start=start,
                end=end,
                highway=highway,
            )
            return True
        else:
            raise NameError("excepted required value lat_start, lon_start, start, end, highway, lat_end, lon_end")
    elif get:
        if all({lat_start, lon_start, start, end, highway}):
            try:
                return TPI.objects.get(
                    lat_start=lat_start,
                    lon_start=lon_start,
                    start=start,
                    end=end,
                    highway=highway,
                )
            except TPI.DoesNotExist:
                return None
        else:
            raise NameError("excepted required value lat_start, lon_start, start, end, highway, lat_end, lon_end")
    else:
        raise MethodNotAllowsError("only get or create method")
