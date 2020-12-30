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
## @file    mMeco/libs/enumLib.py @brief [ FILE   ] - Enums.
## @package mMeco.libs.enumLib    @brief [ MODULE ] - Enums.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
from    os.path import join

import  mMeco.core.enumAbs


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ ENUM CLASS ] - Project folder structure.
class ProjectFolderStructure(mMeco.core.enumAbs.Enum):

    ## [ str ] - Developers folder name.
    kDevelopers                     = 'developers'

    ## [ str ] - Documentation folder name.
    kDoc                            = 'doc'

    ## [ str ] - Developer documentation folder name.
    kDocDeveloper                   = join(kDoc, 'developer')

    ## [ str ] - Developer C++ API reference folder name.
    kDocDeveloperCPPAPIReference    = join(kDocDeveloper, 'cppAPIReference')

    ## [ str ] - Developer Python API reference folder name.
    kDocDeveloperPythonAPIReference = join(kDocDeveloper, 'pythonAPIReference')

    ## [ str ] - External packages folder name.
    kExternal                       = 'external'

    ## [ str ] - Internal packages folder name.
    kInternal                       = 'internal'

    ## [ str ] - Users folder name.
    kUsers                          = 'users'

#
## @brief [ ENUM CLASS ] - Env types.
class EnvType(mMeco.core.enumAbs.Enum):

    ## [ enum ] - Pre build.
    kPreBuild               = 'Pre Build'

    ## [ enum ] - Reserved.
    kReserved               = 'Reserved'

    ## [ enum ] - Development.
    kDevelopment            = 'Development'

    ## [ enum ] - Stage.
    kStage                  = 'Stage'

    ## [ enum ] - Project internal.
    kProjectInternal        = 'Project Internal'

    ## [ enum ] - Project external.
    kProjectExternal        = 'Project External'

    ## [ enum ] - Master project internal.
    kMasterProjectInternal  = 'Master Project Internal'

    ## [ enum ] - Master project external.
    kMasterProjectExternal  = 'Master Project External'

    ## [ enum ] - Env.
    kEnv                    = 'Env'

    ## [ enum ] - Info.
    kInfo                   = 'Info'

    ## [ enum ] - Product info.
    kProductInfo            = 'Product Info'

    ## [ enum ] - Post build.
    kPostBuild              = 'Post Build'

#
## @brief [ ENUM CLASS ] - Env package types.
class EnvPackageType(mMeco.core.enumAbs.Enum):

    ## [ enum ] - Pre build.
    kNonVersioned           = 'NonVersioned'

    ## [ enum ] - Development.
    kVersioned              = 'Versioned'

#
#
#
## @brief [ ENUM CLASS ] - Env envEntry container types.
class EnvEntryContainerType(mMeco.core.enumAbs.Enum):

    ## [ enum ] -  Package.
    kPackage        = 'Package'

    ## [ enum ] - Pre build.
    kPreBuild       = 'PreBuild'

    ## [ enum ] - Post build.
    kPostBuild      = 'PostBuild'

#
## @brief [ ENUM CLASS ] - Env envEntry types.
class EnvEntryType(mMeco.core.enumAbs.Enum):

    ## [ enum ] -  Single.
    kSingle         = 'Single'

    ## [ enum ] -  Multi.
    kMulti          = 'Multi'

    ## [ enum ] -  Script.
    kScript         = 'Script'

    ## [ enum ] -  Command.
    kCommand        = 'Command'

#
## @brief [ ENUM CLASS ] - Color names.
class ColorName(mMeco.core.enumAbs.Enum):

    ## [ enum ] - Color.
    kPackageVariable                = 'packageVariable'

    ## [ enum ] - Color.
    kPackageValue                   = 'packageValue'

    #

    ## [ enum ] - Color.
    kMultiVariable                  = 'multiVariable'

    ## [ enum ] - Color.
    kMultiValue                     = 'multiValue'

    #

    ## [ enum ] - Color.
    kSingleVariable                 = 'singleVariable'

    ## [ enum ] - Color.
    kSingleValue                    = 'singleValue'

    #

    ## [ enum ] - Color.
    kScript                         = 'script'

    ## [ enum ] - Color.
    kCommand                        = 'command'

    #

    ## [ enum ] - Color.
    kColon                          = 'colon'

    ## [ enum ] - Color.
    kArrow                          = 'arrow'

