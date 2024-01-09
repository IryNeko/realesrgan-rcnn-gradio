'''
主要是跑ai放大然后缩小

UI，Gradio
制作：艾瑞
'''

'''
使用的库
moviepy
imageio.v2
realesrgan的依赖
gradio
'''
import os
import imageio.v2 as imageio
import numpy as np
import gradio as gr
from moviepy.editor import *
import time
from PIL import Image
'''
app gradio 组件
用于ui的使用
'''
# 变量
vid=None #视频reader
'''
上传需要放大的video
'''
def upload_video():
    return
'''
选择需要放大的video
从文件夹中选择
'''
def select_video()->[str]:
    return os.listdir("videos")
def select_models()->[str]:
    return ["realesr-animevideov3","realesrgan-x4plus","realesrgan-x4plus-anime"]

'''
Gradio UI

'''
tmp_path=""
tmp_aspect=1.0
with gr.Blocks() as demo:
    with gr.Tab(label="视频放大"):
        with gr.Row():
            videoupload=gr.Video(sources='upload')
            with gr.Column():
                input_metadata=gr.Textbox(value={},label="视频信息")
                label1=gr.Label(value="设置目标的长宽比")
                aspect_ratio=gr.Text(label="长宽比")
                target_height=gr.Text(label="高度")
                target_width=gr.Slider(maximum=1920,step=24)
            with gr.Column():
                label2=gr.Label(value="设置放大模型属性")
                model=gr.Dropdown(["realesr-animevideov3","realesrgan-x4plus","realesrgan-x4plus-anime"],label="模型",value="realesr-animevideov3")
                size=gr.Dropdown(["2","3","4"],label="放大程度",value="2")
                gpu=gr.Text(value=0,label="gpu设置")
                enlarge=gr.Button(interactive=False,value="请选择视频")
        output=gr.Video(label="输出视频")
                
                
            
    # 上传视频
    @videoupload.change(inputs=videoupload, outputs=[input_metadata,enlarge,model,size,gpu,aspect_ratio,target_width])
    def upload_now(source):
        global vid
        global tmp_path
        global tmp_aspect
        tmp_path=source
        vid=imageio.get_reader(tmp_path,  'ffmpeg')
        meta=vid.get_meta_data()
        tmp_aspect=meta['size'][1]/meta['size'][0]
        print("received file",type(source),source)
        return meta,gr.Button(interactive=True,value="进行放大"),gr.Dropdown(interactive=True),gr.Dropdown(interactive=True),gr.Text(interactive=True),tmp_aspect,meta['size'][0]
        #os.rename(source, "videos\\"+source.split("\\")[-1])
        #return gr.Dropdown(select_video(),label="选择放大的视频")
    # 调整幅度
    @target_width.change(inputs=target_width,outputs=target_height)
    def change_height(w):
        global tmp_aspect
        return round(w*tmp_aspect)
    # 视频放大
    @enlarge.click(inputs=[target_width,target_height,model,size,gpu],outputs=output)
    def enlarge_proces(w,h,model,size,gpu):
        global vid
        '''
        切割出帧
        '''
        count=vid.count_frames()
        # clean the temp folder
        for f in os.listdir("temp"):
            os.remove("temp/"+f)
        # save to folder
        i=0
        while i<count:
            image=np.stack(vid.get_data(i))
            fname="{:08d}".format(i)
            imageio.imwrite(f"temp/{fname}.png",image,format="png")
            i+=1
        print("帧切割完毕")
        '''
        放大
        '''
        input="temp"
        output="temp_out"
        format="png"
        # clear the temp_out folder
        for f in os.listdir(output):
            os.remove(output+"/"+f)
        # do the work
        cmd=f"{os. getcwd()}//realesrgan//realesrgan-ncnn-vulkan.exe -i {input} -o {output} -n {model} -s {size} -f {format} -g {gpu}"
        os.system(cmd)
        print("---图像放大完毕")
        '''
        图像缩小
        '''
        path="temp_out/"
        for file in os.listdir(path):
            img = imageio.imread(path+file)
            
            img = Image.fromarray(img).resize((int(w), int(h)))
            imageio.imwrite(path+file,img)
        print("---图像重缩小完毕")
        '''
        重组
        '''
        path="temp_out/"
        # 清理目标videos_out
        for f in os.listdir('videos_out'):
            os.remove('videos_out/'+f)
        meta=vid.get_meta_data()
        fileList = []
        for file in os.listdir(path):
            complete_path = path + file
            fileList.append(complete_path)
        writer = imageio.get_writer('videos_out/tmp_out.mp4', fps=meta['fps'])

        for im in fileList:
            writer.append_data(imageio.imread(im))
        writer.close()
        print("---视频重组完成")
        '''
        合成音频
        '''
        global tmp_path
        # 用ffmpeg把源视频的音轨剪出来，和新的视频合成一下   
        video = VideoFileClip('videos_out/tmp_out.mp4')
        audio = VideoFileClip(tmp_path).audio
        video.audio = audio
        video.write_videofile("videos_out/out.mp4")
        print('print("---视频重组完成")')
        # 读最后的结果
        return gr.Video("videos_out/out.mp4")
if __name__=='__main__':  
    demo.launch()