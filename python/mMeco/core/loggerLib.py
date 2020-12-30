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
## @file    mMeco/core/loggerLib.py @brief [ FILE   ] - Logger.
## @package mMeco.core.loggerLib    @brief [ MODULE ] - Logger.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os

import mMeco.core.displayLib
import mMeco.core.dateTimeLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ ENUM CLASS ] - Log types.
class LogType(object):

    ## [ enum ] - Info.
    kInfo    = 'INFO'

    ## [ enum ] - Success.
    kSuccess = 'SUCCESS'

    ## [ enum ] - Warning.
    kWarning = 'WARNING'

    ## [ enum ] - Failure.
    kFailure = 'FAILURE'

#
## @brief [ CLASS ] - Log.
class Log(LogType):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param message [ str  | None                               | in  ] - Message.
    #  @param logType [ enum | mMeco.core.loggerLib.LogType.kInfo | in  ] - Log type from mMeco.core.loggerLib.LogType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, message, logType=LogType.kInfo):

        ## [ str ] - Message.
        self._message       = message

        ## [ str ] - Full message with time stamp.
        self._fullMessage   = ''

        ## [ enum ] - Log type from `mMeco.core.loggerLib.LogType` enum class.
        self._logType       = logType
        
        #
        self._setFullMessage()

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
    # PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Set full message.
    #  
    #  @exception N/A
    #  
    #  @return None - None.
    def _setFullMessage(self):

        self._fullMessage = '{} - {} - {}'.format(mMeco.core.dateTimeLib.getDateTimeStamp(),
                                                  self._logType,
                                                  self._message)

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

        data = '{} - {}'.format(self._logType, self._fullMessage)

        return data

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return enum - Value.
    def logType(self):

        return self._logType

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def message(self):

        return self._message

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def fullMessage(self):

        return self._fullMessage

#
## @brief [ CLASS ] - Logger.
class Logger(mMeco.core.displayLib.Display):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param logFile [ str | None | in  ] - Absolute path of a log file.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, logFile=None):
        
        ## [ str ] - Absolute path of a log file.
        self._file          = logFile

        ## [ list of mMeco.core.loggerLib.LogType ] - Logs.
        self._logs          = []
        
        ## [ bool ] - Whether a failure has been logged.
        self._hasFailure    = False
        
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
    def file(self):

        return self._file

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def hasFailure(self):

        return self._hasFailure

    #
    ## @brief Set log file.
    #
    #  @param logFile         [ str  | None | in  ] - Absolute path of a log file.
    #  @param discardExisting [ bool | None | in  ] - Discard existing log file, therefore do not append and create a new log file.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def setFile(self, logFile, discardExisting=True):

        self._file = logFile

        if discardExisting and os.path.isfile(self._file):
            os.remove(self._file)

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Add info.
    #
    #  @param message [ str | None | in  ] - Message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def addInfo(self, message):

        self._logs.append(Log(message,
                              LogType.kInfo))

        self.write()

    #
    ## @brief Add success.
    #
    #  @param message [ str | None | in  ] - Message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def addSuccess(self, message):

        self._logs.append(Log(message,
                              LogType.kSuccess))

        self.write()

    #
    ## @brief Add warning.
    #
    #  @param message [ str | None | in  ] - Message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def addWarning(self, message):

        self._logs.append(Log(message,
                              LogType.kWarning))

        self.write()

    #
    ## @brief Add failure.
    #
    #  @param message [ str | None | in  ] - Message.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def addFailure(self, message):

        self._hasFailure = True

        self._logs.append(Log(message,
                              LogType.kFailure))

        self.write()

    #
    ## @brief Get last failure.
    #
    #  @exception N/A
    #
    #  @return mMeco.loggerLib.Log  - Log.
    #  @return None                 - If no failure has been logged.
    def getLastFailure(self):

        if not self._hasFailure:
            return None

        return [x for x in self._logs if x.logType() == LogType.kFailure][-1:][0]

    #
    ## @brief Display last failure.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def displayLastFailure(self):

        lastFailure = self.getLastFailure()
        if not lastFailure:
            return

        self.displayFailure(lastFailure.fullMessage())

    #
    ## @brief Write the log into log file.
    #
    #  @param append [ bool | False | in  ] - Append to log file.
    #
    #  @exception N/A
    #
    #  @return str  - Absolute path of the log file.
    def write(self, append=False):

        if not self._file:
            pass

        if not self._logs:
            self.addInfo('No log has been added.')
            return None

        _file = open(self._file, 'a' if append else 'w')

        for log in self._logs:

            _file.write('{}\n'.format(str(log)))

        _file.close()

        return self._file

