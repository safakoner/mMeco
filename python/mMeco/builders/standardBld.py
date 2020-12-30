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
## @file    mMeco/builders/standardBld.py @brief [ FILE   ] - Builder.
## @package mMeco.builders.standardBld    @brief [ MODULE ] - Builder..


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os

import mMeco.abstract.builderAbs

import mMeco.libs.entryLib
import mMeco.libs.enumLib

import mMeco.operators.packageEnvOpt


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Builder class.
class Builder(mMeco.abstract.builderAbs.Builder):
    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC STATIC MEMBERS
    # ------------------------------------------------------------------------------------------------
    ## [ str ] - Name.
    NAME = 'standardBld'

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

        mMeco.abstract.builderAbs.Builder.__dict__['__init__'](self)

    #
    ## @brief Build package env by using package global env.
    #
    #  @param packageEnvContainer [ mMeco.builderLib.EnvEntryContainer         | None | in  ] - Env envEntry container.
    #  @param appFileOperator     [ mMeco.operators.appFileOpt.AppFileOperator | None | in  ] - App file operator.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _buildPackageByPackageGlobalEnv(self, packageEnvContainer, appFileOperator=None):

        globalEnvClassName  = 'Package'
        folderName          = ''
        version             = ''

        if appFileOperator:
            globalEnvClassName  = appFileOperator.globalEnvClassName()
            folderName          = appFileOperator.folderName()
            version             = appFileOperator.version()

        packageGlobalEnvClass = self._allLib.packageGlobalEnvOperator().getClass(globalEnvClassName)
        if not packageGlobalEnvClass:
            self._allLib.logger().addWarning('Package global env settings doesn\'t exist: {}'.format(globalEnvClassName))
            return

        for attr in packageGlobalEnvClass.attributes():

            for value in attr['value']:

                if 'FOLDER_NAME' in value and not folderName:
                    raise ValueError('App file must have "folderName" key for this configuration: {}'.format(appFileOperator.path()))
                else:
                    value = value.replace('FOLDER_NAME', folderName)

                if 'VERSION' in value and not appFileOperator:
                    raise ValueError('App file must have "version" key for this configuration: {}'.format(appFileOperator.path()))
                else:
                    value = value.replace('VERSION', version)

                path = os.path.join(packageEnvContainer.getPackageRootPath(),
                                    value)

                if not os.path.isdir(path):
                    continue

                packageEnvContainer.addMulti(attr['name'],
                                             path)

    #
    ## @brief Build packages for given `envType`.
    #
    #  @param path     [ str                           | None | in  ] - Env path, where the packages are
    #  @param packages [ list of dicts or list of str  | None | in  ] - Versioned or non-versioned packages.
    #  @param envType  [ enum                          | None | in  ] - Env type from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _buildPackages(self, path, packages, envType):

        if not packages:
            return

        packageEnvOperator = mMeco.operators.packageEnvOpt.PackageEnvOperator()

        for package in packages:

            packageEnvEntryContainer = None

            if isinstance(package, dict) and package['versions']:
                # Versioned package
                packageEnvEntryContainer = mMeco.libs.entryLib.EnvEntryContainer(containerType=mMeco.libs.enumLib.EnvEntryContainerType.kPackage,
                                                                                 path=path,
                                                                                 packageName=package['package'],
                                                                                 version=package['versions'][0])
            else:
                # NonVersioned package
                packageEnvEntryContainer = mMeco.libs.entryLib.EnvEntryContainer(containerType=mMeco.libs.enumLib.EnvEntryContainerType.kPackage,
                                                                                 path=path,
                                                                                 packageName=package)

            #

            # Build env based on package env module
            if not packageEnvOperator.invoke(packageEnvEntryContainer):
                continue

            # Build env based on package global env
            self._buildPackageByPackageGlobalEnv(packageEnvEntryContainer)

            # Build env based on package global env app
            if self._allLib.settingsOperator().appFilePath():
                self._buildPackageByPackageGlobalEnv(packageEnvEntryContainer,
                                                     self._allLib.appFileOperator())

            #

            packageEnvEntryContainer.sort()

            if envType == mMeco.libs.enumLib.EnvType.kReserved:
                self._reservedEnvEntryContainers.append(packageEnvEntryContainer)

            elif envType == mMeco.libs.enumLib.EnvType.kDevelopment:
                self._developmentEnvEntryContainers.append(packageEnvEntryContainer)

            elif envType == mMeco.libs.enumLib.EnvType.kStage:
                self._stageEnvEntryContainers.append(packageEnvEntryContainer)

            elif envType == mMeco.libs.enumLib.EnvType.kProjectInternal:
                self._projectInternalEnvEntryContainers.append(packageEnvEntryContainer)

            elif envType == mMeco.libs.enumLib.EnvType.kProjectExternal:
                self._projectExternalEnvEntryContainers.append(packageEnvEntryContainer)

            elif envType == mMeco.libs.enumLib.EnvType.kMasterProjectInternal:
                self._masterProjectInternalEnvEntryContainers.append(packageEnvEntryContainer)

            elif envType == mMeco.libs.enumLib.EnvType.kMasterProjectExternal:
                self._masterProjectExternalEnvEntryContainers.append(packageEnvEntryContainer)

    #
    ## @brief Callback which will be invoked before mMeco.abstract.buildersAbs.Builder._build method is invoked.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _preBuild(self):

        if self._allLib.request().ignorePre():
            return

        preBuildContainer = mMeco.libs.entryLib.EnvEntryContainer(containerType=mMeco.libs.enumLib.EnvEntryContainerType.kPreBuild)

        self._preBuildEnvEntryContainers.append(preBuildContainer)

        self._allLib.callbackOperator().invokePrePostBuild('getPreBuild', preBuildContainer)

        self._preBuildEnvEntryContainers.sort()

    #
    ## @brief Build.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def _build(self):

        # Reserved
        if self._allLib.solver().reservedEnvPath():
            self._buildPackages(self._allLib.settingsOperator().reservedPackagesPath(),
                                self._allLib.solver().reservedEnvPath().packages(),
                                mMeco.libs.enumLib.EnvType.kReserved)
            self.sortReservedEnvEntryContainers()

        # Development
        if self._allLib.solver().developmentEnvPath():
            self._buildPackages(self._allLib.settingsOperator().developmentPackagesPath(),
                                self._allLib.solver().developmentEnvPath().packages(),
                                mMeco.libs.enumLib.EnvType.kDevelopment)
            self.sortDevelopmentEnvEntryContainers()

        # Stage
        if self._allLib.solver().stageEnvPath():
            self._buildPackages(self._allLib.settingsOperator().stagePackagesPath(),
                                self._allLib.solver().stageEnvPath().packages(),
                                mMeco.libs.enumLib.EnvType.kStage)
            self.sortStageEnvEntryContainers()

        #

        # Project
        if self._allLib.solver().projectInternalEnvPath():
            self._buildPackages(self._allLib.settingsOperator().projectInternalPackagesPath(),
                                self._allLib.solver().projectInternalEnvPath().packages(),
                                mMeco.libs.enumLib.EnvType.kProjectInternal)
            self.sortProjectInternalEnvEntryContainers()

        if self._allLib.solver().projectExternalEnvPath():
            self._buildPackages(self._allLib.settingsOperator().projectExternalPackagesPath(),
                                self._allLib.solver().projectExternalEnvPath().packages(),
                                mMeco.libs.enumLib.EnvType.kProjectExternal)
            self.sortProjectExternalEnvEntryContainers()

        #

        # Master Project
        if self._allLib.solver().masterProjectInternalEnvPath():
            self._buildPackages(self._allLib.settingsOperator().masterProjectInternalPackagesPath(),
                                self._allLib.solver().masterProjectInternalEnvPath().packages(),
                                mMeco.libs.enumLib.EnvType.kMasterProjectInternal)
            self.sortMasterProjectInternalEnvEntryContainers()

        if self._allLib.solver().masterProjectExternalEnvPath():
            self._buildPackages(self._allLib.settingsOperator().masterProjectExternalPackagesPath(),
                                self._allLib.solver().masterProjectExternalEnvPath().packages(),
                                mMeco.libs.enumLib.EnvType.kMasterProjectExternal)
            self.sortMasterProjectExternalEnvEntryContainers()

        return True

    #
    ## @brief Callback which will be invoked after mMeco.abstract.buildersAbs.Builder._build method is invoked.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _postBuild(self):

        if self._allLib.request().ignorePost():
            return

        postBuildContainer = mMeco.libs.entryLib.EnvEntryContainer(containerType=mMeco.libs.enumLib.EnvEntryContainerType.kPostBuild)
        self._postBuildEnvEntryContainers.append(postBuildContainer)

        self._allLib.callbackOperator().invokePrePostBuild('getPostBuild', postBuildContainer)

        self._postBuildEnvEntryContainers.sort()
