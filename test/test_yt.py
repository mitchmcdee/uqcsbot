"""
Tests for yt.py
"""
from test.conftest import MockUQCSBot
from test.helpers import generate_message_object
from unittest import mock

import random
import string

YOUTUBE_VIDEO_URL = 'https://www.youtube.com/watch?v='
NO_QUERY_MESSAGE = "You can't look for nothing. !yt <QUERY>"


def mocked_search_execute(search_query: str, search_part: str, search_type: str, max_results: int):
    """
    Currently only returns a response of video ID's based on max_results.
    Otherwise returns none.
    """
    if search_type == 'video' and search_part == 'id':
        items = []
        for _ in range(max_results):
            # The following line generates an 11 character random string of ascii and digits
            # This simulates a videoId returned by the google api client
            videoId = ''.join(random.choices(
                string.ascii_letters + string.digits, k=11))
            # The response from the client contains a list of items
            # Each item has id object containing a string called videoId
            items.append({'id', {'videoId', videoId}})
        return {'items': items}
    return None


def test_yt_no_query(uqcsbot: MockUQCSBot):
    message = generate_message_object("!yt")
    uqcsbot.test_handle_event(message)
    assert len(uqcsbot.test_posted_messages) == 1
    assert uqcsbot.test_posted_messages[0].text == NO_QUERY_MESSAGE


@mock.patch('uqcsbot.scripts.yt.execute_search', side_effect=mocked_search_execute)
def test_yt_normal(uqcsbot: MockUQCSBot):
    message = generate_message_object("!yt dog")
    uqcsbot.test_handle_event(message)
    assert len(uqcsbot.test_posted_messages) == 1
    assert uqcsbot.test_posted_messages[0].text[0:len(
        YOUTUBE_VIDEO_URL)] == YOUTUBE_VIDEO_URL
