import pytest

from machines import Binder, MachineError, Printer, Cutter, Laminator, Folder


def test_binder_measurement_success():
    binder = Binder(target_width=1.0, tolerance=0.1)
    assert binder.locked
    binder.unlock()
    binder.start_job("bind report")
    binder.progress(1.05)  # within tolerance
    binder.complete()
    assert any("visual: complete" in cue for cue in binder.cues)


def test_binder_measurement_failure_triggers_cues():
    binder = Binder(target_width=1.0, tolerance=0.1)
    binder.unlock()
    binder.start_job("bind report")
    binder.progress(0.5)  # wrong measurement
    with pytest.raises(MachineError):
        binder.complete()
    assert any("error binding failed" in cue for cue in binder.cues)


def test_printer_jam_triggers_cues():
    printer = Printer(jam_at=50)
    printer.start_job("print flyer")
    with pytest.raises(MachineError):
        printer.progress(60)
    assert any("error paper jam" in cue for cue in printer.cues)


def test_cutter_stacks_same_cut_type():
    cutter = Cutter(time_per_cut=1.0, setup_time=2.0)
    assert cutter.locked
    cutter.unlock()
    cutter.start_job("cut cards", cut_type="trim", cuts=2)
    cutter.start_job("cut flyers", cut_type="trim", cuts=2)
    assert cutter.time_required == 6  # setup once + 4 cuts
    cutter.progress(6)
    cutter.complete()
    assert cutter.progress_value == 100


def test_laminator_out_of_film_triggers_cues():
    laminator = Laminator(film_available=False)
    assert laminator.locked
    laminator.unlock()
    with pytest.raises(MachineError):
        laminator.start_job("laminate poster")
    assert any("error out of film" in cue for cue in laminator.cues)


def test_folder_jam_triggers_cues():
    folder = Folder(jam_at=50)
    assert folder.locked
    folder.unlock()
    folder.start_job("fold brochure")
    with pytest.raises(MachineError):
        folder.progress(60)
    assert any("error fold jam" in cue for cue in folder.cues)


def test_advanced_machines_start_locked():
    assert Binder().locked
    assert Cutter().locked
    assert Laminator().locked
    assert Folder().locked
