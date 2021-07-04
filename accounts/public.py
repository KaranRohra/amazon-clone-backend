from accounts import models


def get_address_by_pk(pk):
    try:
        return models.Address.objects.get(pk=pk)
    except models.Address.DoesNotExist:
        raise models.Address.DoesNotExist("Address not registered")
