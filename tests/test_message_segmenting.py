from sms_toolkit.messages import profiling


class TestMessageSegmenting:
    def test_message_profiling_gsm7(self, short_gsm7_text, long_gsm7_text):
        profiled_message = profiling.profile_message(short_gsm7_text)
        assert profiled_message["num_segments"] == 1
        assert profiled_message["message_length"] == 11
        assert len(profiled_message["segments"]) == 1

        profiled_message = profiling.profile_message(long_gsm7_text)
        assert profiled_message["num_segments"] == 3
        assert profiled_message["message_length"] == 329
        assert len(profiled_message["segments"]) == 3

    def test_message_profiling_ucs2(self, short_ucs2_text, long_ucs2_text):
        profiled_message = profiling.profile_message(short_ucs2_text)
        assert profiled_message["num_segments"] == 1
        assert profiled_message["message_length"] == 15
        assert len(profiled_message["segments"]) == 1

        profiled_message = profiling.profile_message(long_ucs2_text)
        assert profiled_message["num_segments"] == 6
        assert profiled_message["message_length"] == 336
        assert len(profiled_message["segments"]) == 6
