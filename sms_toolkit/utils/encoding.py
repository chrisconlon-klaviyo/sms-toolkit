from sms_toolkit import constants
import sys


def is_python_3():
    return sys.version_info[0] == 3


def is_high_surrogate(character):
    if character is None:
        return False

    return ord(character) >= 0xD800 and ord(character) <= 0xDBFF


def convert_to_unicode_characters(string):
    from sms_toolkit.messages.normalization import normalize_to_unicode

    characters = list(normalize_to_unicode(string))
    converted_character_list = []

    while len(characters) > 0:
        current_character = characters.pop(0)
        if is_high_surrogate(current_character):
            converted_character_list.append(current_character + characters.pop(0))
        else:
            converted_character_list.append(current_character)

    return converted_character_list


def encode_unicode_character_to_utf16(character):
    """
    Encode the given unicode code points into utf-16 and return a list of bytes. Note that for code-points within
    the BMP the number of bytes would be 2, but for code-points not in BMP, the number of bytes will be 4.

    Args:
        character: A unicode code-point

    Returns:
        A list of the bytes
    """
    if is_python_3():
        return [c for c in character.encode('utf-16-be')]
    else:
        return [ord(c) for c in character.encode('utf-16-be')]


def encode_unicode_character_to_gsm(character):
    return constants.UNICODE_CODE_POINT_TO_GSM_MAP[ord(character)]


def determine_encoding_for_string(string):
    from sms_toolkit.messages.normalization import normalize_to_unicode

    string = normalize_to_unicode(string)
    if all([ord(character) in constants.UNICODE_CODE_POINT_TO_GSM_MAP.keys() for character in string]):
        return constants.GSM_ENCODING
    else:
        return constants.UCS2_ENCODING
