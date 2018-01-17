call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\bin\vcvars32.bat"
set VisualStudioVersion=12.0
msbuild.exe %1 /t:Clean
msbuild.exe %1
echo -end
