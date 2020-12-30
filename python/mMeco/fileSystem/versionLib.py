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
## @file    mMeco/fileSystem/versionLib.py @brief [ FILE   ] - Version classes.
## @package mMeco.fileSystem.versionLib    @brief [ MODULE ] - Version classes.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import mMeco.core.enumAbs


#
# -----------------------------------------------------------------------------------------------------
# CODE
# -----------------------------------------------------------------------------------------------------
#
## @brief [ ENUM CLASS ] - Versions.
class Version(mMeco.core.enumAbs.Enum):

    ## [ str ] - All.
    kAll        = 'all'

    ## [ str ] - Latest.
    kLatest     = 'latest'

    ## [ str ] - Current.
    kCurrent    = 'current'

    ## [ str ] - First.
    kFirst      = 'first'

    ## [ str ] - Last.
    kLast       = 'last'

    ## [ str ] - Previous.
    kPrevious   = 'previous'
