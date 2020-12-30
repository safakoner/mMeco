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
## @file    mMeco/solvers/prioritySol.py @brief [ FILE   ] - Solver.
## @package mMeco.solvers.prioritySol    @brief [ MODULE ] - Solver.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import mMeco.abstract.solverAbs


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Abstract solver class.
class Solver(mMeco.abstract.solverAbs.Solver):
    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC STATIC MEMBERS
    # ------------------------------------------------------------------------------------------------
    ## [ str ] - Name.
    NAME = 'prioritySol'

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

        mMeco.abstract.solverAbs.Solver.__dict__['__init__'](self)

    #
    # ------------------------------------------------------------------------------------------------
    # PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Solve.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _solve(self):

        # List packages
        if self._reservedEnvPath:
            self._reservedEnvPath.listPackages(invokeShouldInitializePackageCallback=True)

        if self._developmentEnvPath:
            self._developmentEnvPath.listPackages(invokeShouldInitializePackageCallback=True)

        if self._stageEnvPath:
            self._stageEnvPath.listPackages(invokeShouldInitializePackageCallback=True)

        if self._projectInternalEnvPath:
            self._projectInternalEnvPath.listPackages(invokeShouldInitializePackageCallback=True)

        if self._projectExternalEnvPath:
            self._projectExternalEnvPath.listPackages(invokeShouldInitializePackageCallback=True)

        if self._masterProjectInternalEnvPath:
            self._masterProjectInternalEnvPath.listPackages(invokeShouldInitializePackageCallback=True)

        if self._masterProjectExternalEnvPath:
            self._masterProjectExternalEnvPath.listPackages(invokeShouldInitializePackageCallback=True)


        # Remove Internal
        if self._masterProjectInternalEnvPath and self._projectInternalEnvPath:
            Solver.removeVersionedPackagesFromVersionedPackages(self._masterProjectInternalEnvPath.packages(),
                                                                self._projectInternalEnvPath.packages())

        #

        if self._projectInternalEnvPath and self._developmentEnvPath:
            Solver.removeNonVersionedPackagesFromVersionedPackages(self._projectInternalEnvPath.packages(),
                                                                   self._developmentEnvPath.packages())

        if self._masterProjectInternalEnvPath and self._developmentEnvPath:
            Solver.removeNonVersionedPackagesFromVersionedPackages(self._masterProjectInternalEnvPath.packages(),
                                                                   self._developmentEnvPath.packages())

        #
        
        if self._projectInternalEnvPath and self._stageEnvPath:
            Solver.removeNonVersionedPackagesFromVersionedPackages(self._projectInternalEnvPath.packages(),
                                                                   self._stageEnvPath.packages())

        if self._masterProjectInternalEnvPath and self._stageEnvPath:
            Solver.removeNonVersionedPackagesFromVersionedPackages(self._masterProjectInternalEnvPath.packages(),
                                                                   self._stageEnvPath.packages())

        # Remove External
        if self._masterProjectExternalEnvPath and self._projectExternalEnvPath:
            Solver.removeVersionedPackagesFromVersionedPackages(self._masterProjectExternalEnvPath.packages(),
                                                                self._projectExternalEnvPath.packages())

        #

        if self._projectExternalEnvPath and self._developmentEnvPath:
            Solver.removeNonVersionedPackagesFromVersionedPackages(self._projectExternalEnvPath.packages(),
                                                                   self._developmentEnvPath.packages())

        if self._masterProjectExternalEnvPath and self._developmentEnvPath:
            Solver.removeNonVersionedPackagesFromVersionedPackages(self._masterProjectExternalEnvPath.packages(),
                                                                   self._developmentEnvPath.packages())

        #
        
        if self._projectExternalEnvPath and self._stageEnvPath:
            Solver.removeNonVersionedPackagesFromVersionedPackages(self._projectExternalEnvPath.packages(),
                                                                   self._stageEnvPath.packages())

        if self._masterProjectExternalEnvPath and self._stageEnvPath:
            Solver.removeNonVersionedPackagesFromVersionedPackages(self._masterProjectExternalEnvPath.packages(),
                                                                   self._stageEnvPath.packages())

        if self._projectInternalEnvPath:
            Solver.setLastVersionOfThePackageToBeUsed(self._projectInternalEnvPath.packages())

        if self._projectExternalEnvPath:
            Solver.setLastVersionOfThePackageToBeUsed(self._projectExternalEnvPath.packages())

        Solver.setLastVersionOfThePackageToBeUsed(self._masterProjectInternalEnvPath.packages())
        Solver.setLastVersionOfThePackageToBeUsed(self._masterProjectExternalEnvPath.packages())

    #
    # ------------------------------------------------------------------------------------------------
    # STATIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Set latest version of the packages to be used by removing other versions from the version list.
    #
    #  @param packages [ list | None | in  ] - Versioned package list.
    #
    #  @exception N/A
    #
    #  @return None - None.
    @staticmethod
    def setLastVersionOfThePackageToBeUsed(packages):

        if not packages:
            return

        if not isinstance(packages[0], dict):
            return

        for package in packages:
            package['versions'] = package['versions'][-1:]

    #
    ## @brief Remove `versionedPackagesB` from `versionedPackagesA`.
    #
    #  @param versionedPackagesA [ list of dict | None | in  ] - Packages.
    #  @param versionedPackagesB [ list of dict | None | in  ] - Packages.
    #
    #  @exception N/A
    #
    #  @return None - None.
    @staticmethod
    def removeVersionedPackagesFromVersionedPackages(versionedPackagesA, versionedPackagesB):

        if not versionedPackagesA or not versionedPackagesB:
            return

        for pa in versionedPackagesB:

            for pb in versionedPackagesA:

                if pa['package'] == pb['package']:

                    versionedPackagesA.pop(versionedPackagesA.index(pb))

    #
    ## @brief Remove `nonVersionedPackages` from `versionedPackages`.
    #
    #  @param versionedPackages    [ list of dict | None | in  ] - Packages.
    #  @param nonVersionedPackages [ list of str  | None | in  ] - Packages.
    #
    #  @exception N/A
    #
    #  @return None - None.
    @staticmethod
    def removeNonVersionedPackagesFromVersionedPackages(versionedPackages, nonVersionedPackages):

        if not nonVersionedPackages or not versionedPackages:
            return

        for nvp in nonVersionedPackages:

            for vp in versionedPackages:

                if nvp == vp['package']:

                    versionedPackages.pop(versionedPackages.index(vp))
