import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox 
import cv2
import numpy as np
import threading
import time
import torch
from PIL import Image, ImageTk

try:
    from ultralytics import YOLO
except ImportError:
    messagebox.showerror(
        "Ошибка",
        "Не удалось импортировать ultralytics. \пУстановите:\n\npip install ultralytics"
    )
    raise SystemExit

# Определяем устройство для работы с моделью
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("Используем устройство:", DEVICE)

# Определяем фильтр ресемплинга
RESAMPLE_FILTER = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.ANTIALIAS
# Пути к моделям
MODEL_FILES = {
    "YOLO11n-seg": "models/yolo11n-seg.pt",
    "YOLO11s-seg": "models/yolo11s-seg.pt",
    "YOLO11m-seg": "models/yolo11m-seg.pt",
    "YOLO11l-seg": "models/yolo11l-seg.pt", 
    "YOLO11x-seg": "models/yolo11x-seg.pt",
}

model_cache = {}


def preload_all_models():
    for model_name, weight_path in MODEL_FILES.items(): 
        print(f"Пpoбуждаем нодель {model_name}: {weight_path}")
        model = YOLO(weight_path) 
        model.to(DEVICE)
        model_cache[model_name] = model


def get_model_by_name(model_name):
    if model_name not in MODEL_FILES:
        raise ValueError(f"неизвестная нодель: {model_name}")
    
    if model_name not in model_cache:
        model_cache[model_name] = YOLO (MODEL_FILES[model_name]).to(DEVICE)

    return model_cache[model_name]

CLASS_NAMES = ["car", "person", "elephant"]
CLASS_COLORS = {
    "person": (255, 0, 0),
    "car": (0, 255, 0),
    "elephant": (0, 0, 255),
}

def get_class_indexes (yolo_model):
    indexes = []
    for cname in CLASS_NAMES:
        found = None
        for idx, name in yolo_model.names.items():
            if name.lower() == cname.lower():
                found = idx
                break
        if found is not None:
            indexes.append(found)
        else:
            print(f"ВНИМАНИЕ: класс '{cname}' не найден в модели!")
    return indexes

def segment_image(image_path, yolo_model):
    class_idxs = get_class_indexes(yolo_model)
    if not class_idxs:
        raise ValueError("Не найдены индексы классов (аirplane / car) в модели!")
    
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"He удалось открыть: {image_path}")
    
    results = yolo_model.predict(image, classes=class_idxs, device=DEVICE, verbose=False)
    
    for result in results:
        boxes = result.boxes
        masks = result.masks
        if not masks or not masks.xy:
            continue

        for box, poly in zip(boxes, masks.xy):
            cls_idx= int(box.cls[0].item()) if box.cls.numel() > 0 else -1 
            cls_name = yolo_model.names.get(cls_idx, None)
            if cls_name is None:
                continue
            color = CLASS_COLORS.get(cls_name.lower(), (255, 255, 255)) 
            poly_pts= np.array(poly, dtype=np.int32).reshape((-1, 1, 2))
            cv2.polylines(image, [poly_pts], True, color, 2)


            confidence = box.conf[0].item() if box.conf.numel() > 0 else 0.0
            text = f"{cls_name}: {confidence:.2%}"
            x, y = int(box.xyxy[0][0]), int(box.xyxy[0][1])
            font_scale = 0.7
            font_thickness = 2

            text_size, baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness) 
            text_x1, text_y1 = x, y - text_size[1] - 5
            text_x2, text_y2 = x + text_size[0] + 5, y

            cv2.rectangle(image, (text_x1, text_y1), (text_x2, text_y2), (0, 0, 0), cv2.FILLED) 
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, font_thickness, cv2.LINE_AA)

    return image

