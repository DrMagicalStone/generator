import tensorflow as tf
import keras
from keras import layers, models

from TextInfo import TextInfo
from makeSample import makeSample
from preProcessLoss import cuttingLoss

input_layer = layers.Input(shape=(640, 360, 1), name="image_input", dtype="float32")
label = layers.Input(name="label", shape=(None,), dtype="float32")

convH = layers.Conv2D(64, (3, 3),
        activation="relu",
        kernel_initializer="he_normal",
        padding="same",
        name="convH",)(input_layer)
poolH = layers.MaxPooling2D((1, 4), name="poolH")(convH)
reshapeH = layers.Reshape(target_shape=(320, 90), name="reshapeH")(poolH)


convV = layers.Conv2D(64, (3, 3),
        activation="relu",
        kernel_initializer="he_normal",
        padding="same",
        name="convV",)(input_layer)
transpose = layers.Permute((2, 1))(convV)
poolV = layers.MaxPooling2D((1, 4), name="poolV")(transpose)
reshapeV = layers.Reshape(target_shape=(320, 90), name="reshapeH")(poolV)


concat = layers.Concatenate()(reshapeH, reshapeV)

dense1 = layers.Dense(64, activation="relu", name="dense")(concat)
reshapeO = layers.Reshape(target_shape=(8, 0), name="reshapeH")(dense1)
dense2 = layers.Dense(64, activation="relu", name="dense")(reshapeO)

loss = cuttingLoss

model = models.Model(inputs=[input_layer, label], outputs=dense2, name="ocr_preprocess_and_segmentation")

model.compile(loss=loss)

model.summary()