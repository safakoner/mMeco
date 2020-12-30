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
## @file    mMeco/abstract/builderAbs.py @brief [ FILE   ] - Abstract builder.
## @package mMeco.abstract.builderAbs    @brief [ MODULE ] - Abstract builder.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  os
import  sys

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
## @brief [ CLASS ] - Builder container.
class BuilderContainer(object):
    #
    ## @brief Constructor.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self):

        ## [ mMeco.libs.allLib.All ] - All.
        self._allLib    = mMeco.libs.allLib.All.getInstance(**{'builderContainer':self})

        ## [ list of mMeco.abstract.builderAbs.Builder ] - Builders.
        self._builders = []

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of mMeco.abstract.builderAbs.Builder - Builders.
    def builders(self):

        return self._builders

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Get builders.
    #
    #  @exception AttributeError - If builder modules do not have `Builder` class.
    #
    #  @return list of mMeco.abstract.builderAbs.Builder - Builder class instances.
    def list(self):

        builderModulePath = os.path.abspath(os.path.join(__file__, '..', '..', 'builders'))

        for builderModule in mMeco.core.moduleLib.Module.listModules(builderModulePath, 'mMeco.builders.{}'):

            if not hasattr(builderModule, 'Builder'):
                raise AttributeError('Builder module doesn\'t have a class named "Builder": {}'.format(builderModule.__file__))

            builderInstance = getattr(builderModule, 'Builder')()
            self._builders.append(builderInstance)

        return self._builders

    #
    ## @brief Get builder by given name.
    #
    #  @param name [ str | None | in  ] - Name of the builder.
    #
    #  @exception ValueError - If builder no builder found.
    #  @exception ValueError - If builder no builder found with given type.
    #
    #  @return mMeco.abstract.builderAbs.Builder - Builder class instances.
    def getByName(self, name):

        if not self._builders:
            raise ValueError('No builder found.')

        for builder in self._builders:
            if name == builder.NAME:
                return builder

        raise ValueError('No builder found by given name: {}'.format(name))

