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
## @file mMeco/script/powershell/mmeco-powershell-profile.ps1 [ FILE ] - PowerShell script file.


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass

function script:_mMecoBashProfileGetLatestVersionOfAPackage($path)
{
    $versions = (Get-ChildItem $path -Directory).BaseName | Sort-Object
    $versions = $versions | %{ new-object System.Version ($_) } | sort
    $version = $versions[-1]
    return $version
}

function script:_mMecoBashProfileMain()
{
    if($env:IS_MECO_ACTIVATED)
    {
        return
    }


    # USING PROJECT APPS ONLY
    # Uncomment the following line if you want -a flag to only list apps available in the project passed by
    # -p flag. Otherwise apps in master project will also be listed.
    #$env:MECO_USE_PROJECT_APPS_ONLY="1";


    # PATH
    # Absolute path of meco folder.
    # Example path: "D:"
    $env:MECO_PATH="C:"


    # ----------------------------------------------------------------------------------------------------
    # DO NOT CHANGE ANYTHING BELOW
    # ----------------------------------------------------------------------------------------------------

    # USER

    # Some companies use email addresses as actual user names, get user name from the email address if this is the case.
    $user=($env:UserName).Split('@')[0]

    #

    $developmentPackagesPath = "$env:MECO_PATH\meco\master\developers\$user\development\main"
    $masterProjectInternalPackagesPath = "$env:MECO_PATH\meco\master\internal";

    $packages = "mMecoSettings",
                "mMeco"
    $packageNameLower = ""
    $entryPointFile = ""

    foreach($package in $packages)
    {
        $packageNameLower = $package.ToLower()

        # DEVELOPMENT PACKAGES
        $entryPointFile="$developmentPackagesPath\$package\script\powershell\$packageNameLower-entry-point.ps1";
        if (Test-Path $entryPointFile)
        {
            . $entryPointFile
            continue
        }
        else
        {

        }

        # MASTER INTERNAL PACKAGES
        $masterProjectInternalPackageVersionPath="$masterProjectInternalPackagesPath\$package";
        if (Test-Path -Path $masterProjectInternalPackageVersionPath)
        {
            $latestVersion = script:_mMecoBashProfileGetLatestVersionOfAPackage($masterProjectInternalPackageVersionPath)
            $entryPointFile = "$masterProjectInternalPackageVersionPath\$latestVersion\$package\script\powershell\$packageNameLower-entry-point.ps1";
            if (Test-Path $entryPointFile)
            {
                . $entryPointFile
            }
            else
            {

            }
        }
    }

    $env:IS_MECO_ACTIVATED = "1"
}

function meco-init()
{
    _mMecoBashProfileMain
}
