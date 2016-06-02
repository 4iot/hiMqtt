
import sys

if sys.version_info[0] == 2:
	from meminfo import *
else:
	from meminfo.meminfo import *

