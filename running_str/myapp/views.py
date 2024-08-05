import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse

# Create your views here.

def create_running_str_video(text):
    # Параметры видео
    video_width = 100
    video_height = 100
    fps = 30
    duration = 3  # Длительность видео в секундах
    #text = "Хочу на стажировку :)"  # Текст для отображения

    # Создание видео
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter('./tmp/output.avi', fourcc, fps, (video_width, video_height))

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

def video_view(request):
    text = request.GET.get('text', 'Running Text Sample')
    create_running_str_video(text)

    with open('./tmp/output.avi', 'rb') as f:
        response = HttpResponse(f.read(), content_type='video/x-msvideo')
        response['Content-Disposition'] = 'attachment; filename="output.avi"'
        return response
    