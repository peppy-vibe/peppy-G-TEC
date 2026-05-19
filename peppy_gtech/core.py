"""
Core module for Peppy G-TEC

Provides the AlwaysGreen class which monitors user activity and simulates
mouse/keyboard input to keep status indicators active during working hours.
"""
import time
from datetime import datetime
from pynput import mouse, keyboard


DAY_ABBREVIATIONS = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

DEFAULT_WORKING_PERIODS = {
    'MON': [('08:30:00', '17:30:00')],
    'TUE': [('08:30:00', '17:30:00')],
    'WED': [('08:30:00', '17:30:00')],
    'THU': [('08:30:00', '17:30:00')],
    'FRI': [('08:30:00', '17:30:00')],
    'SAT': [],
    'SUN': [],
}

LOGO = '''----------------------------------------------
||||||||||||||||||||||||||||||||||||||||||||||
----------------------------------------------
\033[32m
       ____           _____ _____ ____
      / ___|         |_   _| ____/ ___|
     | |  _   _____    | | |  _|| |
     | |_| | |_____|   | | | |__| |___
      \\____|           |_| |_____\\____|
\033[0m
>>>>>>>>> :: Unleash Green Energy :: <<<<<<<<<
----------------------------------------------
|||||||||||| PRESS CTRL-C TO QUIT ||||||||||||
----------------------------------------------'''


