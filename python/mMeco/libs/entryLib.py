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
## @file    mMeco/libs/entryLib.py @brief [ FILE   ] - Entry.
## @package mMeco.libs.entryLib    @brief [ MODULE ] - Entry.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
import sys

import mMeco.libs.allLib
import mMeco.libs.enumLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Env envEntry container.
#
#  Class to contain mMeco.libs.entryLib.EnvEntry class instances.
class EnvEntryContainer(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param containerType [ enum | None | in  ] - Env envEntry container type from mMeco.libs.enumLib.EnvEntryContainerType enum class.
    #  @param path          [ str  | None | in  ] - Path of the package.
    #  @param packageName   [ str  | None | in  ] - Name of the package.
    #  @param version       [ str  | None | in  ] - Version of the package.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self,
                 containerType=mMeco.libs.enumLib.EnvEntryContainerType.kPackage,
                 path=None,
                 packageName=None,
                 version=None):

        ## [ mMeco.libs.allLib.All ] - All libraries.
        self._allLib        = mMeco.libs.allLib.All.getInstance()

        ## [ enum ] - Container type from mMeco.libs.enumLib.EnvEntryContainerType enum class.
        self._type          = containerType

        ## [ str ] - Path.
        self._path          = path

        ## [ str ] - Package name.
        self._packageName   = packageName

        ## [ str ] - Version.
        self._version       = version

        ## [ list of dict ] - Env entries.
        self._entries       = []

    #
    ## @brief String representation.
    #
    #  @exception N/A
    #
    #  @return str - String representation.
    def __str__(self):

        return self.asStr()

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.libs.enumLib.EnvEntryContainerType - Value.
    def type(self):

        return self._type

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def path(self):

        return self._path

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def packageName(self):

        return self._packageName

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def version(self):

        return self._version

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def entries(self):

        return self._entries

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Get string representation of the class.
    #
    #  @exception N/A
    #
    #  @return str - Information about the package in human readable form.
    def asStr(self):

        data = '\nEnv Entry Container'
        data = '{}\nType             : {}'.format(data, self._type)
        data = '{}\nPath             : {}'.format(data, self._path if self._path else 'N/A')
        data = '{}\nPackage Name     : {}'.format(data, self._packageName if self._packageName else 'N/A')
        data = '{}\nVersion          : {}'.format(data, self._version if self._version else 'N/A')

        return data

    #
    ## @brief Display entries.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def displayEntries(self):

        sys.stdout.write('\n{}\n'.format(self._type.upper()))

        for entry in self._entries:
            sys.stdout.write(entry)
            sys.stdout.write('\n')

    #
    ## @brief Get root path of the package (if applicable) that represented by this instance.
    #
    #  @exception N/A
    #
    #  @return str  - Root path of the package.
    #  @return None - If this instance doesn't represent a package.
    def getPackageRootPath(self):

        if self._type != mMeco.libs.enumLib.EnvEntryContainerType.kPackage:
            return None

        rootPath = os.path.join(self._path, self._packageName)

        if self._version:
            rootPath = os.path.join(rootPath, self._version, self._packageName)

        return rootPath

    #
    ## @brief Add command.
    #
    #  @param command [ str | None | in  ] - Command.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def addCommand(self, command):

        if self._allLib.request().ignoreEnvCommands():
            
            setBy = ''

            if self._type == mMeco.libs.enumLib.EnvEntryContainerType.kPackage:
                setBy = os.path.join(self._path, self._packageName)
            else:
                setBy = self._type

            self._allLib.logger().addWarning('The following command is ignored, which set by {}: {}'.format(setBy, command))

        else:

            self._entries.append(EnvEntry(mMeco.libs.enumLib.EnvEntryType.kCommand, command))

    #
    ## @brief Add script.
    #
    #  @param scriptPath [ str | None | in  ] - Absolute path of a script.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def addScript(self, scriptPath):

        if self._allLib.request().ignoreEnvScripts():

            setBy = ''

            if self._type == mMeco.libs.enumLib.EnvEntryContainerType.kPackage:
                setBy = os.path.join(self._path, self._packageName)
            else:
                setBy = self._type

            self._allLib.logger().addWarning('The following scripts is ignored, which set by {}: {}'.format(setBy, scriptPath))

        else:

            self._entries.append(EnvEntry(mMeco.libs.enumLib.EnvEntryType.kScript, scriptPath))

    #
    ## @brief Add single env variable.
    #
    #  @param variable [ str | None | in  ] - Name.
    #  @param value    [ str | None | in  ] - Value.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def addSingle(self, variable, value):

        self._entries.append(EnvEntry(mMeco.libs.enumLib.EnvEntryType.kSingle, value, variable))

    #
    ## @brief Add multi env variable.
    #
    #  @param variable [ str | None | in  ] - Name.
    #  @param value    [ str | None | in  ] - Value.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def addMulti(self, variable, value):

        self._entries.append(EnvEntry(mMeco.libs.enumLib.EnvEntryType.kMulti, value, variable))

    #
    ## @brief Sort entries.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def sort(self):

        self._entries.sort(key=lambda x: (x.variable() if x.variable() else x.value()))

#
## @brief [ CLASS ] - Env envEntry.
#
#  Single env envEntry, which meant to be contained by mMeco.libs.entryLib.EnvEntry.EnvEntryContainer class.
class EnvEntry(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param envEntryType [ enum | None | in  ] - Env envEntry type from mMeco.libs.enumLib.EnvEntryType enum class.
    #  @param value        [ str  | None | in  ] - Environment variable.
    #  @param variable     [ str  | None | in  ] - Value of the environment variable.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, envEntryType, value, variable=''):

        ## [ enum ] - Type from `mMeco.libs.enumLib.EnvEntryType` enum class.
        self._type      = envEntryType

        ## [ str ] - Environment variable.
        self._variable  = variable

        ## [ str ] - Value of the environment variable.
        self._value     = value

    #
    ## @brief String representation.
    #
    #  @exception N/A
    #
    #  @return str - String representation.
    def __str__(self):

        return self.asStr()

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.libs.entryLib.EnvEntryType - Value.
    def envEntryType(self):

        return self._type

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def variable(self):

        return self._variable

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def value(self):

        return self._value

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Get string representation of the class.
    #
    #  @exception N/A
    #
    #  @return str - Information about the package in human readable form.
    def asStr(self):

        data = '\nEnv Entry'
        data = '{}\nEnv Entry Type   : {}'.format(data, self._type)
        data = '{}\nVariable & Value : {} - {}'.format(data, self._variable if self._variable else 'N/A',
                                                       self._value if self._value else 'N/A')

        return data


