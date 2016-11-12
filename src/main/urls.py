# encoding: utf-8

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from main import views as main_views


urlpatterns = [
    url(r'^$', main_views.IndexView.as_view(), name='home'),
    url(r'^robots\.txt', include('robots.urls')),
    url(r'^admin/', include(admin.site.urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if settings.ENABLE_DEBUG_TOOLBAR:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