def segment_video (video_path, output_path, yolo_model, skip_frames=1, progress_var=None, progress_bar=None):
    cap = cv2.VideoCapture (video_path)
    if not cap.isOpened():
        raise ValueError(f"Hе удалось открыть видео: {video_path}")
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_in = cap.get(cv2.CAP_PROP_FPS)
    total_frames= int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if skip_frames < 1: 
        skip_frames=1
        
    fps_out = max(fps_in / skip_frames, 1)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter (output_path, fourcc, fps_out, (width, height))
    
    class_idxs = get_class_indexes(yolo_model)
    frame_idx = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % skip_frames == 0:
            results = yolo_model.predict(frame, classes=class_idxs, device=DEVICE, verbose=False)
            for result in results:
                boxes = result.boxes
                masks = result.masks
                
                if masks is None or not hasattr(masks, 'xy'):
                    continue
                
                for box, poly in zip (boxes, masks.xy):
                    cls_idx= int(box.cls[0].item()) if box.cls.numel() > 0 else -1 
                    cls_name = yolo_model.names.get(cls_idx, None)

                    if cls_name is None:
                        continue

                    color = CLASS_COLORS.get(cls_name.lower(), (255, 255, 255)) 
                    poly_pts= np.array (poly, dtype=np.int32).reshape((-1, 1, 2))

                    cv2.polylines(frame, [poly_pts], True, color, 2)
                    
                    confidence = box.conf[0].item() if box.conf.numel() > 0 else 0.0 
                    text = f"{cls_name}: {confidence: .2%}"
                    x, y = int(box.xyxy[0][0]), int(box.xyxy[0][1])
                    
                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)
                    
            out.write(frame)

        if progress_var is not None and progress_bar is not None and total_frames > 0:
            current_progress = int((frame_idx / total_frames) * 100)
            progress_var.set(current_progress)
            progress_bar.update()
            
        frame_idx += 1
    
    cap.release()
    out.release()
    
    if progress_var is not None and progress_bar is not None:
        progress_var.set(100)
        progress_bar.update()

# Функция для воспроизведения видео 
def play_video (video_path):
    cap = cv2.VideoCapture (video_path)
    if not cap.isOpened():
        messagebox.showerror("Oшибкa", f"Hе удалось открыть для роигрывания: {video_path}")
        return

    cv2.namedWindow("Video Playback", cv2.WINDOW_NORMAL)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Video Playback", frame)
        if cv2.waitKey(30) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


# Функция для обработки изображений
def open_image():
    ftypes = [("Изображения", "*.jpg *.png *.jpeg *.bmp *.tiff"), ("Все файлы", "*.*")] 
    path = filedialog.askopenfilename(title="Выберите изображение", filetypes=ftypes) 
    if not path:
        return
    
    selected_model = model_var.get()
    try:
        yolo_model = get_model_by_name(selected_model)
    except Exception as e:
        messagebox.showerror("Ouибка модели", str(e))
        return
    
    try:
        processed = segment_image(path, yolo_model)
        processed_rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray (processed_rgb)
        w_orig, h_orig = pil_img.size
        new_w= min(w_orig, 800)
        new_h = int(h_orig * (new_w / w_orig))
        pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        tk_img = ImageTk.PhotoImage (pil_img)
        res_win = tk.Toplevel(root)
        res_win.title("Результат сегментации")
        res_win.geometry (f"{new_w + 20}x{new_h + 20}")
        res_win.configure (bg="#f8f8f8")

        lbl = tk. Label(res_win, image=tk_img, bg="#f8f8f8") 
        lbl.image = tk_img
        lbl.pack(expand=True, fill=tk.BOTH)
    except Exception as e:
        messagebox.showerror("Ouибка обработки изображения", str(e))


