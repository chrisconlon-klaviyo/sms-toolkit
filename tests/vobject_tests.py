# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
import sys
import unittest

from sms_toolkit.vobject import base

from sms_toolkit.vobject.base import __behaviorRegistry as behavior_registry

two_hours = datetime.timedelta(hours=2)


def get_test_file(path):
    """
    Helper function to open and read test files.
    """
    filepath = "test_files/{}".format(path)
    if sys.version_info[0] < 3:
        # On python 2, this library operates on bytes.
        f = open(filepath, "r")
    else:
        # On python 3, it operates on unicode. We need to specify an encoding
        # for systems for which the preferred encoding isn't utf-8 (e.g windows)
        f = open(filepath, "r", encoding="utf-8")
    text = f.read()
    f.close()
    return text


class TestBehaviors(unittest.TestCase):
    """
    Test Behaviors
    """

    def test_general_behavior(self):
        """
        Tests for behavior registry, getting and creating a behavior.
        """
        # Check expected behavior registry.
        self.assertEqual(
            sorted(behavior_registry.keys()),
            [
                "ADR",
                "FN",
                "LABEL",
                "N",
                "ORG",
                "PHOTO",
                "VCARD",
            ],
        )


class TestVcards(unittest.TestCase):
    """
    Test VCards
    """

    @classmethod
    def setUpClass(cls):
        """
        Method for setting up class fixture before running tests in the class.
        Fetches test file.
        """
        cls.test_file = get_test_file("vcard_with_groups.ics")
        cls.card = base.readOne(cls.test_file)

    def test_vcard_creation(self):
        """
        Test creating a vCard
        """
        vcard = base.newFromBehavior("vcard", "3.0")
        self.assertEqual(str(vcard), "<VCARD| []>")

    def test_default_behavior(self):
        """
        Default behavior test.
        """
        card = self.card
        self.assertEqual(base.getBehavior("note"), None)
        self.assertEqual(
            str(card.note.value),
            "The Mayor of the great city of Goerlitz in the great country of Germany.\nNext line.",
        )

    def test_with_groups(self):
        """
        vCard groups test
        """
        card = self.card
        self.assertEqual(str(card.group), "home")
        self.assertEqual(str(card.tel.group), "home")

        card.group = card.tel.group = "new"
        self.assertEqual(
            str(card.tel.serialize().strip()),
            "new.TEL;TYPE=fax,voice,msg:+49 3581 123456",
        )
        self.assertEqual(str(card.serialize().splitlines()[0]), "new.BEGIN:VCARD")

    def test_vcard_3_parsing(self):
        """
        VCARD 3.0 parse test
        """
        test_file = get_test_file("simple_3_0_test.ics")
        card = base.readOne(test_file)
        # value not rendering correctly?
        # self.assertEqual(
        #    card.adr.value,
        #    "<Address: Haight Street 512;\nEscape, Test\nNovosibirsk,  80214\nGnuland>"
        # )
        self.assertEqual(
            card.org.value,
            ["University of Novosibirsk", "Department of Octopus Parthenogenesis"],
        )

        for _ in range(3):
            new_card = base.readOne(card.serialize())
            self.assertEqual(new_card.org.value, card.org.value)
            card = new_card


if __name__ == "__main__":
    unittest.main()
