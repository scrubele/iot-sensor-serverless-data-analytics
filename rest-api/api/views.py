from django.shortcuts import render
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt

from api.models import User, ProtectedObject, Robot, DetourPath
from api.serializers import UserSerializer, ProtectedObjectSerializer, DetourPathSerializer, RobotSerializer

from api.permissions import IsLoggedInUserOrAdmin, IsAdminUser
from rest_framework.permissions import AllowAny, IsAdminUser

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
  
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView, SocialConnectView

from rest_framework.response import Response
from django.http import Http404 

import json

@method_decorator(csrf_exempt, name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Add this code block
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class FacebookConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter

class DetourPathViewSet(viewsets.ModelViewSet):
    queryset = DetourPath.objects.all()
    serializer_class = DetourPathSerializer 

class RobotViewSet(viewsets.ModelViewSet):
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer 

    def get_queryset(self):
        return Robot.objects.filter(protectedobject=self.kwargs.pop('protectedobject_pk', None)) \
               or Robot.objects.all()

    def list(self, request, protectedobject_pk=None):
        print(protectedobject_pk)
        # protectedobject_pk = protectedobject.kwargs.get('pk')
        queryset = Robot.objects.filter(protectedobject__pk=protectedobject_pk)
        serializer_context = {
            'request': request,
        }
        serializer = RobotSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

    def get_object(self):
        pk = self.kwargs.get('pk')
        print(pk)
        try:
            return Robot.objects.get(pk=pk)
        except Robot.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        robot = self.get_object(pk)
        serializer_context = {
            'request': request,
        }
        serializer = RobotSerializer(robot, context=serializer_context)
        return Response(serializer.data)

    def create(self, request, protectedobject_pk=None, *args, **kwargs):
        
        print(request.data)
        serializer_context = {
            'request': request,
        }
        robot_serializer = RobotSerializer(data=request.data, context=serializer_context)
        if robot_serializer.is_valid():
            robot = robot_serializer.save()

        protected_object = ProtectedObject.objects.get(pk=protectedobject_pk)
        print(protected_object.robots.all())
        # name = protected_object.name
        protected_object.robots.add(robot)
        print(protected_object.robots.all())
        # print(name)
        # protected_object_serializer = ProtectedObjectSerializer(protected_object, context=serializer_context)
        # print(protected_object_serializer)
            # self.create(robot_serializer)
            # robot = Robot.objects.create(dict(request.data.lists()))
        return  Response(robot_serializer.data)

    # def retrieve(self, request, pk=None, client_pk=None, maildrop_pk=None):
    #     queryset = MailRecipient.objects.filter(pk=pk, mail_drop=maildrop_pk, mail_drop__client=client_pk)
    #     maildrop = get_object_or_404(queryset, pk=pk)
    #     serializer = MailRecipientSerializer(maildrop)
    #     return Response(serializer.data)

class ProtectedObjectViewSet(viewsets.ModelViewSet):
    queryset = ProtectedObject.objects.all()
    serializer_class = ProtectedObjectSerializer

    # def get_queryset(self):
    #     return ProtectedObject.objects.filter(protectedObject=self.kwargs['protectedobject_pk'])

    def list(self, request, *args, **kwargs):
        queryset = ProtectedObject.objects.all()
        serializer_context = {
            'request': request,
        }
        serializer = ProtectedObjectSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

    def get_object(self):
        pk = self.kwargs.get('pk')
        print(pk)
        try:
            return ProtectedObject.objects.get(pk=pk)
        except ProtectedObject.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        protected_object = self.get_object(pk)
        serializer_context = {
            'request': request,
        }
        serializer = ProtectedObjectSerializer(protected_object, context=serializer_context)
        return Response(serializer.data)
   