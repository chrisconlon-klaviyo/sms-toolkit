# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def short_gsm7_text():
    return "Sup chonus."


@pytest.fixture
def long_gsm7_text():
    return "The option to override automatic detonation expires in T minus three minutes. The option to override automatic detonation expires in T minus one minute. The option to override detonation procedure has now expired. Mother! I've turned the cooling unit back on! Mother! The ship will automatically destruct in T minus five minutes."


@pytest.fixture
def short_ucs2_text():
    return "Sup chonus™ 🤙."


@pytest.fixture
def long_ucs2_text():
    return "The option to override automatic detonation expires in T minus three minutes 🤙. The option to override automatic detonation expires in T minus one minute. The option to override detonation procedure has now expired. Mother™! I've turned the cooling unit back on! Mother 🤙! The ship will automatically destruct in T minus five minutes."


@pytest.fixture
def sample_byte_string():
    return "This is my ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴠᴏɪᴄᴇ."


@pytest.fixture
def sample_unicode_string():
    return u"This is my ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴠᴏɪᴄᴇ."


@pytest.fixture
def sample_emoji_unicode_string():
    return u"This is my ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴠᴏɪᴄᴇ 🤙."


@pytest.fixture
def unicode_gsm7_chars():
    return u"Laisse aller au supermarché. The option to override automatic detonation expires in T minus three minutes."


@pytest.fixture
def byte_string_gsm7_chars(unicode_gsm7_chars):
    return unicode_gsm7_chars.encode('utf-8')
