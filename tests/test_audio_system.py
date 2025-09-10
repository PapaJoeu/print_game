from audio import SoundEvent, sound_manager
from customers.customer import Customer
from customers.queue import QueueManager
from machines import Printer
from ui.hud import CaptionToggle, VolumeSlider
from types import SimpleNamespace
from unittest.mock import MagicMock


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


def test_loading_and_playback_with_mixer(monkeypatch):
    """Sound files are loaded via the loader and played through mixer."""
    sound_manager.sounds.clear()

    mock_sound = MagicMock()
    mixer_mock = SimpleNamespace(Sound=MagicMock(return_value=mock_sound))
    monkeypatch.setattr("audio.mixer", mixer_mock)

    sound_manager.load(SoundEvent.BELL)
    expected_path = str(sound_manager._resolve_sound(SoundEvent.BELL))
    mixer_mock.Sound.assert_called_with(expected_path)

    sound_manager.play(SoundEvent.BELL)
    mock_sound.set_volume.assert_called_once()
    mock_sound.play.assert_called_once()


def test_muting_channel_stops_playback(monkeypatch):
    sound_manager.sounds.clear()
    sound_manager.muted_channels.clear()

    mock_sound = MagicMock()
    mixer_mock = SimpleNamespace(Sound=MagicMock(return_value=mock_sound))
    monkeypatch.setattr("audio.mixer", mixer_mock)

    sound_manager.load(SoundEvent.BELL)
    sound_manager.mute_channel("effects", True)
    sound_manager.play(SoundEvent.BELL)
    mock_sound.play.assert_not_called()
