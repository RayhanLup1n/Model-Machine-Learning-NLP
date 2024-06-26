# -*- coding: utf-8 -*-
"""Rayhan Ananda_Proyek Pertama.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1euRnVTxZleKfspyTOP6TiFop3bu6sXBW

# Proyek Pertama: Membuat NLP dengan Tensorflow
- Nama: Rayhan Ananda Resky
- Email: rayhanananda2002@gmail.com
- Id Dicoding: rayhanananda
"""

import pandas as pd

df = pd.read_csv('/content/drive/MyDrive/tweets.csv')
df = df.drop(columns=(['id', 'location', 'keyword']))
df

df.info('all')
print(df.isna().sum())
print(df.duplicated().sum())

df = df.drop_duplicates()
print(df.duplicated().sum())

kelas = pd.get_dummies(df.target)
df = pd.concat([df, kelas],axis=1)
df = df.drop(columns='target')
df

teks = df['text'].values
label = df.drop(columns='text').values

print(label)
print(teks)

from sklearn.model_selection import train_test_split

teks_latih, teks_uji, label_latih, label_uji = train_test_split(teks, label, test_size=0.2)

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

tokenizer = Tokenizer(num_words=7000, oov_token='x')
tokenizer.fit_on_texts(teks_latih)
tokenizer.fit_on_texts(teks_uji)

sekuens_latih = tokenizer.texts_to_sequences(teks_latih)
sekuens_uji = tokenizer.texts_to_sequences(teks_uji)

padded_latih = pad_sequences(sekuens_latih)
padded_uji = pad_sequences(sekuens_uji)

import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=7000, output_dim=16),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(2, activation='sigmoid')])

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.summary()

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy') > 0.9 and logs.get('val_accuracy') >= 0.9 ):
      print("\nAkurasi telah mencapai >90%!")
      self.model.stop_training = True
callbacks = myCallback()

history = model.fit(padded_latih, label_latih, epochs=30,
                    batch_size=64, validation_data=(padded_uji, label_uji),
                    callbacks=[callbacks])

import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Akurasi Model')
plt.ylabel('Accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Loss Model')
plt.ylabel('Loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()