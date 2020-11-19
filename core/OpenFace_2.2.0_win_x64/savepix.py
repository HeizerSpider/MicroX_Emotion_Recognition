import sys
import pandas as pd
import os
file = sys.argv[1]
table = pd.read_csv(file)
# note: top left is 0x0
left_eyebrow_arr = []
right_eyebrow_arr = []
right_eye_arr = []
left_eye_arr = []
nose_arr = []
o_mouth_arr = []
i_mouth_arr = []
for i in range(17,22):
	left_eyebrow_arr.append(' x_' + str(i))
	left_eyebrow_arr.append(' y_' + str(i))
for i in range(22,27):
	right_eyebrow_arr.append(' x_' + str(i))
	right_eyebrow_arr.append(' y_' + str(i))
for i in range(42,48):
	right_eye_arr.append(' x_' + str(i))
	right_eye_arr.append(' y_' + str(i))
for i in range(36,42):
	left_eye_arr.append(' x_' + str(i))
	left_eye_arr.append(' y_' + str(i))
for i in range(27,36):
	nose_arr.append(' x_' + str(i))
	nose_arr.append(' y_' + str(i))
for i in range(48,60):
	o_mouth_arr.append(' x_' + str(i))
	o_mouth_arr.append(' y_' + str(i))
for i in range(60,68):
	i_mouth_arr.append(' x_' + str(i))
	i_mouth_arr.append(' y_' + str(i))
left_eyebrow = table[left_eyebrow_arr]
right_eyebrow = table[right_eyebrow_arr]
left_eye = table[left_eye_arr]
right_eye = table[right_eye_arr]
nose = table[nose_arr]
o_mouth = table[o_mouth_arr]
i_mouth = table[i_mouth_arr]
# print(left_eyebrow)
# print(right_eyebrow)
# print(left_eye)
# print(right_eye)
# print(nose)
# print(o_mouth)
# print(i_mouth)
shorten_path = file + "results"
path = "C:/Users/arsen/Desktop/OpenFace_2.2.0_win_x64/" + shorten_path
print(path)
os.mkdir(path)
left_eyebrow.to_csv( shorten_path +'/left_eyebrow.csv')
right_eyebrow.to_csv( shorten_path +'/right_eyebrow.csv')
left_eye.to_csv( shorten_path +'/left_eye.csv')
right_eye.to_csv( shorten_path +'/right_eye.csv')
nose.to_csv( shorten_path +'/nose.csv')
o_mouth.to_csv( shorten_path +'/omouth.csv')
i_mouth.to_csv(shorten_path + '/imouth.csv')
