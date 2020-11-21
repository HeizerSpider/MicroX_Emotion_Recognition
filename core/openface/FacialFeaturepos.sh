echo enter path of file
read vidpath
./download_models.ps1
FeatureExtraction.exe -f $vidpath -simsize 300
