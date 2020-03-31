from sms_toolkit.constants import unicode_to_gsm_map
from sms_toolkit.utils import convert_to_unicode_characters


def normalize_optimistic_gsm_characters(message):
    """
    Takes a message as input and returns a new message replacing all the appropriate unicode characters with
    their GSM-7 equivalent.

    Args:
        message (str): a string (can be unicode or a plain byte string).

    Returns:
        str - a normalized unicode string
    """
    if isinstance(message, str):
        message = convert_to_unicode_characters(message)

    return ''.join(map(lambda c: unicode_to_gsm_map.SMART_ENCODING_MAP.get(ord(c), c), message))


def normalize_to_unicode(message):
    if not isinstance(message, unicode):
        return message.decode('utf-8')

    return message
