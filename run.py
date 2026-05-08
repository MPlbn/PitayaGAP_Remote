import os
os.sched_setaffinity(0, {2})

import GUI

GUI.run()