import pytest

from customer import Customer
from machines.base import Machine
from queue_manager import QueueManager
from hud import JobHUD, MachineStatusPanel, QueueDisplay
from navigation import HotkeyManager, NavigationMode, Navigator


def test_queue_display_lists_customers():
    qm = QueueManager()
    qm.add_customer(Customer("copy", patience=5))
    qm.add_customer(Customer("print", patience=5))
    display = QueueDisplay()
    assert display.render(qm) == ["copy", "print"]


def test_machine_status_panel_shows_job_and_progress():
    machine = Machine(name="Printer")
    machine.start_job("flyers")
    machine.progress(30)
    panel = MachineStatusPanel()
    assert panel.render(machine) == "Printer: flyers (30%)"


def test_job_hud_tracks_completed_steps():
    hud = JobHUD()
    hud.mark_complete("greet")
    hud.mark_complete("deliver")
    assert hud.render() == ["[x] greet", "[ ] process_job", "[x] deliver", "[ ] checkout"]


def test_hotkey_manager_triggers_actions():
    manager = HotkeyManager()
    flag = {"called": False}

    def action():
        flag["called"] = True

    manager.register("g", action)
    manager.trigger("g")
    assert flag["called"]


def test_navigator_pathfinding_and_instant_modes():
    graph = {"counter": ["printer"], "printer": ["cutter"], "cutter": []}
    nav = Navigator(graph, NavigationMode.PATHFINDING)
    assert nav.select_station("counter", "cutter") == ["counter", "printer", "cutter"]

    nav_fast = Navigator(graph, NavigationMode.INSTANT)
    assert nav_fast.select_station("counter", "cutter") == ["cutter"]
