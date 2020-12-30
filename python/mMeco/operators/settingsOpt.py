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
## @file    mMeco/operators/settingsOpt.py @brief [ FILE   ] - Operator.
## @package mMeco.operators.settingsOpt    @brief [ MODULE ] - Operator.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  os
from    platform    import system

import  mMeco.abstract.operatorAbs


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Class to operate on Python modules.
class SettingsOperator(mMeco.abstract.operatorAbs.Operator):
    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC STATIC MEMBERS
    # ------------------------------------------------------------------------------------------------
    ## [ str ] - Default Python module import name.
    MODULE  = 'mMecoSettings.settingsLib'

    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param module [ str | None | in  ] - Python module import path or Python module file path.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, module=None):

        ## [ str ] - Name.
        self._name = 'settingsOperator'

        mMeco.abstract.operatorAbs.Operator.__dict__['__init__'](self, module)

        #

        ## [ str ] - Master project name.
        self._masterProjectName                     = None

        ## [ str ] - Project name in use.
        self._projectNameInUse                      = None

        #

        ## [ str ] - Reserved packages path.
        self._reservedPackagesPath                  = None

        ## [ str ] - Development packages path.
        self._developmentPackagesPath               = None

        ## [ str ] - Stage packages path.
        self._stagePackagesPath                     = None

        #

        ## [ str ] - Project internal packages path.
        self._projectInternalPackagesPath           = None

        ## [ str ] - Project external packages path.
        self._projectExternalPackagesPath           = None

        #

        ## [ str ] - Master project internal packages path.
        self._masterProjectInternalPackagesPath     = None

        ## [ str ] - Master project external packages path.
        self._masterProjectExternalPackagesPath     = None

        #

        ## [ str ] - App path.
        self._appFilePath                           = None

        ## [ str ] - Script file path.
        self._scriptFilePath                        = None

        ## [ str ] - Log file.
        self._logFilePath                           = None

        #

        ## [ list of str ] - Terminal header display color.
        self._terminalHeaderDisplayColor            = []

        ## [ list of str ] - Terminal display color.
        self._terminalDisplayColor                  = []

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
    ## @brief Initialize the attributes of the Python module.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _initialize(self):

        self.set()

        #

        self._projectNameInUse  = self._module.MASTER_PROJECT_NAME
        self._masterProjectName = self._module.MASTER_PROJECT_NAME

        if self._all.request().project():
            if self._all.request().project() != self._masterProjectName:
                self._projectNameInUse = self._all.request().project()


        # Log
        self._logFilePath = getattr(self._module, 'getLogFilePath')(self._projectNameInUse,
                                                                    self._all.request().developer(),
                                                                    self._all.request().development(),
                                                                    self._all.request().stage(),
                                                                    system())
        self._all.logger().setFile(self._logFilePath)


        # Reserved
        self._reservedPackagesPath = getattr(self._module, 'getReservedPackagesPath')(self._all.request().developer(),
                                                                                      system())
        if not os.path.isdir(self._reservedPackagesPath):
            self._reservedPackagesPath = None


        # Development
        if self._all.request().development():
            self._developmentPackagesPath = getattr(self._module, 'getDevelopmentPackagesPath')(self._projectNameInUse,
                                                                                                self._all.request().developer(),
                                                                                                self._all.request().development(),
                                                                                                system(),
                                                                                                create=False)

            if not os.path.isdir(self._developmentPackagesPath):
                raise IOError('Development packages path doesn\'t exist: {}'.format(self._developmentPackagesPath))


        # Stage
        if self._all.request().stage():
            self._stagePackagesPath = getattr(self._module, 'getStagePackagesPath')(self._projectNameInUse,
                                                                                    self._all.request().developer(),
                                                                                    self._all.request().stage(),
                                                                                    system())
            if not os.path.isdir(self._stagePackagesPath):
                raise IOError('Stage packages path doesn\'t exist: {}'.format(self._stagePackagesPath))


        # Project
        if self._projectNameInUse != self._masterProjectName:

            self._projectInternalPackagesPath = getattr(self._module, 'getProjectInternalPackagesPath')(self._projectNameInUse,
                                                                                                        system())
            if not os.path.isdir(self._projectInternalPackagesPath):
                raise IOError('Project internal packages path doesn\'t exist: {}'.format(self._projectInternalPackagesPath))

            self._projectExternalPackagesPath = getattr(self._module, 'getProjectExternalPackagesPath')(self._projectNameInUse,
                                                                                                        system())
            if not os.path.isdir(self._projectExternalPackagesPath):
                raise IOError('Project external packages path doesn\'t exist: {}'.format(self._projectExternalPackagesPath))


        # Master Project
        self._masterProjectInternalPackagesPath = getattr(self._module, 'getMasterProjectInternalPackagesPath')(system())
        if not os.path.isdir(self._masterProjectInternalPackagesPath):
            raise IOError('Master project internal packages path doesn\'t exist: {}'.format(self._masterProjectInternalPackagesPath))

        self._masterProjectExternalPackagesPath = getattr(self._module, 'getMasterProjectExternalPackagesPath')(system())
        if not os.path.isdir(self._masterProjectExternalPackagesPath):
            raise IOError('Master project external packages path doesn\'t exist: {}'.format(self._masterProjectExternalPackagesPath))


        # App File Path
        if self._all.request().app():
            self._appFilePath = getattr(self._module, 'getAppFilePath')(self._projectNameInUse,
                                                                        self._all.request().developer(),
                                                                        self._all.request().development(),
                                                                        self._all.request().stage(),
                                                                        system(),
                                                                        self._all.request().app())
            if self._appFilePath and not os.path.isfile(self._appFilePath):
                raise IOError('App file path doesn\'t exist: {}'.format(self._appFilePath))


        # Script File Path
        self._scriptFilePath = getattr(self._module, 'getScriptFilePath')(self._projectNameInUse,
                                                                          self._all.request().developer(),
                                                                          self._all.request().development(),
                                                                          self._all.request().stage(),
                                                                          system(),
                                                                          self._appFilePath)


        # Terminal Header Display Color
        self._terminalHeaderDisplayColor = getattr(self._module, 'getTerminalHeaderDisplayColors')(system())

        # Terminal Display Color
        self._terminalDisplayColor = getattr(self._module, 'getTerminalDisplayColors')(system())

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
    def masterProjectName(self):

        return self._masterProjectName

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def projectNameInUse(self):

        return self._projectNameInUse

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def reservedPackagesPath(self):

        return self._reservedPackagesPath

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def developmentPackagesPath(self):

        return self._developmentPackagesPath

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def stagePackagesPath(self):

        return self._stagePackagesPath

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def projectInternalPackagesPath(self):

        return self._projectInternalPackagesPath

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def projectExternalPackagesPath(self):

        return self._projectExternalPackagesPath

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def masterProjectInternalPackagesPath(self):

        return self._masterProjectInternalPackagesPath

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def masterProjectExternalPackagesPath(self):

        return self._masterProjectExternalPackagesPath

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def appFilePath(self):

        return self._appFilePath

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def scriptFilePath(self):

        return self._scriptFilePath

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def logFilePath(self):

        return self._logFilePath

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of str - Value.
    def terminalHeaderDisplayColor(self):

        return self._terminalHeaderDisplayColor

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of str - Value.
    def terminalDisplayColor(self):

        return self._terminalDisplayColor

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

        data = ''
        data += '\nSETTINGS'
        data += '\n{}'.format('-' * 100)

        data += '\nMaster Project Name                   : {}'.format(self._masterProjectName)
        data += '\nProject Name In Use                   : {}'.format(self._projectNameInUse)

        data += '\nReserved Packages Path                : {}'.format(self._reservedPackagesPath if self._reservedPackagesPath else 'N/A')
        data += '\nDevelopment Packages Path             : {}'.format(self._developmentPackagesPath if self._developmentPackagesPath else 'N/A')
        data += '\nStage Packages Path                   : {}'.format(self._stagePackagesPath if self._stagePackagesPath else 'N/A')

        data += '\nProject Internal Packages Path        : {}'.format(self._projectInternalPackagesPath if self._projectInternalPackagesPath else 'N/A')
        data += '\nProject External Packages Path        : {}'.format(self._projectExternalPackagesPath if self._projectExternalPackagesPath else 'N/A')

        data += '\nMaster Project Internal Packages Path : {}'.format(self._masterProjectInternalPackagesPath if self._masterProjectInternalPackagesPath else 'N/A')
        data += '\nMaster Project External Packages Path : {}'.format(self._masterProjectExternalPackagesPath if self._masterProjectExternalPackagesPath else 'N/A')

        data += '\nLog File                              : {}'.format(self._logFilePath if self._logFilePath else 'N/A')
        data += '\nApp File Path                         : {}'.format(self._appFilePath if self._appFilePath else 'N/A')
        data += '\nScript File Path                      : {}'.format(self._scriptFilePath if self._scriptFilePath else 'N/A')

        return data

    #
    ## @brief Get terminal display color for given env type.
    #
    #  @param colorName [ enum | None | in  ] - Color from mMeco.libs.enumLib.ColorName enum class.
    #  @param envType   [ enum | None | in  ] - Env type from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def getTerminalDisplayColorByColorName(self, colorName, envType=None):

        if envType:
            envType = envType.replace(' ', '-').lower()

        data = self._terminalDisplayColor
        if envType:
            data = self._terminalDisplayColor[envType]

        return data[colorName]
