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
## @file    mMeco/libs/allLib.py @brief [ FILE   ] - All libraries.
## @package mMeco.libs.allLib    @brief [ MODULE ] - All libraries.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import mMeco.core.loggerLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Class contains all required class instances that used throughout the API.
class All(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC STATIC MEMBERS
    # ------------------------------------------------------------------------------------------------
    ## [ mMeco.lib.allLib.All ] - Singleton class instance.
    __INSTANCE = None

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

        if not All.__INSTANCE:
            All.__INSTANCE = self

        #

        ## [ mMeco.core.loggerLib.Logger ] - Logger.
        self._logger                = mMeco.core.loggerLib.Logger()

        #

        if not hasattr(self, '_request'):
            ## [ mmMeco.libs.requestLib.Request ] - Request.
            self._request           = None

        if not hasattr(self, '_settingsOperator'):
            ## [ mMeco.operators.settingsOpt.SettingsOperator ] - Operator.
            self._settingsOperator  = None

        if not hasattr(self, '_callbackOperator'):
            ## [ mMeco.operators.callbackOpt.CallbackOperator ] - Operator.
            self._callbackOperator  = None

        if not hasattr(self, '_appFileOperator'):
            ## [ mMeco.operators.appFileOpt.AppFileOperator ] - Operator.
            self._appFileOperator  = None

        if not hasattr(self, '_packageGlobalEnvOperator'):
            ## [ mMeco.operators.packageGlobalEnvOpt.PackageGlobalEnvOperator ] - Operator.
            self._packageGlobalEnvOperator  = None

        #

        if not hasattr(self, '_solverContainer'):
            ## [ mMeco.abstract.solverAbs.SolverContainer ] - Solver container.
            self._solverContainer   = None

        if not hasattr(self, '_solver'):
            ## [ mMeco.abstract.solverAbs.Solver ] - Solver.
            self._solver            = None

        #

        if not hasattr(self, '_builderContainer'):
            ## [ mMeco.abstract.builderAbs.BuilderContainer ] - Builder container.
            self._builderContainer  = None

        if not hasattr(self, '_builder'):
            ## [ mMeco.abstract.builderAbs.Builder ] - Builder.
            self._builder           = None

        #

        if not hasattr(self, '_responseContainer'):
            ## [ mMeco.abstract.responseAbs.ResponseContainer ] - Response container.
            self._responseContainer = None

        if not hasattr(self, '_response'):
            ## [ mMeco.abstract.responseAbs.Response ] - Response.
            self._response          = None

    #
    ## @brief String representation.
    #
    #  @exception N/A
    #
    #  @return str - String representation.
    def __str__(self):

        data = 'Logger                : {}\n'.format(type(self._logger))

        data = '{}Request               : {}\n'.format(data, type(self._request))
        data = '{}Settings              : {}\n'.format(data, type(self._settingsOperator))
        data = '{}Callback              : {}\n'.format(data, type(self._callbackOperator))

        data = '{}Solver Container      : {}\n'.format(data, type(self._solverContainer))
        data = '{}Solver                : {}\n'.format(data, type(self._solver))

        data = '{}Builder Container     : {}\n'.format(data, type(self._builderContainer))
        data = '{}Builder               : {}\n'.format(data, type(self._builder))

        data = '{}Response Container    : {}\n'.format(data, type(self._responseContainer))
        data = '{}Response              : {}\n'.format(data, type(self._response))

        return data

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.core.loggerLib.Logger - Logger.
    def logger(self):

        return self._logger

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.libs.requestLib.Request - Request.
    def request(self):

        return self._request

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.operators.settingsOpt.SettingsOperator - Operator.
    def settingsOperator(self):

        return self._settingsOperator

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.operators.callbackOpt.CallbackOperator - Operator.
    def callbackOperator(self):

        return self._callbackOperator

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.operators.appFileOpt.AppFileOperator - Operator.
    def appFileOperator(self):

        return self._appFileOperator

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.operators.packageGlobalEnvOpt.PackageGlobalEnvOperator - Operator.
    def packageGlobalEnvOperator(self):

        return self._packageGlobalEnvOperator

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.abstract.solverAbs.SolverContainer - Solver container.
    def solverContainer(self):

        return self._solverContainer

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.abstract.solverAbs.Solver - Solver.
    def solver(self):

        return self._solver

    #
    ## @brief Property.
    #
    #  @param solver [ mMeco.abstract.solverAbs.Solver | None | in  ] - Solver.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def setSolver(self, solver):

        self._solver = solver

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.abstract.builderAbs.BuilderContainer - Builder container.
    def builderContainer(self):

        return self._builderContainer

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.abstract.builderAbs.Builder - Builder.
    def builder(self):

        return self._builder

    #
    ## @brief Property.
    #
    #  @param builder [ mMeco.abstract.builderAbs.Builder | None | in  ] - Builder.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def setBuilder(self, builder):

        self._builder = builder

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.abstract.responseAbs.ResponseContainer - Response container.
    def responseContainer(self):

        return self._responseContainer

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return mMeco.abstract.responseAbs.Response - Response.
    def response(self):

        return self._response

    #
    ## @brief Property.
    #
    #  @param response [ mMeco.abstract.responseAbs.Response | None | in  ] - Response.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def setResponse(self, response):

        self._response = response

    #
    # ------------------------------------------------------------------------------------------------
    # STATIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Get instance.
    #
    #  @param request [ mMeco.libs.requestLib.Request | None | in  ] - Request.
    #  @param kwargs  [ dict                          | None | in  ] - Kwargs.
    #
    #  @exception N/A
    #
    #  @return mMeco.libs.allLib.All - Singleton class instance.
    @staticmethod
    def getInstance(request=None, **kwargs):

        instance = None
        if All.__INSTANCE:
            instance = All.__INSTANCE
        else:
            instance = All()

        for key, value in locals().items():

            if key in ['self', 'kwargs', 'instance']:
                continue

            if not value:
                continue

            setattr(instance, '_{}'.format(key), value)

        if kwargs:
            for key, value in kwargs.items():

                if not value:
                    continue

                setattr(instance, '_{}'.format(key), value)

        return instance