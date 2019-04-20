from django.db import transaction


@transaction.atomic
def instance_remover(instance):
    instance.delete()
