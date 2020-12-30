# DESCRIPTION Change directory to reserved packages path
function _mMecoCDReservedMain()
{
    if (-Not $env:MECO_RESERVED_PACKAGES_PATH)
    {
        Write-Host "`nNo reserved packages path found.`n"
        return
    }

    if (-Not (Test-Path -Path $env:MECO_RESERVED_PACKAGES_PATH))
    {
        Write-Host "`nReserved packages path does not exist: $env:MECO_RESERVED_PACKAGES_PATH`n"
        return
    }

    cd $env:MECO_RESERVED_PACKAGES_PATH
}
_mMecoCDReservedMain