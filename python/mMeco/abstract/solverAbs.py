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
## @file    mMeco/abstract/solverAbs.py @brief [ FILE   ] - Abstract solver.
## @package mMeco.abstract.solverAbs    @brief [ MODULE ] - Abstract solver.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  os

import  mMeco.core.enumAbs
import  mMeco.core.moduleLib

import  mMeco.libs.allLib
import  mMeco.libs.enumLib
import  mMeco.libs.envPathLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Solver container.
class SolverContainer(object):
    #
    ## @brief Constructor.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self):

        ## [ mMeco.libs.allLib.All ] - All.
        self._allLib    = mMeco.libs.allLib.All.getInstance(**{'solverContainer':self})

        ## [ list of mMeco.abstract.solverAbs.Solver ] - Solvers.
        self._solvers   = []

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of mMeco.abstract.solverAbs.Solver - Solvers.
    def solvers(self):

        return self._solvers

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Get solvers.
    #
    #  @exception AttributeError - If solver modules do not have `Solver` class.
    #
    #  @return list of mMeco.abstract.solverAbs.Solver - Solver class instances.
    def list(self):

        solverModulePath = os.path.abspath(os.path.join(__file__, '..', '..', 'solvers'))

        for solverModule in mMeco.core.moduleLib.Module.listModules(solverModulePath, 'mMeco.solvers.{}'):

            if not hasattr(solverModule, 'Solver'):
                raise AttributeError('Solver module doesn\'t have a class named "Solver": {}'.format(solverModule.__file__))

            solverInstance = getattr(solverModule, 'Solver')()
            self._solvers.append(solverInstance)

        return self._solvers

    #
    ## @brief Get solver by given name.
    #
    #  @param name [ str | None | in  ] - Name of the solver.
    #
    #  @exception ValueError - If solver no solver found.
    #  @exception ValueError - If solver no solver found with given type.
    #
    #  @return mMeco.abstract.solverAbs.Solver - Solver class instances.
    def getByName(self, name):

        if not self._solvers:
            raise ValueError('No solver found.')

        for solver in self._solvers:
            if name == solver.NAME:
                return solver

        raise ValueError('No solver found by given name: {}'.format(name))

#
## @brief [ ABSTRACT CLASS ] - Abstract solver class.
class Solver(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC STATIC MEMBERS
    # ------------------------------------------------------------------------------------------------
    ## [ str ] - Name.
    NAME = ''

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

        ## [ mMeco.libs.allLib.All ] - All.
        self._allLib = mMeco.libs.allLib.All.getInstance(**{self.NAME:self})

        #

        if self._allLib.settingsOperator().reservedPackagesPath():
            ## [ list of mMeco.libs.envPathLib.EnvPath ] - Reserved env path.
            self._reservedEnvPath = mMeco.libs.envPathLib.EnvPath(self._allLib.settingsOperator().reservedPackagesPath(),
                                                                  mMeco.libs.enumLib.EnvType.kReserved)
        else:
            self._reservedEnvPath = None

        #

        if self._allLib.settingsOperator().developmentPackagesPath():
            ## [ list of mMeco.libs.envPathLib.EnvPath ] - Development env path.
            self._developmentEnvPath = mMeco.libs.envPathLib.EnvPath(self._allLib.settingsOperator().developmentPackagesPath(),
                                                                     mMeco.libs.enumLib.EnvType.kDevelopment)
        else:
            self._developmentEnvPath = None

        #

        if self._allLib.settingsOperator().stagePackagesPath():
            ## [ list of mMeco.libs.envPathLib.EnvPath ] - Stage env path.
            self._stageEnvPath = mMeco.libs.envPathLib.EnvPath(self._allLib.settingsOperator().stagePackagesPath(),
                                                               mMeco.libs.enumLib.EnvType.kStage)
        else:
            self._stageEnvPath = None

        #

        if self._allLib.settingsOperator().projectInternalPackagesPath():
            ## [ list of mMeco.libs.envPathLib.EnvPath ] - Project internal env path.
            self._projectInternalEnvPath = mMeco.libs.envPathLib.EnvPath(self._allLib.settingsOperator().projectInternalPackagesPath(),
                                                                         mMeco.libs.enumLib.EnvType.kProjectInternal)
        else:
            self._projectInternalEnvPath = None

        if self._allLib.settingsOperator().projectExternalPackagesPath():
            ## [ list of mMeco.libs.envPathLib.EnvPath ] - Project external env path.
            self._projectExternalEnvPath = mMeco.libs.envPathLib.EnvPath(self._allLib.settingsOperator().projectExternalPackagesPath(),
                                                                         mMeco.libs.enumLib.EnvType.kProjectExternal)
        else:
            self._projectExternalEnvPath = None

        #

        ## [ list of mMeco.libs.envPathLib.EnvPath ] - Master project internal env path.
        self._masterProjectInternalEnvPath  = mMeco.libs.envPathLib.EnvPath(self._allLib.settingsOperator().masterProjectInternalPackagesPath(),
                                                                            mMeco.libs.enumLib.EnvType.kMasterProjectInternal)

        ## [ list of mMeco.libs.envPathLib.EnvPath ] - Master project external env path.
        self._masterProjectExternalEnvPath  = mMeco.libs.envPathLib.EnvPath(self._allLib.settingsOperator().masterProjectExternalPackagesPath(),
                                                                            mMeco.libs.enumLib.EnvType.kMasterProjectExternal)

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.libs.envPathLib.EnvPath - Value.
    def reservedEnvPath(self):

        return self._reservedEnvPath

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.libs.envPathLib.EnvPath - Value.
    def developmentEnvPath(self):

        return self._developmentEnvPath

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.libs.envPathLib.EnvPath - Value.
    def stageEnvPath(self):

        return self._stageEnvPath

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.libs.envPathLib.EnvPath - Value.
    def projectInternalEnvPath(self):

        return self._projectInternalEnvPath

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.libs.envPathLib.EnvPath - Value.
    def projectExternalEnvPath(self):

        return self._projectExternalEnvPath

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.libs.envPathLib.EnvPath - Value.
    def masterProjectInternalEnvPath(self):

        return self._masterProjectInternalEnvPath

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.libs.envPathLib.EnvPath - Value.
    def masterProjectExternalEnvPath(self):

        return self._masterProjectExternalEnvPath

    #
    # ------------------------------------------------------------------------------------------------
    # PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Callback which will be invoked before mMeco.abstract.solverAbs.Solver._solve method is invoked.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _preSolve(self):

        pass

    #
    ## @brief Callback which will be invoked after mMeco.abstract.solverAbs.Solver._solve method is invoked.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _postSolve(self):

        pass

    #
    ## @brief Solve.
    #
    #  @exception NotImplementedError - If this method is not implemented in child class.
    #
    #  @return bool - Result.
    def _solve(self):

        raise NotImplementedError('You must overwrite mMeco.abstract.solverAbs.Solver._solve method in child class.')

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Solve.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def solve(self):

        self._preSolve()

        self._solve()

        self._postSolve()






