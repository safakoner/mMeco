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
## @file mMeco/script/shell/mmeco-env.sh [ FILE ] - Shell script file.


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
function _mMecoEnvMain()
{
    local platformName="linux";
    if [[ "$OSTYPE" == *"darwin"* ]]; then
        platformName="darwin";
        export BASH_SILENCE_DEPRECATION_WARNING=1
    fi

    # ----------------------------------------------------------------------------------------------------
    # ENV
    # ----------------------------------------------------------------------------------------------------
    local pythonPath="${BASH_SOURCE%/*/*/*}/python";

    if [[ -d "$pythonPath" ]]; then
        if [[ "$PYTHONPATH" ]]; then
            export PYTHONPATH="$pythonPath:$PYTHONPATH"
        else
            export PYTHONPATH="$pythonPath"
        fi
    fi

    local binPath="${BASH_SOURCE%/*/*/*}/bin/$platformName";
    if [[ -d "$binPath" ]]; then
        export PATH="$binPath:$PATH";
    fi
}
_mMecoEnvMain