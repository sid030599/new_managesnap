from rest_framework import serializers

from .models import *

class temp_verification_ser(serializers.ModelSerializer):
    
    class Meta:
        model = temp_verification
        fields = '__all__'