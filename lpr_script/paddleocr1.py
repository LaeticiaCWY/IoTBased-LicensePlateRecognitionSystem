from paddleocr import PaddleOCR

# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.
# https://pypi.org/project/paddleocr/
#
# supress anoysing logging messages parameter show_log = False
# https://github.com/PaddlePaddle/PaddleOCR/issues/2348
ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log = False) # need to run only once to download and load model into memory
img_path = 'doc/imgs_words_en/malaysian_car_plate.png'
result = ocr.ocr(img_path, det=False, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)