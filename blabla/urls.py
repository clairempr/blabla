from django.conf.urls import url
from chat.views import ajax_chats, home, logout_view, ajax_chats_rendered, send_chat
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^$', home, name='home'),
    url(r'^accounts/logout/$', logout_view, name='logout'),
    url(r'^ajax_chats/$', ajax_chats, name='ajax_chats'),
    url(r'^ajax_chats_rendered/$', ajax_chats_rendered, name='ajax_chats_rendered'),
    url(r'^send_chat/$', send_chat, name='send_chat'), ] + \
            static(settings.STATIC_URL, document_root=settings.STATIC_ROOT+'/js')



