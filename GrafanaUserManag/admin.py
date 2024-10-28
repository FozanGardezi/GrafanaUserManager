from django.contrib import admin
from .models import User, GrafanaOrganization

admin.site.register(User)
admin.site.register(GrafanaOrganization)
