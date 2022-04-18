from typing import Text

from sms_toolkit import utils
from sms_toolkit import constants
from .normalization import normalize_to_unicode


def truncate_message(message, limit, is_for_mms=False):
    """
    Truncate the given SMS message string upto the provided limit. If the SMS length is less than the
    limit, or if the limit is invalid, then the message is returned without any modification.

    Args:
        message (Text): The raw message string to profile.
        limit (int): The length upto which the message must be truncated. Must be greater than 0
        is_for_mms (bool): Is this message for mms sending.

    Returns:
        (Text): The truncated message
    """
    if limit < 1:
        return normalize_to_unicode(message)

    if is_for_mms:
        encoding = constants.UCS2_ENCODING
    else:
        encoding = utils.determine_encoding_for_string(message)

    if encoding == constants.UCS2_ENCODING:
        truncated_message = _perform_truncation(
            message=message,
            max_limit=limit * 2,
            encoder=utils.encode_unicode_character_to_utf16,
        )

    elif encoding == constants.GSM_ENCODING:
        truncated_message = _perform_truncation(
            message=message,
            max_limit=limit,
            encoder=utils.encode_unicode_character_to_gsm,
        )

    else:
        raise RuntimeError('Unknown encoding: {encoding}'.format(encoding=encoding))

    return truncated_message


def _perform_truncation(message, max_limit, encoder):
    characters = utils.convert_to_unicode_characters(message)
    curr_len = 0

    truncated_message = u''
    for character in characters:
        byte_group = encoder(character)
        if curr_len + len(byte_group) > max_limit:
            break
        curr_len = curr_len + len(byte_group)
        truncated_message += character

    return truncated_message