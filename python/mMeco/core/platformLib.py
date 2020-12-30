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
## @file    mMeco/core/platformLib.py @brief [ FILE   ] - Platform related classes and functionalities.
## @package mMeco.core.platformLib    @brief [ MODULE ] - Platform related classes and functionalities.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import platform

import mMeco.core.enumAbs


#
# -----------------------------------------------------------------------------------------------------
# CODE
# -----------------------------------------------------------------------------------------------------
#
## @brief [ ENUM CLASS ] - Class contains platform names.
class Name(mMeco.core.enumAbs.Enum):

    ## [ str ] - Darwin.
    kDarwin  = 'Darwin'

    ## [ str ] - Linux.
    kLinux   = 'Linux'

    ## [ str ] - Windows.
    kWindows = 'Windows'

#
## @brief [ CLASS ] - Platform related class.
class Platform(object):
    #
    # ------------------------------------------------------------------------------------------------
    # STATIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Check whether current platform is Windows.
    #
    #  @exception N/A
    #
    #  @return bool - Whether current platform is Windows.
    @staticmethod
    def isWindows():

        return platform.system() == Name.kWindows

    #
    ## @brief Check whether current platform is Windows 10.
    #
    #  @exception N/A
    #
    #  @return bool - Whether current platform is Windows 10.
    @staticmethod
    def isWindows10():

        if platform.system() != Name.kWindows:
            return False

        return int(str(platform.release()).split('.')[:1][0]) > 10

    #
    ## @brief Check whether current platform is Linux.
    #
    #  @exception N/A
    #
    #  @return bool - Whether current platform is Linux.
    @staticmethod
    def isLinux():

        return platform.system() == Name.kLinux

    #
    ## @brief Check whether current platform is OSX.
    #
    #  @exception N/A
    #
    #  @return bool - Whether current platform is OSX.
    @staticmethod
    def isDarwin():

        return platform.system() == Name.kDarwin

    #
    ## @brief Get the name of current platform.
    #
    #  Available names are listed in mMeco.platformLib.Name class.
    #
    #  @exception N/A
    #
    #  @return str - Platform name, one of the following, Darwin, Linux, Windows.
    @staticmethod
    def system():

        return platform.system()

    #
    ## @brief Get all platform names but the current one.
    #
    #  @exception N/A
    #
    #  @return list of str - Platform names.
    @staticmethod
    def getOthers():

        platformList = Name.listAttributes(stringOnly=True,
                                           getValues=True,
                                           removeK=True)

        platformList.pop(platformList.index(Platform.system()))

        return platformList
