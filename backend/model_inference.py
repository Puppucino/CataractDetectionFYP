import sys
import io
import os
from dotenv import load_dotenv
load_dotenv()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

img_path = sys.argv[1] if len(sys.argv) > 1 else None
lenet5_model_path = os.getenv("LENET_MODEL_PATH") if not (len(sys.argv) > 2) else sys.argv[2]
mobilenetv2_model_path = os.getenv("MOBILENET_MODEL_PATH") if not (len(sys.argv) > 3) else sys.argv[3]

# Load models
lenet5_model = load_model(lenet5_model_path)
mobilenetv2_model = load_model(mobilenetv2_model_path)

# Preprocess for LeNet5 (128x128, grayscale)
img_lenet = image.load_img(img_path, target_size=(128, 128), color_mode='grayscale')
x_lenet = image.img_to_array(img_lenet)
x_lenet = np.expand_dims(x_lenet, axis=0)
x_lenet = x_lenet / 255.0

# Preprocess for MobileNetV2 (128x128, RGB)
img_mobilenet = image.load_img(img_path, target_size=(128, 128), color_mode='rgb')
x_mobilenet = image.img_to_array(img_mobilenet)
x_mobilenet = np.expand_dims(x_mobilenet, axis=0)
x_mobilenet = x_mobilenet / 255.0

# Predict probabilities
p1 = lenet5_model.predict(x_lenet, verbose=0)[0][0]
p2 = mobilenetv2_model.predict(x_mobilenet, verbose=0)[0][0]
p_ensemble = (p1 + p2) / 2

# Ensemble result
threshold = 0.5
result = "Cataract" if p_ensemble >= threshold else "Healthy"

# Print only the ensemble result and confidence
print(f"{result} (confidence: {p_ensemble:.2f})") 