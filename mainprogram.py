# -*- coding: utf-8 -*-
"""MainProgram.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YlK6IEL7QGA9mlp6bn_sBf7TXeVhCOaF

Loading Libraries
"""

import tensorflow as tf
import keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from keras.datasets import fashion_mnist
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/content/gdrive')

"""Loading Dataset"""

#The website that helped me: https://towardsdatascience.com/a-simple-2d-cnn-for-mnist-digit-recognition-a998dbc1e79a
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
print(test_labels.shape)
train_labels = keras.utils.to_categorical(train_labels, 10)
train_images = train_images.reshape(train_images.shape[0], 28, 28, 1)

test_labels = keras.utils.to_categorical(test_labels, 10)
test_images = test_images.reshape(test_images.shape[0], 28, 28, 1)

"""Project: """

#Loading the pretrained model
 def load_NN(filename):
  new_model = load_model("/content/gdrive/MyDrive/" + filename)
  new_model.summary()
  eval = new_model.evaluate(test_images, test_labels, verbose = 1)
  print("The model has a loss of {} \nThe model is {}% accurate".format(eval[0], round(eval[1]*100)))
  return new_model

#Loading Camera (code provided by Google Collab, I added new functionalities such as image pre-processing)
from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode
import matplotlib.image as mpimg
import io
import cv2
import numpy as np
#import imutils
def take_photo(filename='photo.jpg', quality=0.8):
  js = Javascript('''
    async function takePhoto(quality) {
      const div = document.createElement('div');
      const capture = document.createElement('button');
      capture.textContent = 'Capture';
      div.appendChild(capture);

      const video = document.createElement('video');
      video.style.display = 'block';
      const stream = await navigator.mediaDevices.getUserMedia({video: true});

      document.body.appendChild(div);
      div.appendChild(video);
      video.srcObject = stream;
      await video.play();

      // Resize the output to fit the video element.
      google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

      // Wait for Capture to be clicked.
      await new Promise((resolve) => capture.onclick = resolve);

      const canvas = document.createElement('canvas');
      console.log(video.width, video.height);
      canvas.width = 550;
      canvas.height = 450;
      canvas.getContext('2d').drawImage(video, 0, 0);
      stream.getVideoTracks()[0].stop();
      div.remove();
      return canvas.toDataURL('image/jpeg', quality);
    }
    ''')
  display(js)
  data = eval_js('takePhoto({})'.format(quality))
  binary = b64decode(data.split(',')[1])
  image = io.BytesIO(binary)
  i = mpimg.imread(image, format='JPG')
  resized = cv2.resize(i, (28, 28))
  #resized = imutils.resize(i, width =28)
  gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
  gray = np.array(gray)
  fixed = []
  fixed_print = []
  for i in gray:
    current = []
    to_print = []
    for j in i:
      if j <= 150:
        current.append([5])
        to_print.append(5)
      else:
        current.append([j])
        to_print.append(j)
    fixed.append(current)
    fixed_print.append(to_print)
  plt.imshow(fixed_print, interpolation='nearest')
  plt.show()
  return fixed

#User Provided Data
def program():
  done = False
  while not done:
    print("TAKING PHOTO\n==========================================")
    resized = take_photo()
    photo = []
    #resized = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    #resized = resized[:, :, 0]
    photo.append(resized)
    photo = np.array(photo)
    photo.reshape(1, 28, 28, 1)
    print(photo.shape)
    p = model.predict(photo)
    print(p)
    results_index = list(p[0]).index(max(list(p[0])))
    final_answer = class_names[results_index]
    print(final_answer)
    changes = 0
    accurate = input("Is the result accurate? 1 = yes, anything else = no: ")
    if accurate ==  "1":
      print("Thank you")
    else:
      ask2train = input("Should the model be retrained? 1 = yes, anything else = no: ")
      if ask2train == "1":
        changes += 1
        num_epochs = int(input("epochs: "))
        num_data = int(input("number of data: "))
        model.fit(train_images[:num_data], train_labels[:num_data], epochs = num_epochs, validation_data = (test_images, test_labels), verbose = 1)
      else:
        print("ok...")
    askifdone = input("Take another photo? 1 = yes, anything else = no: ")
    print(askifdone)
    if askifdone != "1":
      if changes > 0:
        askifsavemodel = input("Should the model be saved? 1 = yes, anything else = no: ")
        if askifsavemodel == "1":
          saving_filename = input("New model name or directory: ")
          model.save("/content/gdrive/MyDrive/" + saving_filename)
      done = True
      print("Goodbye...")
    else:
      done = False

#Get examples from Dataset
def get_examples():
  repeated = 0
  counter_index = 0
  for i in class_names:
    print("{}: {}".format(counter_index, i))
    counter_index += 1
  search_for = input("What images are you looking for? ")
  total  = int(input("How many of these images do you want: "))
  if search_for in class_names:
    for i in range(len(test_images)):
      test = np.array([test_images[i]])
      prediction_answer = list(model.predict(test)[0])
      prediction_index = prediction_answer.index(max(prediction_answer))
      ans = class_names[prediction_index]
      if ans == search_for:
        image_show = test_images.reshape(10000, 28, 28)
        plt.imshow(image_show[i])
        plt.show()
        repeated += 1

      if repeated == total:
        break
    return None

#Main Program - Menu
def menu():
  exit = False
  while not exit:
    print("\tMenu\n ============================ \n1: Get Test Data Examples\n2: Test with Your Own Data \nAnything Else: Exit")
    choice = input("1,2, or anything else? ")
    if choice == "1":
      get_examples()
    elif choice == "2":
      program()
    else:
      print("Goodbye then...")
      break

#Runs Program
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

print("ImageRecognition/model/")
filename = input("Model filename/directory...")
print("LOADING MODEL\n==========================================")
model = load_NN(filename)
print("==========================================")
menu()