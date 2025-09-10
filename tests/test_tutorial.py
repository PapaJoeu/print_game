import pytest

from machines import Binder, Printer
from tutorial import default_tutorial
from ui.pause_menu import PauseMenu


def test_tutorial_unlocks_machines_and_replays():
    printer = Printer()
    binder = Binder()
    tut = default_tutorial(printer, binder)

    step = tut.start()
    assert step.station == "Printer"
    assert binder.locked

    tut.next_step()  # start job
    step = tut.next_step()  # move to binder step
    assert step.station == "Binder"
    assert not binder.locked  # binder unlocked when step becomes active

    menu = PauseMenu(tut)
    menu.replay_tutorial()
    assert binder.locked  # tutorial reset relocks binder
    assert tut.current_step().station == "Printer"
