from audio import SoundEvent, sound_manager
from customer import Customer
from queue_manager import QueueManager
from machines import Printer
from ui.hud import CaptionToggle, VolumeSlider


def test_entry_bell_and_caption():
    sound_manager.history.clear()
    sound_manager.captions.clear()
    toggle = CaptionToggle()
    toggle.enable()
    qm = QueueManager()
    qm.add_customer(Customer("print", patience=5))
    assert sound_manager.history[-1] is SoundEvent.BELL
    assert "customer entered" in sound_manager.captions


def test_printer_completion_alert():
    sound_manager.history.clear()
    sound_manager.captions.clear()
    toggle = CaptionToggle()
    toggle.enable()
    printer = Printer()
    printer.start_job("flyer")
    printer.progress(100)
    printer.complete()
    assert SoundEvent.ALERT in sound_manager.history
    assert "printer job complete" in sound_manager.captions


def test_volume_slider_and_speak_interface():
    slider = VolumeSlider()
    slider.set_level(0.5)
    assert slider.get_level() == 0.5
    slider.set_level(2.0)
    assert slider.get_level() == 1.0  # clamped

    sound_manager.history.clear()
    sound_manager.captions.clear()
    sound_manager.toggle_captions(True)
    sound_manager.speak("Hello")
    assert sound_manager.history[-1] is SoundEvent.TTS
    assert "Hello" in sound_manager.captions
