#!/usr/bin/env python

from distutils.core import setup

import time

r = 1
v = time.strftime("%Y%m%d%H%M")

projectname = "achilles"

setup(
  name=projectname,
  version=v,
  url="https://repo.zoidtechnologies.com/%s/" % (projectname),
  author="zoid technologies",
  author_email="%s@projects.zoidtechnologies.com" % (projectname),
  py_modules=["libachilles", "achilles"],
  requires=["ttyio5", "bbsengine5", "python-barcode"],
  scripts=["achilles"],
  license="GPLv3+",
  provides=[projectname],
  classifiers=[
    "Programming Language :: Python :: 3.9",
    "Environment :: Console",
    "Development Status :: 4 - Beta",
    "Intended Audience :: End Users",
    "Operating System :: POSIX",
    "Topic :: Terminals",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3+)",
    "Topic :: Communications :: BBS"
  ],
  long_description = """achilles -- tracking use of MSG and related ingredients.""",
  command_options = {
    "build_sphinx": {
      "project": projectname,
      "version": v,
      "release": r,
      "source_dir": ( "setup.py", "doc/" )
    }
  }
)
