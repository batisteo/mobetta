from django.conf.urls import url, include

from .views import (
    EditHistoryView, download_po_file, FileDetailView, FileListView,
    LanguageListView, AddTranslatorView
)


urlpatterns = [
    url(r'^$', LanguageListView.as_view(), name='language_list'),
    url(r'^add_translator/$', AddTranslatorView.as_view(), name='add_translator'),
    url(r'^edit_log/(?P<file_pk>\d+)/$', EditHistoryView.as_view(), name='edit_history'),
    url(r'^download/(?P<file_pk>\d+)/$', download_po_file, name='download'),
    url(r'^file/(?P<pk>\d+)/$', FileDetailView.as_view(), name='file_detail'),
    url(r'^language/(?P<lang_code>[a-z]{2,3}(-[A-Za-z0-9]{1,8})*)/$', FileListView.as_view(), name='file_list'),
    url(r'^api/', include('mobetta.api.urls', namespace='api')),
]
