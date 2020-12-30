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
## @file    mMeco/fileSystem/directoryLib.py    @brief [ FILE   ] - Directory.
## @package mMeco.fileSystem.directoryLib       @brief [ MODULE ] - Directory.

#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
import re
import shutil

import mMeco.core.platformLib

import mMeco.fileSystem.exceptionLib
import mMeco.fileSystem.versionLib


#
# -----------------------------------------------------------------------------------------------------
# CODE
# -----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Class to operate on directories.
class Directory(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param directory [ str | None | in  ] - Absolute path of a directory.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, directory=None):

        ## [ str ] - Directory that being worked on.
        self._directory            = None

        if directory:
            self.setDirectory(directory)

    #
    # ------------------------------------------------------------------------------------------------
    # PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief This method is used by mMeco.fileSystem.directoryLib.Directory.listDirectoriesRecursively method.
    #
    #  @param directory     [ str           | None | in  ] - Absolute path of a directory.
    #  @param directories   [ list of str   | None | in  ] - Where the subdirectories will be stored.
    #  @param ignoreDot     [ bool          | True | in  ] - Ignore directories that start with dot (hidden directories).
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _listDirectoriesRecursively(self, directory, directories, ignoreDot=True):

        if not os.path.isdir(directory):
            return

        directoryList = [Directory.join(directory, x) for x in os.listdir(directory) if
                         os.path.isdir(Directory.join(directory, x))]
        if not directoryList:
            return

        if ignoreDot:
            directoryList = [x for x in directoryList if not x.startswith('.')]

        directories.extend(directoryList)

        for d in directoryList:
            self._listDirectoriesRecursively(d, directories)

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    ## @name PROPERTIES

    ## @{
    #
    ## @brief Directory.
    #
    #  @exception N/A
    #
    #  @return str  - Directory.
    #  @return None - If a directory is not set previously.
    def directory(self):

        return self._directory

    #
    ## @brief Set directory.
    #
    #  @param directory [ str | None | in  ] - Absolute path of a directory.
    #
    #  @exception N/A
    #
    #  @return bool - Returns False if directory doesn't exist.
    def setDirectory(self, directory):

        if not os.path.isdir(directory):
            return False

        self._directory = Directory.removeEndSeparator(directory)

        return True

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    ## @name QUERY

    ## @{
    #
    ## @brief Whether a directory has been set.
    #
    #  @exception mMeco.fileSystem.exceptionLib.DirectoryIsNotSet - If no directory has been set.
    #
    #  @return bool - Result.
    def hasBeenSet(self):

        if not self._directory:
            raise mMeco.fileSystem.exceptionLib.DirectoryIsNotSet('No directory has been set.')

        return True

    #
    ## @brief Whether the directory exists.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def exists(self):

        if not self.hasBeenSet():
            return False

        return os.path.isdir(self._directory)

    #
    ## @}

    ## @name OPERATION

    ## @{
    #
    ## @brief Rename the directory.
    #
    #  Method renames the last folder and sets it.
    #
    #  @param newName [ str | None | in  ] - New name of the directory.
    #
    #  @exception mMeco.fileSystem.exceptionLib.DirectoryAlreadyExists - If a directory with given newName already exists.
    #
    #  @return bool - Returns False if a directory is not set previously or doesn't exist.
    def rename(self, newName):

        if not self.exists():
            return False

        newDirectory = Directory.join(os.path.dirname(self._directory), newName)

        if os.path.isdir(newDirectory):
            raise mMeco.fileSystem.exceptionLib.DirectoryAlreadyExists('Directory already exists, it could not be renamed: {}'.format(newDirectory))

        os.rename(self._directory, newDirectory)

        self.setDirectory(directory=newDirectory)

        return True

    #
    ## @brief Delete the current folder and everything inside it.
    #
    #  Parent directory will be automatically set if deletion is successful.
    #
    #  @exception N/A
    #
    #  @return bool - Returns False if a directory is not set previously or doesn't exist.
    def remove(self):

        if not self.exists():
            return False

        shutil.rmtree(self._directory)

        self.setDirectory(os.path.dirname(self._directory))

        return True

    #
    ## @brief Create a folder in the directory.
    #
    #  You can use slash separated folders, i.e. folderOne/folderTwo for `folderName` argument.
    #  Method returns True if a folder with folderName already exists.
    #
    #  @param folderName   [ str  | None | in ] - Name of the folder.
    #  @param setDirectory [ bool | None | in ] - Set newly created directory.
    #
    #  @exception N/A
    #
    #  @return bool - Returns `False` if a directory is not set previously or doesn't exist.
    def createFolder(self, folderName, setDirectory=True):

        if not self.exists():
            return False

        directory = Directory.join(self._directory, folderName)
        if os.path.isdir(directory):
            if setDirectory:
                self.setDirectory(directory)
            return True

        os.makedirs(directory)

        if setDirectory:
            self.setDirectory(directory)

        return True

    #
    ## @}

    ## @name INFORMATION

    ## @{
    #
    ## @brief Get base name of the directory (name of the last folder of the directory).
    #
    #  @exception N/A
    #
    #  @return str  - Base name.
    #  @return None - Returns None if a directory is not set previously or it doesn't exist.
    def getBaseName(self):

        if not self.exists():
            return None

        return os.path.basename(self._directory)

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # DIRECTORIES & FOLDERS
    # ------------------------------------------------------------------------------------------------
    ## @name LIST DIRECTORIES & FOLDERS

    ## @{
    #
    ## @brief List folders.
    #
    #  @param ignoreDot [ bool | True | in  ] - Ignore folders that start with dot (hidden folders).
    #
    #  @exception N/A
    #
    #  @return list of str - Folders.
    def listFolders(self, ignoreDot=True):

        if not self.exists():
            return None

        folders = sorted([x for x in os.listdir(self._directory) if os.path.isdir(os.path.join(self._directory, x))])

        if ignoreDot:
            folders = [x for x in folders if not x.startswith('.')]

        return folders

    #
    ## @brief List directories (with absolute path).
    #
    #  @param ignoreDot [ bool | True | in  ] - Ignore directories that start with dot (hidden directories).
    #
    #  @exception N/A
    #
    #  @return list of str - Directories.
    def listDirectories(self, ignoreDot=True):

        if not self.exists():
            return None

        directoryList = [os.path.join(self._directory, x) for x in os.listdir(self._directory) \
                         if os.path.isdir(os.path.join(self._directory, x))]

        if ignoreDot:
            directoryList = [x for x in directoryList if not x.startswith('.')]

        return sorted(directoryList)



    #
    ## @brief List directories recursively.
    #
    #  @param ignoreDot [ bool | True | in  ] - Ignore directories that start with dot (hidden directories).
    #
    #  @exception N/A
    #
    #  @return list of str - Directories.
    #  @return None        - Returns None if a directory is not set previously or doesn't exist.
    def listDirectoriesRecursively(self, ignoreDot=True):

        if not self.exists():
            return None

        directories = []

        self._listDirectoriesRecursively(self._directory, directories, ignoreDot)

        directories.sort()

        return directories

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # FILES
    # ------------------------------------------------------------------------------------------------
    ## @name LIST FILES

    ## @{
    #
    ## @brief List files.
    #
    #  @param ignoreDot [ bool | True | in  ] - Ignore files that start with dot (hidden files).
    #  @param extension [ str  | None | in  ] - Extension of the files that need to be listed.
    #
    #  @exception N/A
    #
    #  @return list of str - Files.
    #  @return None        - Returns None if a directory is not set previously or doesn't exist.
    def listFiles(self, ignoreDot=True, extension=None):

        if not self.exists():
            return None

        fileList = []

        if extension:
            if not extension.startswith('.'):
                extension = '.{}'.format(extension)
            fileList = [x for x in os.listdir(self._directory) if os.path.splitext(x)[1] == extension]
        else:
            fileList = [x for x in os.listdir(self._directory) if os.path.isfile(Directory.join(self._directory, x))]

        if ignoreDot and fileList:
            fileList = [x for x in fileList if not x.startswith('.')]

        if fileList:
            fileList = sorted(fileList)

        return fileList

    #
    ## @brief List files with absolute path.
    #
    #  If you don't provide directory argument self directory will be used.
    #
    #  @param directory [ str  | None | in  ] - Directory that will be searched.
    #  @param ignoreDot [ bool | True | in  ] - Ignore files that start with dot (hidden files).
    #  @param extension [ str  | None | in  ] - Extension of the files that need to be found.
    #
    #  @exception N/A
    #
    #  @return list of str - Files.
    #  @return None        - Returns None if a directory is not set previously or doesn't exist.
    def listFilesWithAbsolutePath(self, directory=None, ignoreDot=True, extension=None):

        if not directory:
            directory = self._directory

        if not directory:
            return None

        if not os.path.isdir(directory):
            return None

        fileList = []

        if extension:
            if not extension.startswith('.'):
                extension = '.{}'.format(extension)
            fileList = [Directory.join(directory, x) for x in os.listdir(directory) if
                        os.path.splitext(x)[1] == extension]
        else:
            fileList = [Directory.join(directory, x) for x in os.listdir(directory) if
                        os.path.isfile(Directory.join(directory, x))]

        if not ignoreDot:
            return sorted(fileList)

        newFileList = []

        for i in fileList:
            match = re.search(r'\S+[\\|/]\.\w+', i)
            if match:
                continue
            newFileList.append(i)

        if newFileList:
            newFileList = sorted(newFileList)

        return newFileList

    #
    ## @brief List files including files under sub directories recursively.
    #
    #  All hidden directories and files will be ignored if you provide True for ignoreDot argument.
    #
    #  @param relative         [ bool | False | in  ] - List files relative to the directory.
    #  @param extension        [ str  | None  | in  ] - Extension of the files that need to be listed.
    #  @param ignoreDot        [ bool | True  | in  ] - Ignore files that start with dot (hidden files).
    #  @param ignoreExtensions [ list | None  | in  ] - Extensions that will be ignored.
    #
    #  @exception N/A
    #
    #  @return list of str - Files.
    #  @return None        - Returns None if a directory is not set previously or doesn't exist.
    def listFilesRecursively(self, relative=False, extension=None, ignoreDot=True, ignoreExtensions=None):

        if not self.exists():
            return None

        filesList = []

        # Current directory
        filesList.extend([x for x in self.listFilesWithAbsolutePath(directory=self._directory,
                                                                    ignoreDot=ignoreDot,
                                                                    extension=extension) if x])

        # Sub directories
        directories = self.listDirectoriesRecursively(ignoreDot=ignoreDot)
        if directories:
            for d in directories:
                filesList.extend(f for f in self.listFilesWithAbsolutePath(directory=d,
                                                                           ignoreDot=ignoreDot,
                                                                           extension=extension))

        if filesList and relative:
            filesList = [x.split(self._directory)[1] for x in filesList]

        if filesList and ignoreExtensions:
            filesList = [x for x in filesList if not os.path.splitext(x)[1] in ignoreExtensions]

        if filesList:
            filesList.sort()

        return filesList

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # STATIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Split given path by ignoring empty parts.
    #
    #  @param directory [ str | None | in  ] - Directory.
    #
    #  @exception N/A
    #
    #  @return list of str - Directory.
    @staticmethod
    def split(directory):

        return [x for x in directory.split(os.sep) if x]

    ## @name SEPARATOR

    ## @{
    #
    ## @brief Get native separator.
    #
    #  @exception N/A
    #
    #  @return str - Separator.
    @staticmethod
    def separator():

        return os.sep

    #
    ## @brief Add separator at the start of the given directory.
    #
    #  @param directory [ str | None | in  ] - Directory.
    #
    #  @exception N/A
    #
    #  @return str - Directory.
    @staticmethod
    def addStartSeparator(directory):

        if not directory.startswith(os.sep):
            directory = '{}{}'.format(os.sep, directory)

        return directory

    #
    ## @brief Add separator at the end of the given directory.
    #
    #  @param directory [ str | None | in  ] - Directory.
    #
    #  @exception N/A
    #
    #  @return str - Directory.
    @staticmethod
    def addEndSeparator(directory):

        if not directory.endswith(os.sep):
            directory = '{}{}'.format(directory, os.sep)

        return directory

    #
    ## @brief Remove separator at the beginning of the given directory.
    #
    #  @param directory [ str | None | in  ] - Directory.
    #
    #  @exception N/A
    #
    #  @return str - Directory.
    @staticmethod
    def removeStartSeparator(directory):

        if directory.startswith(os.sep):
            directory = directory[1:]

        return directory

    #
    ## @brief Remove separator at the end of the given directory.
    #
    #  @param directory [ str | None | in  ] - Directory.
    #
    #  @exception N/A
    #
    #  @return str - Directory.
    @staticmethod
    def removeEndSeparator(directory):

        if directory.endswith(os.sep):
            directory = directory[:-1]

        return directory

    #
    ## @brief Convert separators in given directory to native separators.
    #
    #  Separator will only be added at the beginning of the directory if startWithSeparator
    #  provided True and the platform is not Windows.
    #
    #  @param directory          [ str  | None  | in  ] - Directory.
    #  @param startWithSeparator [ bool | True  | in  ] - Add separator at the beginning.
    #  @param endWithSeparator   [ bool | False | in  ] - Add separator at the end.
    #
    #  @exception N/A
    #
    #  @return str - Directory.
    @staticmethod
    def toNativeSeparators(directory, startWithSeparator=True, endWithSeparator=False):

        directory = directory.replace('\\\\', os.sep)
        directory = directory.replace('\\', os.sep)
        directory = directory.replace('//', os.sep)
        directory = directory.replace('/', os.sep)

        if startWithSeparator:
            # Add separator at the beginning if OS is not Windows
            if not mMeco.core.platformLib.Platform.isWindows():
                directory = Directory.addStartSeparator(directory)
        else:
            # Remove separator at the beginning
            directory = Directory.removeStartSeparator(directory)

        if endWithSeparator:
            # Add separator at the end
            directory = Directory.addEndSeparator(directory)
        else:
            # Remove separator at the end
            directory = Directory.removeEndSeparator(directory)

        return directory

    #
    ## @}

    ## @name JOIN

    ## @{
    #
    #
    ## @brief Join given directories and make sure that right separator is used based on the current platform.
    #
    #  @param directory    [ str, list, tuple | None | in  ] - Directory.
    #  @param *directories [ str              | None | in  ] - Directories.
    #
    #  @exception N/A
    #
    #  @return str - Directory.
    @staticmethod
    def join(directory, *directories):

        if not directory:
            directory = ''

        finalDirectory = directory

        if isinstance(finalDirectory, list) or isinstance(finalDirectory, tuple):
            finalDirectory = os.sep.join(finalDirectory)

        if directories:
            for d in directories:
                if not d:
                    continue
                d = Directory.removeStartSeparator(d)
                finalDirectory = os.path.join(finalDirectory, d)

        return Directory.toNativeSeparators(finalDirectory)

    #
    ## @brief Join given directories and make sure that right separator is used based on the current platform.
    #
    #  This method removes separator at the start and at the end of the joined directory.
    #
    #  @param directory    [ str, list, tuple | None | in  ] - Directory.
    #  @param *directories [ str              | None | in  ] - Directories.
    #
    #  @exception N/A
    #
    #  @return str - Directory.
    @staticmethod
    def joinRelative(directory, *directories):

        directory = Directory.join(directory, *directories)
        directory = Directory.removeStartSeparator(directory)
        directory = Directory.removeEndSeparator(directory)

        return directory

    #
    ## @}

    #
    ## @brief Navigate up by giving level.
    #
    #  If '/somePath/with/someOther/folder' is provided, with level 2 the result
    #  would be '/somePath/with'
    #
    #  @param directory  [ str | None | in  ] - Directory.
    #  @param level      [ int | 1    | in  ] - How many times will be navigated up.
    #
    #  @exception N/A
    #
    #  @return str - Directory.
    @staticmethod
    def navigateUp(directory, level=1):

        directory = Directory.removeEndSeparator(directory)

        for i in range(level):
            directory = os.path.abspath(Directory.join(directory, '..'))

        return directory

    #
    ## @brief Create a directory.
    #
    #  mMeco.fileSystem.directoryLib.Directory class instance will be returned for the directory
    #  whether it was exists or newly created.
    #
    #  @param directory [ str | None | in  ] - Directory.
    #
    #  @exception N/A
    #
    #  @return mMeco.fileSystem.directoryLib.Directory - Instance of mMeco.fileSystem.directoryLib.Directory class.
    @staticmethod
    def create(directory):

        if os.path.isdir(directory):
            return Directory(directory=directory)

        os.makedirs(directory)

        return Directory(directory=directory)

    #
    ## @brief Check whether the given directory exists.
    #
    #  @param directory [ str | None | in  ] - Directory.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    @staticmethod
    def directoryExists(directory):

        return os.path.isdir(directory)

    ## @name VERSION

    ## @{
    #
    ## @brief List version folder(s) under given path.
    #
    #  This is a generic method which lists versioned folder(s) under given path.
    #
    #  Semantic version naming convention is 1.2.3 ([0-9]{1,}\.[0-9]{1,}\.[0-9]{1,})
    #
    #  Say you have three folders under a path, like;
    #
    #  - 1.0.0
    #  - 2.0.0
    #  - 3.0.0
    #
    #  The following results would occur for given version options.
    #
    #  Version Option                       | Lists           |
    #  ------------------------------------ | --------------- |
    #  sCore.versionLib.Version.kAll        | All the folders |
    #  sCore.versionLib.Version.kLatest     | 3.0.0           |
    #  sCore.versionLib.Version.kCurrent    | 3.0.0           |
    #  sCore.versionLib.Version.kFirst      | 1.0.0           |
    #  sCore.versionLib.Version.kLast       | 3.0.0           |
    #  sCore.versionLib.Version.kPrevious   | 2.0.0           |
    #  '2.0.0'                              | 2.0.0           |
    #  '2.0.1'                              | None            |
    #  2 / '2' / '02' / '002'               | None            |
    #
    #  @param directory    [ str       | None  | in  ] - Directory where the versioned folders are.
    #  @param absolutePath [ bool      | None  | in  ] - Whether to return absolute path of the versioned folders.
    #  @param version      [ enum, str | None  | in  ] - Requested version from sFileSystem.versionLib.Version class or a string that would match with the name of the versioned folder.
    #  @param semanticOnly [ bool      | None  | in  ] - Check semantic version, leave out any folder without semantic version naming convention.
    #  @param ignore       [ bool      | False | in  ] - Ignore if requested version doesn't exist and return the path of the version folder anyway.
    #  @param createPath   [ bool      | True  | in  ] - Create given path if it doesn't exist.
    #
    #  @exception N/A
    #
    #  @return None        - If no versioned folder found.
    #  @return str         - Versioned folder.
    #  @return list of str - If all versions are requested.
    @staticmethod
    def listVersionedFolders(directory,
                             absolutePath=False,
                             version=mMeco.fileSystem.versionLib.Version.kLatest,
                             semanticOnly=True,
                             ignore=False,
                             createPath=False):

        if not os.path.isdir(directory):
            if createPath:
                os.makedirs(directory)
                return None
            else:
                return None

        _directory  = Directory(directory)

        versionList = None

        if absolutePath:
            versionList = _directory.listDirectories()
        else:
            versionList = _directory.listFolders()

        if versionList and semanticOnly:
            versionList = [x for x in versionList if re.search(r'([0-9]{1,}\.[0-9]{1,}\.[0-9]{1,})', x)]

        if versionList:
            versionList.sort(key=lambda x: [int(x) for x in x.split('.')])


        if version == mMeco.fileSystem.versionLib.Version.kAll:
            return versionList

        elif version == mMeco.fileSystem.versionLib.Version.kLatest:
            return versionList[-1:][0]

        elif version == mMeco.fileSystem.versionLib.Version.kCurrent:
            return versionList[-1:][0]

        elif version == mMeco.fileSystem.versionLib.Version.kFirst:
            return versionList[:1][0]

        elif version == mMeco.fileSystem.versionLib.Version.kLast:
            return versionList[-1:][0]

        elif version == mMeco.fileSystem.versionLib.Version.kPrevious:
            if len(versionList) < 2:
                return versionList[0]
            return versionList[-2:][0]

        else:
            versionList = [x for x in versionList if x == version]
            if versionList:
                return versionList[0]

            if ignore:
                # We ignore if requested version folder doesn't exist
                if absolutePath:
                    return os.path.join(directory, version)
                else:
                    return version
            else:
                return None

        return None

    #
    ## @brief List versioned file(s) under given path.
    #
    #  This is a generic method which lists versioned file(s) under given path.
    #
    #  Say you have three files under a path, like;
    #
    #  - file.v001.txt
    #  - file.v002.txt
    #  - file.v003.txt
    #
    #  The following results would occur for given version options.
    #
    #  Version Option                       | Lists         |
    #  ------------------------------------ | ------------- |
    #  mCore.versionLib.Version.kAll        | All the files |
    #  mCore.versionLib.Version.kLatest     | file.v003.txt |
    #  mCore.versionLib.Version.kCurrent    | file.v003.txt |
    #  mCore.versionLib.Version.kFirst      | file.v001.txt |
    #  mCore.versionLib.Version.kLast       | file.v003.txt |
    #  mCore.versionLib.Version.kPrevious   | file.v002.txt |
    #  2 / '2' / '02' / '002'               | file.v002.txt |
    #
    #  @param directory    [ str            | None  | in  ] - Directory where the versioned files are.
    #  @param absolutePath [ bool           | None  | in  ] - Whether to return absolute path of the versioned files.
    #  @param version      [ enum, str, int | None  | in  ] - Requested version from mMeco.fileSystem.versionLib.Version class, string or int that would match with the version of the file.
    #  @param extension    [ str            | None  | in  ] - Extension of the files to be listed.
    #  @param createPath   [ bool           | True  | in  ] - Create given path if it doesn't exist.
    #
    #  @exception N/A
    #
    #  @return None        - If no versioned file found.
    #  @return str         - Versioned file.
    #  @return list of str - If all versions are requested via mCore.versionLib.Version.kAll.
    @staticmethod
    def listVersionedFiles(directory,
                          absolutePath=False,
                          version=mMeco.fileSystem.versionLib.Version.kLatest,
                          extension=None,
                          createPath=True):

        if not os.path.isdir(directory):
            if createPath:
                os.makedirs(directory)
            else:
                return None

        _directory  = Directory(directory)

        versionList = None

        if absolutePath:
            versionList = _directory.listFilesWithAbsolutePath(extension=extension)
        else:
            versionList = _directory.listFiles(extension=extension)

        if versionList:
            versionList = [x for x in versionList if re.search(r'(.*?)(\w+)(\.v)([0-9]{3})(\.)?([aA-zZ]*)', x)]
            versionList.sort()
        else:
            return None


        if version == mMeco.fileSystem.versionLib.Version.kAll:
            return versionList

        elif version == mMeco.fileSystem.versionLib.Version.kLatest:
            return versionList[-1:][0]

        elif version == mMeco.fileSystem.versionLib.Version.kCurrent:
            return versionList[-1:][0]

        elif version == mMeco.fileSystem.versionLib.Version.kFirst:
            return versionList[:1][0]

        elif version == mMeco.fileSystem.versionLib.Version.kLast:
            return versionList[-1:][0]

        elif version == mMeco.fileSystem.versionLib.Version.kPrevious:
            if len(versionList) < 2:
                return versionList[0]
            return versionList[-2:][0]

        else:
            for v in versionList:
                match = re.search(r'\.v([0-9]{3})', v)
                if match and match.groups()[0] == '{0:03d}'.format(int(version)):
                    return v

        return None

    #
    ## @}
