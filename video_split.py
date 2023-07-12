#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   video_split.py
@Time    :   2023/06/26 13:33:03
@Author  :   Yin Xu 
@Version :   1.0
@Contact :   yin.xu@adwangmai.com
@Desc    :   None
'''

import moviepy.editor as mp
import os

root_dir = 'D:\\tmp\\抖音视频素材\\output\\0627夏季穿搭'

# 加载视频文件
video = mp.VideoFileClip(os.path.join(root_dir, '6月27日夏季穿搭.mp4'))

# 设置时间间隔和起始时间
interval = 14  # 时间间隔，单位为秒
start_time = 0  # 起始时间，单位为秒

# 计算总时长
duration = video.duration

# 循环遍历视频，切割子剪辑并保存为新的视频文件
for i in range(int(duration // interval)):
    # 计算子剪辑的起始时间和结束时间
    subclip_start = i * interval + start_time
    subclip_end = (i + 1) * interval + start_time
    if subclip_end > duration:
        subclip_end = duration

    # 切割子剪辑并保存为新的视频文件
    subclip = video.subclip(subclip_start, subclip_end)
    subclip.write_videofile(os.path.join(root_dir, f'0627_夏季穿搭.mp4_{i}.mp4'), codec='libx264')

# 释放资源
video.close()