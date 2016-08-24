import polib

from django.db import models

from django.conf import settings


# UserModel represents the model used by the project
UserModel = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class TranslationFile(models.Model):

    name = models.CharField(max_length=512, blank=False, null=False)
    filepath = models.CharField(max_length=1024, blank=False, null=False)
    language_code = models.CharField(max_length=32, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{} ({})".format(self.name, self.filepath)

    @property
    def model_name(self):
        return app_name_from_filepath(self.filepath)

    def get_polib_object(self):
        return polib.pofile(self.filepath)

    def get_statistics(self):
        """
        Return statistics for this file:
        - % translated
        - total messages
        - messages translated
        - fuzzy messages
        - obsolete messages
        """
        pofile = self.get_polib_object()

        translated_entries = len(pofile.translated_entries())
        untranslated_entries = len(pofile.untranslated_entries())
        fuzzy_entries = len(pofile.fuzzy_entries())
        obsolete_entries = len(pofile.obsolete_entries())

        return {
            'percent_translated': pofile.percent_translated(),
            'total_messages': translated_entries + untranslated_entries,
            'translated_messages': translated_entries,
            'fuzzy_messages': fuzzy_entries,
            'obsolete_messages': obsolete_entries,
        }


class EditLog(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserModel)
    file_edited = models.ForeignKey(TranslationFile, blank=False, null=False, related_name='edit_logs')
    msgid = models.CharField(max_length=127, null=False)
    fieldname = models.CharField(max_length=127, blank=False, null=False)
    old_value = models.CharField(max_length=255, blank=True, null=True)
    new_value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return u"[{}] Field {} | \"{}\" -> \"{}\" in {}".format(
            str(self.user),
            self.fieldname,
            self.old_value,
            self.new_value,
            self.file_edited.filepath,
        )


class MessageComment(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserModel)
    translation_file = models.ForeignKey(TranslationFile, blank=False, null=False, related_name='comments')
    msgid = models.CharField(max_length=127, null=False)
    body = models.CharField(max_length=1024, blank=False, null=False)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return u"Comment by {} on \"{}\" ({}) at {}".format(
            str(self.user),
            self.msgid,
            self.translation_file.language_code,
            self.created.strftime('%d-%m-%Y')
        )
