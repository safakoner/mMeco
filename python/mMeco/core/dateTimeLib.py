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
## @file    mMeco/core/dateTimeLib.py @brief [ FILE   ] - Functionalities to operate with date and time.
## @package mMeco.core.dateTimeLib    @brief [ MODULE ] - Functionalities to operate with date and time.
#
# @code
#
#import mMeco.dateTimeLib
#
#mMeco.dateTimeLib.getDateIntList()
# #[2013, 10, 6]
#
#mMeco.dateTimeLib.getTimeIntList()
# #[20, 50, 34]
#
#mMeco.dateTimeLib.getDateStrList()
# #['2013', '10', '06']
#
#mMeco.dateTimeLib.getTimeStrList()
# #['19', '31', '59']
#
#mMeco.dateTimeLib.getDateTimeForFileSystem()
# #2013.05.20_19.32.22
#
#mMeco.dateTimeLib.getDateStamp()
# #2013.04.13
#
#mMeco.dateTimeLib.getTimeStamp()
# #19:33:05
#
#mMeco.dateTimeLib.getDateTimeStamp()
# #2013.02.11 - 19:33:20
#
# @endcode

#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
from datetime import datetime


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief Get date as int list in [YYYY, MM, DD] format.
#
#  @exception N/A
#
#  @return list of int - Date.
def getDateIntList():

    return [datetime.now().year, datetime.now().month, datetime.now().day]

#
## @brief Get time as int list in [HH, MM, SS] format.
#
#  @exception N/A
#
#  @return list of int - Time.
def getTimeIntList():

    return [datetime.now().hour, datetime.now().minute, datetime.now().second]

#
## @brief Get date as string list in [YYYY, MM, DD] format.
#
#  @exception N/A
#
#  @return list of str - Date.
def getDateStrList():

    date = getDateIntList()

    return ['{0:04d}'.format(date[0]), '{0:02d}'.format(date[1]), '{0:02d}'.format(date[2])]

#
## @brief Get time as string list in [HH, MM, SS] format.
#
#  @exception N/A
#
#  @return list of str - Time.
def getTimeStrList():

    time = getTimeIntList()

    return ['{0:02d}'.format(time[0]), '{0:02d}'.format(time[1]), '{0:02d}'.format(time[2])]

#
## @brief Get date and time as single string in "YYYY.MM.DD_HH.MM.SS" format.
#
#  @exception N/A
#
#  @return str - Date and time.
def getDateTimeForFileSystem():

    date = getDateStrList()
    time = getTimeStrList()

    return str('{}.{}.{}_{}.{}.{}').format(date[0], date[1], date[2], time[0], time[1], time[2])

#
## @brief Get date as string in "YYYY.MM.DD" format.
#
#  @exception N/A
#
#  @return str - Date.
def getDateStamp():

    date = getDateStrList()

    return str('{}.{}.{}').format(date[0], date[1], date[2])

#
## @brief Get time as string in "HH:MM:SS" format.
#
#  @exception N/A
#
#  @return str - Time.
def getTimeStamp():

    time = getTimeStrList()

    return str('{}:{}:{}').format(time[0], time[1], time[2])

#
## @brief Get date and time as single string in "YYYY.MM.DD - HH:MM:SS" format.
#
#  @exception N/A
#
#  @return str - Date and time.
def getDateTimeStamp():

    date = getDateStrList()
    time = getTimeStrList()

    return str('{}.{}.{} - {}:{}:{}').format(date[0], date[1], date[2], time[0], time[1], time[2])
