import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import TensorBoard
import os
# Указываем путь к данным (все данные находятся здесь) 
base_dir = "/Users/sergey/Desktop/Dogs/Images"
# Параметры 
batch_size = 32
img_height = 224
img_width = 224 
epochs = 10
learning_rate = 0.0001
# Создаем генератор с аугментацией и разбиением на валидацию 
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.5, 1.5], # Изменение яркости
    width_shift_range=0.2, # Горизонтальный сдвиг
    height_shift_range=0.2, # Вертикальный сдвиг
    rotation_range=30, # Вращение на ±30 градусов
    fill_mode='nearest',
    validation_split=0.2 # 20% данных пойдет на валидацию
)
# Создаем генераторы данных
train_generator = train_datagen.flow_from_directory(
    base_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset="training" # 80% данныx на тренировку
)


val_generator = train_datagen.flow_from_directory( 
    base_dir, # Используем тот же каталог 
    target_size=(img_height, img_width),
    batch_size=batch_size, 
    class_mode='categorical', 
    subset="validation" # 20% данных на валидацию
)

# Загружаем предобученную MobileNetV2 без верхних слоев
base_model = MobileNetV2 (weights='imagenet', include_top=False, input_shape=(img_height, img_width, 3)) 
base_model.trainable = False # Замораживаем веса

# Добавляем кастомные слои
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense (1024, activation='relu')(x)
predictions = Dense(train_generator.num_classes, activation='softmax')(x)

# Создаем и компилируем модель
model = Model(inputs=base_model.input, outputs=predictions)
model.compile(optimizer=Adam(learning_rate=learning_rate), loss='categorical_crossentropy', metrics=['accuracy'])

# Выводим структуру модели
model.summary()

# Логирование в TensorBoard
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs (log_dir)

tensorboard_callback = TensorBoard (log_dir=log_dir, histogram_freq=1)

# Обучаем модель
model.fit(
    train_generator,
    epochs=epochs,
    steps_per_epoch=train_generator.samples // batch_size,
    validation_data=val_generator,
    validation_steps=val_generator.samples // batch_size,
    callbacks = [tensorboard_callback] # Добавляем колбэк для TensorBoard
)


# Сохраняем модель
model.save('dog_breed_mobilenetv2.keras')

# Размораживаем верхние слои базовой модели для тонкой настройки
base_model.trainable = True
fine_tune_at = 100
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

# Компилируем для доводки
model.compile(optimizer=Adam(learning_rate=1e-5), loss='categorical_crossentropy', metrics=['accuracy'])

# Доводим модель
model.fit(
    train_generator, epochs=10,
    steps_per_epoch=train_generator.samples // batch_size,
    validation_data=val_generator,
    validation_steps=val_generator.samples // batch_size,
    callbacks = [tensorboard_callback] # Добавляем колбзк для TensoгBoard
)

# Сохраняем финальную модель
model.save('dog_breed_mobilenetv2_finetuned.keras')