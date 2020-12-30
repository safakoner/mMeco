#!/usr/bin/env bash
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
## @file mMeco/script/shell/mmeco-set-compreply.sh [ FILE ] - Shell script file.


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
function _getMasterProjectName()
{
    echo "master"
}

function _getProjectsPath()
{
    echo "$MECO_PATH/meco";
}

# PARAMETER VALUE

function _getParameterValue()
{
    local lastIndex=$#
    local parameterValueIndex=2
    local index=0
    for i in $@; do

        if [[ "$i" == ${!lastIndex} ]]; then
            (( parameterValueIndex += index ))
            break
        fi
        (( index += 1 ))
    done

    echo ${!parameterValueIndex}

    return 0
}

function _getProjectParameterValue()
{
    local parameterValue=$(_getParameterValue $@ "-p")
    [[ ! "$parameterValue" ]] && parameterValue=$(_getParameterValue $@ "--project")

    if [[ "$parameterValue" ]]; then
        echo "$parameterValue"
    else
        echo $(_getMasterProjectName)
    fi
    return 0
}

function _getDeveloperParameterValue()
{
    local parameterValue=$(_getParameterValue $@ "-d")
    [[ ! "$parameterValue" ]] && parameterValue=$(_getParameterValue $@ "--developer")

    if [[ "$parameterValue" ]]; then
        echo "$parameterValue"
    else
        echo "$USER"
    fi
    return 0
}

function _getDevelopmentParameterValue()
{
    local parameterValue=$(_getParameterValue $@ "-de")
    [[ ! "$parameterValue" ]] && parameterValue=$(_getParameterValue $@ "--development")

    if [[ "$parameterValue" ]]; then
        echo "$parameterValue"
    else
        echo ""
    fi
    return 0
}

function _getStageParameterValue()
{
    local parameterValue=$(_getParameterValue $@ "-se")
    [[ ! "$parameterValue" ]] && parameterValue=$(_getParameterValue $@ "--stage")

    if [[ "$parameterValue" ]]; then
        echo "$parameterValue"
    else
        echo ""
    fi
    return 0
}

# PACKAGE

