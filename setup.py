#!/usr/bin/env python
# -*- mode: python; indent-tabs-mode: nil; tab-width: 3 -*-
# vim: set tabstop=3 shiftwidth=3 expandtab:
#
# Copyright (C) 2001-2005 Ichiro Fujinaga, Michael Droettboom,
#                         and Karl MacMillan
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
import sys, os, glob, datetime, platform
from distutils.sysconfig import get_python_lib
from distutils.command.install import INSTALL_SCHEMES

# # unfortunately this does not help installing data_files
# # to the same dir as gamera :(
# for scheme in INSTALL_SCHEMES.values():
#     scheme['data'] = scheme['purelib']

#sys.exit(0)

if sys.hexversion < 0x02030000:
   print "At least Python 2.3 is required to build Gamera.  You have"
   print sys.version
   sys.exit(1)

cross_compiling = False

# We do this first, so that when gamera.__init__ loads gamera.__version__,
# it is in fact the new and updated version
gamera_version = open("version", 'r').readlines()[0].strip()
has_openmp = None
i = 0
for argument in sys.argv:
   i = i + 1
   if argument=="--dated_version":
      d = datetime.date.today()
      monthstring = str(d.month)
      daystring = str(d.day)
      if d.month < 10:
         monthstring = '0' + monthstring
      if d.day < 10:
         daystring = '0' + daystring
      gamera_version = "2_nightly_%s%s%s" % (d.year, monthstring, daystring)
      sys.argv.remove(argument)
      break
   elif argument == '--compiler=mingw32_cross':
      import mingw32_cross_compile
      sys.argv[sys.argv.index('--compiler=mingw32_cross')] = '--compiler=mingw32'
      cross_compiling = True
   elif argument == '--openmp=yes':
       has_openmp = True
   elif argument == '--openmp=no':
       has_openmp = False
open("gamera/__version__.py", "w").write("ver = '%s'\n\n" % gamera_version)
print "Gamera version:", gamera_version

# query OpenMP (parallelization) support and save it to compile time config file
if has_openmp is None:
    has_openmp = False
    if platform.system() == "Linux":
        p = os.popen("gcc -dumpversion","r")
        gccv = p.readline().strip().split(".")
        p.close()
        if int(gccv[0]) >= 4 and int(gccv[1]) >= 3:
            has_openmp = True
f = open("gamera/__compiletime_config__.py", "w")
f.write("# automatically generated configuration at compile time\n")
if has_openmp:
    f.write("has_openmp = True\n")
    print "Compiling genetic algorithms with parallelization (OpenMP)"
else:
    f.write("has_openmp = False\n")
    print "Compiling genetic algorithms without parallelization (OpenMP)"
f.close()

from distutils.core import setup, Extension
from gamera import gamera_setup

##########################################
# generate the command line startup scripts
command_line_utils = (
   ('gamera_gui', 'gamera_gui.py',
    """#!%(executable)s
%(header)s
print "Loading GAMERA..."
print "Use 'gamera_gui --help' to display command line options"
import sys
try:
   from gamera.config import config
   from gamera.gui import gui
   config.parse_args(sys.argv[1:])
   gui.run()
except Exception, e:
   if not isinstance(e, (SystemExit, KeyboardInterrupt)):
     import traceback
     import textwrap
     print "Gamera made the following fatal error:"
     print
     print textwrap.fill(str(e))
     print
     print "=" * 75
     print "The traceback is below.  Please send this to the Gamera developers"
     print "if you feel you got here in error."
     print "-" * 75
     traceback.print_exc()
     print "=" * 75
   if sys.platform == "win32":
     print
     print "Press <ENTER> to exit."
     x = raw_input()
   """), )

if sys.platform == 'win32':
   command_line_filename_at = 1
   scripts_directory_name = "Scripts"
else:
   command_line_filename_at = 0
   scripts_directory_name = "bin/"

info = {'executable': sys.executable,
        'header'    :
        """# This file was automatically generated by the\n"""
        """# Gamera setup script on %s.\n""" % sys.platform}
for util in command_line_utils:
   if sys.platform == 'win32':
      _, file, content = util
   else:
      file, _, content = util
   fd = open(file, 'w')
   fd.write(content % info)
   fd.close()
os.chmod(file, 0700)

scripts = [x[command_line_filename_at] for x in command_line_utils] + ['gamera_post_install.py']

##########################################
# generate the plugins
plugin_extensions = []
plugins = gamera_setup.get_plugin_filenames('gamera/plugins/')
plugin_extensions = gamera_setup.generate_plugins(
   plugins, "gamera.plugins", True)

