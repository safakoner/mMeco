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
## @file mMeco/script/powershell/mmeco.ps1 [ FILE ] - PowerShell script file.


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
function script:_getLastParameter($command)
{
    $providedParameters        = $command.Split(" ")
    $providedParametersLength  = $providedParameters.Length

    if($providedParametersLength -eq 0)
    {
        return ""
    }
    else
    {
        return $providedParameters[$providedParametersLength - 1]
    }
}

function script:_getParameterValues($command)
{
    $providedParameters        = $command.Split(" ")
    $exec, $providedParameters = $providedParameters
    $providedParametersLength  = $providedParameters.Length

    $parameterNames  = "-p", "-d", "-de", "-se"
    $parameterValues = "master", $env:UserName, "", ""

    For($i=0; $i -lt $providedParametersLength; $i++)
    {
        For($a=0; $a -lt $parameterNames.Length; $a++)
        {
            if($providedParameters[$i] -eq $parameterNames[$a])
            {
                $nextIndex = $i + 1

                if($providedParametersLength -gt $nextIndex)
                {
                    $parameterValues[$a] = $providedParameters[$i+1]
                }
            }
        }
    }

    return $parameterValues
}

#
#
#

function script:_getMecoInstallationPath()
{
    return $env:MECO_PATH
}

function script:_getMasterProjectName()
{
    return "master"
}

function script:_getProjectsPath()
{
    $installationPath = script:_getMecoInstallationPath
    return "$installationPath\meco"
}

#

function script:_getDevelopersPath([String]$projectName)
{
    # \meco\$project\developers -> path
    $path = script:_getProjectsPath
    return "$path\$projectName\developers"
}

function script:_getDeveloperNames([String]$projectName)
{
    # \meco\$project\developers\ -> name name name
    $path = script:_getDevelopersPath -projectName $projectName
    return (Get-ChildItem $path -Directory).BaseName | Sort-Object
}

#

function script:_getDevelopmentEnvironmentsPath([String]$project, [String]$developer)
{
    # \meco\$project\developers\$developer\development -> path
    $path = script:_getDevelopersPath -project $project
    return "$path\$developer\development"
}

function script:_getDevelopmentEnvironmentNames([String]$project, [String]$developer)
{
    # \meco\$project\developers\$developer\development -> name name name
    $path = script:_getDevelopmentEnvironmentsPath -project $project -developer $developer
    return (Get-ChildItem $path -Directory).BaseName | Sort-Object
}

#

function script:_getStageEnvironmentsPath([String]$project, [String]$developer)
{
    # \meco\$project\developers\$developer\stage -> path
    $path = script:_getDevelopersPath -project $project
    return "$path\$developer\stage"
}

function script:_getStageEnvironmentNames([String]$project, [String]$developer)
{
    # \meco\$project\developers\$developer\stage -> name name name
    $path = script:_getStageEnvironmentsPath -project $project -developer $developer
    return (Get-ChildItem $path -Directory).BaseName | Sort-Object
}

#

function script:_getAppNames([String]$project, [String]$developer, [String]$envType, [String]$envName)
{
    $packageName = "mMecoSettings"
    $relativePath = "resources\apps\"

    $appNames = @()

    # DEVELOPMENT OR STAGE
    if($envType)
    {
        $envPath = ""
        if($envType -eq "development")
        {
            $envPath = script:_getDevelopmentEnvironmentsPath -project $project -developer $developer
        }
        elseif($envType -eq "stage")
        {
            $envPath = script:_getStageEnvironmentsPath -project $project -developer $developer
        }

        $appPath = "$envPath\$envName\$packageName\$relativePath"
        if(Test-Path -Path $appPath)
        {
            $appNames = (Get-ChildItem $appPath -File -Filter "*.json").BaseName | Sort-Object
        }
    }

    $projectsPath      = script:_getProjectsPath
    $masterProjectName = script:_getMasterProjectName

    # PROJECT
    if($project -ne $masterProjectName)
    {
        $appPath = "$projectsPath\$project\internal\$packageName"
        if (Test-Path -Path $appPath)
        {
            $versions = (Get-ChildItem $appPath -Directory).BaseName | Sort-Object
            $versions = $versions | %{ new-object System.Version ($_) } | sort
            $version  = $versions[-1]
            $appPath  = "$appPath\$version\$packageName\$relativePath"

            if (Test-Path -Path $appPath)
            {
                $appNames += (Get-ChildItem $appPath -File -Filter "*.json").BaseName | Sort-Object
            }
        }
    }

    # MASTER PROJECT
    if(-Not $env:MECO_USE_PROJECT_APPS_ONLY)
    {
        $appPath = "$projectsPath\$masterProjectName\internal\$packageName"
        if (Test-Path -Path $appPath)
        {
            $versions = (Get-ChildItem $appPath -Directory).BaseName | Sort-Object
            $versions = $versions | %{ new-object System.Version ($_) } | sort
            $version  = $versions[-1]
            $appPath  = "$appPath\$version\$packageName\$relativePath"

            if (Test-Path -Path $appPath)
            {
                $appNames += (Get-ChildItem $appPath -File -Filter "*.json").BaseName | Sort-Object
            }
        }
    }

    return $appNames | select -uniq
}

