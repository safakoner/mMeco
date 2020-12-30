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
## @file    mMeco/libs/envPathLib.py @brief [ FILE   ] - Env paths.
## @package mMeco.libs.envPathLib    @brief [ MODULE ] - Env paths.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  glob
import  os

import  mMeco.fileSystem.directoryLib
import  mMeco.fileSystem.versionLib

import  mMeco.libs.allLib
import  mMeco.libs.enumLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Class to operate on env paths.
class EnvPath(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param path    [ str  | None | in  ] - Absolute package path of an environment.
    #  @param envType [ enum | None | in  ] - Value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, path, envType):

        ## [ str ] - Path.
        self._path              = None

        ## [ enum ] - Value from mMeco.libs.enumLib.EnvType enum class.
        self._envType           = None

        ## [ enum ] - Value from mMeco.libs.enumLib.EnvPackageType enum class.
        self._envPackageType    = None

        ## [ list of str | list of dict ] - Packages.
        self._packages          = []

        ## [ mMeco.libs.allLib.All ] - All.
        self._allLib            = mMeco.libs.allLib.All.getInstance(**{envType:self})

        #

        self._set(path, envType)

    #
    ## @brief Get env package type for given env type.
    #
    #  Supported `envType`:
    #
    #  - mMeco.libs.enumLib.EnvType.kReserved
    #  - mMeco.libs.enumLib.EnvType.kDevelopment
    #  - mMeco.libs.enumLib.EnvType.kStage
    #  - mMeco.libs.enumLib.EnvType.kProjectInternal
    #  - mMeco.libs.enumLib.EnvType.kProjectExternal
    #  - mMeco.libs.enumLib.EnvType.kMasterProjectInternal
    #  - mMeco.libs.enumLib.EnvType.kMasterProjectExternal
    #
    #  @param envType [ enum | None | in  ] - Value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception ValueError - If provided `envType` is not supported.
    #
    #  @return enum - A value from mMeco.libs.enumLib.EnvPackageType enum class.
    def __getEnvPackageTypeByEnvType(self, envType):

        if envType in [mMeco.libs.enumLib.EnvType.kReserved,
                       mMeco.libs.enumLib.EnvType.kDevelopment,
                       mMeco.libs.enumLib.EnvType.kStage
                      ]:

            return mMeco.libs.enumLib.EnvPackageType.kNonVersioned

        elif envType in [mMeco.libs.enumLib.EnvType.kProjectInternal,
                         mMeco.libs.enumLib.EnvType.kProjectExternal,
                         mMeco.libs.enumLib.EnvType.kMasterProjectInternal,
                         mMeco.libs.enumLib.EnvType.kMasterProjectExternal
                        ]:

            return mMeco.libs.enumLib.EnvPackageType.kVersioned

        raise ValueError('The following env type is not supported: {}'.format(envType))

    #
    # ------------------------------------------------------------------------------------------------
    # PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Set.
    #
    #  @param path    [ str  | None | in  ] - Absolute package path of an environment.
    #  @param envType [ enum | None | in  ] - Value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception IOError - If provided `path` doesn't exist.
    #
    #  @return None - None.
    def _set(self, path, envType):

        if not os.path.isdir(path):
            raise IOError('Env path doesn\'t exist: {}'.format(path))

        self._path           = path
        self._envType        = envType
        self._envPackageType = self.__getEnvPackageTypeByEnvType(envType)

    #
    ## @brief List non-versioned packages located in the env path.
    #
    #  @param absolutePath                          [ bool | False | in  ] - Whether to return absolute path of the packages.
    #  @param invokeShouldInitializePackageCallback [ bool | False | in  ] - Whether to invoke `shouldInitializePackage` callback.
    #
    #  @exception ValueError - If the env package type is not mMeco.libs.enumLib.EnvPackageType.kNonVersioned.
    #
    #  @return list of str - Packages.
    def _listNonVersionedPackages(self, absolutePath=False, invokeShouldInitializePackageCallback=False):

        if self._envPackageType != mMeco.libs.enumLib.EnvPackageType.kNonVersioned:
            raise ValueError('"{}" env path doesn\'t contain non-versioned packages.'.format(self._envType))

        packageList = []

        for packageRoot in glob.glob('{}/*'.format(self._path)):

            if not os.path.isdir(packageRoot):
                self._allLib.logger().addWarning('Entry is not a package, skipping: {} '.format(packageRoot))
                continue

            packageInfoModuleFilePath = os.path.join(packageRoot, 'python', os.path.basename(packageRoot), 'packageInfoLib.py')
            if not os.path.isfile(packageInfoModuleFilePath):
                self._allLib.logger().addWarning('Package info module is missing, path is ignored since it is not a package: {} '.format(packageInfoModuleFilePath))
                continue

            if invokeShouldInitializePackageCallback and \
               not self._allLib.callbackOperator().invokeShouldInitializePackage(packageRoot):
                    continue

            if absolutePath:
                packageList.append(packageRoot)
            else:
                packageList.append(os.path.basename(packageRoot))

        return packageList

    #
    ## @brief List versioned packages located in the env path.
    #
    #  @param absolutePath                          [ bool | False | in  ] - Whether to return absolute path of the packages.
    #  @param invokeShouldInitializePackageCallback [ bool | True  | in  ] - Whether to invoke `shouldInitializePackage` callback.
    #
    #  @exception ValueError - If the env package type is not mMeco.libs.enumLib.EnvPackageType.kVersioned.
    #
    #  @return list of dict - Packages. Dict keys are `package` and `versions`.
    def _listVersionedPackages(self, absolutePath=False, invokeShouldInitializePackageCallback=True):

        if self._envPackageType != mMeco.libs.enumLib.EnvPackageType.kVersioned:
            raise ValueError('"{}" env path doesn\'t contain versioned packages.'.format(self._envType))

        packageList = []

        for packageRootPath in glob.glob('{}/*'.format(self._path)):

            packageName = os.path.basename(packageRootPath)

            packageData = {'package':packageName, 'versions':[]}

            if absolutePath:
                packageData['package'] = packageRootPath

            for version in glob.glob('{}/*'.format(packageRootPath)):

                packageInfoModuleFilePath = os.path.join(version,
                                                         packageName,
                                                         'python',
                                                         os.path.basename(packageRootPath),
                                                         'packageInfoLib.py')

                if not os.path.isfile(packageInfoModuleFilePath):
                    self._allLib.logger().addWarning('Package info module of "{}" version of the package is missing, '
                                                  'this version is ignored: {} '.format(os.path.basename(version),
                                                                                        packageInfoModuleFilePath
                                                                                        )
                                                     )
                    continue


                if invokeShouldInitializePackageCallback and \
                   not self._allLib.callbackOperator().invokeShouldInitializePackage(os.path.join(version, packageName)):
                    continue

                packageData['versions'].append(os.path.basename(version))

            packageData['versions'].sort(key=lambda x: [int(x) for x in x.split('.')])

            packageList.append(packageData)

        # Remove the package if there is no version of it
        packageList = [x for x in packageList if x['versions']]

        return packageList

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
    def path(self):

        return self._path

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return enum - A value from mMeco.libs.enumLib.EnvType enum class.
    def envType(self):

        return self._envType

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return enum - A value from mMeco.libs.enumLib.EnvPackageType enum class.
    def envPackageType(self):

        return self._envPackageType

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of str | list of dict - Value.
    def packages(self):

        return self._packages

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Check whether given path is a package.
    #
    #  Method checks whether package info module file exists relative to `packageRootPath`.
    #
    #  @param packageRootPath [ str | None | in  ] - Root of a package.
    #
    #  @exception N/A
    #
    #  @return str  - Absolute path of package info module file.
    #  @return None - If given `packageRootPath` is not a package.
    def isAPackage(self, packageRootPath):

        packageInfoFilePath = os.path.join(packageRootPath,
                                           'python',
                                           os.path.basename(packageRootPath),
                                           'packageInfoLib.py')

        if os.path.isfile(packageInfoFilePath):
            return packageInfoFilePath

        return None
    
    #
    ## @brief Check whether the env path has a package with given `packageName`.
    #
    #  If env path wanted to be checked for a versioned package `checkPackageInfoModule` should be provided `False`
    #  as otherwise this method will check package info module file for non-versioned package.
    #
    #  @param packageName            [ str  | None | in  ] - Name of a package to be checked.
    #  @param checkPackageInfoModule [ bool | None | in  ] - Whether package info module file should be checked.
    #
    #  @exception N/A
    #  
    #  @return str  - Absolute path of the package.
    #  @return None - If no package with `packageName` exists in the env.
    def hasPackage(self, packageName, checkPackageInfoModule=False):

        packageRootPath = os.path.join(self._path, packageName)
        if not os.path.isdir(packageRootPath):
            return None

        if checkPackageInfoModule:
            if not self.isAPackage(packageRootPath):
                return None

        return packageRootPath

    #
    ## @brief Check whether a package has a version.
    #
    #  @param packageName [ str | None | in  ] - Name of a package.
    #  @param version     [ str | None | in  ] - Version to be checked.
    #
    #  @exception ValueError - If the env package type is not mMeco.libs.enumLib.EnvPackageType.kVersioned.
    #
    #  @return str  - Absolute root path of the version of the package.
    #  @return None - If `version` doesn't exist for `packageName`.
    def doesPackageHaveAVersion(self, packageName, version):

        if self._envPackageType != mMeco.libs.enumLib.EnvPackageType.kVersioned:
            raise ValueError('"{}" env path doesn\'t contain versioned packages.'.format(self._envType))

        packageRootPath = os.path.join(self._path, packageName, version, packageName)
        if not os.path.isdir(packageRootPath):
            return None

        if not self.isAPackage(packageRootPath):
            return None

        return packageRootPath

    #
    ## @brief List packages in the env path.
    #
    #  @param invokeShouldInitializePackageCallback [ bool | False | in  ] - Whether to invoke `shouldInitializePackage` callback.
    #
    #  @exception N/A
    #
    #  @return list of str  - If env package type is mMeco.libs.enumLib.EnvPackageType.kNonVersioned.
    #  @return list of dict - If env package type is mMeco.libs.enumLib.EnvPackageType.kVersioned.
    def listPackages(self, invokeShouldInitializePackageCallback=False):

        if self._envPackageType == mMeco.libs.enumLib.EnvPackageType.kNonVersioned:
            self._packages = self._listNonVersionedPackages(False, invokeShouldInitializePackageCallback)
        else:
            self._packages = self._listVersionedPackages(False, invokeShouldInitializePackageCallback)

        return self._packages

    #
    ## @brief List versions of the given package.
    #
    #  @param packageName [ str | None | in  ] - Name of a package.
    #
    #  @exception ValueError - If the env package type is not mMeco.libs.enumLib.EnvPackageType.kVersioned.
    #
    #  @return list of str - Versions.
    #  @return None        - If the env path doesn't have package with given `packageName`.
    def listVersionsOfAPackage(self, packageName):

        if self._envPackageType != mMeco.libs.enumLib.EnvPackageType.kVersioned:
            raise ValueError('"{}" env path doesn\'t contain versioned packages.'.format(self._envType))

        packageRootPath = self.hasPackage(packageName, False)
        if not packageRootPath:
            return None

        versionList = mMeco.fileSystem.directoryLib.Directory.listVersionedFolders(directory=packageRootPath,
                                                                                   absolutePath=False,
                                                                                   version=mMeco.fileSystem.versionLib.Version.kAll
                                                                                   )

        versionList = [x for x in versionList if self.isAPackage(os.path.join(packageRootPath, x, packageName))]

        return versionList
