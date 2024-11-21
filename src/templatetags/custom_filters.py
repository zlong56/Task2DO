from django import template
from django.urls import reverse
from src.models import *
import datetime,re
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter(name='mod')
def mod(value, arg):
    return value % arg

@register.filter(name='split')
def split(value, arg):
    return str(value).split(arg)

@register.filter(name='get_file_name')
def get_file_name(value):
    return str(value).split("/")[-1]

@register.filter(name='to_url')
def to_url(value):
    try:
        return reverse(value)
    except Exception as e:
        # Handle exceptions, e.g., return an empty string or log the error
        # return ''
        raise e
    
@register.filter(name='to_decimal')
def to_decimal(value):
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        # If conversion fails, return the original value or handle it accordingly
        return value
    
@register.filter(name='to_str')
def to_str(value):
    return to_str(value)
    
@register.filter(name='remove')
def remove(value,arg):
    try:
        return value.replace(arg,"")
    except Exception as e:
        return value
    
@register.filter(name='get_index')
def get_index(value, arg):
    try:
        return value[int(arg)]
    except ValueError:
        return None
    
@register.filter(name='remove_spaces')
def remove_spaces(value):
    return value.replace(' ', '')

@register.filter
def get_fields(model_instance):
    return model_instance._meta.fields

@register.filter
def get_related_model(field):
    if hasattr(field, 'related_model'):
        return field.related_model.objects.all()
    return None

@register.filter(name='concat')
def concat(value, arg):
    try:
        return str(value) + str(arg)
    except Exception:
        return str(value)
    
@register.filter(name='add')
def add(value, arg):
    try:
        return round(float(value) + float(arg),2)
    except (ValueError, TypeError):
        return 'Invalid Input'

@register.filter(name='add_int')
def add_int(value, arg):
    try:
        return int(int(value) + int(arg))
    except (ValueError, TypeError):
        return 'Invalid Input'
    
@register.filter(name='minus')
def minus(value, arg):
    try:
        return round(float(value) - float(arg),2)
    except (ValueError, TypeError):
        return 'Invalid Input'


@register.filter(name='minus_int')
def minus_int(value, arg):
    try:
        return int(int(value) - int(arg))
    except (ValueError, TypeError):
        return 'Invalid Input'
    
@register.filter(name='mul')
def multiply(value, arg):
    try:
        return round(float(value) * float(arg),2)
    except (ValueError, TypeError):
        return 'Invalid Input'


@register.filter(name='mul_int')
def multiply_int(value, arg):
    try:
        return int(value*arg)
    except (ValueError, TypeError):
        return 'Invalid Input'
    
@register.filter(name='div')
def divide(value, arg):
    try:
        return round(float(value) / float(arg),2)
    except (ValueError, TypeError):
        return 'Invalid Input'

@register.filter(name='div_int')
def divide_int(value, arg):
    try:
        return int(value/arg)
    except (ValueError, TypeError):
        return 'Invalid Input'
    
@register.filter(name='lstrip')
def divide_int(value, arg):
    try:
        value = str(value)
        return value[arg:]
    except (ValueError, TypeError):
        return 'Invalid Input'
    
@register.filter(name='rstrip')
def divide_int(value, arg):
    try:
        value = str(value)
        return value[:len(value)-arg]
    except (ValueError, TypeError):
        return 'Invalid Input'
    

@register.filter(name='is_list')
def is_list(value):
    return isinstance(value, tuple) or isinstance(value, list)


@register.filter(name='zip_lists')
def zip_lists(a, b):
    return zip(a, b)

@register.filter(name='split_left')
def split_left(value, arg):
    value_list = str(value).split(arg)
    if len(value_list) > 1:
        return value_list[0]
    return value

@register.filter(name='split_right')
def split_right(value, arg):
    value_list = str(value).split(arg)
    if len(value_list) > 1:
        return value_list[-1]
    return value


@register.filter(name='stitch')
def stitch(value, arg):
    return [value,arg]

@register.filter(name='to_list')
def to_list(value):
    return [value]

@register.filter(name='add_list')
def add_list(value,arg):
    return [value,arg]

@register.filter(name='get_model_name')
def get_model_name(queryset):
    return queryset.model.__name__

@register.filter(name='get_parameter')
def get_parameter(queryset):
    try:
        return queryset.model.parameter(None)
    except AttributeError:
        return []

@register.filter(name='append')
def append(value, arg):
    value.append(arg)
    return value

@register.filter(name='get_all_objects')
def get_all_objects(value, arg):
    foreign_key_field = value._meta.get_field(arg)
    related_model = foreign_key_field.related_model
    return [str(obj) for obj in related_model.objects.all()]

@register.filter(name='delta_now')
def delta_now(value,arg):
    current_time = datetime.datetime.now()
    delta = current_time - value
    return delta > datetime.timedelta(hours=int(arg))

@register.filter(name='fix_Phone')
def fix_Phone(phone_number):
    # Remove any non-digit characters
    phone_number = re.sub(r'\D', '', phone_number)

    # If the number starts with "0", remove it
    if phone_number.startswith('0'):
        phone_number = phone_number[1:]

    # If the number starts with "+60", remove the country code
    if phone_number.startswith('60'):
        phone_number = phone_number[2:]

    return phone_number

@register.filter(name='add_https')
def add_https(value):
    if 'www.' in value and not value.startswith('https://'):
        return 'https://' + value
    else:
        return value