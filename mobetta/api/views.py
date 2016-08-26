from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from mobetta import util
from mobetta.models import TranslationFile, MessageComment
from mobetta.api.serializers import TranslationFileSerializer, MessageCommentSerializer
from mobetta.api.permissions import CanTranslatePermission


class TranslationFileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for fetching info about a translation file.
    """
    queryset = TranslationFile.objects.all()
    serializer_class = TranslationFileSerializer

    permission_classes = [CanTranslatePermission]


class MessageCommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for fetching/posting `MessageComment`s
    """
    queryset = MessageComment.objects.all()
    serializer_class = MessageCommentSerializer

    permission_classes = [CanTranslatePermission]

    def get_queryset(self):
        queryset = MessageComment.objects.all()
        file_pk = self.request.query_params.get('translation_file', None)

        if file_pk is not None:
            queryset = queryset.filter(translation_file__pk=file_pk)

        msgid = self.request.query_params.get('msgid', None)

        if msgid is not None:
            queryset = queryset.filter(msgid=msgid)

        return queryset


class TranslationSuggestionsView(APIView):
    """
    View for fetching translation suggestions using MS Translate.
    """
    permission_classes = [CanTranslatePermission]

    def get(self, request, format=None):
        original_message = request.query_params.get('msgid')
        language = request.query_params.get('language_code')
        translator = util.get_translator()
        suggestion = util.get_automated_translation(translator, original_message, language)

        return Response({
            'msgid': original_message,
            'language_code': language,
            'suggestion': suggestion,
        })
