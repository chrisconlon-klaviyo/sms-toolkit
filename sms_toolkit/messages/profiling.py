from __future__ import division

from sms_toolkit import utils
from sms_toolkit import constants


def profile_message(message, is_for_mms=False):
    """ Accept a message string and profile its contents.

        We attempt to determine the proper encoding for the string
        based on what characters it contains. If all characters are
        in the gsm7 alphabet we can use gsm7 which is has longer
        segments. Otherwise we have to use ucs2 which can contain
        non-gsm7 characters but only fit half the characters in each
        segment.

        Args:
            message (basestring): The raw message string to profile.
        Kwargs:
            is_for_mms (bool): Is this message for mms sending.
        Returns:
    """
    encoding = utils.determine_encoding_for_string(message)

    if is_for_mms or encoding == constants.UCS2_ENCODING:
        if is_for_mms:
            single_segment_size = constants.MMS_MAX_SEGMENT_SIZE * 2
            concat_segment_size = constants.MMS_MAX_CONCAT_SEGMENT_SIZE * 2
        else:
            single_segment_size = constants.UCS2_MAX_SEGMENT_SIZE
            concat_segment_size = constants.UCS2_MAX_CONCAT_SEGMENT_SIZE

        segments = split_message_into_segments(
            message,
            single_segment_size,
            concat_segment_size,
            utils.encode_unicode_character_to_utf16,
        )
        message_length = sum(len(utils.flatten(segment['byte_groups'])) for segment in segments) // 2
        max_segment_size = (single_segment_size if len(segments) <= 1 else concat_segment_size) // 2

    elif encoding == constants.GSM_ENCODING:
        segments = split_message_into_segments(
            message,
            constants.GSM_MAX_SEGMENT_SIZE,
            constants.GSM_MAX_CONCAT_SEGMENT_SIZE,
            utils.encode_unicode_character_to_gsm,
        )
        message_length = sum(len(segment['byte_groups']) for segment in segments)
        max_segment_size = constants.GSM_MAX_SEGMENT_SIZE if len(segments) <= 1 \
            else constants.GSM_MAX_CONCAT_SEGMENT_SIZE

    else:
        raise RuntimeError('Unknown encoding: {encoding}'.format(encoding=encoding))

    return {
        'num_segments': len(segments),
        'segments': segments,
        'message_length': message_length,
        'max_segment_size': max_segment_size,
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
    is_utf16 = encoder == utils.encode_unicode_character_to_utf16

    if len(characters) == 0:
        return segments

    byte_groups = [encoder(character) for character in characters]
    total_num_bytes = len(utils.flatten(byte_groups))

    if total_num_bytes <= max_segment_size:
        segments.append(format_segment(message, characters, byte_groups, is_utf16))
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

        segment_str = ''
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
            segment_str += character

        segments.append(format_segment(segment_str, segment_characters, segment_byte_groups, is_utf16))

    return segments


def format_segment(message, unicode_characters, byte_groups, is_utf16):
    """ Formats a segment's properties.

        Args:
            message                 (basestring): The raw message string to profile.
            unicode_characters (list of unicode): The message split into unicode
                                                  characters.
            byte_groups          (list of bytes): The message split into byte groups
                                                  for each character.
            is_utf16                   (boolean): If the message is in utf-16 encoding
    """
    total_segment_length = len(utils.flatten(byte_groups))
    if is_utf16:
        total_segment_length = total_segment_length // 2
    return {
        'message': message,
        'unicode_character_list': unicode_characters,
        'byte_groups': byte_groups,
        'total_segment_length': total_segment_length,
    }
