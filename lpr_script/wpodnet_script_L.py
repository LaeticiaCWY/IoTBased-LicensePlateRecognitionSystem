import cv2
import numpy as np
import matplotlib.pyplot as plt
from local_utils import detect_lp
from os.path import splitext, basename
from keras.models import model_from_json
import glob
import time
from paddleocr import PaddleOCR

start_time = time.time()
def load_model(path):
    try:
        path = splitext(path)[0]
        with open('%s.json' % path, 'r') as json_file:
            model_json = json_file.read()
        model = model_from_json(model_json, custom_objects={})
        model.load_weights('%s.h5' % path)
        print("Loading model successfully...")
        return model
    except Exception as e:
        print(e)
wpod_net_path = "wpod-net.json"
wpod_net = load_model(wpod_net_path)

def preprocess_image(image_path,resize=False):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255
    if resize:
        img = cv2.resize(img, (224,224))
    return img
# Create a list of image paths 
image_paths = glob.glob("Plate_example/*.jpg")
print("Found %i images..."%(len(image_paths)))


# forward image through model and return plate's image and coordinates
# if error "No Licensese plate is founded!" pop up, try to adjust Dmin
def get_plate(image_path, Dmax=608, Dmin=300):
    vehicle = preprocess_image(image_path)
    ratio = float(max(vehicle.shape[:2])) / min(vehicle.shape[:2])
    side = int(ratio * Dmin)
    bound_dim = min(side, Dmax)
    _ , LpImg, _, cor = detect_lp(wpod_net, vehicle, bound_dim, lp_threshold=0.5)
    return LpImg, cor

# Obtain plate image and its coordinates from an image
test_image = image_paths[0]


LpImg, cor = get_plate(test_image)


print("Detect %i plate(s) in" % len(LpImg), splitext(basename(test_image))[0])
print("Coordinate of plate(s) in image: \n", cor)



def draw_box(image_path, cor, thickness=3): 
    pts=[]  
    x_coordinates=cor[0][0]
    y_coordinates=cor[0][1]
    # store the top-left, top-right, bottom-left, bottom-right 
    # of the plate license respectively
    for i in range(4):
        pts.append([int(x_coordinates[i]),int(y_coordinates[i])])
    
    pts = np.array(pts, np.int32)
    pts = pts.reshape((-1,1,2))
    vehicle_image = preprocess_image(image_path)
    
    cv2.polylines(vehicle_image,[pts],True,(0,255,0),thickness)
    return vehicle_image


# Save the detected license plate image
license_plate_image_path = r'C:\Users\Laeticia\Vehicle-Detection\sample_license_plate.jpg'
plt.figure(figsize=(5, 5))
plt.axis(False)


plt.imshow(LpImg[0])
# plt.title("Detected License Plate")
end_time = time.time()
elapsed_time = end_time - start_time
print("Time taken to process image: %.4f seconds" % elapsed_time)
plt.tight_layout(True)
plt.savefig(license_plate_image_path)
plt.show()


from paddleocr import PaddleOCR,draw_ocr
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(use_angle_cls=True, lang='en',show_log = False) # need to run only once to download and load model into memory
result = ocr.ocr(license_plate_image_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)
