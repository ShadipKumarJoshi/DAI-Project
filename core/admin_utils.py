from django.contrib import admin

def get_list_display_for_model(model):
    """
    Return the list_display tuple from the registered ModelAdmin
    for the given model. If not registered, fallback to first 3 fields.
    """
    try:
        model_admin = admin.site._registry[model]
        # get_list_display expects a request, but None works fine for this purpose
        return list(model_admin.get_list_display(None))
    except KeyError:
        # Model not registered, fallback to first 3 field names
        return [field.name for field in model._meta.fields[:3]]
