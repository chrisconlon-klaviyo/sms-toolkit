from sms_toolkit import constants
from sms_toolkit.utils.general import flatten


def is_high_surrogate(character):
    if character is None:
        return False

    return ord(character) >= 0xD800 and ord(character) <= 0xDBFF


def convert_to_unicode_characters(string):
    characters = list(string.decode('utf-8'))
    converted_character_list = []

    while len(characters) > 0:
        current_character = characters.pop(0)
        if is_high_surrogate(current_character):
            converted_character_list.append(current_character + characters.pop(0))
        else:
            converted_character_list.append(current_character)

    return converted_character_list


def encode_unicode_character_to_utf16(character):
    if len(character) > 1:
        return flatten(map(encode_unicode_character_to_utf16, character))

    return [((0xff00 & ord(character)) >> 8), 0x00ff & ord(character)]


def encode_unicode_character_to_gsm(character):
    return constants.UNICODE_CODE_POINT_TO_GSM_MAP[ord(character)]


def determine_encoding_for_string(string):
    if all([ord(character) in constants.UNICODE_CODE_POINT_TO_GSM_MAP.keys() for character in string]):
        return constants.GSM_ENCODING
    else:
        return constants.UCS2_ENCODING

