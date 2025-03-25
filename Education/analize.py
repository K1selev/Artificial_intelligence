
import tensorflow as tf 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from tensorflow.keras.utils import plot_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import TensorBoard
import os

# Загружаем модель без компиляции
model = tf.keras.models.load_model("dog_breed_mobilenetv2.keras", compile=False)
model.compile(optimizer=tf.keras.optimizers. Adam (learning_rate=1e-5),
              loss='categorical_crossentropy',
              metrics=['accuracy']
              )

# Выводим структуру модели
model.summary()
try:
    plot_model(model, to_file="model_structure.png", show_shapes=True, show_layer_names=True) 
except Exception as e:
    print(f"Ошибка при создании структуры модели: {e}")

# Вывод информации о слоях модели (аналог summarize_graph) 
print("\n=== Анализ слоёв модели ===")
for layer in model.layers:
    input_shape=getattr(layer, 'input_shape', 'N/A') # Проверяем наличие атрибута 
    output_shape=getattr(layer, 'output_shape', 'N/A')
    print (f"Cлoй: {layer.name}, Bxoд: {input_shape}, Bыxoд: {output_shape}")

# Подготовка данных
base_dir = "/Users/sergey/Desktop/Dogs/Images"
batch_size = 32 
img_height = 224
img_width= 224

# Указываем validation_split=0.2, как в тренировочном коде
val_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

val_generator = val_datagen.flow_from_directory(
    base_dir,
    target_size=(img_height, img_width), 
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False, # Не перемешивать
    subset="validation"# Используем только валидационные данные
)

# Логирование в TensorBoard
log_dir = "logs"
if not os.path.exists(log_dir): 
    os.makedirs(log_dir)

tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

# Включение трассировки графа
tf.summary.trace_on(graph=True)

# Оценка модели
loss, accuracy = model.evaluate(val_generator, callbacks=[tensorboard_callback]) 
print(f"Loss: {loss:.4f}, Accuracy: {accuracy:.4f}")

# Экспортирование трассировки графа в TensorBoard 
with tf.summary.create_file_writer(log_dir).as_default():
    tf.summary.trace_export(name="model_trace", step=0)

# Предсказания
val_predictions = model.predict(val_generator)
predicted_classes = np.argmax(val_predictions, axis=1) 
true_classes = val_generator.classes

# Проверка соответствия размеров
if len(val_predictions) != len(true_classes):
    print("x Ошибка: Количество предсказаний и реальных меток не совпадает!")

# Вывод Тор-5 предсказаний для случайного изображения из валидационного набора 
print("\n=== Топ-5 предсказаний для случайного изображения ===")
img_path, label = val_generator.filepaths[0], true_classes[0]
img = tf.keras.preprocessing.image.load_img(img_path, target_size=(img_height, img_width)) 
img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0 
img_array = np.expand_dims(img_array, axis=0) # Добавляем batch dim

predictions = model.predict(img_array)
top_5= np.argsort(predictions[0])[-5:][::-1] # Тoп-5 предсказаний
print (f"Истинный класс: {label}")
for i in top_5:
    class_name = list(val_generator.class_indices.keys())[i] 
    print(f"{class_name}: {predictions[0][i]:.4f}")

# Матрица ошибок
cm = confusion_matrix(true_classes, predicted_classes)
plt.figure(figsize=(12, 8))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Предсказанный класс")
plt.ylabel("Истинный класс")
plt.title("Матрица ошибок")
plt.show()

# Для запуска TensorBoard:
#В терминале выполнить команду: tensorboard --logdir=logs

