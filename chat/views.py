from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from chat.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import datetime
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
import pytz
from chat.serializers import ChatSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
import json


@login_required
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('logout_view'))
    timezone.activate(pytz.timezone('Europe/Amsterdam'))
    username = get_username_from_request(request)
    latest_chats_first = True
    just_today = True
    pirate = False
    number_of_chats = 30
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat_string = form.cleaned_data['chat_string']
            save_chat(username, chat_string)
        number_of_chats = get_number_of_chats(request.POST)
        latest_chats_first = is_checkbox_checked(request, 'latest_chats_first')
        just_today = is_checkbox_checked(request, 'just_today')
        pirate = is_checkbox_checked(request, 'pirate')
    else:
        form = ChatForm()

    chats = get_chats_min_max(number_of_chats, latest_chats_first, just_today, pirate, 0, 0)
    return render(request, 'blabla.html', {'title': 'BlaBla', 'username': username, 'form': form,
                                           'latest_chats_checked': set_checkbox_checked(latest_chats_first),
                                           'just_today_checked': set_checkbox_checked(just_today),
                                           'pirate_checked': set_checkbox_checked(pirate),
                                           'number_of_chats': number_of_chats,
                                           'chats': chats})


def is_checkbox_checked(request, checkbox_name):
    return checkbox_name in request.POST


def set_checkbox_checked(checked):
    if checked:
        return 'checked'
    else:
        return ''


# this thing should be called using Ajax request to "post"
# a new chat without posting the page
# Page update should be taken care of when message is received
@login_required()
@api_view(('POST',))
def send_chat(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('logout_view'))
    username = get_username_from_request(request)
    chat_string = request.POST.get('chat_string', '')
    save_chat(username, chat_string)
    return Response(chat_string, status=204)


def get_username_from_request(request):
    if request.user.is_authenticated:
        return request.user.get_username()
    else:
        return 'Nobody'


def get_number_of_chats(request_get_or_post):
    number_of_chats = 0
    number_of_chats_str = request_get_or_post.get('number_of_chats', '')
    if number_of_chats_str != '':
        number_of_chats = int(number_of_chats_str)
    return number_of_chats


def save_chat(username, chat_string):
    if chat_string != '':
        chat = Chat()
        chat.user = username
        chat.chat_string = chat_string
        chat.save()
        pub = RedisPublisher(facility="foobar", broadcast=True)
        pub.publish_message(RedisMessage(chat_string))


@api_view()
def ajax_chats(request):
    number_of_chats = int(request.query_params.get('number_of_chats', 0))
    just_today = get_boolean_from_request(request, 'just_today', False)
    latest_chats_first = get_boolean_from_request(request, 'latest_chats_first', False)
    pirate = get_boolean_from_request(request, 'pirate', False)
    min_id = int(request.query_params.get('min_id', 0))
    max_id = int(request.query_params.get('max_id', 0))
    chats = get_chats_min_max(number_of_chats, latest_chats_first, just_today, pirate, min_id, max_id)
    serializer = ChatSerializer(chats, many=True)
    return Response(serializer.data)


def ajax_chats_rendered(request):
    number_of_chats = get_number_of_chats(request.GET)
    just_today = get_boolean_from_get_request(request, 'just_today', False)
    latest_chats_first = get_boolean_from_get_request(request, 'latest_chats_first', False)
    pirate = get_boolean_from_get_request(request, 'pirate', False)
    min_id = int(request.GET.get('min_id', 0))
    max_id = int(request.GET.get('max_id', 0))
    chats = get_chats_min_max(number_of_chats, latest_chats_first, just_today, pirate, min_id, max_id)

    # separate before and after chats
    if min_id == 0 and max_id == 0:
        chats_before = []
        chats_after = chats
    else:
        chats_before = [chat for chat in chats if chat.id < min_id]
        chats_after = [chat for chat in chats if chat.id > max_id]

    if chats:
        min_id_sent = min(chats, key=lambda chat: chat.id).id
        max_id_sent = max(chats, key=lambda chat: chat.id).id
    else:
        min_id_sent = 0
        max_id_sent = 0

    html_before = render_to_string('chats.html', {'chats': chats_before})
    html_after = render_to_string('chats.html', {'chats': chats_after})

    return HttpResponse(json.dumps({
        "min_id_sent": min_id_sent,
        "max_id_sent": max_id_sent,
        "chats_before": html_before,
        "chats_after": html_after}),
        content_type="application/json")


def get_chats_min_max(number, latest_chats_first, just_today, pirate, min_id, max_id):
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    timestamp_min = datetime.datetime.combine(datetime.date.min, datetime.time.min)

    if just_today:
        filter_timestamp = today_min
    else:
        filter_timestamp = timestamp_min

    if latest_chats_first:
        order_by_id = '-id'
    else:
        order_by_id = 'id'

    chats_queryset = Chat.objects.filter(timestamp__gte=filter_timestamp).order_by(order_by_id)[:number]

    # filter for min/max id to make sure we don't send something they already have
    if min_id > 0 or max_id > 0:
        chats = [chat for chat in chats_queryset if chat.id > max_id or chat.id < min_id]
    else:
        chats = chats_queryset

    chats = get_chat_strings_for_display(chats, pirate)
    return chats


def get_boolean_from_request(request, variable_name, default_value):
    value_str = request.query_params.get(variable_name, default_value)
    if value_str.upper() == 'TRUE':
        return True
    else:
        return False


def get_boolean_from_get_request(request, variable_name, default_value):
    value_str = request.GET.get(variable_name, default_value)
    if value_str.upper() == 'TRUE':
        return True
    else:
        return False


def get_chat_strings_for_display(chats, pirate):
    if chats is None:
        return chats
    for chat in chats:
        if chat.chat_string.startswith('{') and chat.chat_string.endswith('}'):
            # remove { } from around string
            chat.chat_string = chat.chat_string[1:-1]
            # remove any line breaks
            chat.chat_string = chat.chat_string.replace('\n', '').replace('\r', '')
            chat.chat_string = mark_safe(chat.chat_string)
        else:
            if pirate:
                chat.chat_string = chat.pirate.chat_like_a_pirate(chat.chat_string)
            long_words = filter(lambda x: len(x) > 10, chat.chat_string.split())
            if long_words is not None:
                for long_word in long_words:
                    word_with_breaks = split_word(long_word, 5)
                    chat.chat_string = chat.chat_string.replace(long_word, word_with_breaks)

    return chats


def split_word(word, size):
    replacement_char = '\0'
    return replacement_char.join([word[i:i+size] for i in range(0, len(word), size)])


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
