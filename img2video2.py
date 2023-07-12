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
import cv2
import numpy as np
from PIL import Image
import moviepy.editor as mp
import random
import datetime

Image_Dir = 'C:\\Users\\A\\Pictures\\\image2video\\image'
Video_Dir = 'C:\\Users\\A\\Pictures\\\image2video\\video'
Audio_Dir = 'C:\\Users\\A\\Pictures\\\image2video\\bgm'

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
    audio_dir = Audio_Dir
    audio_file_list = []
    for root ,dirs, files in os.walk(audio_dir):
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

    # output_image = output_image.convert('RGB')

    # 保存结果图片
    # output_image.save('C:\\Users\\A\\Pictures\\\image2video\\image\\out.jpg')
    # image = cv2.imread('C:\\Users\\A\\Pictures\\\image2video\\image\\out.jpg')
    return output_image


if __name__ == '__main__':
    dt = str(datetime.date.today())
    image_dir = Image_Dir
    video_dir = Video_Dir
    video_tag = '凉鞋'
    # template_image_path = 'C:\\Users\\A\\Pictures\\image2video\\template\\0627-1.png'
    template_image_path = ''
    fps = 24
    duration = 3
    size = (720, 1280)

    audio_file_list = load_audio_files()
    image_files = os.listdir(image_dir)

    video_index = 1
    video_name = os.path.join(video_dir, f'{dt}_{video_tag}_{video_index}.mp4')
    video = cv2.VideoWriter(video_name,cv2.VideoWriter_fourcc(*'mp4v'),fps,(720,1280))
    for i in range(len(image_files)):

        file_name = os.path.join(image_dir, image_files[i])
        if i % 7 == 0 and i > 0:
            print(video_name)
            video.release()

            video_output_name = os.path.join(video_dir, f'ai_{dt}_{video_tag}_{video_index}.mp4')
            video_add_bgm(video_name, audio_file_list, video_output_name)
            os.remove(video_name)

            video_index += 1
            video_name = os.path.join(video_dir, f'{dt}_{video_tag}_{video_index}.mp4')
            video = cv2.VideoWriter(video_name,cv2.VideoWriter_fourcc(*'mp4v'),fps,(720,1280))


        # img = cv2.imread(file_name) #读取图片 叠加模板图片
        # combined_image = template_on_image(file_name,template_image_path)
        if template_image_path !='':
            output_image = template_on_image(template_image_path,file_name,)
        else:
            output_image = cv2.imdecode(np.fromfile(file_name,dtype=np.uint8),-1)
        # 将图像转换为Numpy数组，并将其写入视频文件
        # img = cv2.cvtColor(np.array(output_image), cv2.COLOR_RGB2BGR) # 视频色彩会变化
        img = cv2.resize(output_image, size)
        print(img.shape)

        a=0
        while a < 48:
            img = cv2.resize(img, (720, 1280))
            video.write(img)
            a+=1
    
    print(video_name)
    video.release()
    os.remove(video_name)

        
    # 释放资源
    # video.release()
    # os.remove(video_name)