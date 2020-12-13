ECHO OFF
ECHO Starting up
setlocal enableDelayedExpansion 
set MYDIR= "C:\Users\arsen\Desktop\DSProject\MicroX_Emotion_Recognition\core\openface\OpenFace_2.2.0_win_x64\allframes\testdataset"
for /F %%x in ('dir /B/D %MYDIR%') do (
  set FILENAME=%MYDIR%\%%x
  set OUTFILE=%%x_raw.csv
  echo ===========================  Search in !FILENAME! ===========================
  echo %%x
  echo !FILENAME!\%%x_frame
  echo !OUTFILE!
  echo hi
  echo "C:\Users\arsen\Desktop\openfacetest\OpenFace_2.2.0_win_x64\allframes\finaldataset101-150\%%x\%%x_frame"
  set MYYDIR = C:\Users\arsen\Desktop\openfacetest\OpenFace_2.2.0_win_x64\allframes\finaldataset101-150\%%x\%%x_frame
  FeatureExtraction.exe -fdir !FILENAME!\%%x_frame -2Dfp -of !OUTFILE!
)

PAUSE