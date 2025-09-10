from main import Game
from machines import Printer


def test_game_loop_completes_job():
    game = Game()
    game.spawn_machine(Printer())
    game.add_customer("copy", patience=5)
    assert game.assign_next_customer("printer")
    assert game.progress_jobs(50) == []
    assert game.progress_jobs(50) == ["copy"]
    assert game.queue.list_customers() == []
