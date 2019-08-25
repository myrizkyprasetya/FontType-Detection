from flask import render_template,request
from flask import Flask
import cv2
import imutils
from imutils import contours
import pytesseract
from imageio import imread
from flask import json

import base64
import numpy as np
import re
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './font'

@app.route('/')
def mainPage():
    return render_template('index2.html')


@app.route('/process_image',methods = ['GET', 'POST'])
def processImage():
    font_arial = [{"font": "arial_l_a.jpg", "value": "a"}, {"font": "arial_l_b.jpg", "value": "b"},
                  {"font": "arial_l_c.jpg", "value": "c"}, {"font": "arial_l_d.jpg", "value": "d"},
                  {"font": "arial_l_e.jpg", "value": "e"}, {"font": "arial_l_f.jpg", "value": "f"},
                  {"font": "arial_l_g.jpg", "value": "g"}, {"font": "arial_l_h.jpg", "value": "h"},
                  {"font": "arial_l_i.jpg", "value": "i"}, {"font": "arial_l_j.jpg", "value": "j"},
                  {"font": "arial_l_k.jpg", "value": "k"}, {"font": "arial_l_l.jpg", "value": "l"},
                  {"font": "arial_l_m.jpg", "value": "m"}, {"font": "arial_l_n.jpg", "value": "n"},
                  {"font": "arial_l_o.jpg", "value": "o"}, {"font": "arial_l_p.jpg", "value": "p"},
                  {"font": "arial_l_q.jpg", "value": "q"}, {"font": "arial_l_r.jpg", "value": "r"},
                  {"font": "arial_l_s.jpg", "value": "s"}, {"font": "arial_l_t.jpg", "value": "t"},
                  {"font": "arial_l_u.jpg", "value": "u"}, {"font": "arial_l_v.jpg", "value": "v"},
                  {"font": "arial_l_w.jpg", "value": "w"}, {"font": "arial_l_x.jpg", "value": "x"},
                  {"font": "arial_l_y.jpg", "value": "y"}, {"font": "arial_l_z.jpg", "value": "z"},
                  {"font": "arial_u_A.jpg", "value": "A"}, {"font": "arial_u_B.jpg", "value": "B"},
                  {"font": "arial_u_C.jpg", "value": "C"}, {"font": "arial_u_D.jpg", "value": "D"},
                  {"font": "arial_u_E.jpg", "value": "E"}, {"font": "arial_u_F.jpg", "value": "F"},
                  {"font": "arial_u_G.jpg", "value": "G"}, {"font": "arial_u_H.jpg", "value": "H"},
                  {"font": "arial_u_I.jpg", "value": "I"}, {"font": "arial_u_J.jpg", "value": "J"},
                  {"font": "arial_u_K.jpg", "value": "K"}, {"font": "arial_u_L.jpg", "value": "L"},
                  {"font": "arial_u_M.jpg", "value": "M"}, {"font": "arial_u_N.jpg", "value": "N"},
                  {"font": "arial_u_O.jpg", "value": "O"}, {"font": "arial_u_P.jpg", "value": "P"},
                  {"font": "arial_u_Q.jpg", "value": "Q"}, {"font": "arial_u_R.jpg", "value": "R"},
                  {"font": "arial_u_S.jpg", "value": "S"}, {"font": "arial_u_T.jpg", "value": "T"},
                  {"font": "arial_u_U.jpg", "value": "U"}, {"font": "arial_u_V.jpg", "value": "V"},
                  {"font": "arial_u_W.jpg", "value": "W"}, {"font": "arial_u_X.jpg", "value": "X"},
                  {"font": "arial_u_Y.jpg", "value": "Y"}, {"font": "arial_u_Z.jpg", "value": "Z"}
                  ]

    font_calibri = [{"font": "calibri_l_a.jpg", "value": "a"}, {"font": "calibri_l_b.jpg", "value": "b"},
                    {"font": "calibri_l_c.jpg", "value": "c"}, {"font": "calibri_l_d.jpg", "value": "d"},
                    {"font": "calibri_l_e.jpg", "value": "e"}, {"font": "calibri_l_f.jpg", "value": "f"},
                    {"font": "calibri_l_g.jpg", "value": "g"}, {"font": "calibri_l_h.jpg", "value": "h"},
                    {"font": "calibri_l_i.jpg", "value": "i"}, {"font": "calibri_l_j.jpg", "value": "j"},
                    {"font": "calibri_l_k.jpg", "value": "k"}, {"font": "calibri_l_l.jpg", "value": "l"},
                    {"font": "calibri_l_m.jpg", "value": "m"}, {"font": "calibri_l_n.jpg", "value": "n"},
                    {"font": "calibri_l_o.jpg", "value": "o"}, {"font": "calibri_l_p.jpg", "value": "p"},
                    {"font": "calibri_l_q.jpg", "value": "q"}, {"font": "calibri_l_r.jpg", "value": "r"},
                    {"font": "calibri_l_s.jpg", "value": "s"}, {"font": "calibri_l_t.jpg", "value": "t"},
                    {"font": "calibri_l_u.jpg", "value": "u"}, {"font": "calibri_l_v.jpg", "value": "v"},
                    {"font": "calibri_l_w.jpg", "value": "w"}, {"font": "calibri_l_x.jpg", "value": "x"},
                    {"font": "calibri_l_y.jpg", "value": "y"}, {"font": "calibri_l_z.jpg", "value": "z"},
                    {"font": "calibri_u_A.jpg", "value": "A"}, {"font": "calibri_u_B.jpg", "value": "B"},
                    {"font": "calibri_u_C.jpg", "value": "C"}, {"font": "calibri_u_D.jpg", "value": "D"},
                    {"font": "calibri_u_E.jpg", "value": "E"}, {"font": "calibri_u_F.jpg", "value": "F"},
                    {"font": "calibri_u_G.jpg", "value": "G"}, {"font": "calibri_u_H.jpg", "value": "H"},
                    {"font": "calibri_u_I.jpg", "value": "I"}, {"font": "calibri_u_J.jpg", "value": "J"},
                    {"font": "calibri_u_K.jpg", "value": "K"}, {"font": "calibri_u_L.jpg", "value": "L"},
                    {"font": "calibri_u_M.jpg", "value": "M"}, {"font": "calibri_u_N.jpg", "value": "N"},
                    {"font": "calibri_u_O.jpg", "value": "O"}, {"font": "calibri_u_P.jpg", "value": "P"},
                    {"font": "calibri_u_Q.jpg", "value": "Q"}, {"font": "calibri_u_R.jpg", "value": "R"},
                    {"font": "calibri_u_S.jpg", "value": "S"}, {"font": "calibri_u_T.jpg", "value": "T"},
                    {"font": "calibri_u_U.jpg", "value": "U"}, {"font": "calibri_u_V.jpg", "value": "V"},
                    {"font": "calibri_u_W.jpg", "value": "W"}, {"font": "calibri_u_X.jpg", "value": "X"},
                    {"font": "calibri_u_Y.jpg", "value": "Y"}, {"font": "calibri_u_Z.jpg", "value": "Z"}
                    ]

    font_times = [{"font": "times_l_a.jpg", "value": "a"}, {"font": "times_l_b.jpg", "value": "b"},
                  {"font": "times_l_c.jpg", "value": "c"}, {"font": "times_l_d.jpg", "value": "d"},
                  {"font": "times_l_e.jpg", "value": "e"}, {"font": "times_l_f.jpg", "value": "f"},
                  {"font": "times_l_g.jpg", "value": "g"}, {"font": "times_l_h.jpg", "value": "h"},
                  {"font": "times_l_i.jpg", "value": "i"}, {"font": "times_l_j.jpg", "value": "j"},
                  {"font": "times_l_k.jpg", "value": "k"}, {"font": "times_l_l.jpg", "value": "l"},
                  {"font": "times_l_m.jpg", "value": "m"}, {"font": "times_l_n.jpg", "value": "n"},
                  {"font": "times_l_o.jpg", "value": "o"}, {"font": "times_l_p.jpg", "value": "p"},
                  {"font": "times_l_q.jpg", "value": "q"}, {"font": "times_l_r.jpg", "value": "r"},
                  {"font": "times_l_s.jpg", "value": "s"}, {"font": "times_l_t.jpg", "value": "t"},
                  {"font": "times_l_u.jpg", "value": "u"}, {"font": "times_l_v.jpg", "value": "v"},
                  {"font": "times_l_w.jpg", "value": "w"}, {"font": "times_l_x.jpg", "value": "x"},
                  {"font": "times_l_y.jpg", "value": "y"}, {"font": "times_l_z.jpg", "value": "z"},
                  {"font": "times_u_A.jpg", "value": "A"}, {"font": "times_u_B.jpg", "value": "B"},
                  {"font": "times_u_C.jpg", "value": "C"}, {"font": "times_u_D.jpg", "value": "D"},
                  {"font": "times_u_E.jpg", "value": "E"}, {"font": "times_u_F.jpg", "value": "F"},
                  {"font": "times_u_G.jpg", "value": "G"}, {"font": "times_u_H.jpg", "value": "H"},
                  {"font": "times_u_I.jpg", "value": "I"}, {"font": "times_u_J.jpg", "value": "J"},
                  {"font": "times_u_K.jpg", "value": "K"}, {"font": "times_u_L.jpg", "value": "L"},
                  {"font": "times_u_M.jpg", "value": "M"}, {"font": "times_u_N.jpg", "value": "N"},
                  {"font": "times_u_O.jpg", "value": "O"}, {"font": "times_u_P.jpg", "value": "P"},
                  {"font": "times_u_Q.jpg", "value": "Q"}, {"font": "times_u_R.jpg", "value": "R"},
                  {"font": "times_u_S.jpg", "value": "S"}, {"font": "times_u_T.jpg", "value": "T"},
                  {"font": "times_u_U.jpg", "value": "U"}, {"font": "times_u_V.jpg", "value": "V"},
                  {"font": "times_u_W.jpg", "value": "W"}, {"font": "times_u_X.jpg", "value": "X"},
                  {"font": "times_u_Y.jpg", "value": "Y"}, {"font": "times_u_Z.jpg", "value": "Z"}
                  ]
    arial = []
    calibri = []
    times = []

    image_data = re.sub('^data:image/.+;base64,', '', request.form['data'])
    # print(image_data)
    im = imread(BytesIO(base64.b64decode(image_data)))
    im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    # cv2.imshow("s",im)
    # cv2.waitKey(0)
    ref = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ref = cv2.threshold(ref, 10, 255, cv2.THRESH_BINARY_INV)[1]
    im = np.asarray(im)
    text = pytesseract.image_to_string(cv2.cvtColor(np.array(im), cv2.COLOR_BGR2RGB))
    print(text)
    data_str = text.replace(" ", "")

    to_compare = list(data_str)
    fontArial = [d for d in font_arial if d['value'] in data_str]
    fontCalibri = [d for d in font_calibri if d['value'] in data_str]
    fontTimes = [d for d in font_times if d['value'] in data_str]

    # ada=0
    # SEGMENTASI & NORMALISASI

    # proses menandai
    refCnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    refCnts = refCnts[0] if imutils.is_cv2() else refCnts[1]
    refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]
    digits = {}

    for (i, c) in enumerate(refCnts):

        (x, y, w, h) = cv2.boundingRect(c)
        roi = im[y:y + h, x:x + w]
        roi = cv2.resize(roi, (140, 200))
        # cv2.imshow("a",roi)
        # cv2.waitKey(0)
        digits[i] = roi
        # nf = "D:\KULIAH\SKRIPSI\Alhamdulillah\Tmplt\ial2" + str(ada) + ".jpg"
        # cv2.imwrite(nf, roi)
        # cv2.imshow("gambar",roi)
        # cv2.waitKey(0)

        scores = []
        groupOutput = []

        # PROSES TEMPLATE MATCHING
        # ar_arial = []
        # dict_arial = {}
        for i in fontArial:
            path = "Arial_new/"
            ori = cv2.imread(path + i['font'])
            res = cv2.matchTemplate(roi, ori, cv2.TM_CCOEFF_NORMED)
            (_, score, _, _) = cv2.minMaxLoc(res)
            scores.append(score)
            # scores_arial.append(score)
            # dict_arial[i['value']] = score
            # ar_arial.append(score)
            print("Arial", score)
        # arial.append(dict_arial)
        # print(dict_arial)
        # print(ar_arial)

        # ar_calibri = []
        # dict_calibri = {}
        for i in fontCalibri:
            path = "Calibri_new/"
            ori = cv2.imread(path + i['font'])
            res = cv2.matchTemplate(roi, ori, cv2.TM_CCOEFF_NORMED)
            (_, score, _, _) = cv2.minMaxLoc(res)
            scores.append(score)
            # scores_calibri.append(score)
            # dict_calibri[i['value']] = score
            # ar_calibri.append(score)
            print("Calibri", score)
        # calibri.append(dict_calibri)
        # print(dict_calibri)

        # ar_times=[]
        # dict_times={}
        for i in fontTimes:
            path = "Times_new/"
            ori = cv2.imread(path + i['font'])
            res = cv2.matchTemplate(roi, ori, cv2.TM_CCOEFF_NORMED)
            (_, score, _, _) = cv2.minMaxLoc(res)
            scores.append(score)
            # scores_times.append(score)
            # dict_times[i['value']] = score
            # ar_times.append(score)
            print("Times", score)
        # print(dict_times)

        print(scores)
        groupOutput.append(np.argmax(scores))
        print(groupOutput)
        for g in groupOutput:
            if g >= 16 and 23:
                times.append("1")
                print("-------Times")

            elif g >= 8 and 15:
                calibri.append("1")
                print("-------Calibri")

            else:
                arial.append("1")
                print("-------Arial")

     #   k_arial = int(len(arial) / len(digits) * 100)
      #  k_calibri = int(len(calibri) / len(digits) * 100)
     #   k_times = int(len(times) / len(digits) * 100)
      #  print(k_arial)
      #  print(k_calibri)
      #  print(k_times)

    points_data = [{"arial_percent": int(len(arial) / len(digits) * 100)},
                    {"calibri_percent":int(len(calibri) / len(digits) * 100)},
                    {"times_percent": int(len(times) / len(digits) * 100)},
                    {"TextImage": text}
                    ]

    return json.dumps(points_data)


if __name__ == '__main__':
    app.run()