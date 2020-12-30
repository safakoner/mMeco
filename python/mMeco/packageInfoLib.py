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
## @package mMeco                               @brief [ PACKAGE   ] - Meco.
## @dir     mMeco                               @brief [ DIRECTORY ] - Package root.
## @dir     mMeco/python                        @brief [ DIRECTORY ] - Python path.
## @dir     mMeco/python/mMeco                  @brief [ DIRECTORY ] - Python package.
## @package mMeco.abstract                      @brief [ PACKAGE   ] - Python package.
## @dir     mMeco/python/mMeco/abstract         @brief [ DIRECTORY ] - Python package path.
## @package mMeco.builders                      @brief [ PACKAGE   ] - Python package.
## @dir     mMeco/python/mMeco/builders         @brief [ DIRECTORY ] - Python package path.
## @package mMeco.core                          @brief [ PACKAGE   ] - Python package.
## @dir     mMeco/python/mMeco/core             @brief [ DIRECTORY ] - Python package path.
## @package mMeco.fileSystem                    @brief [ PACKAGE   ] - Python package.
## @dir     mMeco/python/mMeco/fileSystem       @brief [ DIRECTORY ] - Python package path.
## @package mMeco.libs                          @brief [ PACKAGE   ] - Python package.
## @dir     mMeco/python/mMeco/libs             @brief [ DIRECTORY ] - Python package path.
## @package mMeco.operators                     @brief [ PACKAGE   ] - Python package.
## @dir     mMeco/python/mMeco/operators        @brief [ DIRECTORY ] - Python package path.
## @package mMeco.responses                     @brief [ PACKAGE   ] - Python package.
## @dir     mMeco/python/mMeco/responses        @brief [ DIRECTORY ] - Python package path.
## @package mMeco.solvers                       @brief [ PACKAGE   ] - Python package.
## @dir     mMeco/python/mMeco/solvers          @brief [ DIRECTORY ] - Python package path.
## @file    mMeco/packageInfoLib.py             @brief [ FILE      ] - Package info module.
## @package mMeco.packageInfoLib                @brief [ MODULE    ] - Package info module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
## [ str ] - Name of the package.
NAME                = 'mMeco'

## [ str ] - Version of the package.
VERSION             = '1.0.0'

## [ str ] - Description about the package.
DESCRIPTION         = 'Meco'

## [ list of str ] - Keywords to find this package.
KEYWORDS            = ['environment', 'development', 'stage', 'release', 'production', 'package']

## [ list of str ] - Platforms which this package meant to be used on.
PLATFORMS           = ['Linux', 'Darwin', 'Windows']

## [ list of dict ] - Documentations about the package, keys of dict instances are: title, url.
DOCUMENTS           = [{'title':'Developer Reference  - Online', 'url':'https://meco.safakoner.com/'},
                       {'title':'Python API Reference - Online', 'url':'https://meco.api.safakoner.com/'}
                       ]

## [ list of str ] - Applications which this package meant to be initialized for.
APPLICATIONS        = ['all']

## [ list of str ] - Python versions supported by this package.
PYTHON_VERSIONS     = ['2', '3']

## [ bool ] - Whether this package is active (in use).
IS_ACTIVE           = True

## [ bool ] - Whether this package is external (third party).
IS_EXTERNAL         = False

## [ list of str ] - E-mail addresses of the developers.
DEVELOPERS          = ['safak@safakoner.com']

## [ list of str ] - Dependent packages.
DEPENDENT_PACKAGES  = ['mMecoSettings']

## [ list of str ] - Python packages contained by this package.
PYTHON_PACKAGES     = ['mMeco']