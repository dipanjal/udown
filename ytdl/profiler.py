import time
from typing import Optional


class Profiler:
    def __init__(self, debug: bool = False):
        self.timings: dict[str, dict[str, float]] = {}
        self.start_time: Optional[float] = None
        self.debug = debug

    def start_timer(self, name: str) -> None:
        """Start timing a specific operation."""
        self.timings[name] = {"start": time.time()}

    def end_timer(self, name: str) -> None:
        """End timing a specific operation and calculate duration."""
        if name in self.timings:
            self.timings[name]["end"] = time.time()
            self.timings[name]["duration"] = self.timings[name]["end"] - self.timings[name]["start"]

    def start_overall_timer(self) -> None:
        """Start the overall process timer."""
        self.start_time = time.time()

    def end_overall_timer(self) -> None:
        """End the overall process timer and calculate total duration."""
        if self.start_time:
            total_duration = time.time() - self.start_time
            self.timings["total"] = {"duration": total_duration}

    def print_report(self) -> None:
        """Print a formatted timing report."""
        sum_of_duration: float = 0.0
        if self.debug:
            print("\n" + "=" * 50)
            print("DOWNLOAD PERFORMANCE REPORT")
            print("=" * 50)

            for name, timing in self.timings.items():
                if name != "total":
                    duration = timing.get("duration", 0)
                    sum_of_duration += duration
                    print(f"{name.capitalize()} Took: {duration:.2f} seconds")

            print("=" * 50)

        if "total" in self.timings:
            if self.debug:
                print(f"Expected Duration: {sum_of_duration:.2f} seconds")

            actual_total_duration = self.timings["total"]["duration"]
            print(f"Total Process Time: {actual_total_duration:.2f} seconds")

            if self.debug:
                print("=" * 50)
                print(f"Time Saved: {(sum_of_duration - actual_total_duration):.2f} seconds")
