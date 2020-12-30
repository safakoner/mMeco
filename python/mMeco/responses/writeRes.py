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
## @file    mMeco/responses/writeRes.py @brief [ FILE   ] - Response.
## @package mMeco.responses.writeRes    @brief [ MODULE ] - Response.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  os

import  mMeco.abstract.responseAbs

import  mMeco.core.platformLib

import  mMeco.libs.aboutLib
import  mMeco.libs.enumLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Response class.
class Response(mMeco.abstract.responseAbs.Response):
    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC STATIC MEMBERS
    # ------------------------------------------------------------------------------------------------
    ## [ str ] - Name.
    NAME        = 'writeRes'

    ## [ int ] - Padding.
    PADDING_1   = 30

    ## [ int ] - Padding.
    PADDING_2   = 42

    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self):

        mMeco.abstract.responseAbs.Response.__dict__['__init__'](self)

    #
    # ------------------------------------------------------------------------------------------------
    # PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Write the env into a script file.
    #
    #  @exception N/A
    #
    #  @return str - Absolute path of the script file.
    def _write(self):

        path = os.path.dirname(self._allLib.settingsOperator().scriptFilePath())
        if not os.path.isdir(path):
            os.makedirs(path)

        file = open(self._allLib.settingsOperator().scriptFilePath(), 'w')

        file.writelines(self._scriptFileStartEnv)

        if not self._allLib.request().setOnly():
            file.writelines(self._preBuiltDisplay)
            file.writelines(self._reservedDisplay)
            file.writelines(self._developmentDisplay)
            file.writelines(self._stageDisplay)
            file.writelines(self._projectInternalDisplay)
            file.writelines(self._projectExternalDisplay)
            file.writelines(self._masterProjectInternalDisplay)
            file.writelines(self._masterProjectExternalDisplay)
            file.writelines(self._postBuiltDisplay)
            file.writelines(self._envDisplay)
            file.writelines(self._infoDisplay)
            file.writelines(self._productInfoDisplay)
            pass

        if not self._allLib.request().displayOnly():
            file.writelines(self._preBuiltEnv)
            file.writelines(self._reservedEnv)
            file.writelines(self._developmentEnv)
            file.writelines(self._stageEnv)
            file.writelines(self._projectInternalEnv)
            file.writelines(self._projectExternalEnv)
            file.writelines(self._masterProjectInternalEnv)
            file.writelines(self._masterProjectExternalEnv)
            file.writelines(self._postBuiltEnv)
            file.writelines(self._envEnv)

        file.writelines(self._scriptFileEndEnv)

        file.close()

        return self._allLib.settingsOperator().scriptFilePath()

    #
    #
    #
    ## @brief Add script file start.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addScriptFileStartEnv(self):

        if mMeco.core.platformLib.Platform.isWindows():

            self._scriptFileStartEnv.append('function script:_mecoInitializeEnv()\n')
            self._scriptFileStartEnv.append('{\n')

            self._scriptFileStartEnv.append('    if($env:MECO_ES_VERSION)\n')

            self._scriptFileStartEnv.append('    {\n')

            self._scriptFileStartEnv.append('        Write-Host "Meco environment has already been initialized on this shell, please initialize Meco environment on a new shell or exit first.";\n')


            self._scriptFileStartEnv.append('        return 1;\n')

            self._scriptFileStartEnv.append('    }\n\n')

        else:

            self._scriptFileStartEnv.append('function _mecoInitializeEnv()\n')
            self._scriptFileStartEnv.append('{\n')

            self._scriptFileStartEnv.append('    if [[ "$MECO_ES_VERSION" ]]; then\n')

            self._scriptFileStartEnv.append('        echo "";\n')

            self._scriptFileStartEnv.append('        printf "Meco environment has already been initialized on this shell, please initialize Meco environment on a new shell or exit first.";\n')

            self._scriptFileStartEnv.append('        echo "";\n')

            self._scriptFileStartEnv.append('        return 1;\n')

            self._scriptFileStartEnv.append('    fi\n\n')

    #
    ## @brief Add script file end.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addScriptFileEndEnv(self):

        if mMeco.core.platformLib.Platform.isWindows():

            self._scriptFileEndEnv.append('\n}\n')
            self._scriptFileEndEnv.append('_mecoInitializeEnv\n')

        else:

            self._scriptFileEndEnv.append('\n}\n')
            self._scriptFileEndEnv.append('_mecoInitializeEnv\n')

    #
    ## @brief Add multi env.
    #
    #  @param envEntry  [ mMeco.libs.entryLib.EnvEntry  | None | in  ] - Env envEntry.
    #  @param envType   [ enum                          | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addMultiEnv(self, envEntry, envType):

        if self._allLib.request().displayOnly():
            return

        value = ''

        if mMeco.core.platformLib.Platform.isWindows():
            value = '$env:{}="{};$env:{}";\n'.format(envEntry.variable(), envEntry.value(), envEntry.variable())
        else:
            value = 'export {}={}:${};\n'.format(envEntry.variable(), envEntry.value(), envEntry.variable())

        self._getEnvByEnvType(envType).append(value)

    #
    ## @brief Add single env.
    #
    #  @param envEntry  [ mMeco.libs.entryLib.EnvEntry  | None | in  ] - Env envEntry.
    #  @param envType   [ enum                          | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addSingleEnv(self, envEntry, envType):

        if self._allLib.request().displayOnly():
            return

        value = ''

        if mMeco.core.platformLib.Platform.isWindows():
            value = '$env:{}="{}";\n'.format(envEntry.variable(), envEntry.value())
        else:
            value = 'export {}={};\n'.format(envEntry.variable(), envEntry.value())

        self._getEnvByEnvType(envType).append(value)

    #
    ## @brief Add command env.
    #
    #  @param envEntry  [ mMeco.libs.entryLib.EnvEntry  | None | in  ] - Env envEntry.
    #  @param envType   [ enum                          | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addCommandEnv(self, envEntry, envType):

        if self._allLib.request().displayOnly():
            return

        value = envEntry.value()

        if not value.endswith(';'):
            value = '{};\n'.format(value)
        else:
            value = '{}\n'.format(value)

        self._getEnvByEnvType(envType).append(value)

    #
    ## @brief Add script env.
    #
    #  @param envEntry  [ mMeco.libs.entryLib.EnvEntry  | None | in  ] - Env entry.
    #  @param envType   [ enum                          | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addScriptEnv(self, envEntry, envType):

        if self._allLib.request().displayOnly():
            return

        value = ''

        if mMeco.core.platformLib.Platform.isWindows():
            value = '. {};\n'.format(envEntry.value())
        else:
            value = 'source {};\n'.format(envEntry.value())

        self._getEnvByEnvType(envType).append(value)

    #
    ## @brief Add app env.
    #
    #  @param envType [ enum | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addAppEnv(self, envType):

        if not self._allLib.settingsOperator().appFilePath():
            return

        if self._allLib.request().ignoreAppExec():
            return

        appArgs = self._allLib.request().appArgs()
        if not appArgs:
            appArgs = ''

        appExecutableFlags = self._allLib.callbackOperator().invokeGetAppExecutableFlags()
        if not appExecutableFlags:
            appExecutableFlags = ''

        if mMeco.core.platformLib.Platform.isWindows():
            self._getEnvByEnvType(envType).append('& "{}" {} {};\n'.format(self._allLib.appFileOperator().getExecutableForCurrentPlatform(),
                                                                           appExecutableFlags,
                                                                           appArgs
                                                                           )
                                                  )
        else:
            self._getEnvByEnvType(envType).append('{} {} {};\n'.format(self._allLib.appFileOperator().getExecutableForCurrentPlatform(),
                                                                       appExecutableFlags,
                                                                       appArgs
                                                                       )
                                                  )

    #
    #
    #
    ## @brief Get new line.
    #
    #  @exception N/A
    #
    #  @return str - New line.
    def _getNewLine(self):

        if mMeco.core.platformLib.Platform.isWindows():
            return 'Write-Host "";'
        else:
            return 'echo "";\n'

    #
    ## @brief Add new line display.
    #
    #  @param envType [ enum | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addNewLineDisplay(self, envType):

        if self._allLib.request().setOnly():
            return

        newLine = ''

        if mMeco.core.platformLib.Platform.isWindows():
            newLine = 'Write-Host "";'
        else:
            newLine = 'echo "";\n'

        self._getDisplayByEnvType(envType).append(newLine)

    #
    ## @brief Add new line display.
    #
    #  @param envType   [ enum | None  | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #  @param sub       [ bool | False | in  ] - Whether this title is subtitle.
    #  @param str       [ str | None | in  ] - Title.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addHeaderDisplay(self, envType, sub=False, title=None):

        if self._allLib.request().setOnly():
            return

        line1   = '-' * 100
        line2   = '-' * 100

        title = title.upper() if title else envType.upper()

        if mMeco.core.platformLib.Platform.isWindows():
            if not sub:
                line1 = 'Write-Host "{}" -NoNewline -ForegroundColor {};\n'.format(line1, self._allLib.settingsOperator().terminalHeaderDisplayColor()[0])
                title = 'Write-Host "{}" -NoNewline -ForegroundColor {};\n'.format(title, self._allLib.settingsOperator().terminalHeaderDisplayColor()[1])
                line2 = 'Write-Host "{}" -NoNewline -ForegroundColor {};\n'.format(line2, self._allLib.settingsOperator().terminalHeaderDisplayColor()[0])
            else:
                pass

        else:
            if not sub:
                line1 = 'printf {}\n'.format(self._allLib.settingsOperator().terminalHeaderDisplayColor()[0].format(line1))
                title = 'printf {}\n'.format(self._allLib.settingsOperator().terminalHeaderDisplayColor()[1].format(title))
                line2 = 'printf {}\n'.format(self._allLib.settingsOperator().terminalHeaderDisplayColor()[0].format(line2))
            else:
                line1  = '    {}'.format('-' * 96)
                title = '    {}'.format(title)
                line1 = 'printf {}\n'.format(self._allLib.settingsOperator().terminalHeaderDisplayColor()[0].format(line1))
                title = 'printf {}\n'.format(self._allLib.settingsOperator().terminalHeaderDisplayColor()[1].format(title))
                line2 = 'printf {}\n'.format(self._allLib.settingsOperator().terminalHeaderDisplayColor()[0].format(line1))

        value = [
                 line1,
                 self._getNewLine(),
                 title,
                 self._getNewLine(),
                 line2,
                 self._getNewLine()
                ]

        display = self._getDisplayByEnvType(envType)
        display.append(self._getNewLine())
        display.extend(value)

    #
    ## @brief Add container display.
    #
    #  @param envEntryContainer [ mMeco.libs.entryLib.EnvEntryContainer | None | in  ] - Env entry container class instance.
    #  @param envType           [ enum                                  | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addContainerDisplay(self, envEntryContainer, envType):

        if self._allLib.request().setOnly():
            return

        colorVariable = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kPackageVariable, envType)
        colorArrow    = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kArrow, envType)
        colorValue    = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kPackageValue, envType)

        variable = '{}{}'.format(envEntryContainer.packageName(),
                                 ' - {}'.format(envEntryContainer.version()) if envEntryContainer.version() else '')

        variableAndValueDisplay = ''

        if mMeco.core.platformLib.Platform.isWindows():
            variableAndValueDisplay = 'Write-Host "{}" -NoNewline -ForegroundColor {};Write-Host "{} " -NoNewline -ForegroundColor {};Write-Host "{}" -NoNewline -ForegroundColor {};\n'
            variableAndValueDisplay = variableAndValueDisplay.format(variable.ljust(Response.PADDING_1),
                                                                     colorVariable,
                                                                     '>',
                                                                     colorArrow,
                                                                     envEntryContainer.getPackageRootPath(),
                                                                     colorValue
                                                                     )
        else:
            variableAndValueDisplay = 'printf "{}{} {}";\n'.format(colorVariable.format(variable.ljust(Response.PADDING_1)),
                                                                   colorArrow.format('>'),
                                                                   colorValue.format(envEntryContainer.getPackageRootPath())
                                                                   )

        self._getDisplayByEnvType(envType).append(variableAndValueDisplay)

        self._addNewLineDisplay(envType)

    #
    ## @brief Add multi display.
    #
    #  @param envEntry [ mMeco.libs.entryLib.EnvEntry | None | in  ] - Env entry class instance.
    #  @param envType  [ enum                         | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addMultiDisplay(self, envEntry, envType):

        if self._allLib.request().setOnly():
            return

        if not envType in [mMeco.libs.enumLib.EnvType.kPreBuild,
                           mMeco.libs.enumLib.EnvType.kPostBuild] and \
           not self._allLib.request().verbose() in [2, 3, 4]:
            return

        colorVariable = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kMultiVariable, envType)
        colorColon    = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kColon, envType)
        colorValue    = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kMultiValue, envType)

        value = ''

        if mMeco.core.platformLib.Platform.isWindows():

            value = 'Write-Host "{}" -NoNewline -ForegroundColor {};Write-Host "{} " -NoNewline -ForegroundColor {};Write-Host "{}" -NoNewline -ForegroundColor {};\n'
            value = value.format(envEntry.variable().ljust(Response.PADDING_1),
                                 colorVariable,
                                 ':',
                                 colorColon,
                                 envEntry.value(),
                                 colorValue
                                 )

        else:

            value = 'printf "{}";\n'.format('{}{} {}'.format(colorVariable.format(envEntry.variable().ljust(Response.PADDING_1)),
                                                             colorColon.format(':'),
                                                             colorValue.format(envEntry.value())
                                                             )
                                            )

        self._getDisplayByEnvType(envType).append(value)
        self._addNewLineDisplay(envType)

    #
    ## @brief Add single display.
    #
    #  @param envEntry [ mMeco.libs.entryLib.EnvEntry | None | in  ] - Env entry class instance.
    #  @param envType  [ enum                         | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addSingleDisplay(self, envEntry, envType):

        if self._allLib.request().setOnly():
            return

        if not envType in [mMeco.libs.enumLib.EnvType.kPreBuild,
                           mMeco.libs.enumLib.EnvType.kPostBuild] and \
           not self._allLib.request().verbose() in [2, 3, 4]:
            return

        padding = Response.PADDING_1
        if envType in [mMeco.libs.enumLib.EnvType.kPreBuild,mMeco.libs.enumLib.EnvType.kPostBuild]:
            padding = Response.PADDING_2

        colorVariable = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kSingleVariable, envType)
        colorColon    = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kColon, envType)
        colorValue    = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kSingleValue, envType)

        value = ''

        if mMeco.core.platformLib.Platform.isWindows():

            value = 'Write-Host "{}" -NoNewline -ForegroundColor {};Write-Host "{} " -NoNewline -ForegroundColor {};Write-Host "{}" -NoNewline -ForegroundColor {};\n'
            value = value.format(envEntry.variable().ljust(padding),
                                 colorVariable,
                                 ':',
                                 colorColon,
                                 envEntry.value(),
                                 colorValue
                                 )

        else:

            value = 'printf "{}{} {}";'.format(colorVariable.format(envEntry.variable().ljust(padding)),
                                               colorColon.format(':'),
                                               colorValue.format(envEntry.value()))

        self._getDisplayByEnvType(envType).append(value)
        self._addNewLineDisplay(envType)

    #
    ## @brief Add command display.
    #
    #  @param envEntry [ mMeco.libs.entryLib.EnvEntry | None | in  ] - Env entry class instance.
    #  @param envType  [ enum                         | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addCommandDisplay(self, envEntry, envType):

        if self._allLib.request().setOnly():
            return

        if envType in [mMeco.libs.enumLib.EnvType.kPreBuild, mMeco.libs.enumLib.EnvType.kPostBuild] and \
            not self._allLib.request().verbose() in [4]:
            return

        if not envType in [mMeco.libs.enumLib.EnvType.kPreBuild, mMeco.libs.enumLib.EnvType.kPostBuild] and \
           not self._allLib.request().verbose() in [3, 4]:
                return

        colorValue = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kCommand, envType)

        value = ''

        if mMeco.core.platformLib.Platform.isWindows():

            value = 'Write-Host "{}" -NoNewline -ForegroundColor {};\n'.format(envEntry.value(), colorValue)

        else:

            value = 'printf "{}";\n'.format(colorValue.format(envEntry.value()))

        self._getDisplayByEnvType(envType).append(value)
        self._addNewLineDisplay(envType)

    #
    ## @brief Add script display.
    #
    #  @param envEntry [ mMeco.libs.entryLib.EnvEntry | None | in  ] - Env entry class instance.
    #  @param envType  [ enum                         | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addScriptDisplay(self, envEntry, envType):

        if self._allLib.request().setOnly():
            return

        if envType in [mMeco.libs.enumLib.EnvType.kPreBuild, mMeco.libs.enumLib.EnvType.kPostBuild] and \
            not self._allLib.request().verbose() in [4]:
            return

        if not envType in [mMeco.libs.enumLib.EnvType.kPreBuild, mMeco.libs.enumLib.EnvType.kPostBuild] and \
           not self._allLib.request().verbose() in [3, 4]:
                return

        colorValue = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kCommand, envType)

        value = ''

        if mMeco.core.platformLib.Platform.isWindows():

            value = 'Write-Host "{}" -NoNewline -ForegroundColor {};\n'.format(envEntry.value(), colorValue)

        else:

            value = 'printf "{}";\n'.format(colorValue.format(envEntry.value()))

        self._getDisplayByEnvType(envType).append(value)
        self._addNewLineDisplay(envType)

    #
    ## @brief Add app display.
    #
    #  @param envType [ enum | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addAppDisplay(self, envType):

        if not self._allLib.settingsOperator().appFilePath():
            return

        colorVariable = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kSingleVariable, envType)
        colorColon    = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kColon, envType)
        colorValue    = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kSingleValue, envType)

        description         = self._allLib.appFileOperator().description()        if self._allLib.appFileOperator().description()         else 'N/A'
        globalEnvClassName  = self._allLib.appFileOperator().globalEnvClassName() if self._allLib.appFileOperator().globalEnvClassName()  else 'N/A'
        application         = self._allLib.appFileOperator().application()        if self._allLib.appFileOperator().application()         else 'N/A'
        folderName          = self._allLib.appFileOperator().folderName()         if self._allLib.appFileOperator().folderName()          else 'N/A'
        version             = self._allLib.appFileOperator().version()            if self._allLib.appFileOperator().version()             else 'N/A'

        launchInfo   = ' (Launching...)'
        if self._allLib.request().ignoreAppExec():
            launchInfo   = ' (App executable is ignored)'

        description = '{}{}'.format(description, launchInfo)

        display = self._getDisplayByEnvType(envType)

        if mMeco.core.platformLib.Platform.isWindows():

            valueTemplate = 'Write-Host "{}" -NoNewline -ForegroundColor {};Write-Host "{} " -NoNewline -ForegroundColor {};Write-Host "{}" -NoNewline -ForegroundColor {};\n'

            value = valueTemplate.format('App File'.ljust(35),
                                         colorVariable,
                                         ':',
                                         colorColon,
                                         self._allLib.settingsOperator().appFilePath(),
                                         colorValue
                                         )

            display.append(value)
            self._addNewLineDisplay(envType)

            value = valueTemplate.format('Description'.ljust(35),
                                         colorVariable,
                                         ':',
                                         colorColon,
                                         description,
                                         colorValue
                                         )

            display.append(value)
            self._addNewLineDisplay(envType)

            value = valueTemplate.format('Global Env Class Name'.ljust(35),
                                         colorVariable,
                                         ':',
                                         colorColon,
                                         globalEnvClassName,
                                         colorValue
                                         )

            display.append(value)
            self._addNewLineDisplay(envType)

            value = valueTemplate.format('Application'.ljust(35),
                                         colorVariable,
                                         ':',
                                         colorColon,
                                         application,
                                         colorValue
                                         )

            display.append(value)
            self._addNewLineDisplay(envType)

            value = valueTemplate.format('Folder Name'.ljust(35),
                                         colorVariable,
                                         ':',
                                         colorColon,
                                         folderName,
                                         colorValue
                                         )

            display.append(value)
            self._addNewLineDisplay(envType)

            value = valueTemplate.format('Version'.ljust(35),
                                         colorVariable,
                                         ':',
                                         colorColon,
                                         version,
                                         colorValue
                                         )

            display.append(value)
            self._addNewLineDisplay(envType)

        else:

            display.append('printf "{} {} {}";\n'.format(colorVariable.format('App File').ljust(35),
                                                                 colorColon.format(':'),
                                                                 colorValue.format(self._allLib.settingsOperator().appFilePath())
                                                                 )
                           )
            self._addNewLineDisplay(envType)

            display.append('printf "{} {} {}";\n'.format(colorVariable.format('Description').ljust(35),
                                                                 colorColon.format(':'),
                                                                 colorValue.format(description)
                                                                 )
                           )
            self._addNewLineDisplay(envType)

            display.append('printf "{} {} {}";\n'.format(colorVariable.format('Global Env Class Name').ljust(35),
                                                                 colorColon.format(':'),
                                                                 colorValue.format(globalEnvClassName)
                                                                 )
                           )
            self._addNewLineDisplay(envType)

            display.append('printf "{} {} {}";\n'.format(colorVariable.format('Application').ljust(35),
                                                                 colorColon.format(':'),
                                                                 colorValue.format(application)
                                                                 )
                           )
            self._addNewLineDisplay(envType)

            display.append('printf "{} {} {}";\n'.format(colorVariable.format('Folder Name').ljust(35),
                                                                 colorColon.format(':'),
                                                                 colorValue.format(folderName)
                                                                 )
                           )
            self._addNewLineDisplay(envType)

            display.append('printf "{} {} {}";\n'.format(colorVariable.format('Version').ljust(35),
                                                                 colorColon.format(':'),
                                                                 colorValue.format(version)
                                                                 )
                           )
            self._addNewLineDisplay(envType)

    #
    ## @brief Add info display.
    #
    #  @param envType [ enum | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addInfoDisplay(self, envType):

        display = self._getDisplayByEnvType(envType)

        colorVariable = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kSingleVariable, envType)
        colorColon    = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kColon, envType)
        colorValue    = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kSingleValue, envType)

        if mMeco.core.platformLib.Platform.isWindows():
            
            if self._allLib.builder().reservedEnvEntryContainers():
                value = 'Write-Host "{}" -NoNewline -ForegroundColor {};Write-Host "{} " -NoNewline -ForegroundColor {};Write-Host "{}" -NoNewline -ForegroundColor {};\n'
                value = value.format('Reserved Packages ({})'.format(self._allLib.settingsOperator().projectNameInUse()).ljust(Response.PADDING_2),
                                     colorVariable,
                                     ':',
                                     colorColon,
                                     len(self._allLib.builder().reservedEnvEntryContainers()),
                                     colorValue
                                     )

                display.append(value)
                self._addNewLineDisplay(envType)

            if self._allLib.builder().developmentEnvEntryContainers():
                value = 'Write-Host "{}" -NoNewline -ForegroundColor {};Write-Host "{} " -NoNewline -ForegroundColor {};Write-Host "{}" -NoNewline -ForegroundColor {};\n'
                value = value.format('Development Packages ({})'.format(self._allLib.settingsOperator().projectNameInUse()).ljust(Response.PADDING_2),
                                     colorVariable,
                                     ':',
                                     colorColon,
                                     len(self._allLib.builder().developmentEnvEntryContainers()),
                                     colorValue
                                     )

                display.append(value)
                self._addNewLineDisplay(envType)

            if self._allLib.builder().stageEnvEntryContainers():
                value = 'Write-Host "{}" -NoNewline -ForegroundColor {};Write-Host "{} " -NoNewline -ForegroundColor {};Write-Host "{}" -NoNewline -ForegroundColor {};\n'
                value = value.format('Stage Packages ({})'.format(self._allLib.settingsOperator().stage()).ljust(Response.PADDING_2),
                                     colorVariable,
                                     ':',
                                     colorColon,
                                     len(self._allLib.builder().stageEnvEntryContainers()),
                                     colorValue
                                     )

                display.append(value)
                self._addNewLineDisplay(envType)

            if self._allLib.builder().projectInternalEnvEntryContainers():
                value = 'Write-Host "{}" -NoNewline -ForegroundColor {};Write-Host "{} " -NoNewline -ForegroundColor {};Write-Host "{}" -NoNewline -ForegroundColor {};\n'
                value = value.format('Project Internal Packages ({})'.format(self._allLib.settingsOperator().projectNameInUse()).ljust(Response.PADDING_2),
                                     colorVariable,
                                     ':',
                                     colorColon,
                                     len(self._allLib.builder().projectInternalEnvEntryContainers()),
                                     colorValue
                                     )

                display.append(value)
                self._addNewLineDisplay(envType)

            if self._allLib.builder().projectExternalEnvEntryContainers():
                value = 'Write-Host "{}" -NoNewline -ForegroundColor {};Write-Host "{} " -NoNewline -ForegroundColor {};Write-Host "{}" -NoNewline -ForegroundColor {};\n'
                value = value.format('Project External Packages ({})'.format(self._allLib.settingsOperator().projectNameInUse()).ljust(Response.PADDING_2),
                                     colorVariable,
                                     ':',
                                     colorColon,
                                     len(self._allLib.builder().projectExternalEnvEntryContainers()),
                                     colorValue
                                     )

                display.append(value)
                self._addNewLineDisplay(envType)

            if self._allLib.builder().masterProjectInternalEnvEntryContainers():
                value = 'Write-Host "{}" -NoNewline -ForegroundColor {};Write-Host "{} " -NoNewline -ForegroundColor {};Write-Host "{}" -NoNewline -ForegroundColor {};\n'
                value = value.format('Master Project Internal Packages ({})'.format(self._allLib.settingsOperator().masterProjectName()).ljust(Response.PADDING_2),
                                     colorVariable,
                                     ':',
                                     colorColon,
                                     len(self._allLib.builder().masterProjectInternalEnvEntryContainers()),
                                     colorValue
                                     )

                display.append(value)
                self._addNewLineDisplay(envType)

            if self._allLib.builder().masterProjectExternalEnvEntryContainers():
                value = 'Write-Host "{}" -NoNewline -ForegroundColor {};Write-Host "{} " -NoNewline -ForegroundColor {};Write-Host "{}" -NoNewline -ForegroundColor {};\n'
                value = value.format('Master Project External Packages ({})'.format(self._allLib.settingsOperator().masterProjectName()).ljust(Response.PADDING_2),
                                     colorVariable,
                                     ':',
                                     colorColon,
                                     len(self._allLib.builder().masterProjectExternalEnvEntryContainers()),
                                     colorValue
                                     )

                display.append(value)
                self._addNewLineDisplay(envType)

        else:

            if self._allLib.builder().reservedEnvEntryContainers():
                display.append('printf "{}{} {}"\n'.format(colorVariable.format('Reserved Packages ({})' \
                                                                                .format(self._allLib.settingsOperator().projectNameInUse()).ljust(Response.PADDING_2)),
                                                           colorColon.format(':'),
                                                           colorValue.format(len(self._allLib.builder().reservedEnvEntryContainers())))
                               )
                self._addNewLineDisplay(envType)

            if self._allLib.builder().developmentEnvEntryContainers():
                display.append('printf "{}{} {}"\n'.format(colorVariable.format('Development Packages ({})' \
                                                                                .format(self._allLib.settingsOperator().projectNameInUse()).ljust(Response.PADDING_2)),
                                                           colorColon.format(':'),
                                                           colorValue.format(len(self._allLib.builder().developmentEnvEntryContainers())))
                               )
                self._addNewLineDisplay(envType)

            if self._allLib.builder().stageEnvEntryContainers():
                display.append('printf "{}{} {}"\n'.format(colorVariable.format('Stage Packages ({})' \
                                                                                .format(self._allLib.request().stage()).ljust(Response.PADDING_2)),
                                                           colorColon.format(':'),
                                                           colorValue.format(len(self._allLib.builder().stageEnvEntryContainers())))
                               )
                self._addNewLineDisplay(envType)

            #

            if self._allLib.builder().projectInternalEnvEntryContainers():
                display.append('printf "{}{} {}"\n'.format(colorVariable.format('Project Internal Packages ({})' \
                                                                                .format(self._allLib.settingsOperator().projectNameInUse()).ljust(Response.PADDING_2)),
                                                           colorColon.format(':'),
                                                           colorValue.format(len(self._allLib.builder().projectInternalEnvEntryContainers())))
                               )
                self._addNewLineDisplay(envType)

            if self._allLib.builder().projectExternalEnvEntryContainers():
                display.append('printf "{}{} {}"\n'.format(colorVariable.format('Project External Packages ({})' \
                                                                                .format(self._allLib.settingsOperator().projectNameInUse()).ljust(Response.PADDING_2)),
                                                           colorColon.format(':'),
                                                           colorValue.format(len(self._allLib.builder().projectExternalEnvEntryContainers())))
                               )
                self._addNewLineDisplay(envType)
            #

            if self._allLib.builder().masterProjectInternalEnvEntryContainers():
                display.append('printf "{}{} {}"\n'.format(colorVariable.format('Master Project Internal Packages ({})' \
                                                                                .format(self._allLib.settingsOperator().masterProjectName()).ljust(Response.PADDING_2)),
                                                           colorColon.format(':'),
                                                           colorValue.format(len(self._allLib.builder().masterProjectInternalEnvEntryContainers()))
                                                           )
                               )
                self._addNewLineDisplay(envType)

            if self._allLib.builder().masterProjectExternalEnvEntryContainers():
                display.append('printf "{}{} {}"\n'.format(colorVariable.format('Master Project External Packages ({})' \
                                                                                .format(self._allLib.settingsOperator().masterProjectName()).ljust(Response.PADDING_2)),
                                                           colorColon.format(':'),
                                                           colorValue.format(len(self._allLib.builder().masterProjectExternalEnvEntryContainers()))
                                                           )
                               )
                self._addNewLineDisplay(envType)

    #
    ## @brief Add product info display.
    #
    #  @param envType [ enum | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addProductInfoDisplay(self, envType):

        display = self._getDisplayByEnvType(envType)

        colorVariable = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kSingleVariable, envType)
        colorColon    = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kColon, envType)
        colorValue    = self._allLib.settingsOperator().getTerminalDisplayColorByColorName(mMeco.libs.enumLib.ColorName.kSingleValue, envType)

        value = ''

        if mMeco.core.platformLib.Platform.isWindows():

            value = 'Write-Host "{}" -NoNewline -ForegroundColor {};Write-Host "{} " -NoNewline -ForegroundColor {};Write-Host "{}" -NoNewline -ForegroundColor {};\n'
            value = value.format(mMeco.libs.aboutLib.NAME.ljust(Response.PADDING_2),
                                 colorVariable,
                                 ':',
                                 colorColon,
                                 mMeco.libs.aboutLib.getVersionAndDate(),
                                 colorValue
                                 )

        else:

            value = 'printf "{}{} {}";\n'.format(colorVariable.format(mMeco.libs.aboutLib.NAME.ljust(Response.PADDING_2)),
                                                 colorColon.format(':'),
                                                 colorValue.format(mMeco.libs.aboutLib.getVersionAndDate()),
                                                 )

        display.append(value)
        self._addNewLineDisplay(envType)
        self._addNewLineDisplay(envType)

    #
    #
    #
    ## @brief Add entries.
    #
    #  @param envEntryContainer [ mMeco.libs.entryLib.EnvEntryContainer | None | in  ] - Env entry container.
    #  @param envType           [ enum                                  | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _addEntries(self, envEntryContainer, envType):

        if not envEntryContainer.entries():
            return

        if not envType in [mMeco.libs.enumLib.EnvType.kPreBuild, mMeco.libs.enumLib.EnvType.kPostBuild]:
            if not self._allLib.request().setOnly():
                self._addContainerDisplay(envEntryContainer, envType)

        for entry in envEntryContainer.entries():

            if entry.envEntryType() == mMeco.libs.enumLib.EnvEntryType.kMulti:

                if not self._allLib.request().displayOnly():
                    self._addMultiEnv(entry, envType)

                if not self._allLib.request().setOnly():
                    self._addMultiDisplay(entry, envType)

            elif entry.envEntryType() == mMeco.libs.enumLib.EnvEntryType.kSingle:

                if not self._allLib.request().displayOnly():
                    self._addSingleEnv(entry, envType)

                if not self._allLib.request().setOnly():
                    self._addSingleDisplay(entry, envType)

            elif entry.envEntryType() == mMeco.libs.enumLib.EnvEntryType.kCommand:

                if not self._allLib.request().displayOnly():
                    self._addCommandEnv(entry, envType)

                if not self._allLib.request().setOnly():
                    self._addCommandDisplay(entry, envType)

            elif entry.envEntryType() == mMeco.libs.enumLib.EnvEntryType.kScript:

                if not self._allLib.request().displayOnly():
                    self._addScriptEnv(entry, envType)

                if not self._allLib.request().setOnly():
                    self._addScriptDisplay(entry, envType)

        if self._allLib.request().verbose() != 1 and \
           not self._allLib.request().setOnly():
            self._addNewLineDisplay(envType)

    #
    ## @brief Respond.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _respond(self):

        # print(self._name)

        self._addScriptFileStartEnv()


        # Pre
        if self._allLib.builder().preBuildEnvEntryContainers():

            if not self._allLib.request().setOnly():
                self._addHeaderDisplay(mMeco.libs.enumLib.EnvType.kPreBuild)

            for envEntryContainer in self._allLib.builder().preBuildEnvEntryContainers():
                self._addEntries(envEntryContainer, mMeco.libs.enumLib.EnvType.kPreBuild)


        # Reserved
        if self._allLib.builder().reservedEnvEntryContainers():

            if not self._allLib.request().setOnly():
                self._addHeaderDisplay(mMeco.libs.enumLib.EnvType.kReserved)

            for envEntryContainer in self._allLib.builder().reservedEnvEntryContainers():
                self._addEntries(envEntryContainer, mMeco.libs.enumLib.EnvType.kReserved)


        # Development
        if self._allLib.builder().developmentEnvEntryContainers():

            if not self._allLib.request().setOnly():
                self._addHeaderDisplay(mMeco.libs.enumLib.EnvType.kDevelopment)

            for envEntryContainer in self._allLib.builder().developmentEnvEntryContainers():
                self._addEntries(envEntryContainer, mMeco.libs.enumLib.EnvType.kDevelopment)


        # Stage
        if self._allLib.builder().stageEnvEntryContainers():

            if not self._allLib.request().setOnly():
                self._addHeaderDisplay(mMeco.libs.enumLib.EnvType.kStage)

            for envEntryContainer in self._allLib.builder().stageEnvEntryContainers():
                self._addEntries(envEntryContainer, mMeco.libs.enumLib.EnvType.kStage)


        # Project
        if self._allLib.builder().projectInternalEnvEntryContainers():

            if not self._allLib.request().setOnly():
                self._addHeaderDisplay(mMeco.libs.enumLib.EnvType.kProjectInternal)

            for envEntryContainer in self._allLib.builder().projectInternalEnvEntryContainers():
                self._addEntries(envEntryContainer, mMeco.libs.enumLib.EnvType.kProjectInternal)

        if self._allLib.builder().projectExternalEnvEntryContainers():

            if not self._allLib.request().setOnly():
                self._addHeaderDisplay(mMeco.libs.enumLib.EnvType.kProjectExternal)

            for envEntryContainer in self._allLib.builder().projectExternalEnvEntryContainers():
                self._addEntries(envEntryContainer, mMeco.libs.enumLib.EnvType.kProjectExternal)


        # Master
        if self._allLib.builder().masterProjectInternalEnvEntryContainers():

            if not self._allLib.request().setOnly():
                self._addHeaderDisplay(mMeco.libs.enumLib.EnvType.kMasterProjectInternal)

            for envEntryContainer in self._allLib.builder().masterProjectInternalEnvEntryContainers():
                self._addEntries(envEntryContainer, mMeco.libs.enumLib.EnvType.kMasterProjectInternal)

        if self._allLib.builder().masterProjectExternalEnvEntryContainers():

            if not self._allLib.request().setOnly():
                self._addHeaderDisplay(mMeco.libs.enumLib.EnvType.kMasterProjectExternal)

            for envEntryContainer in self._allLib.builder().masterProjectExternalEnvEntryContainers():
                self._addEntries(envEntryContainer, mMeco.libs.enumLib.EnvType.kMasterProjectExternal)


        # Post
        if self._allLib.builder().postBuildEnvEntryContainers():

            if not self._allLib.request().setOnly():
                self._addHeaderDisplay(mMeco.libs.enumLib.EnvType.kPostBuild)

            for envEntryContainer in self._allLib.builder().postBuildEnvEntryContainers():
                self._addEntries(envEntryContainer, mMeco.libs.enumLib.EnvType.kPostBuild)


        # App
        if self._allLib.settingsOperator().appFilePath():

            if not self._allLib.request().setOnly():
                self._addHeaderDisplay(mMeco.libs.enumLib.EnvType.kEnv)
                self._addAppDisplay(mMeco.libs.enumLib.EnvType.kEnv)

            if not self._allLib.request().displayOnly():
                self._addAppEnv(mMeco.libs.enumLib.EnvType.kEnv)


        # Info
        if not self._allLib.request().setOnly():
            self._addHeaderDisplay(mMeco.libs.enumLib.EnvType.kInfo)
            self._addInfoDisplay(mMeco.libs.enumLib.EnvType.kInfo)


        # Product Info
        if not self._allLib.request().setOnly():
            self._addHeaderDisplay(mMeco.libs.enumLib.EnvType.kProductInfo)
            self._addProductInfoDisplay(mMeco.libs.enumLib.EnvType.kProductInfo)

        #

        self._addScriptFileEndEnv()

        self._write()

        return True
