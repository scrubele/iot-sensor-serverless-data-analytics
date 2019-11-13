from rest_framework import serializers
from api.models import *
from rest_framework.authtoken.models import Token
from .models import ProtectedObject, Robot, DetourPath, Sensor
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ('title', 'dob', 'address', 'country', 'city', 'zip', 'photo')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'username', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.save(commit=False)
        if password is not None:
            user.set_password(password)
        robots
        user.save(commit=False)
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.title = profile_data.get('title', profile.title)
        profile.dob = profile_data.get('dob', profile.dob)
        profile.address = profile_data.get('address', profile.address)
        profile.country = profile_data.get('country', profile.country)
        profile.city = profile_data.get('city', profile.city)
        profile.zip = profile_data.get('zip', profile.zip)
        profile.photo = profile_data.get('photo', profile.photo)
        profile.save()

        return instance


class TokenSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Token
        fields = ('key', 'user')   

class RobotSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Robot
        fields = '__all__'

class DetourPathSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = DetourPath
        fields = '__all__'


class ProtectedObjectSerializer(serializers.ModelSerializer):
    robots = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,   # Or add a queryset
        view_name='protectedobjects-robots-detail',
        parent_lookup_kwargs={'protectedobject_pk': 'protectedobject__pk'}    
    )
    detour_paths = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,   # Or add a queryset
        view_name='protectedobjects-detours-detail',
        parent_lookup_kwargs={'protectedobject_pk': 'protectedobject__pk'}    
    )

    class Meta:
        model = ProtectedObject
        fields = '__all__'

    def create(self, validated_data):
        robots_data, detour_paths_data = [],[]
        try:
            robots_data = validated_data.pop('protectedobject')
            detour_paths_data = validated_data.pop('detour_paths')
        except:
            print('No')

        protected_object = ProtectedObject.objects.create(**validated_data)
        protected_object.detour_paths.set([])
        return protected_object

    def destroy(self, request, pk, format=None):
        try:
            instance = self.get_object(pk)
            self.perform_destroy(instance)
        except Http404:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'status': 'location deleted'})

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.size = validated_data.get('size', instance.size)
        instance.robots = validated_data.get('robots', instance.robots)
        instance.detour_paths = validated_data.get('detour_paths', instance.detour_paths)
        instance.photo = validated_data.get('photo', instance.photo)
        return instance



class SensorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sensor
        fields = '__all__'