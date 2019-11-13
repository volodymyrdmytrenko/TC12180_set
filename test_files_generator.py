import shutil
from shutil import copyfile
s = 'tc12180_orig.py'
n = 0

main_matrix = [["for_em", "for_mn", "for_hr", "role", "any", "oi", "all", "dir", "sub"],
                       ["True", "True", "True", "em", "can", "can", "can", "skip", "skip"],  # 1
                       ["True", "True", "True", "mn", "can", "can", "can", "can", "can"],  # 2
                       ["True", "True", "True", "hr", "can", "can", "can", "skip", "skip"],  # 3
                       ["True", "True", "True", "hrmn", "skip", "skip", "skip", "skip", "skip"],  # 4
                       ["True", "False", "True", "em", "can", "can", "can", "skip", "skip"],  # 5
                       ["True", "False", "True", "mn", "can", "can", "can", "can", "can"],  # 6
                       ["True", "False", "True", "hr", "can", "can", "can", "skip", "skip"],  # 7
                       ["True", "False", "True", "hrmn", "skip", "skip", "skip", "skip", "skip"],  # 8
                       ["True", "False", "False", "em", "can", "can", "can", "skip", "skip"],  # 9
                       ["True", "False", "False", "mn", "can", "can", "can", "can", "can"],  # 10
                       ["True", "False", "False", "hr", "can", "can", "can", "skip", "skip"],  # 11
                       ["True", "False", "False", "hrmn", "skip", "skip", "skip", "skip", "skip"],  # 12
                       ["True", "True", "False", "em", "can", "can", "can", "skip", "skip"],  # 13
                       ["True", "True", "False", "mn", "can", "can", "can", "can", "can"],  # 14
                       ["True", "True", "False", "hr", "can", "can", "can", "skip", "skip"],  # 15
                       ["True", "True", "False", "hrmn", "skip", "skip", "skip", "skip", "skip"],  # 16
                       ["False", "False", "False", "em", "no", "no", "no", "no", "no"],  # 17
                       ["False", "False", "False", "mn", "cannot", "cannot", "cannot", "can", "can"],  # 18
                       ["False", "False", "False", "hr", "no", "no", "no", "no", "no"],  # 19
                       ["False", "False", "False", "hrmn", "cannot", "cannot", "cannot", "can", "can"],  # 20
                       ["False", "False", "True", "em", "no", "no", "no", "no", "no"],  # 21
                       ["False", "False", "True", "mn", "cannot", "cannot", "cannot", "can", "can"],  # 22
                       ["False", "False", "True", "hr", "can", "can", "can", "skip", "skip"],  # 23
                       ["False", "False", "True", "hrmn", "can", "can", "can", "can", "can"],  # 24
                       ["False", "True", "False", "em", "no", "no", "no", "no", "no"],  # 25
                       ["False", "True", "False", "mn", "can", "can", "can", "can", "can"],  # 26
                       ["False", "True", "False", "hr", "no", "no", "no", "no", "no"],  # 27
                       ["False", "True", "False", "hrmn", "can", "can", "can", "can", "can"],  # 28
                       ["False", "True", "True", "em", "no", "no", "no", "no", "no"],  # 29
                       ["False", "True", "True", "mn", "can", "can", "can", "can", "can"],  # 30
                       ["False", "True", "True", "hr", "can", "can", "can", "skip", "skip"],  # 31
                       ["False", "True", "True", "hrmn", "can", "can", "can", "can", "can"]]  # 32

for i in range(1, len(main_matrix)):
    filename = "tc12180_"
    if main_matrix[i][0] == "True":
        filename = filename + "on_"
    else:
        filename = filename + "off_"

    if main_matrix[i][1] == "True":
        filename = filename + "on_"
    else:
        filename = filename + "off_"

    if main_matrix[i][2] == "True":
        filename = filename + "on_"
    else:
        filename = filename + "off_"

    filename = filename + main_matrix[i][3] + "_"
    for j in range(4, 9):
        if main_matrix[i][j] == "skip": 
            break
        f = filename
        n += 1
        nstr = ("00" + str(n))[-3:]
        f = nstr + f + main_matrix[0][j] + "_" + main_matrix[i][j] + ".py"
        print(f)
        shutil.copyfile(s,f)

