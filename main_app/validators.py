from django.core.validators import EmailValidator, ValidationError
from main_app.models import *


def validate_plan_day(plan_day, plan_id):
    if plan_day < 1 or plan_day > Plan.objects.get(pk=plan_id).plan_length:
        raise ValidationError('Haha')