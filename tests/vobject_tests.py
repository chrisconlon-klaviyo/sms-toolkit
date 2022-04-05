# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime
import sys
import unittest

from sms_toolkit.vobject import base

from sms_toolkit.vobject.base import __behaviorRegistry as behavior_registry
from sms_toolkit.vobject.base import ContentLine
from sms_toolkit.vobject.base import textLineToContentLine


from sms_toolkit.vobject.icalendar import (
    MultiDateBehavior,
    PeriodBehavior,
)

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
                "",
                "ACTION",
                "ADR",
                "AVAILABLE",
                "BUSYTYPE",
                "CALSCALE",
                "CATEGORIES",
                "CLASS",
                "COMMENT",
                "COMPLETED",
                "CONTACT",
                "CREATED",
                "DAYLIGHT",
                "DESCRIPTION",
                "DTEND",
                "DTSTAMP",
                "DTSTART",
                "DUE",
                "DURATION",
                "EXDATE",
                "EXRULE",
                "FN",
                "FREEBUSY",
                "LABEL",
                "LAST-MODIFIED",
                "LOCATION",
                "METHOD",
                "N",
                "ORG",
                "PHOTO",
                "PRODID",
                "RDATE",
                "RECURRENCE-ID",
                "RELATED-TO",
                "REQUEST-STATUS",
                "RESOURCES",
                "RRULE",
                "STANDARD",
                "STATUS",
                "SUMMARY",
                "TRANSP",
                "TRIGGER",
                "UID",
                "VALARM",
                "VAVAILABILITY",
                "VCALENDAR",
                "VCARD",
                "VEVENT",
                "VFREEBUSY",
                "VJOURNAL",
                "VTIMEZONE",
                "VTODO",
            ],
        )

        # test get_behavior
        behavior = base.getBehavior("VCALENDAR")
        self.assertEqual(
            str(behavior), "<class 'sms_toolkit.vobject.icalendar.VCalendar2_0'>"
        )
        self.assertTrue(behavior.isComponent)

        self.assertEqual(base.getBehavior("invalid_name"), None)
        # test for ContentLine (not a component)
        non_component_behavior = base.getBehavior("RDATE")
        self.assertFalse(non_component_behavior.isComponent)

    def test_MultiDateBehavior(self):
        """
        Test MultiDateBehavior
        """
        parseRDate = MultiDateBehavior.transformToNative
        self.assertEqual(
            str(
                parseRDate(
                    textLineToContentLine(
                        "RDATE;VALUE=DATE:19970304,19970504,19970704,19970904"
                    )
                )
            ),
            "<RDATE{'VALUE': ['DATE']}[datetime.date(1997, 3, 4), datetime.date(1997, 5, 4), datetime.date(1997, 7, "
            "4), datetime.date(1997, 9, 4)]>",
        )
        self.assertEqual(
            str(
                parseRDate(
                    textLineToContentLine(
                        "RDATE;VALUE=PERIOD:19960403T020000Z/19960403T040000Z,19960404T010000Z/PT3H"
                    )
                )
            ),
            "<RDATE{'VALUE': ['PERIOD']}[(datetime.datetime(1996, 4, 3, 2, 0, tzinfo=tzutc()), datetime.datetime("
            "1996, 4, 3, 4, 0, tzinfo=tzutc())), (datetime.datetime(1996, 4, 4, 1, 0, tzinfo=tzutc()), "
            + (
                "datetime.timedelta(0, 10800)"
                if sys.version_info < (3, 7)
                else "datetime.timedelta(seconds=10800)"
            )
            + ")]>",
        )

    def test_periodBehavior(self):
        """
        Test PeriodBehavior
        """
        line = ContentLine("test", [], "", isNative=True)
        line.behavior = PeriodBehavior
        line.value = [(datetime.datetime(2006, 2, 16, 10), two_hours)]

        self.assertEqual(line.transformFromNative().value, "20060216T100000/PT2H")
        self.assertEqual(
            line.transformToNative().value,
            [(datetime.datetime(2006, 2, 16, 10, 0), datetime.timedelta(0, 7200))],
        )

        line.value.append((datetime.datetime(2006, 5, 16, 10), two_hours))

        self.assertEqual(
            line.serialize().strip(), "TEST:20060216T100000/PT2H,20060516T100000/PT2H"
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
