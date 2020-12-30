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
## @file    mMeco/mecoLib.py @brief [ FILE   ] - Meco.
## @package mMeco.mecoLib    @brief [ MODULE ] - Meco.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
import subprocess

import mMeco.core.platformLib

import mMeco.abstract.builderAbs
import mMeco.abstract.responseAbs
import mMeco.abstract.solverAbs

import mMeco.operators.appFileOpt
import mMeco.operators.callbackOpt
import mMeco.operators.settingsOpt
import mMeco.operators.packageGlobalEnvOpt

import mMeco.libs.aboutLib
import mMeco.libs.allLib
import mMeco.libs.requestLib

import mMeco.solvers.cacheReadSol
import mMeco.solvers.prioritySol

import mMeco.builders.cacheReadBld
import mMeco.builders.standardBld

import mMeco.responses.cacheWriteRes
import mMeco.responses.writeRes


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Meco.
class Meco(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param parameters [ str | None | in  ] - Parameters.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, parameters=None):

        ## [ str ] - Parameters.
        self._parameters                = parameters

        ## [ mMeco.requestLib.Request ] - Request.
        self._request                   = mMeco.libs.requestLib.Request()

        ## [ mMeco.operators.settingsOpt.SettingsOperator ] - Operator.
        self._settingsOperator          = mMeco.operators.settingsOpt.SettingsOperator()

        ## [ mMeco.operators.packageGlobalEnvOpt.PackageGlobalEnvOperator ] - Operator.
        self._packageGlobalEnvOperator  = mMeco.operators.packageGlobalEnvOpt.PackageGlobalEnvOperator()

        ## [ mMeco.operators.callbackOpt.CallbackOperator ] - Operator.
        self._callbackOperator          = mMeco.operators.callbackOpt.CallbackOperator()

        ## [ mMeco.operators.appFileOpt.AppFileOperator ] - Operator.
        self._appFileOperator           = mMeco.operators.appFileOpt.AppFileOperator()

        ## [ mMeco.libs.allLib.All ] - All libraries.
        self._allLib                    = mMeco.libs.allLib.All.getInstance()

        #

        ## [ list of mMeco.abstract.solverAbs.SolverContainer ] - Solver container.
        self._solverContainer           = mMeco.abstract.solverAbs.SolverContainer()

        ## [ mMeco.abstract.solverAbs.Solver ] - Solver.
        self._solver                    = None
        
        #
        
        ## [ list of mMeco.abstract.builderAbs.BuilderContainer ] - Builders container.
        self._builderContainer          = mMeco.abstract.builderAbs.BuilderContainer()

        ## [ mMeco.abstract.builderAbs.Builder ] - Builder.
        self._builder                   = None
        
        #
        
        ## [ list of mMeco.abstract.responseAbs.ResponseContainer ] - Responses container.
        self._responseContainer         = mMeco.abstract.responseAbs.ResponseContainer()

        ## [ mMeco.abstract.responseAbs.Response ] - Response.
        self._response                  = None

        #

        ## [ str ] - PowerShell executable path.
        self._powerShellExecutablePath = 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'

    #
    # ------------------------------------------------------------------------------------------------
    # PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Process common requests.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _common(self):

        if self._request.version():
            self._allLib.logger().displayInfo(mMeco.libs.aboutLib.getVersion(), startNewLine=False)
            return True

        if self._request.about():
            self._allLib.logger().displayInfo(mMeco.libs.aboutLib.getAboutInformation())
            return True

        return False

    #
    ## @brief Display info.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _displayInfo(self):

        info = self._request.displayInfo()
        if not info:
            return False

        if info == 1 or info == 3:
            self._allLib.logger().displayInfo(self._request)

        if info == 2 or info == 3:
            self._allLib.logger().displayInfo(self._settingsOperator)

        return True

    #
    ## @brief Get solver to be used.
    #
    #  @exception NotImplementedError - If no solver found to operate with.
    #
    #  @return mMeco.abstract.solverAbs.Solver - A solver class that inherits mMeco.abstract.solverAbs.Solver class.
    def _getSolver(self):

        if self._allLib.request().cacheRead():
            return self._solverContainer.getByName(mMeco.solvers.cacheReadSol.Solver.NAME)

        return self._solverContainer.getByName(mMeco.solvers.prioritySol.Solver.NAME)

    #
    ## @brief Get builder to be used.
    #
    #  @exception NotImplementedError - If no solver found to operate with.
    #
    #  @return mMeco.abstract.builderAbs.Builder - A builder class that inherits mMeco.abstract.builderAbs.Builder class.
    def _getBuilder(self):

        if self._allLib.request().cacheRead():
            return self._builderContainer.getByName(mMeco.builders.cacheReadBld.Builder.NAME)

        return self._builderContainer.getByName(mMeco.builders.standardBld.Builder.NAME)

    #
    ## @brief Get response to be used.
    #
    #  @exception NotImplementedError - If no solver found to operate with.
    #
    #  @return mMeco.abstract.responseAbs.Response - A response class that inherits mMeco.abstract.responseAbs.Response class.
    def _getResponse(self):

        if self._allLib.request().cacheWrite():
            return self._responseContainer.getByName(mMeco.responses.cacheWriteRes.Response.NAME)

        return self._responseContainer.getByName(mMeco.responses.writeRes.Response.NAME)

    #
    ## @brief Parse the request.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _parse(self):

        if self._parameters:
            self._request.parseFromStr(self._parameters)
        else:
            self._request.parse()

    #
    ## @brief Initialize.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _initialize(self):

        # Settings Module
        try:
            self._settingsOperator.initialize()
        except Exception as error:
            self._allLib.logger().addFailure(str(error))
            if self._allLib.request().raiseExceptions():
                raise
            return False

        # Callback Module
        try:
            self._callbackOperator.initialize()
        except Exception as error:
            self._allLib.logger().addFailure(str(error))
            if self._allLib.request().raiseExceptions():
                raise
            return False

        # Env File Module
        if self._settingsOperator.appFilePath():
            try:
                self._appFileOperator.set(self._settingsOperator.appFilePath())
            except Exception as error:
                self._allLib.logger().addFailure(str(error))
                if self._allLib.request().raiseExceptions():
                    raise
                return False

        # Package Global Env Module
        try:
            self._packageGlobalEnvOperator.initialize()
        except Exception as error:
            self._allLib.logger().addFailure(str(error))
            if self._allLib.request().raiseExceptions():
                raise
            return False

        # Solvers
        self._solverContainer.list()

        # Builders
        self._builderContainer.list()

        # Responses
        self._responseContainer.list()

        return True

    #
    ## @brief Respond last request.
    #
    #  @exception IOError - If there is no previously created script file exist for the request.
    #
    #  @return bool - Result.
    def _respondLast(self):

        if os.path.isfile(self._allLib.settingsOperator().scriptFilePath()):
            return True

        message = 'Script file doesn\'t exist for this env configuration, -l|--last ignored: {}'.format(self._allLib.settingsOperator().scriptFilePath())
        self._allLib.logger().addFailure(message)

        if self._allLib.request().raiseExceptions():
            raise IOError(message)

        return False

    #
    ## @brief Solve.
    #
    #  Determine which packages will be used.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _solve(self):

        try:
            self._solver = self._getSolver()
            self._allLib.setSolver(self._solver)
            self._solver.solve()
            return True

        except Exception as error:
            self._allLib.logger().addFailure(str(error))
            if self._allLib.request().raiseExceptions():
                raise

            return False

    #
    ## @brief Build.
    #
    #  Build the env, keys, values, paths, scripts, commands, etc.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _build(self):

        try:
            self._builder = self._getBuilder()
            self._allLib.setBuilder(self._builder)
            self._builder.build()
            return True

        except Exception as error:
            self._allLib.logger().addFailure(str(error))
            if self._allLib.request().raiseExceptions():
                raise

            return False

    #
    ## @brief Respond.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _respond(self):

        try:
            self._response = self._getResponse()
            self._allLib.setResponse(self._response)
            self._response.respond()
            return True

        except Exception as error:
            self._allLib.logger().addFailure(str(error))
            if self._allLib.request().raiseExceptions():
                raise

            return False

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.libs.allLib.All - Value.
    def allLib(self):

        return self._allLib

    #
    ## @brief Set Powershell executable path.
    #
    #  @param path [ str | None | in  ] - Absolute path of Powershell executable.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def setPowerShellExecutablePath(self, path):

        if not os.path.isfile(path):
            raise IOError('Powershell executable path does\'t exist: {}'.format(path))

        self._powerShellExecutablePath = path

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Execute.
    #
    #  - Parse the request
    #  - Initialize.
    #  - Solve.
    #  - Build.
    #  - Respond.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def execute(self):

        self._parse()

        if self._common():
            return False

        if not self._initialize():
            return False

        if self._displayInfo():
            return False

        if self._allLib.request().last():
            return self._respondLast()

        if not self._solve():
            return False

        if not self._build():
            return False

        if not self._respond():
            return False

        return True

    #
    ## @brief Execute given command in resolved environment.
    #
    #  Method adds `--set-only` flag to the request and invokes mMeco.mecoLib.Meco.execute method first.
    #  Then given `commands` is executed in the resolved environment via `subprocess.Popen`.
    #
    #  @param commands  [ str, list of str  | None | in  ] - Commands to be executed (`;` separated).
    #  @param cwd       [ str               | None | in  ] - Current working directory for `subprocess.Popen`.
    #
    #  @exception IOError - If PowerShell executable path doesn't exist on Windows OS .
    #
    #  @return tuple - stdout and stderr.
    def executeCommand(self, commands, cwd=None):

        if self._allLib.request().platform() == mMeco.core.platformLib.Name.kWindows and \
           not os.path.isfile(self._powerShellExecutablePath):
            raise IOError('PowerShell executable path doesn\'t exist: {}'.format(self._powerShellExecutablePath))

        #

        self._parameters = '{} --set-only'.format(self._parameters)

        if not self.execute():
            return None, None

        #

        if isinstance(commands, list):
            commands = ';'.join(commands)

        env                 = os.environ.copy()
        envScriptFilePath   = self._settingsOperator.scriptFilePath()
        executable          = None
        arguments           = []

        if self._allLib.request().platform() == mMeco.core.platformLib.Name.kWindows:

            executable  = self._powerShellExecutablePath
            arguments   = ['& {}. "{}"{};{}'.format('{', envScriptFilePath, '}', commands)]

        else:

            arguments = ['source {};{}'.format(envScriptFilePath, commands)]

        #

        process = subprocess.Popen(arguments,
                                 cwd=cwd,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 env=env,
                                 executable=executable,
                                 shell=True)

        stdOut, stdErr = process.communicate()

        return stdOut, stdErr

    #
    ## @brief Execute and return the path of the script file.
    #
    #  @exception N/A
    #
    #  @return str  - Absolute path of the script file.
    #  @return None - If a problem occurs during execution.
    def writeFile(self):

        if not self.execute():
            return None

        return self._settingsOperator.scriptFilePath()
