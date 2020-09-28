from sms_toolkit.messages import profiling
from sms_toolkit import constants


class TestMessageSegmenting:
    @staticmethod
    def assert_segment_lengths_for_profiled_message(profiled_message, expected_total_segment_lengths):
        for i, segment in enumerate(profiled_message["segments"]):
            assert expected_total_segment_lengths[i] == segment["total_segment_length"]

    def test_message_profiling_gsm7(self, short_gsm7_text, long_gsm7_text, byte_string_gsm7_chars, unicode_gsm7_chars):
        profiled_message = profiling.profile_message(short_gsm7_text)
        assert profiled_message["num_segments"] == 1
        assert profiled_message["message_length"] == 11
        assert len(profiled_message["segments"]) == 1
        assert profiled_message["max_segment_size"] == constants.GSM_MAX_SEGMENT_SIZE
        self.assert_segment_lengths_for_profiled_message(
            profiled_message,
            expected_total_segment_lengths=[11]
        )

        profiled_message = profiling.profile_message(long_gsm7_text)
        assert profiled_message["num_segments"] == 3
        assert profiled_message["message_length"] == 329
        assert len(profiled_message["segments"]) == 3
        assert profiled_message["max_segment_size"] == constants.GSM_MAX_CONCAT_SEGMENT_SIZE
        self.assert_segment_lengths_for_profiled_message(
            profiled_message,
            expected_total_segment_lengths=[153, 153, 23]
        )

        profiled_message = profiling.profile_message(unicode_gsm7_chars)
        assert profiled_message["num_segments"] == 1
        assert profiled_message["message_length"] == 106
        assert len(profiled_message["segments"]) == 1
        assert profiled_message["max_segment_size"] == constants.GSM_MAX_SEGMENT_SIZE
        self.assert_segment_lengths_for_profiled_message(
            profiled_message,
            expected_total_segment_lengths=[106]
        )

        profiled_message = profiling.profile_message(byte_string_gsm7_chars)
        assert profiled_message["num_segments"] == 1
        assert profiled_message["message_length"] == 106
        assert len(profiled_message["segments"]) == 1
        assert profiled_message["max_segment_size"] == constants.GSM_MAX_SEGMENT_SIZE
        self.assert_segment_lengths_for_profiled_message(
            profiled_message,
            expected_total_segment_lengths=[106]
        )

    def test_message_profiling_ucs2(self, short_ucs2_text, long_ucs2_text):
        profiled_message = profiling.profile_message(short_ucs2_text)
        assert profiled_message["num_segments"] == 1
        assert profiled_message["message_length"] == 14
        assert len(profiled_message["segments"]) == 1
        assert profiled_message["max_segment_size"] == (constants.UCS2_MAX_SEGMENT_SIZE // 2)
        self.assert_segment_lengths_for_profiled_message(
            profiled_message,
            expected_total_segment_lengths=[14]
        )

        profiled_message = profiling.profile_message(long_ucs2_text)
        assert profiled_message["num_segments"] == 5
        assert profiled_message["message_length"] == 334
        assert len(profiled_message["segments"]) == 5
        assert profiled_message["max_segment_size"] == (constants.UCS2_MAX_CONCAT_SEGMENT_SIZE // 2)
        self.assert_segment_lengths_for_profiled_message(
            profiled_message,
            expected_total_segment_lengths=[67, 67, 67, 67, 66]
        )

    def test_message_profiling_mms_gsm7(self, short_gsm7_text, long_gsm7_text, byte_string_gsm7_chars,
                                        unicode_gsm7_chars):
        profiled_message = profiling.profile_message(short_gsm7_text, is_for_mms=True)
        assert profiled_message["num_segments"] == 1
        assert profiled_message["message_length"] == 11
        assert len(profiled_message["segments"]) == 1
        assert profiled_message["max_segment_size"] == constants.MMS_MAX_SEGMENT_SIZE
        self.assert_segment_lengths_for_profiled_message(
            profiled_message,
            expected_total_segment_lengths=[11]
        )

        profiled_message = profiling.profile_message(long_gsm7_text, is_for_mms=True)
        assert profiled_message["num_segments"] == 1
        assert profiled_message["message_length"] == 329
        assert len(profiled_message["segments"]) == 1
        assert profiled_message["max_segment_size"] == constants.MMS_MAX_SEGMENT_SIZE
        self.assert_segment_lengths_for_profiled_message(
            profiled_message,
            expected_total_segment_lengths=[329]
        )

        profiled_message = profiling.profile_message(unicode_gsm7_chars, is_for_mms=True)
        assert profiled_message["num_segments"] == 1
        assert profiled_message["message_length"] == 106
        assert len(profiled_message["segments"]) == 1
        assert profiled_message["max_segment_size"] == constants.MMS_MAX_SEGMENT_SIZE
        self.assert_segment_lengths_for_profiled_message(
            profiled_message,
            expected_total_segment_lengths=[106]
        )

        profiled_message = profiling.profile_message(byte_string_gsm7_chars, is_for_mms=True)
        assert profiled_message["num_segments"] == 1
        assert profiled_message["message_length"] == 106
        assert len(profiled_message["segments"]) == 1
        assert profiled_message["max_segment_size"] == constants.MMS_MAX_SEGMENT_SIZE
        self.assert_segment_lengths_for_profiled_message(
            profiled_message,
            expected_total_segment_lengths=[106]
        )

    def test_message_profiling_mms_ucs2(self, short_ucs2_text, long_ucs2_text):
        profiled_message = profiling.profile_message(short_ucs2_text, is_for_mms=True)
        assert profiled_message["num_segments"] == 1
        assert profiled_message["message_length"] == 14
        assert len(profiled_message["segments"]) == 1
        assert profiled_message["max_segment_size"] == constants.MMS_MAX_SEGMENT_SIZE
        self.assert_segment_lengths_for_profiled_message(
            profiled_message,
            expected_total_segment_lengths=[14]
        )

        profiled_message = profiling.profile_message(long_ucs2_text, is_for_mms=True)
        assert profiled_message["num_segments"] == 1
        assert profiled_message["message_length"] == 334
        assert len(profiled_message["segments"]) == 1
        assert profiled_message["max_segment_size"] == constants.MMS_MAX_SEGMENT_SIZE
        self.assert_segment_lengths_for_profiled_message(
            profiled_message,
            expected_total_segment_lengths=[334]
        )
