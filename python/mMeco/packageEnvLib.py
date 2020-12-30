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
## @file    mMeco/packageEnvLib.py @brief [ FILE   ] - Package environment module.
## @package mMeco.packageEnvLib    @brief [ MODULE ] - Package environment module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
from os.path import join


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief Set environment.
#
#  @param allLib            [ mMeco.libs.allLib.All                 | None | in  ] - All libraries.
#  @param envEntryContainer [ mMeco.libs.entryLib.EnvEntryContainer | None | in  ] - Env entry lib container.
#
#  @exception N/A
#
#  @return True  - If this package should be initialized.
#  @return False - If this package shouldn't be initialized.
def setEnvironment(allLib, envEntryContainer):

    if allLib.request().platform() in ['Darwin', 'Linux']:

        envEntryContainer.addScript(join(envEntryContainer.getPackageRootPath(),
                                         'bin',
                                         allLib.request().platform().lower(),
                                         'mmeco-cd-dev')
                                    )

        envEntryContainer.addScript(join(envEntryContainer.getPackageRootPath(),
                                         'bin',
                                         allLib.request().platform().lower(),
                                         'mmeco-cd-reserved')
                                    )

        envEntryContainer.addScript(join(envEntryContainer.getPackageRootPath(),
                                         'bin',
                                         allLib.request().platform().lower(),
                                         'mmeco-cd-stage')
                                    )

    return True
