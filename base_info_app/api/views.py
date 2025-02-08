from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from base_info_app.api.serializers import BaseInfoSerializer
from base_info_app.models import BaseInfo


class BaseInfoView(APIView):
    def get(self, request):
        base_info = BaseInfo.objects.all()
        serializer = BaseInfoSerializer(base_info, many=True)
        return Response({'status': 'success'}, status=status.HTTP_200_OK)