########################################
# Non-plugin extensions

eodev_files = glob.glob("src/eodev/*.cpp") + glob.glob("src/eodev/*/*.cpp")
eodev_dir = glob.glob("src/eodev/*")
eodev_includes = ["src/eodev"]
for entry in eodev_dir:
   if os.path.isdir(entry):
      eodev_includes.append(entry)

graph_files = glob.glob("src/graph/*.cpp") + glob.glob("src/graph/graphmodule/*.cpp")
kdtree_files = ["src/kdtreemodule.cpp", "src/geostructs/kdtree.cpp"]

if has_openmp:
    ExtGA = Extension("gamera.knnga",
                      ["src/knngamodule.cpp"] + eodev_files,
                      include_dirs=["include", "src"] + eodev_includes,
                      libraries=["stdc++"],
                      extra_compile_args=["-Wall", "-fopenmp"],
                      extra_link_args=["-fopenmp"]
                      )
else:
    ExtGA = Extension("gamera.knnga",
                      ["src/knngamodule.cpp"] + eodev_files,
                      include_dirs=["include", "src"] + eodev_includes,
                      libraries=["stdc++"],
                      extra_compile_args=["-Wall"]
                      )


extensions = [Extension("gamera.gameracore",
                        ["src/gameramodule.cpp",
                         "src/sizeobject.cpp",
                         "src/pointobject.cpp",
                         "src/floatpointobject.cpp",
                         "src/dimobject.cpp",
                         "src/rectobject.cpp",
                         "src/regionobject.cpp",
                         "src/regionmapobject.cpp",
                         "src/rgbpixelobject.cpp",
                         "src/imagedataobject.cpp",
                         "src/imageobject.cpp",
                         "src/imageinfoobject.cpp",
                         "src/iteratorobject.cpp"
                         ],
                        include_dirs=["include"],
                        **gamera_setup.extras
                        ),
              Extension("gamera.knncore", 
                        ["src/knncoremodule.cpp"],
                        include_dirs=["include", "src"],
                        **gamera_setup.extras
                        ),
              ExtGA,
              Extension("gamera.graph", graph_files,
                        include_dirs=["include", "src", "include/graph", "src/graph/graphmodule"],
                        **gamera_setup.extras),
              Extension("gamera.kdtree", kdtree_files,
                        include_dirs=["include", "src", "include/geostructs"],
                        **gamera_setup.extras)]
extensions.extend(plugin_extensions)

##########################################
# Here's the basic distutils stuff

# read versions from compile computer
pythonversion = "%d.%d" % (sys.version_info[0],sys.version_info[1])
import wx
wx_version_info = wx.__version__.split(".")
wxversion = "%s.%s" % (wx_version_info[0],wx_version_info[1])
description = ("This is the Gamera installer.\n" + \
               "\tPlease ensure that Python " + pythonversion + \
               " and wxPython " + wxversion + "\n" + \
               "\tare installed before proceeding.")

includes = [(os.path.join(gamera_setup.include_path, path),
             glob.glob(os.path.join("include", os.path.join(path, ext))))
            for path, ext in
            ("", "*.hpp"),
            ("plugins", "*.hpp"),
            ("vigra", "*.hxx"),
            ("geostructs", "*.hpp"),
            ("graph", "*.hpp")]

srcfiles = [(os.path.join(gamera_setup.lib_path,path),
             glob.glob(os.path.join(path, ext)))
            for path, ext in
            [("src/geostructs", "*.cpp"), ("src/graph", "*.cpp")]]

packages = ['gamera', 'gamera.gui', 'gamera.gui.gaoptimizer', 'gamera.plugins',
            'gamera.toolkits', 'gamera.backport']

if sys.hexversion >= 0x02040000:
   data_files = includes
   package_data = {"gamera": ["test/*.tiff"]}
else:
   data_files = [(os.path.join(gamera_setup.lib_path, "$LIB/test"),
                  glob.glob("gamera/test/*.tiff"))] + includes
   package_data = {}

data_files += srcfiles

if sys.platform == 'darwin':
   packages.append("gamera.mac")

setup(cmdclass = gamera_setup.cmdclass,
      name = "gamera",
      version = gamera_version,
      url = "http://gamera.sourceforge.net/",
      author = "Michael Droettboom and Christoph Dalitz",
      author_email = "gamera-devel@yahoogroups.com",
      ext_modules = extensions,
      description = description,
      packages = packages,
      scripts = scripts,
      package_data = package_data,
      data_files = data_files
      )

