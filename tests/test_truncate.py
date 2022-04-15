# -*- coding: utf-8 -*-
from sms_toolkit import truncate_message


class TestTruncateMessage:
    def test_truncate_with_invalid_truncation_length(self, short_gsm7_text, long_ucs2_text):
        # Check for truncation length > message length
        assert truncate_message(short_gsm7_text, 20) == short_gsm7_text
        assert truncate_message(long_ucs2_text, 500) == long_ucs2_text

        # Invalid Lengths
        assert truncate_message(short_gsm7_text, 0) == short_gsm7_text
        assert truncate_message(long_ucs2_text, -1) == long_ucs2_text

    def test_truncate_with_gsm_string(self, short_gsm7_text, long_gsm7_text):
        assert truncate_message(short_gsm7_text, 1) == u'S'
        assert truncate_message(short_gsm7_text, 3) == u'Sup'
        assert truncate_message(long_gsm7_text, 300) == long_gsm7_text[:300]

    def test_truncate_with_ucs_string(
            self,
            short_ucs2_text,
            long_ucs2_text,
            ucs2_with_surrogate_pairs
    ):
        assert truncate_message(short_ucs2_text, 1) == u'S'
        assert truncate_message(short_ucs2_text, 14) == u'Sup chonus™ 🤙'
