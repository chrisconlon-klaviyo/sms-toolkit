sms-toolkit
===========

A collection of tools used to send SMS messages.

.. image:: https://github.com/chrisconlon-klaviyo/sms-toolkit/workflows/Tests/badge.svg
   :target: https://github.com/chrisconlon-klaviyo/sms-toolkit/actions?query=workflow%3ATests+event%3Apush+branch%3Amaster
   :alt: Test Status

Tools
-----

Message Profiling
~~~~~~~~~~~~~~~~~

Accepts a raw SMS message string and determines its most efficient
encoding, then determines how many segments would be used to send it.

Largely based on `this tool`_ (code found `here`_).

The segmenting logic for GSM-7 and UCS-2 encoding follows `these standards`_

Here is an example with simple ascii input, which will be profiled as GSM-7 format:

.. code-block:: python

    from sms_toolkit.messages.profiling import profile_message
    profile_message("Sup chonus")

    '''
    # Outputs -
    {
       "num_segments": 1,
       "segments": [
           {
               "message": "Sup chonus",
               "total_segment_length": 10,
               "unicode_character_list": [
                   "S", "u", "p", " ", "c", "h", "o", "n", "u", "s"
               ],
               "byte_groups": [
                   [83], [117], [112], [32], [99], [104], [111], [110], [117], [115]
               ]
           }
       ],
       "message_length": 10,
       "max_segment_size": 160
    }
    '''

Here is an example with non-ascii input, containing characters from `BMP`_ (represented as 2 bytes byte-group)
and non-BMP (representing as 4 bytes in the byte-group) ranges which will be profiled as UCS-2 format:

.. code-block:: python

    from sms_toolkit.messages.profiling import profile_message
    profile_message("fuel ⛽ fiⓇe 🔥 emojis 😉")

    '''
    # Outputs -
    {
        'num_segments': 1,
        'segments': [
            {
                'message': 'fuel ⛽ fiⓇe 🔥 emojis 😉',
                'unicode_character_list': [
                    'f', 'u', 'e', 'l', ' ', '⛽', ' ', 'f', 'i', 'Ⓡ', 'e', ' ', '🔥', ' ', 'e', 'm', 'o', 'j', 'i', 's', ' ', '😉'
                ],
                'byte_groups': [
                    [0, 102], [0, 117], [0, 101], [0, 108], [0, 32], [38, 253], [0, 32], [0, 102], [0, 105], [36, 199], [0, 101], [0, 32], [216, 61, 221, 37], [0, 32], [0, 101], [0, 109], [0, 111], [0, 106], [0, 105], [0, 115], [0, 32], [216, 61, 222, 9]
                ],
                'total_segment_length': 24
            }
        ],
        'message_length': 24,
        'max_segment_size': 70
    }
    '''

Testing
-------
This library needs is tested against python 2 and 3. Both interpreters need to be available to tox

::

  pyenv versions  # shows all versions available
  pyenv local 2.7.* 3.7.*


Run tests:

``tox .``

.. _this tool: http://chadselph.github.io/smssplit/
.. _here: https://github.com/chadselph/smssplit/blob/master/js/smssplit.js
.. _these standards:https://en.wikipedia.org/wiki/SMS#Message_size
.. _BMP:https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane