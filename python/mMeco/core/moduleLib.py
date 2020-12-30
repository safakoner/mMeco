#
# Copyright 2020 Safak Oner.
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ----------------------------------------------------------------------------------------------------
# DESCRIPTION
# ----------------------------------------------------------------------------------------------------
## @file    mMeco/core/moduleLib.py @brief [ FILE   ] - Operate on Python modules.
## @package mMeco.core.moduleLib    @brief [ MODULE ] - Operate on Python modules.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  os
import  glob

from    importlib import import_module


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Class to operate on Python modules.
class Module(object):
    #
    # ------------------------------------------------------------------------------------------------
    # STATIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief List Python module files.
    #
    #  @param path          [ str  | False | in  ] - Path.
    #  @param absolutePath  [ bool | False | in  ] - Whether to return absolute path of the Python module files.
    #  @param withExtension [ bool | False | in  ] - Whether to return files with extension when `absolutePath` is `False`.
    #
    #  @exception IOError - If given `path` doesn't exist.
    #  
    #  @return generator - Files.
    @staticmethod
    def listFiles(path, absolutePath=False, withExtension=False):
        
        if not os.path.isdir(path):
            raise IOError('Path doesn\'t exist: {}'.format(path))

        for file in glob.glob('{}/*.py'.format(path)):

            if file.endswith('__.py'):
                continue

            if absolutePath:
                yield file
            else:
                if withExtension:
                    yield os.path.basename(file)
                else:
                    yield os.path.splitext(os.path.basename(file))[0]

    #
    ## @brief List Python modules.
    #
    #  @param path       [ str | None | in  ] - Path of the Python modules, which will be imported and listed.
    #  @param importPath [ str | None | in  ] - Modules will be imported with the path if provided.
    #
    #  @exception N/A
    #
    #  @return generator - Modules.
    @staticmethod
    def listModules(path, importPath=None):

        for file in Module.listFiles(path):

            if importPath:
                yield import_module(importPath.format(file))
            else:
                yield import_module(file)
