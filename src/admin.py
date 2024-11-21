from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from src.models import *
from django.apps import apps


app_config = apps.get_app_config('src')  # Replace 'src' with the name of your app

for model in app_config.get_models():
    try:
        # Get the names of all CharField of the model for search_fields
        search_fields = [field.name for field in model._meta.fields if isinstance(field, models.CharField)]
        
        # Get the names of all BooleanField, DateTimeField, DateField, and fields with choices for list_filter
        filter_fields = [field.name for field in model._meta.fields if isinstance(field, (models.BooleanField, models.DateTimeField, models.DateField)) or bool(field.choices)]
        
        # Dynamically create a ModelAdmin class
        class ModelAdminClass(admin.ModelAdmin):
            list_display = [field.name for field in model._meta.fields]
            search_fields = search_fields
            list_filter = filter_fields
            class Meta:
                model = model
        
        # Register the model with the dynamically created ModelAdmin class
        admin.site.register(model, ModelAdminClass)
    except admin.sites.AlreadyRegistered:
        pass


class AccountAdmin(admin.ModelAdmin):
    list_display = ["Username","Name","pk"]
    search_fields = ["Username","Name"]
    class Meta:
        model = Account


