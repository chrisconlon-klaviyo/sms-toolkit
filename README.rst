sms-toolkit
===========

A collection of tools used to send SMS messages.

Tools
-----

Message Profiling
~~~~~~~~~~~~~~~~~

Accepts a raw SMS message string and determines its most efficient
encoding, then determines how many segments would be used to send it.

Largely based on `this tool`_ (code found `here`_).

Example:

::

   from sms_toolkit.messages.profiling import profile_message
   import json

   profile = profile_message("Sup chonus")
   print(json.dumps(profile, indent=4))

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
       "message_length": 10
   }

Testing
-------

From the root repository directory run the following:

``pytest -s tests``

.. _this tool: http://chadselph.github.io/smssplit/
.. _here: https://github.com/chadselph/smssplit/blob/master/js/smssplit.js