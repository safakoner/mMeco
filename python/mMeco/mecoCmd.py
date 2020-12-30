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
## @file    mMeco/mecoCmd.py @brief [ FILE   ] - Command module.
## @package mMeco.mecoCmd    @brief [ MODULE ] - Command module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import  os
import  argparse
from    getpass import getuser

import  mMeco.core.displayLib

import  mMeco.core.platformLib
import  mMeco.mecoLib

import  mMecoSettings.envVariablesLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief Main function.
#
#  @exception N/A
#
#  @return None - None.
def main():

    meco    = mMeco.mecoLib.Meco()
    result  = meco.writeFile()

    if meco.allLib().logger().hasFailure():
        meco.allLib().logger().displayLastFailure()
        return 1

    if isinstance(result, str):
        meco.allLib().logger().display(result,
                                       startNewLine=False,
                                       endNewLine=False,
                                       useColor=False,
                                       color=None)

    return 0

#
## @brief Create development environment.
#
#  @exception N/A
#
#  @return None.
def createDevelopment():

    import  mMeco.libs.projectLib

    _parser = argparse.ArgumentParser(description='Create a development environment')

    _parser.add_argument('name',
                         type=str,
                         help='Name of the development environment to be created')

    _args = _parser.parse_args()

    #

    projectName        = os.environ.get(mMecoSettings.envVariablesLib.MECO_PROJECT_NAME, '')
    developerName      = getuser()
    developmentEnvName = _args.name

    _project = None
    developmentEnvPath = None

    try:
        _project = mMeco.libs.projectLib.Project(projectName)
        developmentEnvPath = _project.createDevelopmentEnvironment(developmentEnvName, developerName)
    except Exception as error:
        mMeco.core.displayLib.Display.displayFailure(str(error))
        mMeco.core.displayLib.Display.displayBlankLine()
        return

    mMeco.core.displayLib.Display.displaySuccess('Development environment has been created: {}'.format(developmentEnvPath))
    mMeco.core.displayLib.Display.displayInfo('You can initialize the newly created development environment by invoking the following command:\n')

    if mMeco.core.platformLib.Platform.isWindows():
        mMeco.core.displayLib.Display.displayInfo('mmeco -p {} -de {}'.format(projectName, developmentEnvName), startNewLine=False)
    else:
        mMeco.core.displayLib.Display.displayInfo('mmeco --project {} --development {}'.format(projectName, developmentEnvName), startNewLine=False)

    mMeco.core.displayLib.Display.displayBlankLine()

#
## @brief Create a project.
#
#  @exception N/A
#
#  @return None.
def createProject():

    import  mMeco.libs.projectLib

    _parser = argparse.ArgumentParser(description='Create a project')

    _parser.add_argument('name',
                         type=str,
                         help='Name of the project to be created')

    _args = _parser.parse_args()

    #

    projectName = _args.name

    _project = None

    try:
        _project = mMeco.libs.projectLib.Project.create(projectName)
    except Exception as error:
        mMeco.core.displayLib.Display.displayFailure(str(error))
        mMeco.core.displayLib.Display.displayBlankLine()
        return

    mMeco.core.displayLib.Display.displaySuccess('Project has been created: {}'.format(_project.projectRoot()))
    mMeco.core.displayLib.Display.displayInfo('You can initialize the newly created project by invoking the following command:')

    if mMeco.core.platformLib.Platform.isWindows():
        mMeco.core.displayLib.Display.displayInfo('meco -p {}'.format(_project.name()), startNewLine=True)
    else:
        mMeco.core.displayLib.Display.displayInfo('meco --project {}'.format(_project.name()), startNewLine=True)

    mMeco.core.displayLib.Display.displayBlankLine()

#
## @brief Create reserved environment.
#
#  @exception N/A
#
#  @return None.
def createReserved():

    import  mMeco.libs.projectLib

    #

    projectName         = os.environ.get(mMecoSettings.envVariablesLib.MECO_PROJECT_NAME, '')
    developerName       = getuser()
    reservedEnvPath     = None

    try:
        project = mMeco.libs.projectLib.Project(projectName)
        reservedEnvPath = project.createReservedEnvironment(developerName)
    except Exception as error:
        mMeco.core.displayLib.Display.displayFailure(str(error))
        mMeco.core.displayLib.Display.displayBlankLine()
        return

    mMeco.core.displayLib.Display.displaySuccess('Reserved environment has been created: {}'.format(reservedEnvPath))

    mMeco.core.displayLib.Display.displayBlankLine()

#
## @brief Create a stage env for development packages.
#
#  @exception N/A
#
#  @return None - None.
def createStage():

    import  mMeco.libs.projectLib

    developmentEnvName = os.environ.get(mMecoSettings.envVariablesLib.MECO_DEVELOPMENT_ENV_NAME)
    if not developmentEnvName:
        mMeco.core.displayLib.Display.displayFailure('You must initialize development environment to create a stage environment.')
        return

    parser = argparse.ArgumentParser(description='Create a stage env for development packages')

    parser.add_argument('-n',
                        '--name',
                        type=str,
                        default='',
                        help='Name of the stage environment',
                        required=False)

    _args = parser.parse_args()

    #

    projectName     = os.environ.get(mMecoSettings.envVariablesLib.MECO_PROJECT_NAME)
    userName        = os.environ.get(mMecoSettings.envVariablesLib.MECO_DEVELOPER_NAME)
    stageEnvName    = _args.name

    if not stageEnvName:
        stageEnvName = developmentEnvName

    _project        = None
    stageEnvPath    = None

    try:
        _project = mMeco.libs.projectLib.Project(projectName)
        stagePackagesPath = _project.createStageEnvironment(name=stageEnvName,
                                                            developmentEnvName=developmentEnvName,
                                                            developerName=userName,
                                                            verbose=True
                                                            )
    except Exception as error:
        mMeco.core.displayLib.Display.displayFailure(str(error))
        mMeco.core.displayLib.Display.displayBlankLine()
        return


    mMeco.core.displayLib.Display.displaySuccess('Stage environment has been created: {}'.format(stagePackagesPath))
    mMeco.core.displayLib.Display.displayInfo('You can initialize the newly created stage environment by invoking the following command:')

    if mMeco.core.platformLib.Platform.isWindows():
        mMeco.core.displayLib.Display.displayInfo('meco -p {} -d {} -se {}'.format(projectName, userName, stageEnvName))
    else:
        mMeco.core.displayLib.Display.displayInfo('meco --project {} --developer {} --stage {}'.format(projectName, userName, stageEnvName))

    mMeco.core.displayLib.Display.displayBlankLine()

