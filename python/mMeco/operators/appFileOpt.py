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
## @file    mMeco/operators/appFileOpt.py @brief [ FILE   ] - App file.
## @package mMeco.operators.appFileOpt    @brief [ MODULE ] - App file.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  os
import  json

import  mMeco.core.enumAbs
import  mMeco.core.platformLib

import  mMeco.libs.allLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ ENUM CLASS ] - App file attributes.
class AppFileAttribute(mMeco.core.enumAbs.Enum):

    ## [ str ] - Attribute.
    kDeveloper          = 'developer'

    ## [ str ] - Attribute.
    kDescription        = 'description'

    #

    ## [ str ] - Attribute.
    kDarwinExecutable   = 'darwinExecutable'

    ## [ str ] - Attribute.
    kLinuxExecutable    = 'linuxExecutable'

    ## [ str ] - Attribute.
    kWindowsExecutable  = 'windowsExecutable'

    #

    ## [ str ] - Attribute.
    kGlobalEnvClassName = 'globalEnvClassName'

    ## [ str ] - Attribute.
    kApplication        = 'application'

    ## [ str ] - Attribute.
    kFolderName         = 'folderName'

    ## [ str ] - Attribute.
    kVersion            = 'version'

    ## [ str ] - Attribute.
    kPackages           = 'packages'

#
## @brief [ CLASS ] - Class to operate on App files.
class AppFileOperator(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param path [ str | None | in  ] - Absolute path of an app file.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, path=None):

        ## [ mMeco.libs.allLib.All ] - All.
        self._all                   = mMeco.libs.allLib.All.getInstance(**{'appFileOperator':self})

        ## [ str ] - Absolute path of an app file.
        self._path                  = None

        #

        ## [ str ] - Description.
        self._description           = None

        ## [ str ] - Developer.
        self._developer             = None

        #

        ## [ str ] - Darwin Executable.
        self._darwinExecutable      = None

        ## [ str ] - Linux Executable.
        self._linuxExecutable       = None

        ## [ str ] - Windows Executable.
        self._windowsExecutable     = None

        #

        ## [ str ] - Global env class name.
        self._globalEnvClassName    = None

        ## [ str ] - Folder Name.
        self._application           = None

        ## [ str ] - Folder Name.
        self._folderName            = None

        ## [ str ] - Version.
        self._version               = None

        ## [ str ] - Packages.
        self._packages              = None

        if path:
            self.set(path)

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
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
    def description(self):

        return self._description

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def developer(self):

        return self._developer

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def darwinExecutable(self):

        return self._darwinExecutable

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def linuxExecutable(self):

        return self._linuxExecutable

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def windowsExecutable(self):

        return self._windowsExecutable

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def globalEnvClassName(self):

        return self._globalEnvClassName

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def application(self):

        return self._application

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def folderName(self):

        return self._folderName

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
    def packages(self):

        return self._packages

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Set app file.
    #
    #  @param path [ str | None | in  ] - Absolute path of an app file.
    #
    #  @exception IOError - If given `path` of app file doesn't exist.
    #
    #  @return None - None.
    def set(self, path):

        if not os.path.isfile(path):
            raise IOError('App file doesn\'t exist: {}'.format(path))

        self._path = path

        file = open(path, 'r')
        content = json.loads(file.read())
        file.close()

        for attr in AppFileAttribute.listAttributes(stringOnly=True,
                                                    getValues=True,
                                                    removeK=True):

            if not attr in content:
                continue

            setattr(self, '_{}'.format(attr), content[attr])

    #
    ## @brief Get executable for current platform.
    #
    #  @exception N/A
    #
    #  @return str - Executable.
    def getExecutableForCurrentPlatform(self):

        if mMeco.core.platformLib.Platform.isDarwin():
            return self._darwinExecutable

        elif mMeco.core.platformLib.Platform.isLinux():
            return self._linuxExecutable

        elif mMeco.core.platformLib.Platform.isWindows():
            return self._windowsExecutable


