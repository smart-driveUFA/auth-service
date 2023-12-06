from django.db.utils import IntegrityError

from core.models import TPI


def mixin_tpi_model(create=False, get=False, kwargs=None):
    lat_start = kwargs.data.get("lat_start", None)
    lon_start = kwargs.data.get("lon_start", None)
    lat_end = kwargs.data.get("lat_end", None)
    lon_end = kwargs.data.get("lon_end", None)
    start = kwargs.data.get("start", None)
    end = kwargs.data.get("end", None)
    highway = kwargs.data.get("highway", None)
    user = kwargs.user

    if create:
        if all({lat_start, lon_start, start, end, highway, lat_end, lon_end}):
            try:
                TPI.objects.create(
                    user=user,
                    lat_start=lat_start,
                    lon_start=lon_start,
                    lon_end=lon_end,
                    lat_end=lat_end,
                    start=start,
                    end=end,
                    highway=highway,
                )
            except IntegrityError as e:
                return {"error": f"{e.args}"}

            return {"message": f"TPI created successfully"}

    elif get:
        if all({lat_start, lon_start, start, end, highway}):
            try:
                return TPI.objects.get(
                    user=user,
                    lat_start=lat_start,
                    lon_start=lon_start,
                    start=start,
                    end=end,
                    highway=highway,
                )
            except TPI.DoesNotExist as er_tpi:
                return {"error": f"{er_tpi.args}"}

            except IntegrityError as er_int:
                return {"error": f"{er_int.args}"}
