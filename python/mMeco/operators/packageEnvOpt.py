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
## @file    mMeco/operators/packageEnvOpt.py @brief [ FILE   ] - Library to operate on package env module.
## @package mMeco.operators.packageEnvOpt    @brief [ MODULE ] - Library to operate on package env module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  os
import  sys

from    importlib import import_module

import  mMeco.libs.allLib

import  mMeco.libs.entryLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
#
## @brief [ CLASS ] - Class to operate on package env module.
class PackageEnvOperator(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param envEntryContainer [ mMeco.libs.entryLib.EnvEntryContainer | None | in  ] - Env envEntry container, which represents a package.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, envEntryContainer=None):

        ## [ mMeco.libs.allLib.All ] - All.
        self._allLib = mMeco.libs.allLib.All.getInstance()

        if envEntryContainer:
            self.invoke(envEntryContainer)

    #
    ## @brief Invoke `setEnvironment` function in env module of the package.
    #
    #  @param envEntryContainer [ mMeco.libs.entryLib.EnvEntryContainer | None | in  ] - Env envEntry container, which represents a package.
    #
    #  @exception N/A
    #
    #  @return True  - If package doesn't have env module.
    #  @return True  - If package env module doesn't have `setEnvironment` function.
    #  @return False - If `setEnvironment` function of the env module of the package returns `False`.
    def invoke(self, envEntryContainer):

        packageEnvFilePath = None

        if envEntryContainer.version():
            packageEnvFilePath = os.path.join(envEntryContainer.path(),
                                              envEntryContainer.packageName(),
                                              envEntryContainer.version(),
                                              envEntryContainer.packageName(),
                                              'python',
                                              envEntryContainer.packageName(),
                                              'packageEnvLib.py')
        else:
            packageEnvFilePath = os.path.join(envEntryContainer.path(),
                                              envEntryContainer.packageName(),
                                              'python',
                                              envEntryContainer.packageName(),
                                              'packageEnvLib.py')

        if not os.path.isfile(packageEnvFilePath):
            return True

        #
        packagePythonPath       = None
        packagePythonPathAdded  = False

        if envEntryContainer.version():
            packagePythonPath = os.path.join(envEntryContainer.path(),
                                             envEntryContainer.packageName(),
                                             envEntryContainer.version(),
                                             envEntryContainer.packageName(),
                                             'python')
        else:
            packagePythonPath = os.path.join(envEntryContainer.path(),
                                             envEntryContainer.packageName(),
                                             'python')

        if not packagePythonPath in sys.path:
            sys.path.append(packagePythonPath)

        module = import_module('{}.packageEnvLib'.format(envEntryContainer.packageName()))

        if not hasattr(module, 'setEnvironment'):
            if packagePythonPathAdded:
                sys.path.pop()
            return True

        result = getattr(module, 'setEnvironment')(self._allLib, envEntryContainer)

        if packagePythonPathAdded:
            sys.path.pop()

        return result