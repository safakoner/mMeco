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
## @file    mMeco/core/displayLib.py @brief [ FILE   ] - Display functionalities.
## @package mMeco.core.displayLib    @brief [ MODULE ] - Display functionalities.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import sys

import mMeco.core.enumAbs
import mMeco.core.platformLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ ENUM CLASS ] - Display color names enum class.
class ColorName(mMeco.core.enumAbs.Enum):

    ## [ str ] - Header line color name.
    kHeaderLine = 'kHeaderLine'

    ## [ str ] - Header color name.
    kHeaderText = 'kHeaderText'

    #

    ## [ str ] - Info color name.
    kInfo       = 'kInfo'

    ## [ str ] - Success color name.
    kSuccess    = 'kSuccess'

    ## [ str ] - Warning color name.
    kWarning    = 'kWarning'

    ## [ str ] - Failure color name.
    kFailure    = 'kFailure'

#
## @brief [ ENUM CLASS ] - Display color enum class for Mac OS platform.
class DarwinColor(mMeco.core.enumAbs.Enum):

    ## [ str ] - Header line color.
    kHeaderLine = '\033[0;37m{}\033[0m'

    ## [ str ] - Header color.
    kHeaderText = '\033[0;97m{}\033[0m'

    #

    ## [ str ] - Info color.
    kInfo       = '\033[0;94m{}\033[0m'

    ## [ str ] - Success color.
    kSuccess    = '\033[0;32m{}\033[0m'

    ## [ str ] - Warning color.
    kWarning    = '\033[0;33m{}\033[0m'

    ## [ str ] - Failure color.
    kFailure    = '\033[0;31m{}\033[0m'

#
## @brief [ ENUM CLASS ] - Display color enum class for Linux OS platform.
class LinuxColor(mMeco.core.enumAbs.Enum):

    ## [ str ] - Header line color.
    kHeaderLine = '\033[0;37m{}\033[0m'

    ## [ str ] - Header color.
    kHeaderText = '\033[0;97m{}\033[0m'

    #

    ## [ str ] - Info color.
    kInfo       = '\033[0;94m{}\033[0m'

    ## [ str ] - Success color.
    kSuccess    = '\033[0;32m{}\033[0m'

    ## [ str ] - Warning color.
    kWarning    = '\033[0;33m{}\033[0m'

    ## [ str ] - Failure color.
    kFailure    = '\033[0;31m{}\033[0m'

#
## @brief [ ENUM CLASS ] - Display color enum class for legacy Windows OS platform.
class WindowsLegacyColor(mMeco.core.enumAbs.Enum):

    ## [ str ] - Header line color.
    kHeaderLine = '{}'

    ## [ str ] - Header color.
    kHeaderText = '{}'

    #

    ## [ str ] - Info color.
    kInfo       = '{}'

    ## [ str ] - Success color.
    kSuccess    = '{}'

    ## [ str ] - Warning color.
    kWarning    = '{}'

    ## [ str ] - Failure color.
    kFailure    = '{}'

#
## @brief [ ENUM CLASS ] - Display color enum class for legacy Windows OS platform.
class WindowsColor(mMeco.core.enumAbs.Enum):

    ## [ str ] - Header line color.
    kHeaderLine = '{}'

    ## [ str ] - Header color.
    kHeaderText = '{}'

    #

    ## [ str ] - Info color.
    kInfo       = '{}'

    ## [ str ] - Success color.
    kSuccess    = '{}'

    ## [ str ] - Warning color.
    kWarning    = '{}'

    ## [ str ] - Failure color.
    kFailure    = '{}'

