# DESCRIPTION Change directory to development packages path
function _mMecoCDDevMain()
{
    if (-Not $env:MECO_DEVELOPMENT_PACKAGES_PATH)
    {
        Write-Host "`nYou must initialize development environment to navigate to development packages path.`n"
        return
    }

    if (-Not (Test-Path -Path $env:MECO_DEVELOPMENT_PACKAGES_PATH))
    {
        Write-Host "`nDevelopment packages path does not exist: $env:MECO_DEVELOPMENT_PACKAGES_PATH`n"
        return
    }

    cd $env:MECO_DEVELOPMENT_PACKAGES_PATH
}
_mMecoCDDevMain