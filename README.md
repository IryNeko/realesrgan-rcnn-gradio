# realesrgan-rcnn-gradio
Gradio UI for realesrgan-rcnn, useful for deployment on a server
(I may have the license inheretence wrong so please correct me)

# installation
*before everything* 
get the rcnn-vulcan model from:
https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan/releases/tag/v0.2.0
pick the binary that works on your os
dump everything into *realesrgan* folder

## windows
double click start.bat
1. creates a simple venv
2. creates some io folders
3. installation of dependencies (not really optimized, you can see some big package overlaps, expect large downloads)
4. start the gradio server on *port 7860*
if you want to share, or change port, probably edit the py yourself

## linux
execute the start.sh
same as above (not tested as for now)

# upcoming fixes
1. auto detect all the gpus for generation
2. create addons for more models like dlcs but open source
