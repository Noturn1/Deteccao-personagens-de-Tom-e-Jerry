import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import json
import matplotlib.pyplot as plt

# Obtem o caminho do arquivo de configurações
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config.json'))

# Carrega as configs do projeto
with open(config_path) as config_file:
    config = json.load(config_file)

train_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
img_height, img_width = config["img_size"]
batch_size = 32

# carrega imagens e rótulos
def carregar_imagens_e_rotulos(diretorio):
    imagens = []
    rotulos = []
    classes = os.listdir(diretorio)
    class_indices = {classe: idx for idx, classe in enumerate(classes)}
    for classe in classes:
        caminho_classe = os.path.join(diretorio, classe)
        if os.path.isdir(caminho_classe):
            for nome_arquivo in os.listdir(caminho_classe):
                caminho_imagem = os.path.join(caminho_classe, nome_arquivo)
                if os.path.isfile(caminho_imagem):
                    img = load_img(caminho_imagem, target_size=(img_height, img_width))
                    img_array = img_to_array(img)
                    imagens.append(img_array)
                    rotulos.append(class_indices[classe])
    return np.array(imagens), np.array(rotulos)

# Carrega imagens e rótulos
imagens, rotulos = carregar_imagens_e_rotulos(train_data_dir)

# Verifica os rótulos
num_classes = len(np.unique(rotulos))
print(f"Número de classes: {num_classes}")
print(f"Rótulos únicos: {np.unique(rotulos)}")

# Ajusta os rótulos para garantir que estão no intervalo correto
rotulos = np.where(rotulos == 4, 1, rotulos) 

# Dividi os dados em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(imagens, rotulos, test_size=0.2, random_state=42)

# Codifica os rótulos como categorias
y_train = to_categorical(y_train, num_classes=num_classes)
y_test = to_categorical(y_test, num_classes=num_classes)

train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow(X_train, y_train, batch_size=batch_size)
validation_generator = test_datagen.flow(X_test, y_test, batch_size=batch_size)

# Cria o modelo com taxa de aprendizagem ajustável
def criar_modelo(learning_rate=0.001):
    model = Sequential([
        Conv2D(16, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dropout(0.5),
        Dense(128, activation='relu'),
        Dense(num_classes, activation='softmax'),  # Número de classes
        
    ])
    
    # Configura o otimizador com a taxa de aprendizagem
    optimizer = Adam(learning_rate=learning_rate)
    
    # Compila o modelo
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()
    return model

# Treina o modelo
modelo = criar_modelo(learning_rate=0.001)
history = modelo.fit(
    train_generator,
    epochs=10,
    validation_data=validation_generator
)

# Salvan o modelo treinado
modelo.save('teste4.h5')

# Plota a precisão e a perda
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(len(acc))

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Acurácia de Treinamento')
plt.plot(epochs_range, val_acc, label='Acurácia de Validação')
plt.legend(loc='lower right')
plt.title('Acurácia de Treinamento e Validação')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Perda de Treinamento')
plt.plot(epochs_range, val_loss, label='Perda de Validação')
plt.legend(loc='upper right')
plt.title('Perda de Treinamento e Validação')
plt.show()
