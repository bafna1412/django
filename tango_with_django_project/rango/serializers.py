from django.forms import widgets
from rest_framework import serializers
from rango.models import Category, Page, UserProfile

class RangoSerializer(serializers.Serializer):
    
