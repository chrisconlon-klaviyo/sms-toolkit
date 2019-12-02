from sms_toolkit import utils
from sms_toolkit import constants


def profile_message(message):
    """ Accept a message string and profile its contents.

        We attempt to determine the proper encoding for the string
        based on what characters it contains. If all characters are
        in the gsm7 alphabet we can use gsm7 which is has longer
        segments. Otherwise we have to use ucs2 which can contain
        non-gsm7 characters but only fit half the characters in each
        segment.

        Args:
            message (basestring): The raw message string to profile.
        Returns:
            (dict) A dict with the profiling results.
    """
    encoding = utils.determine_encoding_for_string(message)

    if encoding == constants.GSM_ENCODING:
        segments = split_message_into_segments(
            message,
            constants.GSM_MAX_SEGMENT_SIZE,
            constants.GSM_MAX_CONCAT_SEGMENT_SIZE,
            utils.encode_unicode_character_to_gsm,
        )
        message_length = sum(len(segment['byte_groups']) for segment in segments)
    elif encoding == constants.UCS2_ENCODING:
        segments = split_message_into_segments(
            message,
            constants.UCS2_MAX_SEGMENT_SIZE,
            constants.UCS2_MAX_CONCAT_SEGMENT_SIZE,
            utils.encode_unicode_character_to_utf16,
        )
        message_length = sum(len(utils.flatten(segment['byte_groups'])) for segment in segments) / 2
    else:
        raise RuntimeError('Unknown encoding: {encoding}'.format(encoding=encoding))

    return {
        'num_segments': len(segments),
        'segments': segments,
        'message_length': message_length,
    }

def split_message_into_segments(message, max_segment_size, max_concat_segment_size, encoder):
    """ Using the given encoder, the raw message is split into segments

        Args:
            message          (basestring): The raw message string to profile.
            max_segment_size        (int): How large a single segment message
                                           could be.
            max_concat_segment_size (int): How large each segment can be.
            encoder            (function): A function to encode each character.
    """
    segments = []
    characters = utils.convert_to_unicode_characters(message)

    if len(characters) == 0:
        return segments

    byte_groups = map(lambda character: encoder(character), characters)
    total_num_bytes = len(utils.flatten(byte_groups))

    if total_num_bytes <= max_segment_size:
        segments.append(format_segment(message, characters, byte_groups))
        return segments

    while len(characters) > 0:
        segment_characters = []
        segment_byte_groups = []
        current_length = 0

        def get_next_character_length():
            try:
                return current_length + len(byte_groups[0])
            except IndexError:
                return current_length

        while len(characters) > 0 and get_next_character_length() <= max_concat_segment_size:
            character = characters.pop(0)

            try:
                byte_group = byte_groups.pop(0)
            except IndexError:
                byte_group = None

            segment_characters.append(character)
            segment_byte_groups.append(byte_group)

            if byte_group is not None:
                current_length += len(byte_group)

        segments.append(format_segment(message, segment_characters, segment_byte_groups))

    return segments

def format_segment(message, unicode_characters, byte_groups):
    """ Formats a segment's properties.

        Args:
            message                 (basestring): The raw message string to profile.
            unicode_characters (list of unicode): The message split into unicode
                                                  characters.
            byte_groups          (list of bytes): The message split into byte groups
                                                  for each character.
    """
    return {
        'message': message,
        'unicode_character_list': unicode_characters,
        'byte_groups': byte_groups,
        'total_segment_length': len(utils.flatten(byte_groups)),
    }
