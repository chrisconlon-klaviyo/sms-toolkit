# -*- coding: utf-8 -*-
from sms_toolkit import truncate_message
from sms_toolkit.messages.normalization import normalize_to_unicode


class TestTruncateMessage:
    def test_truncate_with_invalid_truncation_length(self, short_gsm7_text, long_ucs2_text):
        expected_unicode_long_ucs2_text = normalize_to_unicode(long_ucs2_text)

        # Check for truncation length > message length
        assert truncate_message(short_gsm7_text, 20) == u'Sup chonus.'
        assert truncate_message(long_ucs2_text, 1000) == expected_unicode_long_ucs2_text

        # Invalid Lengths
        assert truncate_message(short_gsm7_text, 0) == u'Sup chonus.'
        assert truncate_message(long_ucs2_text, -1) == expected_unicode_long_ucs2_text

    def test_truncate_with_gsm_string(self, short_gsm7_text, long_gsm7_text):
        assert truncate_message(short_gsm7_text, 1) == u'S'
        assert truncate_message(short_gsm7_text, 3) == u'Sup'
        assert truncate_message(long_gsm7_text, 300) == normalize_to_unicode(long_gsm7_text[:300])

    def test_truncate_with_ucs_string(
            self,
            short_ucs2_text,
            long_ucs2_text,
            ucs2_with_surrogate_pairs,
            ucs2_without_surrogate_pairs
    ):
        assert truncate_message(short_ucs2_text, 14) == u'Sup chonus™ 🤙'
        assert truncate_message(short_ucs2_text, 12) == u'Sup chonus™ '
        assert truncate_message(short_ucs2_text, 11) == u'Sup chonus™'
        assert truncate_message(short_ucs2_text, 10) == u'Sup chonus'
        assert truncate_message(short_ucs2_text, 1) == 'S'

        assert truncate_message(
            long_ucs2_text,
            80
        ) == u'The option to override automatic detonation expires in T minus three minutes 🤙.'

        assert truncate_message(ucs2_with_surrogate_pairs, 8) == u'a 😀 lot'
        assert truncate_message(ucs2_without_surrogate_pairs, 13) == u'This woⓡks as'

        # Since the emoji used has a length of 2, truncating upto 1 char should
        # turn up empty (not half an emoji)
        assert truncate_message(u'🤙', 1) == u''
