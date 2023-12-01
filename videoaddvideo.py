from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
from datetime import datetime, date
import logging
import sys

sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

VIDEO_FINAL = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'video_final')
VIDEO_INPUT = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'video_input')
VIDEO_OUTPUT = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'video_output')
POOL_SIZE = 6


def add_intro_video_with_moviepy(folder_path, intro_video_path, output_folder, head_tail_tag):
    # 获取文件夹中的所有视频文件
    video_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]
    logging.info(f"##" * 5 + f"now:{datetime.now()},视频数量:{len(video_files)}")

    # 加载指定的2秒尾部视频
    intro_clip = VideoFileClip(intro_video_path)

    # 遍历每个视频文件并添加指定的2秒视频
    for video_file in video_files:
        input_file = os.path.join(folder_path, video_file)
        output_file = os.path.join(output_folder, video_file)

        try:
            # 加载原始视频
            video_clip = VideoFileClip(input_file)

            # 将指定的2秒视频与原始视频进行合并
            if head_tail_tag == '1':
                final_clip = concatenate_videoclips([video_clip, intro_clip])
            else:
                final_clip = concatenate_videoclips([intro_clip, video_clip])

            # 保存合并后的视频
            final_clip.write_videofile(output_file)
        except Exception as e:
            logging.info(f"{input_file}添加尾部视频失败：{e}")


if __name__ == '__main__':
    logging.info(f"{'*'*30},start,{'*'*30}")
    # 指定参数
    start_time = datetime.now()
    dt = str(date.today())
    head_tail_tag = '1'
    video_tag = '1'

    # 接受video tag参数,    # 传入参数为空时
    if len(sys.argv) > 1:
        video_tag = sys.argv[1]
        head_tail_tag = sys.argv[1]

    # 指定的2秒尾部视频路径
    intro_video_path = os.path.join(VIDEO_FINAL, video_tag+'.mp4')
    logging.info(f"尾部视频地址：{intro_video_path}")

    # # 调用函数进行视频处理
    try:
        add_intro_video_with_moviepy(
            VIDEO_INPUT, intro_video_path, VIDEO_OUTPUT, head_tail_tag)
    except Exception as e:
        logging.info(f"添加尾部视频失败：{e}")

    # end
    end_time = datetime.now()
    logging.info(f"##" * 20 + f"now:{end_time},end" + "##" * 20)
    logging.info(
        f"##" * 20 + f"duration:{end_time-start_time},end" + "##" * 20)
