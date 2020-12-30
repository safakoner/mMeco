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
## @file    mMeco/libs/requestLib.py @brief [ FILE   ] - Request.
## @package mMeco.libs.requestLib    @brief [ MODULE ] - Request.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  sys
import  argparse

from    getpass         import getuser
from    platform        import system

import  mMeco.libs.allLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Request.
class Request(object):
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

        ## [ argparse.ArgumentParser ] - Argument parser.
        self._argumentParser        = argparse.ArgumentParser(description='Meco CLI')

        ## [ argparse.Namespace ] - Parsed known arguments.
        self._args                  = None

        ## [ list of str ] - Parsed unknown arguments.
        self._unknownArgs           = None

        ## [ str ] - command.
        self._command               = None


        #

        ## [ str ] - Python version.
        self._pythonVersion         = '.'.join([str(x) for x in sys.version_info[:3]])

        ## [ str ] - Platform.
        self._platform              = system()


        # MECO

        ## [ bool ] - About.
        self._about                 = False

        ## [ bool ] - Version.
        self._version               = False

        # ENVS

        ## [ str ] - Project name.
        self._project               = None

        ## [ str ] - Developer name.
        self._developer             = getuser()

        ## [ str ] - Development env name.
        self._development           = None

        ## [ str ] - Stage env name.
        self._stage                 = None

        # APP

        ## [ str ] - App name.
        self._app                   = None

        ## [ str ] - App arguments.
        self._appArgs               = None

        ## [ bool ] - Ignore app executable.
        self._ignoreAppExec         = False

        # SET STATE

        ## [ bool ] - Display only.
        self._displayOnly           = False
        
        ## [ bool ] - Set only.
        self._setOnly               = False

        ## [ int ] - Verbose.
        self._verbose               = False

        ## [ int ] - Display info.
        self._displayInfo           = None

        ## [ bool ] - Ignore env script entries.
        self._ignoreEnvScripts      = False

        ## [ bool ] - Ignore env command entries.
        self._ignoreEnvCommands     = False

        ## [ bool ] - Ignore pre build env.
        self._ignorePre             = False

        ## [ bool ] - Ignore post build env.
        self._ignorePost            = False

        ## [ bool ] - Raise exceptions.
        self._raiseExceptions       = False

        ## [ bool ] - Repeat last env.
        self._last                  = False

        # CACHE

        ## [ bool ] - Cache write.
        self._cacheWrite            = False

        ## [ bool ] - Cache get.
        self._cacheRead             = False

        #

        ## [ mMeco.allLib.All ] - All.
        self._all                   = mMeco.libs.allLib.All.getInstance(request=self)

        #

        self._initialize()

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
    # PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Initialize.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def _initialize(self):

        # MECO

        meco = self._argumentParser.add_argument_group('MECO', '')

        meco.add_argument('-ab',
                          '--about',
                          action='store_true',
                          help='Display information about Meco.')

        meco.add_argument('-ver',
                          '--version',
                          action='store_true',
                          help='Display version.')


        # ENVS

        environments = self._argumentParser.add_argument_group('ENVIRONMENTS', '')

        environments.add_argument('-p',
                                  '--project',
                                  type=str,
                                  required=False,
                                  metavar='PROJECT_NAME',
                                  help='Project name. Default project name "master" will be used If this flag'
                                       'is not provided.')

        environments.add_argument('-d',
                                  '--developer',
                                  type=str,
                                  required=False,
                                  metavar='DEVELOPER_NAME',
                                  help='Development (-de|--development) or stage (-se|--stage) environment will be '
                                       'initialized for the provided developer (user). Default value is set to '
                                       'current user.')

        environments.add_argument('-de',
                                  '--development',
                                  type=str,
                                  required=False,
                                  metavar='DEVELOPMENT_ENV_NAME',
                                  help='Development environment name. Optionally -de|--developer flag can be '
                                       'provided.')

        environments.add_argument('-se',
                                  '--stage',
                                  type=str,
                                  required=False,
                                  metavar='STAGE_ENV_NAME',
                                  help='Stage environment name. Optionally --developer flag can be provided. '
                                       'Stage environment will be ignored if -de|--development flag is provided.')

        # APP

        app = self._argumentParser.add_argument_group('APP', '')

        app.add_argument('-a',
                         '--app',
                         type=str,
                         required=False,
                         metavar='APP_NAME',
                         help='App name.')

        app.add_argument('-aa',
                         '--app-args',
                         type=str,
                         required=False,
                         metavar='',
                         help='Custom arguments which will be added to the app executable. For this '
                              'flag to have affect, -a|--app flag must be provided.')

        app.add_argument('-iae',
                         '--ignore-app-exec',
                         action='store_true',
                         help='If you provide this flag, the executable provided by app (if any) for '
                              'the platform will be ignored and not run. However its environment will be '
                              'initialized. For this flag to have affect, -a|--app flag must be provided.')

        # SET STATE

        setState = self._argumentParser.add_argument_group('SET STATE', '')

        setState.add_argument('-do',
                              '--display-only',
                              action='store_true',
                              help='Environment script will be written only to display the environment but '
                                   'not to set it.')

        setState.add_argument('-so',
                              '--set-only',
                              action='store_true',
                              help='Environment script will be written only to set the environment but not '
                                   'to display it. If -so|--set-only flag is provided, -do|--display flag will '
                                   'be ignored.')

        setState.add_argument('-v',
                              '--verbose',
                              type=int,
                              required=False,
                              default=2,
                              choices=[1, 2, 3, 4],
                              metavar='',
                              help='Verbosity of the displayed data. '
                                   '1 - Env packages. '
                                   '2 - Env packages with variables. '
                                   '3 - Env packages with variables, command and scripts. '
                                   '4 - All including variables, command and scripts in pre and post envs. '
                              )

        setState.add_argument('-di',
                              '--display-info',
                              type=int,
                              required=False,
                              default=0,
                              choices=[0, 1, 2, 3],
                              metavar='',
                              help='Write data. '
                                   '0 - Display no info. '
                                   '1 - Display request. '
                                   '2 - Display settings. '
                                   '3 - Display all. '
                              )

        setState.add_argument('-ies',
                              '--ignore-env-scripts',
                              action='store_true',
                              help='Ignore script type env entries')

        setState.add_argument('-iec',
                              '--ignore-env-commands',
                              action='store_true',
                              help='Ignore command type env entries')

        setState.add_argument('-ipre',
                              '--ignore-pre',
                              action='store_true',
                              help='Ignore pre env build')

        setState.add_argument('-ipost',
                              '--ignore-post',
                              action='store_true',
                              help='Ignore post env build')

        setState.add_argument('-re',
                              '--raise-exceptions',
                              action='store_true',
                              help='Raise exceptions instead of showing error messages.')

        setState.add_argument('-l',
                              '--last',
                              action='store_true',
                              help='Repeat last initialized environment exactly.')

        #

        # CACHE

        cache = self._argumentParser.add_argument_group('CACHE', '')

        cache.add_argument('-cw',
                           '--cache-write',
                           action='store_true',
                           help='')

        cache.add_argument('-cr',
                           '--cache-read',
                           action='store_true',
                           help='')

    #
    ## @brief Set attributes after either `parse` or `parseFromStr` method is invoked.
    #  
    #  @exception N/A
    #  
    #  @return None - None.
    def _setAttributes(self):

        self._about             = self._args.about
        self._version           = self._args.version

        #

        self._project = self._args.project

        if self._args.developer:
            self._developer = self._args.developer

        self._development = self._args.development
        self._stage       = self._args.stage

        if self._development:
            self._stage = None

        #

        self._app               = self._args.app
        self._appArgs           = self._args.app_args
        self._ignoreAppExec     = self._args.ignore_app_exec

        #

        self._displayOnly       = self._args.display_only
        self._setOnly           = self._args.set_only
        if self._setOnly:
            self._displayOnly   = False
        self._verbose           = self._args.verbose
        self._displayInfo       = self._args.display_info
        self._ignoreEnvScripts  = self._args.ignore_env_scripts
        self._ignoreEnvCommands = self._args.ignore_env_commands
        self._ignorePre         = self._args.ignore_pre
        self._ignorePost        = self._args.ignore_post

        self._raiseExceptions   = self._args.raise_exceptions
        self._last              = self._args.last

        #

        self._cacheWrite         = self._args.cache_write
        self._cacheRead          = self._args.cache_read

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
    def argumentParser(self):

        return self._argumentParser

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def args(self):

        return self._args

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def unknownArgs(self):

        return self._unknownArgs

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def command(self):

        return self._command

    #
    ## @brief Property.
    #
    #  @param command [ str | None | in  ] - Command.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def setCommand(self, command):

        self._command = command

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def pythonVersion(self):

        return self._pythonVersion

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def platform(self):

        return self._platform

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def about(self):

        return self._about

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def version(self):

        return self._version

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def project(self):

        return self._project

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def developer(self):

        return self._developer

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def development(self):

        return self._development

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def stage(self):

        return self._stage

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def app(self):

        return self._app

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def appArgs(self):

        return self._appArgs

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def ignoreAppExec(self):

        return self._ignoreAppExec

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def displayOnly(self):

        return self._displayOnly

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def setOnly(self):

        return self._setOnly

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def verbose(self):

        return self._verbose

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def displayInfo(self):

        return self._displayInfo

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def ignoreEnvScripts(self):

        return self._ignoreEnvScripts

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def ignoreEnvCommands(self):

        return self._ignoreEnvCommands

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def ignorePre(self):

        return self._ignorePre

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def ignorePost(self):

        return self._ignorePost

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def raiseExceptions(self):

        return self._raiseExceptions

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def last(self):

        return self._last

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def cacheWrite(self):

        return self._cacheWrite

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Value.
    def cacheRead(self):

        return self._cacheRead

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Value.
    def allLib(self):

        return self._all

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Get string representation of the class.
    #
    #  @exception N/A
    #
    #  @return str - Information about the package in human readable form.
    def asStr(self):

        data = ''
        data += '\nREQUEST'
        data += '\n{}'.format('-' * 100)

        data += '\nCommand                               : {}'.format(self._command)

        data += '\nPlatform                              : {}'.format(self._platform)

        data += '\nAbout                                 : {}'.format(self._about)
        data += '\nVersion                               : {}'.format(self._version)

        data += '\nProject                               : {}'.format(self._project if self._project else 'N/A')
        data += '\nDeveloper                             : {}'.format(self._developer if self._developer else 'N/A')
        data += '\nDevelopment                           : {}'.format(self._development if self._development else 'N/A')
        data += '\nStage                                 : {}'.format(self._stage if self._stage else 'N/A')

        data += '\nApp                                   : {}'.format(self._app if self._app else 'N/A')
        data += '\nApp Args                              : {}'.format(self._appArgs if self._appArgs else 'N/A')
        data += '\nIgnore App Exec                       : {}'.format(self._ignoreAppExec)

        data += '\nDisplay Only                          : {}'.format(self._displayOnly)
        data += '\nSet Only                              : {}'.format(self._setOnly)
        data += '\nVerbose                               : {}'.format(self._verbose)
        data += '\nDisplay Info                          : {}'.format(self._displayInfo)
        data += '\nIgnore Env Scripts                    : {}'.format(self._ignoreEnvScripts)
        data += '\nIgnore Env Commands                   : {}'.format(self._ignoreEnvCommands)
        data += '\nIgnore Pre Env                        : {}'.format(self._ignorePre)
        data += '\nIgnore Post Env                       : {}'.format(self._ignorePost)
        data += '\nRaise Exceptions                      : {}'.format(self._raiseExceptions)
        data += '\nLast                                  : {}'.format(self._last)

        data += '\nCache Write                           : {}'.format(self._cacheWrite)
        data += '\nCache Read                            : {}'.format(self._cacheRead)

        return data

    #
    ## @brief Parse parameters from sys.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def parse(self):

        self._command = 'meco {}'.format(' '.join(sys.argv[1:]))

        self._args, self._unknownArgs = self._argumentParser.parse_known_args()

        self._setAttributes()

    #
    ## @brief Parse parameters from given string.
    #
    #  @param parameters [ str | None | in  ] - Parameters.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def parseFromStr(self, parameters):

        self._command = 'meco {}'.format(parameters)

        self._args, self._unknownArgs = self._argumentParser.parse_known_args(parameters.split())

        self._setAttributes()
