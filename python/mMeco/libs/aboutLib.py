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
## @file    mMeco/libs/aboutLib.py @brief [ FILE   ] - About.
## @package mMeco.libs.aboutLib    @brief [ MODULE ] - About.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import mMeco.packageInfoLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
## [ int ] - Major version.
VERSION_MAJOR   = int(mMeco.packageInfoLib.VERSION.split('.')[0])

## [ int ] - Minor version.
VERSION_MINOR   = int(mMeco.packageInfoLib.VERSION.split('.')[1])

## [ int ] - Fix version.
VERSION_FIX     = int(mMeco.packageInfoLib.VERSION.split('.')[2])

## [ str ] - Release date of the version.
DATE            = '2021-01-01'

## [ str ] - Name.
NAME            = 'MECO'

## [ str ] - Author.
__author__      = 'Safak Oner'

## [ str ] - Version.
__version__     = mMeco.packageInfoLib.VERSION


#
# ----------------------------------------------------------------------------------------------------
# FUNCTIONS
# ----------------------------------------------------------------------------------------------------
#
## @brief Get version.
#
#  @exception N/A
#
#  @return str - Version.
def getVersion():

    return __version__

#
## @brief Get version and date.
#
#  @exception N/A
#
#  @return str - Version and date.
def getVersionAndDate():

    return '{} - {}'.format(__version__, DATE)

#
## @brief Get name, version and date.
#
#  @exception N/A
#
#  @return str - Name, version and date.
def getNameVersionDate():

    return '{} {} - {}'.format(NAME, __version__, DATE)

#
## @brief Get information about Meco.
#
#  @exception N/A
#
#  @return str - Information.
def getAboutInformation():

    info = 'MECO - Package and Environment Management Ecosystem'
    info = '{}\n{} - {}'.format(info, __version__, DATE)

    info = '{}\n\nBy Safak Oner'.format(info)
    info = '{}\nsafak@safakoner.com'.format(info)

    info = '{}\n\nhttps://meco.safakoner.com'.format(info)
    info = '{}\n\nhttps://www.safakoner.com'.format(info)
    info = '{}\nhttps://twitter.com/safakoner'.format(info)
    info = '{}\nhttps://blog.safakoner.com'.format(info)
    info = '{}\nhttps://github.com/safakoner/mMeco\n'.format(info)

    return info



