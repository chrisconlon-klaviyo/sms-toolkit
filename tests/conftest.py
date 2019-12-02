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
