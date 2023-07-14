#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   img2video.py
@Time    :   2023/06/25 15:37:12
@Author  :   yang Xu 
@Version :   1.0
@Contact :   yang.xu@adwangmai.com
@Desc    :   None
'''

import os
import sys
import multiprocessing
import cv2
import numpy as np
from PIL import Image
import moviepy.editor as mp
import random
from datetime import datetime, date

sys.stdout.reconfigure(encoding='utf-8')

IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image')
VIDEO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video')
BGM_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bgm')
FPS = 24
SIZE = (720, 1280)
CHUNK_SIZE = 7
POOL_SIZE = 6


def video_add_bgm(video_input_file, audio_file_list, video_output_file):
    video_clip = mp.VideoFileClip(video_input_file)
    audio_file_name = random.choice(audio_file_list)
    audio_clip = mp.AudioFileClip(audio_file_name)

    # 计算音频和视频的长度差
    duration_diff = video_clip.duration - audio_clip.duration

    # 如果音频比视频短，则重复音频直到与视频长度相同
    if duration_diff > 0:
        audio_clip = audio_clip.set_duration(video_clip.duration)
    else:
        # 如果视频比音频短，则截取音频以匹配视频长度
        audio_clip = audio_clip.subclip(0, video_clip.duration)

    # 将音频文件合并到视频文件中
    final_clip = video_clip.set_audio(audio_clip)

    # 保存输出文件
    final_clip.write_videofile(video_output_file, fps=24, codec='libx264')
    print(video_output_file)


def load_audio_files():
    # 加载所有音频文件
    audio_file_list = []
    for root, dirs, files in os.walk(BGM_DIR):
        for file in files:
            if '.mp3' not in file:
                continue
            file_name = os.path.join(root, file)
            audio_file_list.append(file_name)
    return audio_file_list


def template_on_image(template_path, image_path):
    # 打开 模板图片 和 原图片
    template_image = Image.open(template_path).convert("RGBA")
    origin_image = Image.open(image_path).convert("RGBA")

    # 确保两张图片的尺寸相同，如果需要，可以调整 模板图片的尺寸。
    template_image = template_image.resize(origin_image.size, Image.ANTIALIAS)

    # 创建一个新的RGBA模式的图像，RGBA模式包含红、绿、蓝和透明度通道
    output_image = Image.new("RGBA", origin_image.size)

    # 将背景图片和叠加的图片合并到新的图像上，
    output_image = Image.alpha_composite(output_image, origin_image)
    output_image = Image.alpha_composite(output_image, template_image)

    # 保存结果图片
    # output_image.save('C:\\Users\\A\\Pictures\\\image2video\\image\\out.jpg')
    # image = cv2.imread('C:\\Users\\A\\Pictures\\\image2video\\image\\out.jpg')
    return output_image


def create_video(images, video_name):
    print("##" * 5 + f"now:{datetime.now()},video_name:{video_name}")

    audio_file_list = load_audio_files()

    # 创建一个视频写入器
    video_path = os.path.join(VIDEO_DIR, video_name)
    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), FPS,
                            SIZE)

    # 逐帧将图片写入视频
    for image_path in images:
        img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
        a = 0
        while a < 48:
            img = cv2.resize(img, SIZE)
            video.write(img)
            a += 1
    # 释放视频写入器和窗口资源,
    video.release()
    # 添加bgm
    new_video_path = os.path.join(VIDEO_DIR, 'AI_' + video_name)
    try:
        video_add_bgm(video_path, audio_file_list, new_video_path)
    except Exception as e:
        print("##" * 5 + f"now:{datetime.now()},Exception:{e}")
    # 删除未添加bgm视频
    os.remove(video_path)


if __name__ == '__main__':
    # 指定参数
    start_time = datetime.now()
    print("##" * 20 + f"now:{start_time},start" + "##" * 20)
    dt = str(date.today())
    video_tag = '素材'

    # 接受video tag参数
    if len(sys.argv) > 1:
        video_tag = sys.argv[1]
    # template_image_path = ''

    images = sorted([
        os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR)
        if f.endswith('.jpg') or f.endswith('.png')
    ])

    # 按照每7张图片一组的方式将图片分组，并且排除最后不足7张图片的组

    chunks = [
        images[i:i + CHUNK_SIZE] for i in range(0, len(images), CHUNK_SIZE)
    ]
    if len(chunks[-1]) != CHUNK_SIZE:
        chunks.pop()

    # 使用进程池创建6个进程，并异步地对每组图片调用create_video函数处理成一个视频文件
    pool = multiprocessing.Pool(processes=POOL_SIZE)
    for i, chunk in enumerate(chunks):
        try:
            video_name = f'{dt}_{video_tag}_{i+1}.mp4'
            pool.apply_async(create_video, args=(chunk, video_name))
        except Exception as e:
            print("##" * 5 + f"now:{datetime.now()},Exception:{e}")
    pool.close()
    pool.join()

    # end
    end_time = datetime.now()
    print("##" * 20 + f"now:{end_time},end" + "##" * 20)
    print("##" * 20 + f"duration:{end_time-start_time},end" + "##" * 20)
