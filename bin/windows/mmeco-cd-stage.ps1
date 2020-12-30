# DESCRIPTION Navigate to stage packages path
function _mMecoCDStageMain()
{
    if (-Not $env:MECO_STAGE_PACKAGES_PATH)
    {
        Write-Host "`nYou must initialize stage environment to navigate to stage packages path.`n"
        return
    }

    if (-Not (Test-Path -Path $env:MECO_STAGE_PACKAGES_PATH))
    {
        Write-Host "`nStage packages path does not exist: $env:MECO_STAGE_PACKAGES_PATH`n"
        return
    }

    cd $env:MECO_STAGE_PACKAGES_PATH
}
_mMecoCDStageMain