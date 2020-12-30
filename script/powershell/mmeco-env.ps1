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
## @file mMeco/script/powershell/mmeco-env.ps1 [ FILE ] - PowerShell script file.


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
$Script:scriptPath = split-path -parent $MyInvocation.MyCommand.Definition

function script:_mMecoEnvMain
{
    $Local:mecoPackageRootPath = (get-item $scriptPath).parent.parent.FullName


    # ----------------------------------------------------------------------------------------------------
    # ENV
    # ----------------------------------------------------------------------------------------------------
    $Local:pythonPath = "$mecoPackageRootPath\python"
    if ($env:PYTHONPATH)
    {
        $env:PYTHONPATH="$pythonPath;$env:PYTHONPATH"
    }
    else
    {
        $env:PYTHONPATH=$pythonPath
    }

    $Local:binPath = "$mecoPackageRootPath\bin\windows"
    if (Test-Path $binPath)
    {
        $env:PATH="$binPath;$env:PATH"
    }
}
_mMecoEnvMain