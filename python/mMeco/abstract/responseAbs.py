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
## @file    mMeco/abstract/responseAbs.py @brief [ FILE   ] - Abstract response.
## @package mMeco.abstract.responseAbs    @brief [ MODULE ] - Abstract response.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  os

import  mMeco.core.enumAbs
import  mMeco.core.moduleLib

import  mMeco.libs.allLib
import  mMeco.libs.enumLib
import  mMeco.libs.envPathLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Response container.
class ResponseContainer(object):
    #
    ## @brief Constructor.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self):

        ## [ mMeco.libs.allLib.All ] - All.
        self._allLib    = mMeco.libs.allLib.All.getInstance(**{'responseContainer':self})

        ## [ list of mMeco.abstract.responseAbs.Response ] - Responses.
        self._responses = []

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of mMeco.abstract.responseAbs.Response - Responses.
    def responses(self):

        return self._responses

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Get responses.
    #
    #  @exception AttributeError - If response modules do not have `Response` class.
    #
    #  @return list of mMeco.abstract.responseAbs.Response - Response class instances.
    def list(self):

        responseModulePath = os.path.abspath(os.path.join(__file__, '..', '..', 'responses'))

        for responseModule in mMeco.core.moduleLib.Module.listModules(responseModulePath, 'mMeco.responses.{}'):

            if not hasattr(responseModule, 'Response'):
                raise AttributeError('Response module doesn\'t have a class named "Response": {}'.format(responseModule.__file__))

            responseInstance = getattr(responseModule, 'Response')()
            self._responses.append(responseInstance)

        return self._responses

    #
    ## @brief Get response by given type.
    #
    #  @param name [ str | None | in  ] - Name of the response.
    #
    #  @exception ValueError - If response no response found.
    #  @exception ValueError - If response no response found with given type.
    #
    #  @return mMeco.abstract.responseAbs.Response - Response class instances.
    def getByName(self, name):

        if not self._responses:
            raise ValueError('No response found.')

        for response in self._responses:
            if name == response.NAME:
                return response

        raise ValueError('No response found by given name: {}'.format(name))

