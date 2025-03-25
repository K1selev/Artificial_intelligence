import tensorflow as tf 
import os

# Загружаем модель
model = tf.keras.models.load_model('dog_breed_mobilenetv2.keras')

# Конвертируем модель в TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model (model)

# Применяем квантование
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Получаем квантованную модель 
tflite_model = converter.convert()

# Сохраняем модель в формате .tflite
with open('optimized_model_quantized.tflite', 'wb') as f:
    f.write(tflite_model)

# Сохраняем модель в формате .keras (не SavedModel)
keras_model_path = 'dog_breed_mobilenetv2_optimized.keras'
model.save(keras_model_path)

# Если нужно сохранить только оптимизированную модель в SavedModel формате 
saved_model_dir = '/Users/sergey/Desktop/II/saved_model'

# Убедитесь, что директория существует. Если нет, создайте её: 
if not os.path.exists(saved_model_dir):
    os.makedirs(saved_model_dir)

# Сохраняем модель в SavedModel 
model.save(saved_model_dir)

# Используем tf.compat.v1 для удаления узлов тренировки 
saved_model_path = saved_model_dir

# Загружаем граф
graph = tf.compat.v1.get_default_graph()

# Удаляем неиспользуемые узлы
output_graph = tf.compat.v1.graph_util.remove_training_nodes(graph.as_graph_def())


# Сохраняем результат
with tf.io.gfile.GFile('optimized_model.pb', 'wb') as f:
    f.write(output_graph.SerializeToString())