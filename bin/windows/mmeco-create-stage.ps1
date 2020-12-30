# DESCRIPTION Create a stage env for development packages
& $env:MECO_PYTHON_EXECUTABLE_PATH -c "import mMeco.mecoCmd;mMeco.mecoCmd.createStage()" $args