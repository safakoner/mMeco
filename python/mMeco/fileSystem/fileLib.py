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
## @file    mMeco/fileSystem/fileLib.py @brief [ FILE   ] - Operate on files.
## @package mMeco.fileSystem.fileLib    @brief [ MODULE ] - Operate on files.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
import shutil

import mMeco.fileSystem.directoryLib
import mMeco.fileSystem.exceptionLib


#
# -----------------------------------------------------------------------------------------------------
# CODE
# -----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Operate on files.
class File(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param path [ str | None | in  ] - Absolute path of a file.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, path=None):

        ## [ str ] - Absolute path of the file.
        self._file      = None

        ## [ str ] - Directory where the file is located in.
        self._directory = None

        ## [ str ] - Name of the file with it's extension.
        self._fileName  = None

        ## [ str ] - Name of the file without extension, base name.
        self._baseName  = None

        ## [ str ] - File's extension.
        self._extension = None

        ## [ int ] - File size in bytes.
        self._size      = 0

        ## [ str ] - File size as human readable string.
        self._sizeStr   = None

        ## [ str ] - Content of the file.
        self._content   = None

        if path:
            self.setFile(path=path)

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
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    ## @name PROPERTIES

    ## @{
    #
    ## @brief Absolute path of the file.
    #
    #  @exception N/A
    #
    #  @return str - File.
    def file(self):

        return self._file

    #
    ## @brief Directory where the file is located in.
    #
    #  @exception N/A
    #
    #  @return str - Directory.
    def directory(self):

        return self._directory

    #
    ## @brief Name of the file with it's extension.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def fileName(self):

        return self._fileName

    #
    ## @brief Name of the file without extension, base name.
    #
    #  @exception N/A
    #
    #  @return str - Base name.
    def baseName(self):

        return self._baseName

    #
    ## @brief File's extension.
    #
    #  @exception N/A
    #
    #  @return str - Extension.
    def extension(self):

        return self._extension

    #
    ## @brief File size in bytes.
    #
    #  @exception N/A
    #
    #  @return int - Size.
    def size(self):

        return self._size

    #
    ## @brief File size as human readable string.
    #
    #  @exception N/A
    #
    #  @return str - Human readable size.
    def sizeStr(self):

        return self._sizeStr

    #
    ## @brief Content of the file.
    #
    #  @exception N/A
    #
    #  @return str         - If read method is used to read the content.
    #  @return list fo str - If readLines method is used to read the content.
    def content(self):

        return self._content

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Get string representation.
    #
    #  @exception N/A
    #
    #  @return str - String representation.
    def asStr(self):

        info = '\n'
        info += 'Object              : {}\n'.format(self.__class__)
        info += 'File                : {}\n'.format(self._file)
        info += 'Directory           : {}\n'.format(self._directory)
        info += 'File Name           : {}\n'.format(self._fileName)
        info += 'Base Name           : {}\n'.format(self._baseName)
        info += 'Extension           : {}\n'.format(self._extension)
        info += 'Size                : {}\n'.format(self._size)
        info += 'Size String         : {}\n'.format(self._sizeStr)

        return info

    #
    ## @brief Get file information as dict instance.
    #
    #  @exception N/A
    #
    #  @return dict - Keys are; file, directory, fileName, baseName, extension, size, sizeStr.
    def asDict(self):

        return {'file'      : self._file,
                'directory' : self._directory,
                'fileName'  : self._fileName,
                'baseName'  : self._baseName,
                'extension' : self._extension,
                'size'      : self._size,
                'sizeStr'   : self._sizeStr
                }

    #
    ## @brief Set file.
    #
    #  @param path [ str | None | in  ] - Absolute path of a file.
    #
    #  @exception N/A
    #
    #  @return bool - Result, returns `False` is the file doesn't exist, `True` otherwise.
    def setFile(self, path):

        if not os.path.isfile(path):
            self._file      = None
            self._directory = None
            self._fileName  = None
            self._baseName  = None
            self._extension = None
            self._size      = 0
            self._sizeStr   = None
            self._content   = None
            return False

        self._file      = path
        self._directory = os.path.dirname(path)
        self._fileName  = os.path.basename(path)
        self._baseName  = os.path.splitext(self._fileName)[0]
        self._extension = os.path.splitext(path)[1][1:]
        self._size      = os.path.getsize(self._file)
        self._sizeStr   = File.getFileSizeAsStr(self._size)

        return True

    #
    ## @brief Update information of the file in case it has been altered.
    #
    #  @exception N/A
    #
    #  @return bool - Result, returns False is the file doesn't exist.
    def update(self):

        if not self.exists():
            return False

        return self.setFile(self._file)

    #
    ## @brief Check whether the file exists.
    #
    #  @exception mMeco.fileSystem.exceptionLib.FileIsNotSet - If no file is set.
    #
    #  @return bool - Result, returns `False` is the file doesn't exist, `True` otherwise.
    def exists(self):

        if not self._file:
            raise mMeco.fileSystem.exceptionLib.FileIsNotSet('No file is set.')

        return os.path.isfile(self._file)

    #
    ## @brief Rename the file.
    #
    #  @param newName [ str | None | in  ] - New name of the file without the path.
    #
    #  @exception mMeco.fileSystem.exceptionLib.FileAlreadyExists - If a file with given newName already exists.
    #
    #  @return bool - Result.
    def rename(self, newName):

        if not self.exists():
            return False

        newFile = mMeco.fileSystem.directoryLib.Directory.join(self._directory, newName)

        if os.path.isfile(newFile):
            raise mMeco.fileSystem.exceptionLib.FileAlreadyExists('File could not be renamed because a file with new name already exists: {}'.format(newFile))

        shutil.move(self._file, newFile)

        self.setFile(path=newFile)

        return True

    ## @name COPY

    ## @{
    #
    #
    ## @brief Copy the file.
    #
    #  Method will create the destination path if it doesn't exist.
    #
    #  @param destinationFile [ str  | None  | in  ] - Destination file with absolute path.
    #  @param overwrite       [ bool | False | in  ] - Whether to overwrite existing file.
    #
    #  @exception mMeco.fileSystem.exceptionLib.FileDoesNotExist  - If source file doesn't exist.
    #  @exception mMeco.fileSystem.exceptionLib.FileAlreadyExists - If destination file exists and overwrite argument provided False.
    #
    #  @return str - Absolute path of copied file.
    def copy(self, destinationFile, overwrite=False):

        if not self.exists():
            raise mMeco.fileSystem.exceptionLib.FileDoesNotExist('Source file doesn\'t exist: {}'.format(self._file))

        # Destination file already exists
        if os.path.isfile(destinationFile) and not overwrite:
            raise mMeco.fileSystem.exceptionLib.FileAlreadyExists('Destination file already exists: {}'.format(destinationFile))

        # Create destination path
        destinationPath = os.path.dirname(destinationFile)
        if not os.path.isdir(destinationPath):
            os.makedirs(destinationPath)

        shutil.copy2(self._file, destinationFile)

        return destinationFile

    #
    ## @brief Copy the file to given path. File name will be intact.
    #
    #  Method will create the destination path if it doesn't exist.
    #
    #  @param destinationPath [ str  | None  | in  ] - Absolute path.
    #  @param overwrite       [ bool | False | in  ] - Whether to overwrite existing file.
    #
    #  @exception mMeco.fileSystem.exceptionLib.FileDoesNotExist  - If source file doesn't exist.
    #  @exception mMeco.fileSystem.exceptionLib.FileAlreadyExists - If destination file exists and overwrite argument provided False.
    #
    #  @return str - Absolute path of the copied file.
    def copyToPath(self, destinationPath, overwrite=False):

        if not self.exists():
            raise mMeco.fileSystem.exceptionLib.FileDoesNotExist('Source file doesn\'t exist: {}'.format(self._file))

        destinationFile = mMeco.fileSystem.directoryLib.Directory.join(destinationPath, self._fileName)

        # Destination file already exists
        if os.path.isfile(destinationFile) and not overwrite:
            raise mMeco.fileSystem.exceptionLib.FileAlreadyExists('Destination file already exists: {}'.format(destinationFile))

        # Create destination path
        if not os.path.isdir(destinationPath):
            os.makedirs(destinationPath)

        shutil.copy2(self._file, destinationFile)

        return destinationFile

    #
    ## @}

    #
    ## @brief Remove the file.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def remove(self):

        if not self.exists():
            return False

        os.remove(self._file)

        try:
            # Set this instance to None, since this will raise an IOError
            # this we do not give an existing file
            # Catch it, user doesn't need to know about the exception
            self.setFile('')
        except:
            pass

        return True

    ## @name CONTENT

    ## @{
    #
    ## @brief Write given line into the file.
    #
    #  @param line   [ str  | None | in  ] - Line to be written.
    #  @param append [ bool | True | in  ] - Whether the line will be appended.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def write(self, line, append=True):

        if not self.exists():
            return False

        _file = open(self._file, 'a' if append else 'w')
        _file.write(line)
        _file.close()

        self.update()

        return True

    #
    ## @brief Write given lines into the file.
    #
    #  @param lines  [ list of str | None | in  ] - Lines to be written.
    #  @param append [ bool        | True | in  ] - Whether the lines will be appended.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def writeLines(self, lines, append=True):

        if not self.exists():
            return False

        _file = open(self._file, 'a' if append else 'w')
        _file.writelines(lines)
        _file.close()

        self.update()

        return True

    #
    ## @brief Read content of the file.
    #
    #  @see content
    #
    #  @exception N/A
    #
    #  @return str  - Content.
    #  @return None - If file doesn't exist.
    def read(self):

        if not self.exists():
            return None

        _file = open(self._file, 'r')
        self._content = _file.read()
        _file.close()

        return self._content

    #
    ## @brief Read lines.
    #
    #  @see content
    #
    #  @exception N/A
    #
    #  @return list of str - Content.
    #  @return None        - If file doesn't exist.
    def readLines(self):

        if not self.exists():
            return None

        _file = open(self._file, 'r')
        self._content = _file.readlines()
        _file.close()

        return self._content

    #
    ## @brief Get line count of the file.
    #
    #  @exception N/A
    #
    #  @return int - Line count.
    def lineCount(self):

        lineList = self.readLines()
        if not lineList:
            return 0

        return len([x for x in lineList if x])

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # STATIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Check whether the given file exists.
    #
    #  @param path [ str | None | in  ] - Absolute path of the file.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    @staticmethod
    def fileExists(path):

        return os.path.isfile(path)

    #
    ## @brief Get given byte size in human readable string.
    #
    #  @param size      [ int | None | in  ] - Size in bytes.
    #  @param precision [ int | 2    | in  ] - Precision.
    #
    #  @exception N/A
    #
    #  @return str - Size.
    @staticmethod
    def getFileSizeAsStr(size, precision=2):

        suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
        index = 0
        while size > 1024:
            index += 1
            size = size / 1024.0
        return '%.*f %s' % (precision, size, suffixes[index])

    #
    ## @brief Replace given files extension with given extension.
    #
    #  Absolute or relative path of a file can be provided for absFile argument.
    #
    #  Method doesn't check whether the given absFile exists.
    #
    #  New extension will be added to absFile regardless it already has an extension.
    #
    #  @param path         [ str | None | in  ] - File.
    #  @param newExtension [ str | None | in  ] - New extension.
    #
    #  @exception N/A
    #
    #  @return str - File with new extension.
    @staticmethod
    def replaceExtension(path, newExtension):

        if not newExtension.startswith('.'):
            newExtension = '.{}'.format(newExtension)

        return '{}{}'.format(os.path.splitext(path)[0], newExtension)

    #
    # ------------------------------------------------------------------------------------------------
    # CLASS METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Create a file and return a mFileSystem.fileLib.File instance for it.
    #
    #  Directory, where the file will be created in, will be created if it doesn't exists.
    #
    #  @param cls       [ object | None  | in  ] - Class object.
    #  @param path      [ str    | None  | in  ] - File name with absolute path.
    #  @param overwrite [ bool   | False | in  ] - Whether existing file will be overwritten.
    #  @param binary    [ bool   | False | in  ] - Whether the file will be written in binary format.
    #
    #  @exception IOError - If absFile exists and overwrite argument is provided False.
    #
    #  @return mFileSystem.fileLib.File - Instance of mFileSystem.fileLib.File class for created file.
    @classmethod
    def create(cls, path, overwrite=False, binary=False):

        if os.path.isfile(path) and not overwrite:
            raise IOError('File already exists, could not be created: {}'.format(path))

        directory = os.path.dirname(path)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        open(path, 'wb' if binary else 'w').close()

        return cls(path=path)
