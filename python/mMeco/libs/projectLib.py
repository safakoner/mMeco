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
## @file    mMeco/libs/projectLib.py @brief [ FILE   ] - Meco project library.
## @package mMeco.libs.projectLib    @brief [ MODULE ] - Meco project library.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
from   getpass import getuser

import mMeco.core.displayLib

import mMeco.fileSystem.directoryLib
import mMeco.fileSystem.fileLib

import mMeco.core.platformLib
import mMeco.core.enumAbs
import mMeco.libs.enumLib

import mMecoPackage.packageLib

import mMecoSettings.settingsLib


#
# -----------------------------------------------------------------------------------------------------
# CODE
# -----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Class to operate on Meco projects.
class Project(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  This method calls setPackage method regardless absolutePath argument is provided or not.
    #
    #  @param name [ str | None | in  ] - Name of the project to be set.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, name=None):

         ## [ str ] - Projects path.
        self._projectsPath  = mMecoSettings.settingsLib.getProjectsPath(mMeco.core.platformLib.Platform.system())

        ## [ str ] - Project name.
        self._name          = None

        ## [ str ] - Project root.
        self._projectRoot   = None

        if name:
            self.setProject(name)

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    ## @name PROPERTIES

    ## @{
    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Project name.
    def name(self):

        return self._name

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Project root.
    def projectRoot(self):

        return self._projectRoot

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Set project.
    #
    #  @param name [ str | None | in  ] - Name of the project to be set.
    #
    #  @exception IOError - If a project with given `name` doesn't exist.
    #
    #  @return bool - Result.
    def setProject(self, name):

        projectRoot = os.path.join(self._projectsPath, name)

        if not os.path.isdir(projectRoot):
            raise IOError('Project does not exist: {}'.format(projectRoot))

        self._name        = name
        self._projectRoot = projectRoot

        return True

    #
    ## @brief Get absolute path of given `relativePath`.
    #
    #  Method doesn't check whether the returned path exists.
    #
    #  @param relativePath [ str | None | in  ] - A value from mMeco.libs.enumLib.ProjectFolderStructure enum class.
    #
    #  @exception N/A
    #
    #  @return str  - Absolute path of the requested folder.
    #  @return None - If no package has been set.
    def getLocalPath(self, relativePath):

        if not self._projectRoot:
            return None

        return os.path.join(self._projectRoot, relativePath)

    #
    ## @brief Get absolute path of the requested local help file.
    #
    #  @param folder [ str | None | in  ] - A value from mMeco.libs.enumLib.ProjectFolderStructure enum class.
    #
    #  @exception N/A
    #
    #  @return str  - Absolute path of the help file.
    #  @return None - If help file doesn't exist.
    #  @return None - If no project has been set.
    def getLocalHelpFile(self, folder):

        if not self._projectRoot:
            return None

        htmlFile = os.path.join(self._projectRoot, folder, 'html', 'index.html')
        if os.path.isfile(htmlFile):
            return htmlFile

        return None

    #
    ## @brief Create reserved environment.
    #
    #  @param developerName [ str | getuser() | in  ] - Name of the developer.
    #
    #  @exception IOError - If reserved environment already exists.
    #
    #  @return str - Absolute path of the reserved environment.
    def createReservedEnvironment(self, developerName=getuser()):

        reservedEnvPath = mMecoSettings.settingsLib.getReservedPackagesPath(developerName=developerName,
                                                                            platformName=mMeco.core.platformLib.Platform.system())

        if os.path.isdir(reservedEnvPath):
            raise IOError('Reserved environment already exists: {}'.format(reservedEnvPath))

        os.makedirs(reservedEnvPath)

        return reservedEnvPath

    #
    ## @brief Create development environment.
    #
    #  @param name          [ str | None      | in  ] - Name of the development environment.
    #  @param developerName [ str | getuser() | in  ] - Name of the developer.
    #
    #  @exception IOError - If development environment with given `name` already exists.
    #
    #  @return str - Absolute path of the development environment.
    def createDevelopmentEnvironment(self, name, developerName=getuser()):

        developmentEnvPath = mMecoSettings.settingsLib.getDevelopmentPackagesPath(projectName=self._name,
                                                                                  developerName=developerName,
                                                                                  developmentEnvName=name,
                                                                                  platformName=mMeco.core.platformLib.Platform.system(),
                                                                                  create=False)

        if os.path.isdir(developmentEnvPath):
            raise IOError('Development environment already exists: {}'.format(developmentEnvPath))

        os.makedirs(developmentEnvPath)

        return developmentEnvPath

    #
    ## @brief Create stage environment.
    #
    #  @param name               [ str  | None      | in  ] - Name of the stage environment.
    #  @param developmentEnvName [ str  | None      | in  ] - Name of the development environment where packages will be copied from.
    #  @param developerName      [ str  | getuser() | in  ] - Name of the developer who owns the development and stage environment.
    #  @param verbose            [ bool | False     | in  ] - Displayed created package names.
    #
    #  @exception IOError - If development environment with given `developmentEnvName` doesn't exist.
    #  @exception IOError - If stage environment with given `name` already exists.
    #  @exception IOError - If no package found in development environment.
    #
    #  @return str - Absolute path of the stage environment.
    def createStageEnvironment(self, name, developmentEnvName, developerName=getuser(), verbose=False):

        developmentPackagesPath = mMecoSettings.settingsLib.getDevelopmentPackagesPath(projectName=self._name,
                                                                                       developerName=developerName,
                                                                                       developmentEnvName=developmentEnvName,
                                                                                       platformName=mMeco.core.platformLib.Platform.system(),
                                                                                       create=False)

        if not os.path.isdir(developmentPackagesPath):
            raise IOError('Development environment doesn\'t exist: {}'.format(developmentPackagesPath))

        #

        stagePackagesPath = mMecoSettings.settingsLib.getStagePackagesPath(projectName=self._name,
                                                                           developerName=developerName,
                                                                           stageEnvName=name,
                                                                           platformName=mMeco.core.platformLib.Platform.system())

        if os.path.isdir(stagePackagesPath):
            raise IOError('Stage environment already exists: {}'.format(stagePackagesPath))

        _dir = mMeco.fileSystem.directoryLib.Directory(developmentPackagesPath)

        directoryList = _dir.listDirectories()
        if not directoryList:
            raise IOError('No package found in development environment: {}'.format(developmentPackagesPath))

        _package    = mMecoPackage.packageLib.Package()
        _file       = mMeco.fileSystem.fileLib.File()

        if verbose:
            mMeco.core.displayLib.Display.displayBlankLine()

        for package in directoryList:

            if not _package.setPackage(package):
                continue

            _dir.setDirectory(package)

            packageFileList = _dir.listFilesRecursively(relative=True, ignoreExtensions=['.pyc'])
            if not packageFileList:
                continue

            for packageFile in packageFileList:

                fromFile = mMeco.fileSystem.directoryLib.Directory.join(package, packageFile)
                toFile   = mMeco.fileSystem.directoryLib.Directory.join(stagePackagesPath, _package.name(), packageFile)

                _file.setFile(fromFile)
                _file.copy(toFile)

            if verbose:
                mMeco.core.displayLib.Display.displaySuccess('Stage Package Created: {}'.format(_package.name()), startNewLine=False)

        return stagePackagesPath

    #
    # ------------------------------------------------------------------------------------------------
    # STATIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Create a project.
    #
    #  @param name [ str | None | in  ] - Name of the project, which will be created.
    #
    #  @exception IOError - If a project with given `name` already exists.
    #
    #  @return mMeco.libs.projectLib.Project - Instance of mMeco.libs.projectLib.Project, which represents the created project.
    @staticmethod
    def create(name):

        projectsPath = mMecoSettings.settingsLib.getProjectsPath(mMeco.core.platformLib.Platform.system())
        projectsPath = os.path.join(projectsPath, name)

        if os.path.isdir(projectsPath):
            raise IOError('Project already exists: {}'.format(projectsPath))

        for path in mMeco.libs.enumLib.ProjectFolderStructure.listAttributes(getValues=True):
            os.makedirs(os.path.join(projectsPath, path))

        return Project(name)

    #
    ## @brief List projects
    #
    #  @exception IOError - If projects path doesn't exist.
    #
    #  @return list of str - Name of the projects.
    @staticmethod
    def list():

        projectsPath = mMecoSettings.settingsLib.getProjectsPath(mMeco.core.platformLib.Platform.system())

        if not os.path.isdir(projectsPath):
            raise IOError('Projects path does not exist: {}'.format(projectsPath))

        return mMeco.fileSystem.directoryLib.Directory(projectsPath).listFolders()