class AlwaysGreen:
    """
    A class to prevent inactivity by detecting user input and moving the mouse.

    Attributes:
        timeout_period (int): Timeout period in seconds before moving the mouse.
        working_periods (dict): Dict mapping day abbreviations (MON-SUN) to
            lists of (start, end) time tuples during which activity is enforced.
        modern_output (bool): Enables modern output with colored text and emojis.
        show_status (bool): Displays the user activity status.
    """

    def __init__(
        self,
        timeout_period: int = 60,
        working_periods: dict = None,
        modern_output: bool = True,
        show_status: bool = True
    ):
        """
        Initializes the AlwaysGreen instance with user-configurable parameters.

        Args:
            timeout_period (int): Seconds of inactivity before action is triggered.
            working_periods (dict): Dict mapping day abbreviation strings to lists
                of (start_time_str, end_time_str) tuples in HH:MM:SS format.
                Activity is only enforced during these periods.
            modern_output (bool): Enables or disables colored and emoji status output.
            show_status (bool): Enables or disables the display of user activity status.
        """
        self._time_format = '%H:%M:%S'
        self._mouse = mouse.Controller()
        self._move_distance = 100
        self._status_str = None
        self._is_moved = False

        self._timeout_period = timeout_period
        self._working_periods = self._process_working_periods(working_periods)
        self._modern_output = modern_output
        self._show_status = show_status

        self._in_working_period = self._check_working_period()
        self._time_left = self._timeout_period

        if self._modern_output:
            self._reset_color = '\033[0m'
            self._green_color = '\033[32m'
            self._red_color = '\033[31m'
            self._user_active_status = 'Status:🟢'
            self._user_inactive_status = 'Status:🟡'
        else:
            self._reset_color = ''
            self._green_color = ''
            self._red_color = ''
            self._user_active_status = ' #ACTIVE '
            self._user_inactive_status = '#INACTIVE'

    @property
    def status_str(self):
        """
        Returns the current status string.

        Returns:
            str: Current status string.
        """
        return self._status_str

    @property
    def working_periods(self):
        """
        Returns the processed working periods dict.

        Returns:
            dict: Working periods keyed by day abbreviation with
            lists of (start, end) datetime.time tuples.
        """
        return self._working_periods

    def _process_working_periods(self, working_periods):
        """
        Processes working periods and converts time strings to datetime.time objects.

        Args:
            working_periods (dict): Dict mapping day abbreviation strings to lists
                of (start_str, end_str) tuples in HH:MM:SS format.

        Returns:
            dict: Dict mapping day abbreviations to lists of (start, end) time tuples.
        """
        processed = {day: [] for day in DAY_ABBREVIATIONS}
        if working_periods is None:
            return processed
        for day, periods in working_periods.items():
            day_upper = day.upper()
            if day_upper not in DAY_ABBREVIATIONS:
                raise ValueError(
                    f"Invalid day: '{day}'. Must be one of {DAY_ABBREVIATIONS}"
                )
            for start_str, end_str in periods:
                start = datetime.strptime(start_str, self._time_format).time()
                end = datetime.strptime(end_str, self._time_format).time()
                processed[day_upper].append((start, end))
        return processed

    def print_working_periods(self):
        """
        Prints the working periods per day if any are set.

        Returns:
            bool: True if working periods exist, False otherwise.
        """
        has_periods = any(
            len(periods) > 0
            for periods in self._working_periods.values()
        )
        if has_periods:
            print('Working Periods:')
            for day in DAY_ABBREVIATIONS:
                periods = self._working_periods[day]
                if periods:
                    for start, end in periods:
                        print(
                            f'    {day}: ',
                            start.strftime(self._time_format),
                            '-',
                            end.strftime(self._time_format),
                        )
            return True
        return False

    def _check_working_period(self):
        """
        Checks if the current day and time falls within a working period.

        Returns:
            bool: True if within a working period, False otherwise.
        """
        now = datetime.now()
        day_abbr = DAY_ABBREVIATIONS[now.weekday()]
        current_time = now.time()
        for start, end in self._working_periods.get(day_abbr, []):
            if start <= current_time <= end:
                return True
        return False

    def _set_active(self):
        """
        Resets the inactive timer when user activity is detected.
        """
        self._is_moved = True
        self._time_left = self._timeout_period
        self._in_working_period = self._check_working_period()
        self._report_status()

    def _on_move(self, _x, _y):
        """
        Callback for mouse move events.
        """
        self._set_active()

    def _on_click(self, _x, _y, _button, _pressed):
        """
        Callback for mouse click events.
        """
        self._set_active()

    def _on_scroll(self, _x, _y, _dx, _dy):
        """
        Callback for mouse scroll events.
        """
        self._set_active()

    def _on_press(self, _key):
        """
        Callback for keyboard press events.
        """
        self._set_active()

    def _on_release(self, _key):
        """
        Callback for keyboard release events.
        """
        self._set_active()

    def _report_status(self):
        """
        Displays the current user activity status.
        """
        if self._show_status:
            if self._in_working_period:
                app_status = f'{self._green_color}ENFORCED{self._reset_color}'
            else:
                app_status = f'{self._red_color}RELEASED{self._reset_color}'

            if self._is_moved:
                user_status = self._user_active_status
            else:
                user_status = self._user_inactive_status

            app_status_str = f'| {app_status}'
            countdown_str = f'| Inactive in {self._time_left:>6}s'
            user_status_str = f'| {user_status} |'

            self._status_str = ' '.join([
                app_status_str,
                countdown_str,
                user_status_str,
            ])
            print(self._status_str, end='\r')

    def _wait(self):
        """
        Waits for the timeout period while reporting status.
        Also re-checks working period each tick to handle hour boundaries.
        """
        while self._time_left >= 0:
            self._in_working_period = self._check_working_period()
            self._report_status()
            self._time_left -= 1
            time.sleep(1)

    def _move_mouse(self):
        """
        Moves the mouse and clicks to prevent inactivity.
        Only acts during working periods when no user activity was detected.
        Moving to (0,0) and clicking (or moving by distance if already there)
        is required so that Teams transitions from orange back to green.
        """
        if self._in_working_period and not self._is_moved:
            if self._mouse.position != (0, 0):
                self._mouse.position = (0, 0)
                self._mouse.press(mouse.Button.left)
                self._mouse.release(mouse.Button.left)
            else:
                self._mouse.move(
                    self._move_distance,
                    self._move_distance
                )

    def run(self):
        """
        Main loop: monitors inactivity and moves the mouse as needed.
        Continuously alternates between waiting for inactivity and
        simulating activity, respecting configured working periods.
        """
        self._is_moved = False

        while True:
            self._time_left = self._timeout_period

            mouse_listener = mouse.Listener(
                on_move=self._on_move,
                on_click=self._on_click,
                on_scroll=self._on_scroll
            )
            keyboard_listener = keyboard.Listener(
                on_press=self._on_press,
                on_release=self._on_release
            )

            mouse_listener.start()
            keyboard_listener.start()

            self._wait()

            mouse_listener.stop()
            keyboard_listener.stop()
            mouse_listener.join()
            keyboard_listener.join()

            self._in_working_period = self._check_working_period()
            self._move_mouse()
            self._is_moved = False