#
## @brief [ ABSTRACT CLASS ] - Abstract response class.
class Response(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC STATIC MEMBERS
    # ------------------------------------------------------------------------------------------------
    ## [ str ] - Name.
    NAME = ''

    #
    # ------------------------------------------------------------------------------------------------
    # PRIVATE METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self):

        ## [ mMeco.libs.allLib.All ] - All.
        self._allLib = mMeco.libs.allLib.All.getInstance(**{self.NAME:self})

        #

        ## [ list of str ] - Script file start.
        self._scriptFileStartEnv            = []

        ## [ list of str ] - Display member.
        self._preBuiltDisplay               = []
        ## [ list of str ] - Env member.
        self._preBuiltEnv                   = []

        ## [ list of str ] - Display member.
        self._reservedDisplay               = []
        ## [ list of str ] - Env member.
        self._reservedEnv                   = []

        ## [ list of str ] - Display member.
        self._developmentDisplay            = []
        ## [ list of str ] - Env member.
        self._developmentEnv                = []

        ## [ list of str ] - Display member.
        self._stageDisplay                  = []
        ## [ list of str ] - Env member.
        self._stageEnv                      = []

        ## [ list of str ] - Display member.
        self._projectInternalDisplay        = []
        ## [ list of str ] - Env member.
        self._projectInternalEnv            = []

        ## [ list of str ] - Display member.
        self._projectExternalDisplay        = []
        ## [ list of str ] - Env member.
        self._projectExternalEnv            = []

        ## [ list of str ] - Display member.
        self._masterProjectInternalDisplay  = []
        ## [ list of str ] - Env member.
        self._masterProjectInternalEnv      = []

        ## [ list of str ] - Display member.
        self._masterProjectExternalDisplay  = []
        ## [ list of str ] - Env member.
        self._masterProjectExternalEnv      = []

        ## [ list of str ] - Display member.
        self._postBuiltDisplay              = []
        ## [ list of str ] - Env member.
        self._postBuiltEnv                  = []

        ## [ list of str ] - Display member.
        self._envDisplay                    = []
        ## [ list of str ] - Env member.
        self._envEnv                        = []

        ## [ list of str ] - Display member.
        self._infoDisplay                   = []

        ## [ list of str ] - Display member.
        self._productInfoDisplay            = []

        ## [ list of str ] - Script file end.
        self._scriptFileEndEnv              = []
        
    #
    # ------------------------------------------------------------------------------------------------
    # PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Get env member of the class by given env type.
    #
    #  @param envType [ enum | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return list - Env member of this class that represents given `envType`.
    def _getEnvByEnvType(self, envType):

        if envType == mMeco.libs.enumLib.EnvType.kReserved:
            return self._reservedEnv

        elif envType == mMeco.libs.enumLib.EnvType.kDevelopment:
            return self._developmentEnv

        elif envType == mMeco.libs.enumLib.EnvType.kStage:
            return self._stageEnv

        elif envType == mMeco.libs.enumLib.EnvType.kProjectInternal:
            return self._projectInternalEnv

        elif envType == mMeco.libs.enumLib.EnvType.kProjectExternal:
            return self._projectExternalEnv

        elif envType == mMeco.libs.enumLib.EnvType.kMasterProjectInternal:
            return self._masterProjectInternalEnv

        elif envType == mMeco.libs.enumLib.EnvType.kMasterProjectExternal:
            return self._masterProjectExternalEnv

        elif envType == mMeco.libs.enumLib.EnvType.kPreBuild:
            return self._preBuiltEnv

        elif envType == mMeco.libs.enumLib.EnvType.kPostBuild:
            return self._postBuiltEnv

        elif envType == mMeco.libs.enumLib.EnvType.kEnv:
            return self._envEnv

    #
    ## @brief Get display member of the class by given env type.
    #
    #  @param envType [ enum | None | in  ] - A value from mMeco.libs.enumLib.EnvType enum class.
    #
    #  @exception N/A
    #
    #  @return list - Display member of this class that represents given `envType`.
    def _getDisplayByEnvType(self, envType):

        if envType == mMeco.libs.enumLib.EnvType.kReserved:
            return self._reservedDisplay

        elif envType == mMeco.libs.enumLib.EnvType.kDevelopment:
            return self._developmentDisplay

        elif envType == mMeco.libs.enumLib.EnvType.kStage:
            return self._stageDisplay

        elif envType == mMeco.libs.enumLib.EnvType.kProjectInternal:
            return self._projectInternalDisplay

        elif envType == mMeco.libs.enumLib.EnvType.kProjectExternal:
            return self._projectExternalDisplay

        elif envType == mMeco.libs.enumLib.EnvType.kMasterProjectInternal:
            return self._masterProjectInternalDisplay

        elif envType == mMeco.libs.enumLib.EnvType.kMasterProjectExternal:
            return self._masterProjectExternalDisplay

        elif envType == mMeco.libs.enumLib.EnvType.kPreBuild:
            return self._preBuiltDisplay

        elif envType == mMeco.libs.enumLib.EnvType.kPostBuild:
            return self._postBuiltDisplay

        elif envType == mMeco.libs.enumLib.EnvType.kEnv:
            return self._envDisplay

        elif envType == mMeco.libs.enumLib.EnvType.kInfo:
            return self._infoDisplay

        elif envType == mMeco.libs.enumLib.EnvType.kProductInfo:
            return self._productInfoDisplay

    #
    ## @brief Callback which will be invoked before mMeco.abstract.responsesAbs.Response._respond method is invoked.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _preRespond(self):

        pass

    #
    ## @brief Callback which will be invoked after mMeco.abstract.responsesAbs.Response.respond method is invoked.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _postRespond(self):

        pass

    #
    ## @brief Respond.
    #
    #  @exception NotImplementedError - If this method is not implemented in child class.
    #
    #  @return bool - Result.
    def _respond(self):

        raise NotImplementedError('You must overwrite mMeco.abstract.responsesAbs.Response.respond method in child class.')

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Respond.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def respond(self):

        self._preRespond()

        self._respond()

        self._postRespond()



