from copy import deepcopy

BONUS_START = "bonusStart"
MYSTERY_REVEAL = "mysteryReveal"
DRAGON_METER = "dragonMeter"
DRAGON_EVENT = "dragonEvent"
BONUS_COMPLETE = "bonusComplete"


def add_event(gamestate, event_type, **payload):
    event = {"index": len(gamestate.book.events), "type": event_type}
    event.update(deepcopy(payload))
    gamestate.book.add_event(event)
