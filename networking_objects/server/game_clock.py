import time

class GameClock:
    def __init__(self, target_fps: int = 100):
        self.tick_rate = 1.0 / target_fps
        self.accumulator = 0.0
        self.current_time = time.perf_counter()
        self.current_tick = 0

    def tick(self) -> int:
        new_time = time.perf_counter()
        frame_time = new_time - self.current_time

        if frame_time > 0.25: # clamp massive lag spikes
            frame_time = 0.25

        self.current_time = new_time
        self.accumulator += frame_time

        # calculate how many fixed steps to process
        ticks_to_run = int(self.accumulator / self.tick_rate)
        self.accumulator -= ticks_to_run * self.tick_rate # subtracts only what gets consumed
        self.current_tick += ticks_to_run

        return ticks_to_run

    def sleep_until_next_frame(self):
        end_time = time.perf_counter()
        sleep_time = self.tick_rate - (end_time - self.current_time)
        if sleep_time > 0:
            time.sleep(sleep_time)
