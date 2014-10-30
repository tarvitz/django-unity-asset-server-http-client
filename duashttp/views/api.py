# coding: utf-8

from duashttp.serializers import AssetVersionSerializer
from duashttp.models import AssetVersion
from duashttp.filters import AssetVersionFilter

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status

from django.http import HttpResponse
__all__ = ['AssetVersionViewSetBase', ]


class AssetVersionViewSetBase(viewsets.ModelViewSet):
    """
    AssetVersionViewSetBase api control viewset
    """
    queryset = AssetVersion.objects.all()
    serializer_class = AssetVersionSerializer
    permission_classes = [IsAuthenticated, ]
    filter_class = AssetVersionFilter

    @action(methods=['GET', ])
    def blob(self, request, pk=None):
        """
        fetch large object from pg and gives it back to user via HTTP 1.1
        request

        :param request: django request instance
        :param pk: requested resource primary key
        :rtype: django.http.HttpResponse
        :rtype: HttpResponse
        :return: file with its filename stored in database
        """
        obj = self.get_object_or_none()
        if obj:
            blob = obj.get_blob_data()
            content_type = 'octet/stream'
            response = HttpResponse(blob, content_type=content_type,
                                    status=status.HTTP_200_OK)
            response['Content-Disposition'] = (
                'attachment; filename="%s"' % obj.name
            )
            return response
        return HttpResponse('404', status=status.HTTP_404_NOT_FOUND,
                            content_type='application/json')
