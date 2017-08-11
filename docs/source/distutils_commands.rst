.. author KGerring
.. filename distutils_commands
.. date = 7/20/17

=====
Title
=====

from `python setup.py --help-commands`

================  ===================================================================
command           description
================  ===================================================================
build             build everything needed to install
build_py          "build" pure Python modules (copy to build directory)
build_ext         build C/C++ and Cython extensions (compile/link to build directory)
build_clib        build C/C++ libraries used by Python extensions
build_scripts     "build" scripts (copy and fixup #! line)
clean             clean up temporary files from 'build' command
install           install everything from build directory
install_lib       install all Python modules (extensions and pure Python)
install_headers   install C/C++ header files
install_scripts   install scripts (Python or otherwise)
install_data      install data files
sdist             create a source distribution (tarball, zip file, etc.)
register          register the distribution with the Python package index
bdist             create a built (binary) distribution
bdist_dumb        create a "dumb" built distribution
bdist_rpm         create an RPM distribution
bdist_wininst     create an executable installer for MS Windows
check             perform some checks on the package
upload            upload binary package to PyPI
bdist_wheel       create a wheel distribution
build_sphinx      Build Sphinx documentation
alias             define a shortcut to invoke one or more commands
bdist_egg         create an "egg" distribution
develop           install package in 'development mode'
easy_install      Find/get/install Python packages
egg_info          create a distribution's .egg-info directory
install_egg_info  Install an .egg-info directory for the package
rotate            delete older distributions, keeping N newest files
saveopts          save supplied options to setup.cfg or other config file
setopt            set an option in setup.cfg or another config file
test              run unit tests after in-place build
upload_docs       Upload documentation to PyPI
py2app            create a Mac OS X application or plugin from Python scripts
nosetests         Run unit tests using nosetests
isort             Run isort on modules registered in setuptools
compile_catalog   compile message catalogs to binary MO files
extract_messages  extract localizable strings from the project code
init_catalog      create a new catalog based on a POT file
update_catalog    update message catalogs from a POT file
================  ===================================================================








.. |date| date:: %Y-%m-%dT%H:%M:%S

.. [#] This document was generated |date| .
