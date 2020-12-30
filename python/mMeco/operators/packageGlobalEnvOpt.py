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
## @file    mMeco/operators/packageGlobalEnvOpt.py @brief [ FILE   ] - Operator.
## @package mMeco.operators.packageGlobalEnvOpt    @brief [ MODULE ] - Operator.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
from   inspect import isclass

import mMeco.abstract.operatorAbs


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Package global env.
class PackageGlobalEnv(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param name [ str | None | in  ] - Name of the Package global env class.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, name):

        ## [ str ] - Package Env class name.
        self._name          = name

        ## [ list of dicts ] - Attributes.
        self._attributes    = []

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
    #  @return list of dict - Value.
    def attributes(self):

        return self._attributes

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Sort attributes.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def sort(self):

        self._attributes.sort(key=lambda x: x['name'])

    #
    ## @brief Add variable.
    #
    #  @param name  [ str         | None | in  ] - Name of the variable.
    #  @param value [ list of str | None | in  ] - Values.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def addAttribute(self, name, value):

        self._attributes.append({'name' :name,
                                 'value':value})

    #
    ## @brief Get string representation of the class.
    #
    #  @exception N/A
    #
    #  @return str - Information about the package in human readable form.
    def asStr(self):

        data = '\n\nName                    : {}'.format(self.name())

        for attr in self._attributes:
            data += '{}\nAttribute Name & Value  : {} - {}'.format(data, attr['name'].ljust(28), ', '.join(attr['value']))

        return data

#
## @brief [ CLASS ] - Class to operate on Python modules.
class PackageGlobalEnvOperator(mMeco.abstract.operatorAbs.Operator):
    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC STATIC MEMBERS
    # ------------------------------------------------------------------------------------------------
    ## [ str ] - Default Python module import name.
    MODULE  = 'mMecoSettings.packageGlobalEnvLib'

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
        self._name = 'packageGlobalEnvOperator'

        mMeco.abstract.operatorAbs.Operator.__dict__['__init__'](self, module)

        ## [ list of mMeco.operators.packageGlobalEnvOpt.PackageGlobalEnv ] - Package global env.
        self._packageGlobalEnvs = []

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of mMeco.operators.packageGlobalEnvOpt.PackageGlobalEnv - Value.
    def packageGlobalEnvs(self):

        return self._packageGlobalEnvs

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

        for className in self._module.__dict__:

            classInstance = getattr(self._module, className)

            if not isclass(classInstance):
                continue

            packageEnv = PackageGlobalEnv(name=className)

            for attr in dir(classInstance):

                if attr.startswith('__'):
                    continue

                values = getattr(classInstance, attr)
                if not values:
                    continue

                packageEnv.addAttribute(attr, values)

            packageEnv.sort()

            self._packageGlobalEnvs.append(packageEnv)


    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Get mMeco.operators.packageGlobalEnvOpt.PackageGlobalEnvOperator class instance for given `className`.
    #
    #  @param className [ str | None | in  ] - Name of the class.
    #
    #  @exception N/A
    #
    #  @return mMeco.operators.packageGlobalEnvOpt.PackageGlobalEnvOperator - Class instance.
    #  @return None                                                         - If no class found for given name.
    def getClass(self, className):

        if not self._packageGlobalEnvs:
            return None

        className = '{}{}'.format(className.title(), self._all.request().platform())

        for app in self._packageGlobalEnvs:

            if className == app.name():
                return app

        return None