#
## @brief Display class.
class Display(object):
    #
    # ------------------------------------------------------------------------------------------------
    # STATIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Display given text in info format.
    #
    #  @param text         [ str, list, tuple   | None  | in  ] - Text to be displayed.
    #  @param startNewLine [ bool               | True  | in  ] - Display blank line at the start.
    #  @param endNewLine   [ bool               | True  | in  ] - Display blank line at the end.
    #  @param useColor     [ bool               | False | in  ] - Use color to display the text.
    #
    #  @exception N/A
    #
    #  @return None - None.
    @staticmethod
    def displayInfo(text, startNewLine=True, endNewLine=True, useColor=True):

        Display.display(text=text,
                        startNewLine=startNewLine,
                        endNewLine=endNewLine,
                        useColor=useColor,
                        color=Display.getDisplayColor(ColorName.kInfo),
                        out=sys.stdout)

    #
    ## @brief Display given text in success format.
    #
    #  @param text         [ str, list, tuple   | None  | in  ] - Text to be displayed.
    #  @param startNewLine [ bool               | True  | in  ] - Display blank line at the start.
    #  @param endNewLine   [ bool               | True  | in  ] - Display blank line at the end.
    #  @param useColor     [ bool               | False | in  ] - Use color to display the text.
    #
    #  @exception N/A
    #
    #  @return None - None.
    @staticmethod
    def displaySuccess(text, startNewLine=True, endNewLine=True, useColor=True):

        Display.display(text=text,
                        startNewLine=startNewLine,
                        endNewLine=endNewLine,
                        useColor=useColor,
                        color=Display.getDisplayColor(ColorName.kSuccess),
                        out=sys.stdout)

    #
    ## @brief Display given text in warning format.
    #
    #  @param text         [ str, list, tuple   | None  | in  ] - Text to be displayed.
    #  @param startNewLine [ bool               | True  | in  ] - Display blank line at the start.
    #  @param endNewLine   [ bool               | True  | in  ] - Display blank line at the end.
    #  @param useColor     [ bool               | False | in  ] - Use color to display the text.
    #
    #  @exception N/A
    #
    #  @return None - None.
    @staticmethod
    def displayWarning(text, startNewLine=True, endNewLine=True, useColor=True):

        Display.display(text=text,
                        startNewLine=startNewLine,
                        endNewLine=endNewLine,
                        useColor=useColor,
                        color=Display.getDisplayColor(ColorName.kWarning),
                        out=sys.stdout)

    #
    ## @brief Display given text in failure format.
    #
    #  @param text         [ str, list, tuple   | None  | in  ] - Text to be displayed.
    #  @param startNewLine [ bool               | True  | in  ] - Display blank line at the start.
    #  @param endNewLine   [ bool               | True  | in  ] - Display blank line at the end.
    #  @param useColor     [ bool               | False | in  ] - Use color to display the text.
    #  @param stdErr       [ bool               | False | in  ] - Whether to use sys.stderr instead of sys.stdout.
    #
    #  @exception N/A
    #
    #  @return None - None.
    @staticmethod
    def displayFailure(text, startNewLine=True, endNewLine=True, useColor=True, stdErr=False):

        Display.display(text=text,
                        startNewLine=startNewLine,
                        endNewLine=endNewLine,
                        useColor=useColor,
                        color=Display.getDisplayColor(ColorName.kFailure),
                        out=sys.stderr if stdErr else sys.stdout)

    #
    ## @brief Display header line.
    #
    #  @param text         [ str, list, tuple   | None | in  ] - Text to be displayed.
    #  @param startNewLine [ bool               | True | in  ] - Display blank line at the start.
    #  @param endNewLine   [ bool               | True | in  ] - Display blank line at the end.
    #  @param useColor     [ bool               | True | in  ] - Use color to display the text.
    #
    #  @exception N/A
    #
    #  @return None - None.
    @staticmethod
    def displayHeaderLine(text, startNewLine=True, endNewLine=True, useColor=True):

        Display.display(text=text,
                        startNewLine=startNewLine,
                        endNewLine=endNewLine,
                        useColor=useColor,
                        color=Display.getDisplayColor(ColorName.kHeaderLine))

    #
    ## @brief Display header text.
    #
    #  @param text         [ str, list, tuple   | None  | in  ] - Text to be displayed.
    #  @param startNewLine [ bool               | False | in  ] - Display blank line at the start.
    #  @param endNewLine   [ bool               | False | in  ] - Display blank line at the end.
    #  @param useColor     [ bool               | True  | in  ] - Use color to display the text.
    #
    #  @exception N/A
    #
    #  @return None - None.
    @staticmethod
    def displayHeaderText(text, startNewLine=False, endNewLine=False, useColor=True):

        Display.display(text=text,
                        startNewLine=startNewLine,
                        endNewLine=endNewLine,
                        useColor=useColor,
                        color=Display.getDisplayColor(ColorName.kHeaderText))

    #
    ## @brief Display given text by using file like object.
    #
    #  @param text         [ str, list, tuple | None       | in  ] - Text to be displayed.
    #  @param startNewLine [ bool             | True       | in  ] - Display blank line at the start.
    #  @param endNewLine   [ bool             | True       | in  ] - Display blank line at the end.
    #  @param useColor     [ bool             | False      | in  ] - Use color to display the text. This argument does nothing if `color` is not provided.
    #  @param color        [ bool             | False      | in  ] - Text to format the color (like ANSI).
    #  @param out          [ file             | sys.stdout | in  ] - sys.stdout or sys.stderr
    #
    #  @exception N/A
    #
    #  @return None - None.
    @staticmethod
    def display(text, startNewLine=True, endNewLine=True, useColor=True, color=None, out=sys.stdout):

        if isinstance(text, (list, tuple)):
            text = ' '.join([str(x) for x in text])

        if useColor and color:
            text = color.format(text)

        if startNewLine:
            text = '\n{}'.format(text)

        if endNewLine:
            text = '{}\n'.format(text)

        out.write(text)

    #
    ## @brief Display given text by using stdout.
    #
    #  @param text         [ str, list, tuple | None       | in  ] - Text to be displayed.
    #  @param startNewLine [ bool             | True       | in  ] - Display blank line at the start.
    #  @param endNewLine   [ bool             | True       | in  ] - Display blank line at the end.
    #
    #  @exception N/A
    #
    #  @return None - None.
    @staticmethod
    def displayStdOut(text, startNewLine=True, endNewLine=True):

        Display.display(text, startNewLine=True, endNewLine=True, useColor=False, color=None, out=sys.stdout)

    #
    ## @brief Display given text by using stderr.
    #
    #  @param text         [ str, list, tuple | None       | in  ] - Text to be displayed.
    #  @param startNewLine [ bool             | True       | in  ] - Display blank line at the start.
    #  @param endNewLine   [ bool             | True       | in  ] - Display blank line at the end.
    #
    #  @exception N/A
    #
    #  @return None - None.
    @staticmethod
    def displayStdErr(text, startNewLine=True, endNewLine=True):

        Display.display(text, startNewLine=True, endNewLine=True, useColor=False, color=None, out=sys.stderr)

    #
    ## @brief Display blank lines by giving counts.
    #
    #  @param count [ int  | 1          | in  ] - How many blank lines will be displayed.
    #  @param out   [ file | sys.stdout | in  ] - sys.stdout or sys.stderr
    #
    #  @exception N/A
    #
    #  @return None - None.
    @staticmethod
    def displayBlankLine(count=1, out=sys.stdout):

        out.write('\n' * count)

    #
    ## @brief Get display color string for given `color` based on current platform.
    #
    #  @param color [ enum | None | in  ] - Any value from mMeco.displayLib.DisplayColorName enum class.
    #
    #  @exception N/A
    #
    #  @return str - Color.
    @staticmethod
    def getDisplayColor(color):

        displayColorClass = LinuxColor

        if mMeco.core.platformLib.Platform.isDarwin():
            displayColorClass = DarwinColor

        elif mMeco.core.platformLib.Platform.isWindows10():
            displayColorClass = WindowsColor

        else:
            displayColorClass = WindowsLegacyColor

        return displayColorClass.getValueFromAttributeName(color)



