# -*- coding: utf-8 -*-

from sms_toolkit.messages.normalization import normalize_optimistic_gsm_characters


class TestMessageNormalization:
    def test_normalize_unicode(self, sample_unicode_string):
        assert normalize_optimistic_gsm_characters(sample_unicode_string) == u"This is my MANAGEMENT VOICE."

    def test_normalize_byte_string(self, sample_byte_string):
        assert normalize_optimistic_gsm_characters(sample_byte_string) == u"This is my MANAGEMENT VOICE."

    def test_emoji_unicode_string(self, sample_emoji_unicode_string):
        assert normalize_optimistic_gsm_characters(sample_emoji_unicode_string) == u"This is my MANAGEMENT VOICE 🤙."
