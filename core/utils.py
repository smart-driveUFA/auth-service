import uuid

from django.db.utils import IntegrityError

from core.models import TPI
from core.serializers import TPISerializer


def mixin_tpi_model(create=False, get=False, data=None, user=None):
    if create:
        try:
            serializer = TPISerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data["user"] = user
            serializer.save()
        except IntegrityError as e:
            return {"error": f"{e.args}"}

        return {"message": "TPI created successfully"}

    elif get:
        try:
            serializer = TPISerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data["user"] = user
            composite_id_string = f"{user.username}|{data['lat_start']}|{data['lon_start']}|{data['lat_end']}|{data['lon_end']}|{data['start']}|{data['end']}|{data['highway']}"
            composite_id = uuid.uuid5(uuid.NAMESPACE_DNS, composite_id_string)
            return TPI.objects.get(composite_id=composite_id)
        except TPI.DoesNotExist as er_tpi:
            return {"error": f"{er_tpi.args}"}

        except IntegrityError as er_int:
            return {"error": f"{er_int.args}"}
