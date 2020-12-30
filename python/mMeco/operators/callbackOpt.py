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
## @file    mMeco/operators/callbackOpt.py @brief [ FILE   ] - Operator.
## @package mMeco.operators.callbackOpt    @brief [ MODULE ] - Operator.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  mMeco.abstract.operatorAbs


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Class to operate on Python modules.
class CallbackOperator(mMeco.abstract.operatorAbs.Operator):
    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC STATIC MEMBERS
    # ------------------------------------------------------------------------------------------------
    ## [ str ] - Default Python module import name.
    MODULE  = 'mMecoSettings.callbackLib'

    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param module [ str | None | in  ] - Python module import path or Python module file path.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, module=None):

        ## [ str ] - Name.
        self._name = 'callbackOperator'

        mMeco.abstract.operatorAbs.Operator.__dict__['__init__'](self, module)

    #
    # ------------------------------------------------------------------------------------------------
    # PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Initialize the attributes of the Python module.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _initialize(self):

        self.set()

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Invoke given `functionName` pre/post env build function in the settings module.
    #
    #  @param functionName      [ str                                            | None | in  ] - Function name, which will be invoked.
    #  @param envEntryContainer [ mMeco.libs.entryLib.EnvEntry.EnvEntryContainer | None | in  ] - Env envEntry container to be passed to the function.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def invokePrePostBuild(self, functionName, envEntryContainer):

        getattr(self._module, functionName)(self._all, envEntryContainer)

    #
    ## @brief Invoke `shouldInitializePackage` function in the settings module.
    #
    #  @param packagePath [ str | None | in  ] - Absolute path of the root of a package.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def invokeShouldInitializePackage(self, packagePath):

        return getattr(self._module, 'shouldInitializePackage')(self._all, packagePath)

    #
    ## @brief Invoke `getAppExecutableFlags` function in the settings module.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def invokeGetAppExecutableFlags(self):

        return getattr(self._module, 'getAppExecutableFlags')(self._all)