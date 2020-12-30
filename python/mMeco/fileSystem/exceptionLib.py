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
## @file    mMeco/fileSystem/exceptionLib.py @brief [ FILE   ] - Exception module.
## @package mMeco.fileSystem.exceptionLib    @brief [ MODULE ] - Exception module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
#
# DIRECTORY
#
## @brief [ EXCEPTION CLASS ] - Directory is not set.
class DirectoryIsNotSet(Exception):

    pass

#
## @brief [ EXCEPTION CLASS ] - Directory already exists.
class DirectoryAlreadyExists(Exception):

    pass

#
#
# FILE
#
## @brief [ EXCEPTION CLASS ] - File is not set.
class FileIsNotSet(Exception):

    pass

#
## @brief [ EXCEPTION CLASS ] - File doesn't exist.
class FileDoesNotExist(Exception):

    pass
#
## @brief [ EXCEPTION CLASS ] - File already exists.
class FileAlreadyExists(Exception):

    pass
