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
## @file mMeco/script/shell/mmeco-bash-profile.sh [ FILE ] - Shell script file.


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
function _mMecoBashProfileMain()
{
    [[ "$IS_MECO_ACTIVATED" ]] && return;

    # USING PROJECT APPS ONLY
    # Uncomment the following line if you want -a|--app flag to only list apps available in the project passed by
    # -p|--project flag. Otherwise apps in master project will also be listed.
    #export MECO_USE_PROJECT_APPS_ONLY="1";


    # PATH
    # Absolute path of meco folder.
    # Example path: "/mnt"
    export MECO_PATH="$HOME/_development";


    # ----------------------------------------------------------------------------------------------------
    # DO NOT CHANGE ANYTHING BELOW
    # ----------------------------------------------------------------------------------------------------

    # USER

    # Some companies use email addresses as actual user names, get user name from the email address if this is the case.
    local user=$(echo "$USER" | cut -f1 -d@);

    #

    local developmentPackagesPath="$MECO_PATH/meco/master/developers/$user/development/main";
    local masterProjectInternalPackagesPath="$MECO_PATH/meco/master/internal";

    local packageList=("mMeco" "mMecoSettings")
    local packageNameLower="";
    local entryPointFile="";

    for package in ${packageList[@]};
    do
        packageNameLower=$(echo "$package" | tr '[:upper:]' '[:lower:]');

        # DEVELOPMENT PACKAGES
        entryPointFile="$developmentPackagesPath/$package/script/shell/$packageNameLower-entry-point.sh";
        if [[ -f "$entryPointFile" ]]; then
            source "$entryPointFile";
            continue;
        else
            :
        fi

        # MASTER INTERNAL PACKAGES
        local masterInternalPackageVersionPath="$masterProjectInternalPackagesPath/$package/";
        [[ ! -d "$masterInternalPackageVersionPath" ]] && continue

        local versions=($(find "$masterInternalPackageVersionPath" -type d -maxdepth 1 -execdir basename '{}' ';' | sort -V));
        local latestVersion=${versions[${#versions[@]}-1]};

        entryPointFile="$masterInternalPackageVersionPath$latestVersion/$package/script/shell/$packageNameLower-entry-point.sh";
        if [[ -f "$entryPointFile" ]]; then
            source "$entryPointFile";
        else
            :
        fi

    done

    export IS_MECO_ACTIVATED="1"
}
alias meco-init=_mMecoBashProfileMain
