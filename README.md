# MicroX_Emotion_Recognition
While most studies focus on the model and its parameters, our study aims to add an additional depth to the field of emotion recognition, by learning from the best applications of neural networks and processing, us humans. As we try so hard to innovate and derive new models, our study places emphasis instead on the approach, and how we intend to break down the problem. Studies of the human behaviour, body language and micro expressions specialists are those who we can learn from. This forms the motivation for our micro expression (MicroX) model. While the average human understands emotion based on past exposure or experience, subconsciously being able to tell how another person might be feeling through his/her facial expressions, experts on the other hand are able to quantify what they see before them and make accurate judgements. 

Research paper can be found [here](https://github.com/HeizerSpider/MicroX_Emotion_Recognition/blob/main/MicroX%20Emotion%20Recognition.pdf)

### Datasets Used
- BAUM-1
- BAUM-2

### Pre-Processing
for openface (works only in windows):

- download [this binary](https://github.com/TadasBaltrusaitis/OpenFace/releases/download/OpenFace_2.2.0/OpenFace_v2.2.0_win_x64.zip) and move [this file](https://github.com/HeizerSpider/MicroX_Emotion_Recognition/blob/main/core/openface/automation.bat) into the OpenFace_2.2.0_win_x64 folder downloaded from  the openface link

- execute the download_models.ps1 PowerShell script(right click on the script and select Run with PowerShell)

- replace MYDIR with folder path of images and run the batch script by double clicking on the batch file

- results will appear in processed/ folder when completed

- Run the preprocessing script core/main.py with ```python main.py -d [dataset directory]```
- Output Folder will have all microX images as well as main frame


<img src=res/preprocessing.png width="300">

### Model Overview
Our model takes into consideration temporal images derived from frames in sequence, with each input spanning 10 frames from a single video. Frames are extracted from videos using OpenCV with a frame rate of 30fps. For each of these frames, we further break them down into its individual micro expression components. Mainly, the right eye, left eye, nose and mouth. We also retain the original full-face frame. We then feed each of these components into a single ConvLSTM block. This is done so that each MicroX component will output a value in relation to time that is dependent only on the component itself (eg. The changes in the right eye relative to time will be given an output value that is independent of the other MicroX components).

<img src=res/model_overview.png width="300">

### Acknowledgements
- S. Zhalehpour, O. Onder, Z. Akhtar and C. E. Erdem, “BAUM-1: A Spontaneous Audio-Visual Face Database of Affective and Mental States”, IEEE Trans. on Affective Computing, DOI: 10.1109/TAFFC.2016.2553038.
- C. E. Erdem, C. Turan and Z. Aydın, “BAUM-2: A Multilingual Audio-Visual Affective Database”, Multimedia Tools and Applications, DOI: 10.1007/s11042-014-1986-2, 2014. Database web site: http://baum2.bahcesehir.edu.tr.

### References
- [1] Convolutional experts constrained local model for facial landmark detection A. Zadeh, T. Baltrušaitis, and Louis-Philippe Morency. Computer Vision and Pattern Recognition Workshops, 2017
- [2] Zhalehpour, S.; Onder, O.; Akhtar, Z.; Erdem, C.E. BAUM-1: A Spontaneous Audio-Visual Face Database of Affective and Mental States. IEEE Trans. Affect. Comput. 2017, 8, 300–313.
- [3] Deep Temporal–Spatial Aggregation for Video-Based Facial Expression Recognition Xianzhang Pan , Wenping Guo , Xiaoying Guo, Wenshu Li, Junjie Xu and Jinzhao Wu, Symmetry 2019
