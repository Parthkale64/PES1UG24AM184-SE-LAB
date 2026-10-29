# Issues in the starter

Line numbers refer to the original gym_system.py at starter commit a2af42b.

| Issue | Type | Line(s) | Description | Fix approach |
| --- | --- | --- | --- | --- |
| Shell command | Security / High | 36 | Bandit B605 flagged a filename prefix passed into a shell command. | Match literal filenames in the current directory and unlink matching JSON files. |
| Shared log | Correctness | 8, 15 | Pylint W0102 found a default list retained across calls. | Default to None and append only when the caller supplies a log. |
| Bare exception | Reliability | 19-22 | Pylint W0702 and Flake8 E722 flagged cancellation catching every exception. | Catch KeyError for a missing class and ValueError for a missing member. |
| Open export file | Reliability | 31-33 | Pylint R1732 and W1514 flagged an unmanaged file and implicit encoding. | Write JSON inside a with block using explicit UTF-8 encoding. |
| Function spacing | Style | 8-58 | Flake8 E302 and E305 found nine places with a missing blank line. | Use two blank lines around top-level functions. |
| Capacity check | Booking logic | 9-14 | The demo admitted a fourth member to a three-seat class and created an unlisted class. | Check class membership first and reject bookings when the roster reaches capacity. |