# Функция для обработки видео
def open_video():
    ftypes = [("Bидеo", "*.mp4 *.avi *.mov *.mkv"), ("Bсе файлы", "*.*")] 
    vid_path = filedialog.askopenfilename (title="Выберите видеo", filetypes=ftypes)
    if not vid_path:
        return
    skip_str = skip_frames_entry.get()
    try:
        skip_val = int(skip_str)
        if skip_val < 1:
            skip_val = 1
    except:
        skip_val = 1

    selected_model = model_var.get()
    try:
        yolo_model = get_model_by_name(selected_model)
    except Exception as e:
        messagebox.showerror ("Owибка модели", str(e))
        return
    
    base, ext = os.path.splitext(vid_path) 
    out_path = base + "_segmented.mp4"
    
    def process_thread():
        try:
            segment_video(
                vid_path,
                out_path,
                yolo_model,
                skip_frames=skip_val,
                progress_var=progress_var,
                progress_bar=progress_bar,
            )
            time.sleep(0.5) 
            play_video(out_path)
        except Exception as e:
            messagebox.showerror("Oшибка обработки видео", stг(e))
        finally:
            progress_var.set(0)
            progress_bar.update()


    threading.Thread(target=process_thread, daemon=True).start()
preload_all_models()

root = tk.Tk()
root.title(f"Сегментачия YOLO - Устройство: {DEVICE}")
root.geometry("680x420")
root.config(bg="#f8f8f8")
# Заголовок
title_label = tk. Label(
    root,
    text="Сегментация объектов (YOLO-Seg)",
    font=("Arial", 17, "bold"),
    bg="#f8f8f8",
    fg="#333333",
)
title_label.pack(pady=5)

# Метка устройства
device_label = tk. Label(
    root,
    text=f"Устройство: {DEVICE}",
    font=("Arial", 10), 
    bg="#f8f8f8",
    fg="#666666",
)
device_label.pack()

# Описание
desc_label = tk.Label(
    root, 
    text=(
        "1) Выберите модель из списка.\n"
        "2) Нажмите \"Обработать изображение\" или \"Обработать видео\".\n"
        "3) skip_frames > 1 => берëм каждый No-й кадр, при этом fps_out = fps_in / N.\n" 
        "Общее время воспроизведения остаётся прежним."
    ),
    font=("Arial", 10),
    bg="#f8f8f8",
    fg="#666666",
)
desc_label.pack(pady=(0, 10))
# Выбор модели
model_frame = tk. Frame (root, bg="#f8f8f8")
model_frame.pack(pady=5)

tk.Label(
    model_frame,
    text="Модель:",
    bg="#f8f8f8",
    fg="#333333",
).pack(side=tk.LEFT)

model_var = tk.StringVar()
model_combobox = ttk.Combobox(
    model_frame,
    textvariable=model_var,
    state="readonly",
    values=list(MODEL_FILES.keys()),
    width=18,
)
model_combobox.pack(side=tk. LEFT, padx=5)
model_combobox.current(0)

# Кнопки обработки
buttons_frame = tk.Frame(root, bg="#f8f8f8") 
buttons_frame.pack(pady=10)

img_button = tk.Button(
    buttons_frame,
    text="Обработать изображение",
    font=("Arial", 12),
    bg="#4caf50",
    fg="white",
    command=open_image,
)
img_button.grid(row=0, column=0, padx=10, pady=5)

vid_button= tk.Button(
    buttons_frame,
    text="Обработать видео",
    font=("Arial", 12),
    bg="#2196f3",
    fg="white",
    command=open_video,
)
vid_button.grid(row=0, column=1, padx=10, pady=5)

#Ввод skip_frames
tk.Label(
    buttons_frame,
    text="skip_frames (N):",
    font=("Arial", 10),
    bg="#f8f8f8",
    fg="#333333",
).grid(row=1, column=0, sticky="e")

skip_frames_entry = tk.Entry(buttons_frame, width=5) 
skip_frames_entry.insert(0, "1") 
skip_frames_entry.grid(row=1, column=1, sticky="w")

# Прогресс-бар
progress_frame = tk.Frame(root, bg="#f8f8f8")
progress_frame.pack(pady=10)

progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(
    progress_frame,
    orient="horizontal",
    length=400,
    mode="determinate",
    variable=progress_var,
)

progress_bar.pack()

root.mainloop()