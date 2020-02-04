from sms_toolkit.constants import unicode_to_gsm_map
from sms_toolkit.utils import convert_to_unicode_characters


def normalize_optimistic_gsm_characters(message, character_map=None):
    """
    Takes a message as input and returns a new message will all the appropriate unicode characters replaced with
    their GSM-7 equivalent.

    Args:
        message (str): a string.
        character_map (dict([Int: str])): an optional mapping from unicode ordinal values to their GSM7 equivalent.

    Returns:
        str - a normalized unicode string
    """
    if isinstance(message, str):
        message = convert_to_unicode_characters(message)

    if character_map is None:
        character_map = unicode_to_gsm_map.SMART_ENCODING_MAP
    return ''.join(map(lambda c: character_map.get(ord(c), c), message))
