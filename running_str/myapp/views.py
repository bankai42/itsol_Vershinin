import cv2
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
import tempfile
from .models import VideoRequest

# Create your views here.

def create_running_str_video(text):
    # Параметры видео
    video_width = 100
    video_height = 100
    fps = 30
    duration = 3  # Длительность видео в секундах
    #text = "Хочу на стажировку :)"  # Текст для отображения

    temp_file = tempfile.NamedTemporaryFile(suffix='.avi', delete=False)
    video_path = temp_file.name
    temp_file.close()


    # Создание видео
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(video_path, fourcc, fps, (video_width, video_height))

    # Загрузка шрифта
    font_size = 40
    font = ImageFont.truetype('running_str/myapp/fonts/arial.ttf', size=font_size)

    # Рассчитываем длину текста в пикселях
    (left, top, right, bottom) = font.getbbox(text)
    text_width = right-left
    text_height = top-bottom

    # Начальная позиция текста
    x = video_width

    for frame_num in range(fps * duration):
        # Создаем пустое изображение
        image = Image.new("RGB", (video_width, video_height), (255,192,203))
        draw = ImageDraw.Draw(image)

        # Рисуем текст
        draw.text((x, int(video_height+text_height)/2), text, font=font, fill=(255, 255, 255))

        # Конвертируем изображение в массив numpy
        frame = np.array(image)

        # Записываем кадр в видео
        video.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        # Обновляем позицию текста
        x -= int(text_width/(duration*fps))*1.5
        if x < -text_width:
            x = video_width

    # Освобождаем ресурсы
    video.release()
    
    return video_path


def video_view(request):
    text = request.GET.get('text', 'Running Text Sample')
    #create_running_str_video(text)

    video_path = create_running_str_video(text)

    # Сохранение данных в базе данных
    video_request = VideoRequest(text=text)
    video_request.video_file.save(os.path.basename(video_path), open(video_path, 'rb'))
    video_request.save()

    # Открытие видеофайла и возврат в HTTP-ответе
    with open(video_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='video/x-msvideo')
        response['Content-Disposition'] = f'attachment; filename="{video_path}.avi"'

    # Удаляем временный файл
    os.remove(video_path)
    return response
    