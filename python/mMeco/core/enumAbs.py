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
## @file    mMeco/core/enumAbs.py @brief [ FILE   ] - Enumeration.
## @package mMeco.core.enumAbs    @brief [ MODULE ] - Enumeration.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
from mMeco.core.pythonVersionLib import isPython3


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ ABSTRACT CLASS ] - Abstract class for enum classes.
#
# @code
#import sys
#
#class Type(Enum):
#
#    kPublished = 'published'
#    kWIP       = 'wip'
#    kProduct   = 'product'
#
#for a, v in zip(Type.listAttributes(False, False, False), Type.listAttributes(True, True, True, False)):
#
#    sys.stdout.write(a, '-', v)
#
# #kProduct - product
# #kPublished - published
# #kWIP - wip
#
#sys.stdout.write(Type.getAttributeNameFromValue('product', removeK=False))
# #kProduct
#
#sys.stdout.write(Type.getValueFromAttributeName('kProduct'))
# #product
#
#sys.stdout.write(Type.asDict())
# #{'Product': 'product', 'WIP': 'wip', 'Published': 'published'}
#
# @endcode
class Enum(object):
    #
    # ------------------------------------------------------------------------------------------------
    # CLASS METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief List static public attributes of the class.
    #
    #  @param cls                 [ object | None  | in  ] - Class object.
    #  @param stringOnly          [ bool   | True  | in  ] - List attributes only with string values.
    #  @param getValues           [ bool   | True  | in  ] - Get values of the attributes instead of their names.
    #  @param removeK             [ bool   | True  | in  ] - Remove k character from the attribute names if getValues is provided False.
    #  @param startAttrNamesLower [ bool   | False | in  ] - Start attribute names with lower case.
    #
    #  @exception N/A
    #
    #  @return list of str - Names or values of the attributes.
    @classmethod
    def listAttributes(cls, stringOnly=True, getValues=True, removeK=True, startAttrNamesLower=False):

        data = []

        for attr, value in cls.__dict__.items():

            if attr.startswith('__'):
                continue

            if getValues:

                if stringOnly:
                    if isinstance(value, str):
                        data.append(value)
                else:
                    data.append(value)

            else:

                if removeK and attr.startswith('k'):
                    attr = attr[1:]

                if startAttrNamesLower:
                    attr = '{}{}'.format(attr[:1].lower(), attr[1:])

                data.append(attr)

        data.sort(key=lambda x: (1, x, '') if isinstance(x, list) else (0, x, ''))

        return data

    #
    ## @brief List elements of a static public attribute.
    #
    #  @param cls       [ object | None | in ] - Class object.
    #  @param attribute [ str    | None | in ] - Name of the attribute.
    #
    #  @exception N/A
    #
    #  @return list - Elements.
    #  @return None - If given attribute doesn't exist.
    @classmethod
    def listAttributeElements(cls, attribute):

        if not attribute in cls.listAttributes(getValues=False, removeK=False):
            return None

        return getattr(cls, attribute)

    #
    ## @brief Get the name of the attribute for given value.
    #
    #  @param cls                  [ object | None  | in  ] - Class object.
    #  @param value                [ None   | None  | in  ] - Value.
    #  @param removeK              [ bool   | True  | in  ] - Remove k character from the name of the attribute.
    #  @param defaultAttributeName [ None   | None  | in  ] - Default value to return if given value doesn't exist.
    #  @param startLower           [ bool   | False | in  ] - Start attribute names with lower case.
    #
    #  @exception N/A
    #
    #  @return str     - Attribute name.
    #  @return variant - If given value doesn't exist based on provided value for `defaultAttributeName` argument.
    @classmethod
    def getAttributeNameFromValue(cls, value, removeK=True, defaultAttributeName=None, startLower=False):

        attributeDict = cls.asDict(removeK=removeK)

        if not attributeDict:
            return defaultAttributeName

        try:
            attributeName = attributeDict.keys()[attributeDict.values().index(value)]
            if startLower:
                attributeName = '{}{}'.format(attributeName[:1].lower(), attributeName[1:])
            return attributeName
        except:
            return defaultAttributeName

    #
    ## @brief Get value from attribute name.
    #
    #  @param cls          [ object | None  | in  ] - Class object.
    #  @param attribute    [ str    | None  | in  ] - Name of the attribute.
    #  @param removeK      [ bool   | False | in  ] - Remove k character from the name of the attribute.
    #  @param defaultValue [ None   | None  | in  ] - Default value to return if requested value doesn't exist.
    #
    #  @exception N/A
    #
    #  @return variant - Value.
    #  @return variant - If given attribute doesn't exist based on provided value for `defaultValue` argument.
    @classmethod
    def getValueFromAttributeName(cls, attribute, removeK=False, defaultValue=None):

        attributeDict = cls.asDict(removeK=removeK)

        if attribute in attributeDict:
            return attributeDict[attribute]

        return defaultValue

    #
    ## @brief Get all the attributes and their values in a dict instance.
    #
    #  @param cls     [ object | None | in  ] - Class object.
    #  @param removeK [ bool   | True | in  ] - Remove k characters from the name of the attributes.
    #
    #  @exception N/A
    #
    #  @return dict - Instance of dict object that contains attributes and their values.
    @classmethod
    def asDict(cls, removeK=True):

        data = {}

        items = None

        if isPython3():
            items = cls.__dict__.items()
        else:
            items = cls.__dict__.iteritems()

        for attr, value in items:

            if not attr.startswith('__'):

                if removeK:
                    data[attr[1:]] = value
                else:
                    data[attr] = value

        return data
