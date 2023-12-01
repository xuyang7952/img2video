chcp 65001
@echo off


set /p name1=请输入尾部视频对应编号1-手淘,2-快手,默认为1:
set /p name2=请输入插入头部还是尾部0-头部,1-尾部,默认为1:

REM 如果参数为空，则使用默认值
if "%name1%"=="" set "name1=1"
if "%name2%"=="" set "name2=1"


@REM 部署到新机器，需要指定python环境，并安装相应的包
@REM D:\soft\anaconda\envs\img2video\python.exe D:\soft\img2video\videoaddvideo.py %name% >> log.txt
C:\Users\yangxu\miniconda3\envs\img2video\python.exe C:\Users\yangxu\Documents\xuyang\CODE\CODE_PYTHON\img2video\videoaddvideo.py %name1% %name2% >> log.txt 


type log.txt


echo 任务已完成，窗口将在 3 秒钟后关闭。
ping 127.0.0.1 -n 4 > nul
exit