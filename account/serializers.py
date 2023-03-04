from rest_framework import serializers
from account.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('title', 'first_name', 'last_name', 'gender', 'email', 'password')
    extra_kwargs= {
      'password': { 'write_only': True}
    }

  def create(self, data):
      return User.objects.create_user(**data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ('email', 'password')

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'email', 'title', 'first_name', 'last_name', 'gender')