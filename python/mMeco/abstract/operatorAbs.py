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
## @file    mMeco/abstract/operatorAbs.py @brief [ FILE   ] - Abstract operator to operate on Python modules.
## @package mMeco.abstract.operatorAbs    @brief [ MODULE ] - Abstract operator to operate on Python modules.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  os
import  sys
from    importlib import import_module

import  mMeco.libs.allLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ ABSTRACT CLASS ] - Class to operate on Python modules.
class Operator(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC STATIC MEMBERS
    # ------------------------------------------------------------------------------------------------
    ## [ str ] - Default Python module import name.
    MODULE  = None

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

        if not hasattr(self, '_name'):

            ## [ str ] - Name.
            self._name = None

            raise AttributeError('Child class must have mMeco.abstract.operatorAbs.Operator._name member implemented.')

        ## [ module ] - Python module.
        self._module    = None

        ## [ mMeco.libs.allLib.All ] - All.
        self._all       = mMeco.libs.allLib.All.getInstance(**{self._name:self})

        if module:
            self.set(module)

    #
    # ------------------------------------------------------------------------------------------------
    # PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Callback which will be invoked before mMeco.abstract.operatorAbs.Operator._initialize method is invoked.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _preInitialize(self):

        pass

    #
    ## @brief Callback which will be invoked after mMeco.abstract.operatorAbs.Operator._initialize method is invoked.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _postInitialize(self):

        pass

    #
    ## @brief Initialize the attributes of the Python module.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _initialize(self):

        pass

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
    def name(self):

        return self._name

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def allLib(self):

        return self._all

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return module - Value.
    def module(self):

        return self._module

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Set Python module.
    #
    #  @param module [ str | None | in  ] - Python module import path or Python module file path.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def set(self, module=None):

        if not module:
            module = self.MODULE

        self._module = Operator.importModule(module)

    #
    ## @brief Initialize the attributes of the Python module.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def initialize(self):

        self._preInitialize()

        self._initialize()

        self._postInitialize()

    #
    # ------------------------------------------------------------------------------------------------
    # STATIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Import Python module.
    #
    #  @param module [ str | None | in  ] - Python module import path or Python module file path.
    #
    #  @exception IOError - If `module` provided as file and it doesn't exist.
    #
    #  @return module - Python module.
    @staticmethod
    def importModule(module):

        if module.endswith('.py') or module.endswith('.pyc'):

            if not os.path.isfile(module):
                raise IOError('Python module doesn\'t exist: {}'.format(module))

            modulePath = os.path.dirname(module)
            moduleName = os.path.basename(module).split('.')[0]

            pathAdded = False
            if not modulePath in sys.path:
                sys.path.append(modulePath)
                pathAdded = True

            module = import_module(moduleName)

            if pathAdded:
                sys.path.pop()

        else:
            module = import_module(module)

        return module