function _getLatestVersionOfAPackage()
{
    local versions=($(find "$1" -type d -maxdepth 1 -execdir basename '{}' ';' | sort -V));
    local latestVersion=${versions[${#versions[@]}-1]};
    echo "$latestVersion";
    return 0
}

# PROJECT

function _getProjectNames()
{
    local projectsPath=$(_getProjectsPath)
    local projectNames=$(/bin/ls -1 "${projectsPath}" 2> /dev/null)
    echo "$projectNames" | tr '\n' ' '
    return 0
}

function _getProjectPackagesPath()
{
    local projectName=$1
    local internalExternal=$2

    local projectPackagesPath="$(_getProjectsPath)/$projectName/$internalExternal"
    if [[ ! -d "$projectPackagesPath" ]] || echo "$projectPackagesPath"; then
        return 0
    else
        return 1
    fi
}

# DEVELOPER

function _getDevelopersPath()
{
    local developersPath="$(_getProjectsPath)/$1/developers"

    if [[ ! -d "$developersPath" ]] || echo "$developersPath"; then
        return 0
    else
        return 1
    fi
}

function _getDeveloperNames()
{
    local developersPath=$(_getDevelopersPath $1)
    local developerNames=$(/bin/ls -1 "${developersPath}" 2> /dev/null)
    echo "$developerNames" | tr '\n' ' '
    return 0
}

# DEVELOPMENT

function _getDevelopmentEnvironmentsPath()
{
    local developmentEnvironmentPath="$(_getDevelopersPath $1)/$2/development";
    if [[ ! -d "$developmentEnvironmentPath" ]] || echo "$developmentEnvironmentPath"; then
        return 0
    else
        return 1
    fi
}

function _getDevelopmentEnvironmentNames()
{
    local developmentEnvironmentPath=$(_getDevelopmentEnvironmentsPath $1 $2)
    local developmentEnvironmentNames=$(/bin/ls -1 "${developmentEnvironmentPath}" 2> /dev/null)
    echo "$developmentEnvironmentNames" | tr '\n' ' '
    return 0
}

# STAGE

function _getStageEnvironmentsPath()
{
    local stageEnvironmentPath="$(_getDevelopersPath $1)/$2/stage"
    if [[ ! -d "$stageEnvironmentPath" ]] || echo "$stageEnvironmentPath"; then
        return 0
    else
        return 1
    fi
}

function _getStageEnvironmentNames()
{
    local stageEnvironmentPath=$(_getStageEnvironmentsPath $1 $2)
    local stageEnvironmentNames=$(/bin/ls -1 "${stageEnvironmentPath}" 2> /dev/null)
    echo "$stageEnvironmentNames" | tr '\n' ' '
    return 0
}

# APP

function _getAppNames()
{
    local masterProjectName=$(_getMasterProjectName)
    local projectName=$1
    local developerName=$2
    local developmentEnvironmentName=$3
    local stageEnvironmentName=$4

    local packageName="mMecoSettings";
    local relativePath="resources/apps/";

    # DEVELOPMENT
    if [[ "$developmentEnvironmentName" ]]; then

        local appPath="$(_getDevelopmentEnvironmentsPath "$projectName" "$developerName")/$developmentEnvironmentName/$packageName/$relativePath";

        if [[ -d "$appPath" ]]; then

            local appNames=$(/bin/ls -1 "${appPath}" 2> /dev/null)
            appNames=$(echo "$appNames" | sed 's/\.json$//' | tr '\n' ' ')
            appNames=$(echo "$appNames" | tr '\n' ' ')
            allAppNames+=("$appNames")

        fi

    fi

    # STAGE
    if [[ "$stageEnvironmentName" ]]; then

        local appPath="$(_getStageEnvironmentsPath "$projectName" "$developerName")/$stageEnvironmentName/$packageName/$relativePath";

        if [[ -d "$appPath" ]]; then

            local appNames=$(/bin/ls -1 "${appPath}" 2> /dev/null)
            appNames=$(echo "$appNames" | sed 's/\.json$//' | tr '\n' ' ')
            appNames=$(echo "$appNames" | tr '\n' ' ')
            allAppNames+=("$appNames")

        fi

    fi

    # PROJECT
    if [[ "$projectName" !=  "$masterProjectName" ]]; then

        local packagePath="$(_getProjectPackagesPath "$projectName" "internal")/$packageName/";

        if [[ -d "$packagePath" ]]; then

            local latestVersion=$(_getLatestVersionOfAPackage "$packagePath");
            local appPath="$packagePath$latestVersion/$packageName/$relativePath";

            if [[ -d "$appPath" ]]; then

                local appNames=$(/bin/ls -1 "${appPath}" 2> /dev/null)
                appNames=$(echo "$appNames" | sed 's/\.json$//' | tr '\n' ' ')
                appNames=$(echo "$appNames" | tr '\n' ' ')
                allAppNames+=("$appNames")

            fi

        fi

    fi

    # MASTER PROJECT
    if [[ ! "$MECO_USE_PROJECT_APPS_ONLY" ]]; then

        local packagePath="$(_getProjectPackagesPath "$masterProjectName" "internal")/$packageName/";
        if [[ -d "$packagePath" ]]; then

            local latestVersion=$(_getLatestVersionOfAPackage "$packagePath");
            local appPath="$packagePath$latestVersion/$packageName/$relativePath";

            if [[ -d "$appPath" ]]; then

                local appNames=$(/bin/ls -1 "${appPath}" 2> /dev/null)
                appNames=$(echo "$appNames" | sed 's/\.json$//' | tr '\n' ' ')
                appNames=$(echo "$appNames" | tr '\n' ' ')
                allAppNames+=("$appNames")

            fi

        fi

    fi

    echo $(printf "%s " "${allAppNames[@]}")

    return 0
}

#

function _mMecoSetCompreplyMain()
{
    local parameters="-ab --about";
    parameters="$parameters -ver   --version";

    parameters="$parameters -p     --project";
    parameters="$parameters -d     --developer ";
    parameters="$parameters -de    --development";
    parameters="$parameters -se    --stage";

    parameters="$parameters -a     --app";
    parameters="$parameters -aa    --app-args";
    parameters="$parameters -iae   --ignore-app-exec";

    parameters="$parameters -do    --display-only";
    parameters="$parameters -so    --set-only";
    parameters="$parameters -v     --verbose";
    parameters="$parameters -di    --display-info";
    parameters="$parameters -ies   --ignore-env-scripts";
    parameters="$parameters -iec   --ignore-env-commands";
    parameters="$parameters -ipre  --ignore-pre";
    parameters="$parameters -ipost --ignore-post";
    parameters="$parameters -re    --raise-exceptions";
    parameters="$parameters -l     --last";

    parameters="$parameters -cw     --cache-write";
    parameters="$parameters -cr     --cache-read";

    COMPREPLY=()
    previous="${COMP_WORDS[COMP_CWORD-1]}"
    current="${COMP_WORDS[COMP_CWORD]}"

    local developerName="$USER"
    local projectName=$(_getMasterProjectName)

    # PROJECT
    if [[ "$previous" == "-p" ]] || [[ "$previous" == "--project" ]]; then

        local projectNames=$(_getProjectNames)
        COMPREPLY=( $(compgen -W "$projectNames" -- "$current") )

    # DEVELOPER
    elif [[ "$previous" == "-d" ]] || [[ "$previous" == "--developer" ]]; then

        projectName=$(_getProjectParameterValue ${COMP_WORDS[@]})
        local developerNames=$(_getDeveloperNames "$projectName")
        COMPREPLY=( $(compgen -W "$developerNames" -- "$current") )

    # DEVELOPMENT
    elif [[ "$previous" == "-de" ]] || [[ "$previous" == "--development" ]]; then

        projectName=$(_getProjectParameterValue ${COMP_WORDS[@]})
        developerName=$(_getDeveloperParameterValue ${COMP_WORDS[@]})
        local developmentEnvironmentNames=$(_getDevelopmentEnvironmentNames "$projectName" "$developerName")
        COMPREPLY=( $(compgen -W "$developmentEnvironmentNames" -- "$current") )

    # STAGE
    elif [[ "$previous" == "-se" ]] || [[ "$previous" == "--stage" ]]; then

        projectName=$(_getProjectParameterValue ${COMP_WORDS[@]})
        developerName=$(_getDeveloperParameterValue ${COMP_WORDS[@]})
        local stageEnvironmentNames=$(_getStageEnvironmentNames "$projectName" "$developerName")
        COMPREPLY=( $(compgen -W "$stageEnvironmentNames" -- "$current") )

    # APP
    elif [[ "$previous" == "-a" ]] || [[ "$previous" == "--app" ]]; then

        projectName=$(_getProjectParameterValue ${COMP_WORDS[@]})
        developerName=$(_getDeveloperParameterValue ${COMP_WORDS[@]})
        local developmentEnvironmentName=$(_getDevelopmentParameterValue ${COMP_WORDS[@]})
        local stageEnvironmentName=$(_getStageParameterValue ${COMP_WORDS[@]})

        local appNames=$(_getAppNames "$projectName" "$developerName" "$developmentEnvironmentName" "$stageEnvironmentName")

        COMPREPLY=( $(compgen -W "$appNames" -- "$current") )

    else

        case "$current" in

            *--*|*-*)
                COMPREPLY=( $(compgen -W "${parameters}" -- "$current") )

            ;;

        esac

    fi

    return 0
}
complete -o nospace -F _mMecoSetCompreplyMain meco sss