#

function script:mMecoCompleter($wordToComplete, $commandAst, $cursorPosition)
{
    $lastParameter = script:_getLastParameter -command $commandAst.toString()

    $project, $developer, $development, $stage = script:_getParameterValues -command $commandAst.toString()

    #

    # Development or stage environment
    $envType = ""
    $envName = ""
    if ($development)
    {
        $envType = "development"
        $envName = $development
    }
    elseif($stage)
    {
        $envType = "stage"
        $envName = $stage
    }

    #

    if ($lastParameter -eq "-p")
    {
        $projectsPath = script:_getProjectsPath
        return (Get-ChildItem $projectsPath -Directory).BaseName | Sort-Object
    }
    if ($lastParameter -eq "-d")
    {
        $developerNames = script:_getDeveloperNames -projectName $project
        return $developerNames
    }
    if ($lastParameter -eq "-de")
    {
        $developmentEnvironmentNames = script:_getDevelopmentEnvironmentNames -project $project -developer $developer
        return $developmentEnvironmentNames
    }
    if ($lastParameter -eq "-se")
    {
        $stageEnvironmentNames = script:_getStageEnvironmentNames -project $project -developer $developer
        return $stageEnvironmentNames
    }
    if ($lastParameter -eq "-a")
    {
        $appNames = script:_getAppNames -project $project -developer $developer -envType $envType -envName $envName
        return $appNames
    }
}

Register-ArgumentCompleter -Native -CommandName meco -ScriptBlock {

    param($wordToComplete, $commandAst, $cursorPosition)
    $values = mMecoCompleter -wordToComplete $wordToComplete -commandAst $commandAst -cursorPosition $cursorPosition
    echo -- $values
}

Register-ArgumentCompleter -Native -CommandName sss -ScriptBlock {

    param($wordToComplete, $commandAst, $cursorPosition)
    $values = mMecoCompleter -wordToComplete $wordToComplete -commandAst $commandAst -cursorPosition $cursorPosition
    echo -- $values
}

