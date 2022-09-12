from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import UserApiBack
from .serializers import UserRegisterSerializersBackend, LoginSerializersBackend


class RegistrationAPIView(CreateAPIView):
    queryset = UserApiBack.objects.all()
    serializer_class = UserRegisterSerializersBackend
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializersBackend(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"status": "User register successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            data = serializer.errors
            return Response(data)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializersBackend

    def post(self, request):
        data = {"error": status.HTTP_400_BAD_REQUEST}
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data)