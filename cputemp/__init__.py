
import sys

if sys.version_info[0] == 2:
	from cputemp import *
else:
	from cputemp.cputemp import *