#
## @brief [ ABSTRACT CLASS ] - Abstract builder class.
class Builder(object):
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

        ## [ list of mMeco.libs.entryLib.EnvEntryContainer ] - Env containers.
        self._preBuildEnvEntryContainers                = []

        ## [ list of mMeco.libs.entryLib.EnvEntryContainer ] - Env containers.
        self._postBuildEnvEntryContainers               = []

        #

        ## [ list of mMeco.libs.entryLib.EnvEntryContainer ] - Env containers.
        self._reservedEnvEntryContainers                = []

        #

        ## [ list of mMeco.libs.entryLib.EnvEntryContainer ] - Env containers.
        self._developmentEnvEntryContainers             = []

        ## [ list of mMeco.libs.entryLib.EnvEntryContainer ] - Env containers.
        self._stageEnvEntryContainers                   = []

        #

        ## [ list of mMeco.libs.entryLib.EnvEntryContainer ] - Env containers.
        self._projectInternalEnvEntryContainers         = []

        ## [ list of mMeco.libs.entryLib.EnvEntryContainer ] - Env containers.
        self._projectExternalEnvEntryContainers         = []

        #

        ## [ list of mMeco.libs.entryLib.EnvEntryContainer ] - Env containers.
        self._masterProjectInternalEnvEntryContainers   = []

        ## [ list of mMeco.libs.entryLib.EnvEntryContainer ] - Env containers.
        self._masterProjectExternalEnvEntryContainers   = []

    #
    # ------------------------------------------------------------------------------------------------
    # PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Callback which will be invoked before mMeco.abstract.buildersAbs.Builder._build method is invoked.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _preBuild(self):

        pass

    #
    ## @brief Callback which will be invoked after mMeco.abstract.buildersAbs.Builder._build method is invoked.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _postBuild(self):

        pass

    #
    ## @brief Build.
    #
    #  @exception NotImplementedError - If this method is not implemented in child class.
    #
    #  @return bool - Result.
    def _build(self):

        raise NotImplementedError('You must overwrite mMeco.abstract.buildersAbs.Builder.build method in child class.')

    #
    ## @brief Display env envEntry container.
    #
    #  @param envEntryContainers [ list of mMeco.libs.entryLib.EnvEntryContainer | None | in  ] - Env envEntry container.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _displayEnvEntryContainers(self, envEntryContainers):

        if not envEntryContainers:
            return

        for envEntryContainer in envEntryContainers:

            sys.stdout.write('-' * 100)
            sys.stdout.write('\n')
            sys.stdout.write(envEntryContainer)

            for envEntry in envEntryContainer.entries():
                sys.stdout.write(envEntry)
                sys.stdout.write('\n')

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of mMeco.libs.entryLib.EnvEntryContainer - Value.
    def preBuildEnvEntryContainers(self):

        return self._preBuildEnvEntryContainers

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of mMeco.libs.entryLib.EnvEntryContainer - Value.
    def postBuildEnvEntryContainers(self):

        return self._postBuildEnvEntryContainers

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of mMeco.libs.entryLib.EnvEntryContainer - Value.
    def reservedEnvEntryContainers(self):

        return self._reservedEnvEntryContainers

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of mMeco.libs.entryLib.EnvEntryContainer - Value.
    def developmentEnvEntryContainers(self):

        return self._developmentEnvEntryContainers

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of mMeco.libs.entryLib.EnvEntryContainer - Value.
    def stageEnvEntryContainers(self):

        return self._stageEnvEntryContainers

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of mMeco.libs.entryLib.EnvEntryContainer - Value.
    def projectInternalEnvEntryContainers(self):

        return self._projectInternalEnvEntryContainers

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of mMeco.libs.entryLib.EnvEntryContainer - Value.
    def projectExternalEnvEntryContainers(self):

        return self._projectExternalEnvEntryContainers

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of mMeco.libs.entryLib.EnvEntryContainer - Value.
    def masterProjectInternalEnvEntryContainers(self):

        return self._masterProjectInternalEnvEntryContainers

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of mMeco.libs.entryLib.EnvEntryContainer - Value.
    def masterProjectExternalEnvEntryContainers(self):

        return self._masterProjectExternalEnvEntryContainers

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Sort env entry containers.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def sortReservedEnvEntryContainers(self):

        if self._reservedEnvEntryContainers:
            self._reservedEnvEntryContainers.sort(key=lambda x: x.packageName())

    #
    ## @brief Sort env entry containers.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def sortDevelopmentEnvEntryContainers(self):

        if self._developmentEnvEntryContainers:
            self._developmentEnvEntryContainers.sort(key=lambda x: x.packageName())

    #
    ## @brief Sort env entry containers.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def sortStageEnvEntryContainers(self):

        if self._stageEnvEntryContainers:
            self._stageEnvEntryContainers.sort(key=lambda x: x.packageName())

    #
    ## @brief Sort env entry containers.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def sortProjectInternalEnvEntryContainers(self):

        if self._projectInternalEnvEntryContainers:
            self._projectInternalEnvEntryContainers.sort(key=lambda x: x.packageName())

    #
    ## @brief Sort env entry containers.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def sortProjectExternalEnvEntryContainers(self):

        if self._projectExternalEnvEntryContainers:
            self._projectExternalEnvEntryContainers.sort(key=lambda x: x.packageName())

    #
    ## @brief Sort env entry containers.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def sortMasterProjectInternalEnvEntryContainers(self):

        if self._masterProjectInternalEnvEntryContainers:
            self._masterProjectInternalEnvEntryContainers.sort(key=lambda x: x.packageName())

    #
    ## @brief Sort env entry containers.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def sortMasterProjectExternalEnvEntryContainers(self):

        if self._masterProjectExternalEnvEntryContainers:
            self._masterProjectExternalEnvEntryContainers.sort(key=lambda x: x.packageName())

    #
    ## @brief Display pre build env envEntry container.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def displayPreBuildEnvEntryContainers(self):

        self._displayEnvEntryContainers(self._preBuildEnvEntryContainers)

    #
    ## @brief Display post build env envEntry container.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def displayPostBuildEnvEntryContainers(self):

        self._displayEnvEntryContainers(self._postBuildEnvEntryContainers)

    #
    ## @brief Display reserved env envEntry container.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def displayReservedEnvEntryContainers(self):

        self._displayEnvEntryContainers(self._reservedEnvEntryContainers)

    #
    ## @brief Display development env envEntry container.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def displayDevelopmentEnvEntryContainers(self):

        self._displayEnvEntryContainers(self._developmentEnvEntryContainers)

    #
    ## @brief Display stage env envEntry container.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def displayStageEnvEntryContainers(self):

        self._displayEnvEntryContainers(self._stageEnvEntryContainers)

    #
    ## @brief Display project internal env envEntry container.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def displayProjectInternalEnvEntryContainers(self):

        self._displayEnvEntryContainers(self._projectInternalEnvEntryContainers)

    #
    ## @brief Display project external env envEntry container.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def displayProjectExternalEnvEntryContainers(self):

        self._displayEnvEntryContainers(self._projectExternalEnvEntryContainers)

    #
    ## @brief Display master project internal env envEntry container.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def displayMasterProjectInternalEnvEntryContainers(self):

        self._displayEnvEntryContainers(self._masterProjectInternalEnvEntryContainers)

    #
    ## @brief Display master project external env envEntry container.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def displayMasterProjectExternalEnvEntryContainers(self):

        self._displayEnvEntryContainers(self._masterProjectExternalEnvEntryContainers)

    #
    ## @brief Build.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def build(self):

        self._preBuild()

        self._build()

        self._postBuild()

