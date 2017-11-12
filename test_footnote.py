import footnote

import json

FOOTNOTES = json.loads("""
[
  ["giffgaff_free",
   "giffgaff free calls and texts to giffgaff numbers lasts for 3 months from each top-up."],
  ["fonome_quiet",
   ["poor", "Both of Fonome’s contact telephone numbers are currently unavailable."]],
  ["not_uk", "Auracall and GO-SIM have mobile numbers issued in the Isle of Man or Jersey.",
   "Those are not UK 07 numbers and most other operators charge extra to call them,",
   "the calls are not in most inclusive plans or contracts."],
  ["not_pounds",
   "GO-SIM publish their rates in USD.",
   "You can buy credit in GBP but the effective call rates depend on the exchange rate.",
   "The same applies to MAXROAM who set their rates in euros."],
  ["maxroam_incoming",
   ["poor", "MAXROAM charges 4p / min for incoming calls."],
   "Incoming texts are free."],
  ["voda_payg1", "Daily charge is capped at £1."]
]""")

RICHTEXT = json.loads("""
[
  ["poor", "MAXROAM charges 4p / min for incoming calls."],
  "Incoming texts are free."
]""")


def test_definitions():
    defs, index = footnote.definitions(FOOTNOTES)
    assert len(defs) == 6
    assert defs[0]['id'] == 'giffgaff_free'
    assert index['not_uk'] == 2
    assert defs[4]['richtext'][0] == ['poor', 'MAXROAM charges 4p / min for incoming calls.']
    assert defs[4]['richtext'][1] == 'Incoming texts are free.'


def test_tooltip():
    tooltip = footnote.tooltip(RICHTEXT)
    assert tooltip == """MAXROAM charges 4p / min for incoming
calls. Incoming texts are free."""
