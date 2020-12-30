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
## @file    mMeco/core/packageLib.py    @brief [ FILE   ] - Package utils.
## @package mMeco.core.packageLib       @brief [ MODULE ] - Package utils.

#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os

import mMeco.fileSystem.directoryLib
import mMeco.fileSystem.versionLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief Get version of a package.
#
#  @param path        [ str  | None | in  ] - Path, where the package is.
#  @param packageName [ str  | None | in  ] - Name of the package.
#  @param version     [ enum | None | in  ] - Requested version from mMeco.fileSystem.versionLib.Version enum class.
#  
#  @exception N/A
#  
#  @return None - If no versioned folder found.
#  @return str  - Versioned folder.
def getVersionOfAPackage(path, packageName, version=mMeco.fileSystem.versionLib.Version.kLatest):

    if not os.path.isdir(path):
        return None

    path = os.path.join(path, packageName)
    if not os.path.isdir(path):
        return None

    versionFolder = mMeco.fileSystem.directoryLib.Directory.listVersionedFolders(directory=path,
                                                                                 absolutePath=False,
                                                                                 semanticOnly=True,
                                                                                 version=version)

    return versionFolder
