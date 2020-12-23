import os

from app import app

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import decode_predictions
from tensorflow.keras.applications.vgg16 import VGG16

def getModel():
    #From scratch 10G
    model = load_model("models/scratch_224_224_10G")

    #Ajouter choix pour les autres models.

    return model


def getPrediction(filename,model):

    img = load_img(os.path.join(app.config['UPLOAD_FOLDER'],filename), target_size=(224,224))
    img = img_to_array(img)
    img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2]))
    y = model.predict(img)
    return str(y[0][0])