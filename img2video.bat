chcp 65001
@echo off


set /p name=请输入素材tag名称参数,例如风扇:


@REM D:\soft\anaconda\envs\img2video\python.exe D:\soft\img2video\img2video2.py %name% >> log.txt
video/AI_2023-12-01_素材_3.mp4 video/AI_2023-12-01_素材_1.mp4 video/AI_2023-12-01_素材_2.mp4
C:/Users/yangxu/miniconda3/envs/img2video/python.exe c:/Users/yangxu/Documents/xuyang/CODE/CODE_PYTHON/img2video/img2video2.py %name% >> log.txt
type log.txt


echo 任务已完成，窗口将在 3 秒钟后关闭。
ping 127.0.0.1 -n 4 > nul
exit