function global:sss([switch]$h,
                    [switch]$ab,
                    [switch]$ver,

                    [string]$p="",
                    [string]$d="",
                    [string]$de="",
                    [string]$se="",

                    [string]$a="",
                    [string]$aa="",
                    [switch]$iae,

                    [switch]$do,
                    [switch]$so,
                    [int]$v,
                    [int]$di,
                    [switch]$ies,
                    [switch]$iec,
                    [switch]$ipre,
                    [switch]$ipost,
                    [switch]$re,
                    [switch]$l,

                    [switch]$cw,
                    [switch]$cr
                    )
{

    # Check whether development and stage environments are given at the same time
    if(-Not [string]::IsNullOrEmpty($de) -And -Not [string]::IsNullOrEmpty($se))
    {
        Write-Host ""
        Write-Host "Both -de (development) and -se (stage) flags can not be used at the same time, please only use either one." -ForegroundColor Red
        Write-Host ""
        return
    }

    $arguments = "-c", '"import mMeco.mecoCmd;mMeco.mecoCmd.main()"'

    foreach($boundParameter in $PSBoundParameters.GetEnumerator())
    {
        # Parameters are passed without dash so add it
        $arguments += "-" + $boundParameter.Key

        if (($boundParameter.Value -ne $true) -And ($boundParameter.Value -ne $false))
        {
            $arguments += "`"" + $boundParameter.Value + "`""
        }
    }

    $info = New-Object System.Diagnostics.ProcessStartInfo
    $info.FileName  = "python.exe"
    $info.Arguments = $arguments
    $info.RedirectStandardError = $true
    $info.RedirectStandardOutput = $true
    $info.UseShellExecute = $false

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $info
    $process.Start() | Out-Null
    $process.WaitForExit()
    $coutResult = $process.StandardOutput.ReadToEnd().Trim()
    $cerrResult = $process.StandardError.ReadToEnd().Trim()

    # Result is an error, display it
    if($cerrResult)
    {
        Write-Host ""
        Write-Host $cerrResult -ForegroundColor Red
        Write-Host ""
        return
    }

    # Result is empty, display it
    # This might be because of incorrect arguments
    if([string]::IsNullOrEmpty($coutResult) -And [string]::IsNullOrEmpty($cerrResult))
    {
        Write-Host ""
        Write-Host "Result is empty. You probably did not provide some of the reqired flags." -ForegroundColor Red
        Write-Host ""
        return
    }

    # Result is not a file, display it
    # Even though its cout, it just might be an error
    if(-Not (Test-Path $coutResult -PathType Leaf))
    {
        Write-Host ""
        Write-Host $coutResult
        Write-Host ""
        return
    }

    # File type is invalid, display it
    if (-Not ($coutResult -Like "*.ps1"))
    {
        Write-Host ""
        Write-Host "File is not an environment powershell script: $coutResult" -ForegroundColor Red
        Write-Host ""
        return
    }

    & {. "$coutResult"}

    # Change directory if development environment is set
    if($development -And (Test-Path -Path $env:MECO_DEVELOPMENT_PACKAGES_PATH))
    {
        Set-Location $env:MECO_DEVELOPMENT_PACKAGES_PATH
        return
    }

    # Change directory if stage environment is set
    if($stage -And (Test-Path -Path $env:MECO_STAGE_PACKAGES_PATH))
    {
        Set-Location $env:MECO_STAGE_PACKAGES_PATH
        return
    }
}


function global:meco([switch]$h,
                     [switch]$ab,
                     [switch]$ver,

                     [string]$p="",
                     [string]$d="",
                     [string]$de="",
                     [string]$se="",

                     [string]$a="",
                     [string]$aa="",
                     [switch]$iae,

                     [switch]$do,
                     [switch]$so,
                     [int]$v,
                     [int]$di,
                     [switch]$ies,
                     [switch]$iec,
                     [switch]$ipre,
                     [switch]$ipost,
                     [switch]$re,
                     [switch]$l,

                     [switch]$cw,
                     [switch]$cr
                    )
{

    # Check whether development and stage environments are given at the same time
    if(-Not [string]::IsNullOrEmpty($de) -And -Not [string]::IsNullOrEmpty($se))
    {
        Write-Host ""
        Write-Host "Both -de (development) and -se (stage) flags can not be used at the same time, please only use either one." -ForegroundColor Red
        Write-Host ""
        return
    }

    $arguments = "-c", '"import mMeco.mecoCmd;mMeco.mecoCmd.main()"'

    foreach($boundParameter in $PSBoundParameters.GetEnumerator())
    {
        # Parameters are passed without dash so add it
        $arguments += "-" + $boundParameter.Key

        if (($boundParameter.Value -ne $true) -And ($boundParameter.Value -ne $false))
        {
            $arguments += "`"" + $boundParameter.Value + "`""
        }
    }

    $info = New-Object System.Diagnostics.ProcessStartInfo
    $info.FileName  = "python.exe"
    $info.Arguments = $arguments
    $info.RedirectStandardError = $true
    $info.RedirectStandardOutput = $true
    $info.UseShellExecute = $false

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $info
    $process.Start() | Out-Null
    $process.WaitForExit()
    $coutResult = $process.StandardOutput.ReadToEnd().Trim()
    $cerrResult = $process.StandardError.ReadToEnd().Trim()

    # Result is an error, display it
    if($cerrResult)
    {
        Write-Host ""
        Write-Host $cerrResult -ForegroundColor Red
        Write-Host ""
        return
    }

    # Result is empty, display it
    # This might be because of incorrect arguments
    if([string]::IsNullOrEmpty($coutResult) -And [string]::IsNullOrEmpty($cerrResult))
    {
        Write-Host ""
        Write-Host "Result is empty. You probably did not provide some of the reqired flags." -ForegroundColor Red
        Write-Host ""
        return
    }

    # Result is not a file, display it
    # Even though its cout, it just might be an error
    if(-Not (Test-Path $coutResult -PathType Leaf))
    {
        Write-Host ""
        Write-Host $coutResult
        Write-Host ""
        return
    }

    # File type is invalid, display it
    if (-Not ($coutResult -Like "*.ps1"))
    {
        Write-Host ""
        Write-Host "File is not an environment powershell script: $coutResult" -ForegroundColor Red
        Write-Host ""
        return
    }

    & {. "$coutResult"}

    # Change directory if development environment is set
    if($development -And (Test-Path -Path $env:MECO_DEVELOPMENT_PACKAGES_PATH))
    {
        Set-Location $env:MECO_DEVELOPMENT_PACKAGES_PATH
        return
    }

    # Change directory if stage environment is set
    if($stage -And (Test-Path -Path $env:MECO_STAGE_PACKAGES_PATH))
    {
        Set-Location $env:MECO_STAGE_PACKAGES_PATH
        return
    }
}




