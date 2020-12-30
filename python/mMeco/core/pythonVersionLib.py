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
## @file    mMeco/core/pythonVersionLib.py @brief [ FILE   ] - Python version.
## @package mMeco.core.pythonVersionLib    @brief [ MODULE ] - Python version.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
from sys import version_info


#
# -----------------------------------------------------------------------------------------------------
# CODE
# -----------------------------------------------------------------------------------------------------
#
## @brief Whether its Python 2.
#
#  @exception N/A
#
#  @return bool - Result.
def isPython2():

    return version_info[0] == 2

#
## @brief Whether its Python 3.
#
#  @exception N/A
#
#  @return bool - Result.
def isPython3():

    return version_info[0] == 3

