import sys
from pathlib import Path


sys.path.insert(0, str(Path.cwd().resolve()))

project = 'empty-contents'
extensions = ['sympy_texinfo_patch']
master_doc = 'index'
exclude_patterns = ['_build']
texinfo_no_detailmenu = True
