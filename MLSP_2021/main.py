# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import tensorflow as tf
#import tflite_runtime.interpreter as tflite
from record import record_to_file
import librosa
import os
import numpy as np

path = os.path.dirname(os.path.realpath(__file__))

def trigger():
    record_to_file()
    print("salvo")
    x, sr = librosa.load('src/audio.wav', mono=True)

    interpreter = tf.lite.Interpreter(model_path='src/litemodel_ASR.tflite')
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.resize_tensor_input(input_details[0]["index"], x.shape)
    interpreter.allocate_tensors()
    interpreter.set_tensor(input_details[0]["index"], x)
    interpreter.set_tensor(
            input_details[1]["index"],
            np.array(0).astype('int32')
    )
    interpreter.set_tensor(
    input_details[2]["index"],
    np.zeros([1, 2, 1, 320]).astype('float32'))
    interpreter.invoke()
    hyp = interpreter.get_tensor(output_details[0]["index"])

    texto = "".join([chr(u) for u in hyp])
    print(texto)
    return texto