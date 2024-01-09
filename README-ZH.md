# realesrgan-rcnn-gradio
用于realesrgan放大的的简单gradio ui <br>
(可能把license搞错了谁知道的告诉我下谢谢) <br>
虽然已经有现成的了，但是写都写了...

# 安装：
*首先* <br>
下载模型（我不做模型，我只是模型的搬运工）: <br>
https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan/releases/tag/v0.2.0 <br>
找个你os能跑的起来的 <br>
解压进项目的realesrgan文件夹

## windows
双击 click start.bat
1. 制造一个venv环境（依赖里面好几个环境污染大户）
2. 制造一些必要的文件夹
3. 下载依赖（因为看得出来这依赖重叠很高，有很多要下的）
4. gradio服务会在localhost的7860端口，浏览器打开http://localhost:7860
如果对外提供服务或者换端口请自己改py文件

## linux
执行 start.sh <br>
和上面的玩意儿一样 (暂时没测)

之后的工作
1. 需要对现有机器的gpu进行监测
2. 可以增加更多模型的控制和流水线之类的东西
