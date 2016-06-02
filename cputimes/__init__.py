
import sys

if sys.version_info[0] == 2:
	from cputimes import *
else:
	from cputimes.cputimes import *
