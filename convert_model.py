from tensorflow import keras

# Update these paths to your actual model files
old_lenet_path = "C:/Users/USER/Desktop/FYP/Cataract Detection/CataractDetection code/lenet5_cataract_model.keras"
old_mobilenet_path = "C:/Users/USER/Desktop/FYP/Cataract Detection/CataractDetection code/mobilenetv2_cataract_model.keras"

# New paths for the re-saved models
new_lenet_path = "C:/Users/USER/Desktop/FYP/Cataract Detection/CataractDetection code/lenet5_cataract_model_resaved.keras"
new_mobilenet_path = "C:/Users/USER/Desktop/FYP/Cataract Detection/CataractDetection code/mobilenetv2_cataract_model_resaved.keras"

# Load and re-save LeNet5
lenet_model = keras.models.load_model(old_lenet_path)
lenet_model.save(new_lenet_path)

# Load and re-save MobileNetV2
mobilenet_model = keras.models.load_model(old_mobilenet_path)
mobilenet_model.save(new_mobilenet_path)

print("Models re-saved successfully!") 