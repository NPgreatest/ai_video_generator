import os
from typing import List

from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.video.VideoClip import ImageClip

from config import *
import requests
import shutil
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip
output_audio = 'audio'
output_dir = 'output'
port = 9880


def read_txt_to_list(file_path):
    """
    读取给定文件路径的 TXT 文件，将每行内容存储为列表的一个元素。

    :param file_path: str, TXT文件的完整路径
    :return: list, 包含文件每行内容的列表
    """
    file_path = 'scripts/' + file_path
    content_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content_list = file.readlines()
            content_list = [line.strip() for line in content_list]
    except Exception as e:
        print(f"读取文件出错: {e}")
    return content_list

import cv2
from PIL import Image, ImageDraw, ImageFont

def genPic(config: ConfigParser) ->bool:
    bigtitle = config.get_bigtitle()
    smalltitle = config.get_smalltitle()
    output_path = f'pic/{config.get_project()}.jpg'
    bgpic_path = 'pic/'+config.get_background_picture()[0]['name']
    bgvideo_path = 'video/'+ config.get_video_file()

    # 从视频中提取第一帧
    cap = cv2.VideoCapture(bgvideo_path)
    success, frame = cap.read()
    cap.release()
    if not success:
        return False

    # 将提取的帧转换为PIL图像
    video_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # 加载背景图片并缩放（保持透明度）
    bg_image = Image.open(bgpic_path).convert("RGBA")
    bg_image = bg_image.resize((int(bg_image.width * 0.6), int(bg_image.height * 0.6)), Image.ANTIALIAS)

    # 创建一个和视频帧一样大的画布
    canvas = Image.new('RGBA', video_frame.size, (255, 255, 255, 0))
    canvas.paste(video_frame, (0, 0))

    # 将缩放后的背景图片贴在左下角
    canvas.paste(bg_image, (0, video_frame.height - bg_image.height), bg_image)

    # 在图片上添加文字
    draw = ImageDraw.Draw(canvas)
    font_big = ImageFont.truetype("font/bold.ttf", 120)  # 可能需要调整字体路径
    font_small = ImageFont.truetype("font/bold.ttf", 80)  # 可能需要调整字体路径

    # 计算文字位置并居中显示
    w_big, h_big = draw.textsize(bigtitle, font=font_big)
    w_small, h_small = draw.textsize(smalltitle, font=font_small)

    draw.text(((video_frame.width - w_big) // 2 + 200, (video_frame.height - h_big) // 2 + 500), bigtitle, font=font_big,
              fill=(255, 255, 0, 255),stroke_width=2,stroke_fill='black')
    draw.text(((video_frame.width - w_small) // 2 + 150, (video_frame.height - h_small) // 2 + 200), smalltitle,
              font=font_small, fill=(255, 255, 255, 255),stroke_width=2,stroke_fill='black')

    # 保存最终图片
    canvas = canvas.convert("RGB")  # 如果不需要透明背景
    canvas.save(output_path)
    return True

    # 保存最终图片
    canvas.save(output_path)
    return True


# , video_path, audio_path, subtitles
def generateVideo(config: ConfigParser) -> bool:
    print(TextClip.list("font"))
    videoFile = config.get_video_file()
    projectNmae = config.get_project()
    scriptPath = config.get_script()
    backMusic = config.get_bg_music()
    backPicture = config.get_background_picture()
    output_name = config.get_output_file()
    print(backPicture)

    # 加载视频文件
    video_clip = VideoFileClip( 'video/'+videoFile)
    final_clips = []

    # 加载剧本
    script = read_txt_to_list(scriptPath)

    # 构建音频文件路径列表
    audio_paths = [os.path.join(output_audio, f"{projectNmae}_{i + 1}.mp3") for i in range(len(script))]
    print(f'所需的音频列表为: {audio_paths}')
    # 初始化当前时间为0
    current_time = 0

    # 循环处理每个音频文件和字幕
    round = 0
    for audio_path, subtitle in zip(audio_paths, script):
        # if round == 3:
        #     break
        round += 1
        # 加载音频文件
        audio_clip = AudioFileClip(audio_path)
        audio_duration = audio_clip.duration

        txt_clips = []
        subtitle_clips = subtitle.split('\\\\')
        print(f'切分后的字幕片段为{subtitle_clips}')
        for i, subtitle_clip in enumerate(subtitle_clips):
            # 拼凑起来
            font_path = 'font/bold.ttf'
            txt_clip = TextClip(subtitle_clip, fontsize=100, color='yellow', font=font_path, kerning=-1, stroke_color='black',
                                stroke_width=4)
            txt_clip = txt_clip.set_position(('center', 400 + 100 * i)).set_duration(audio_duration)
            txt_clips.append(txt_clip)

        # 裁剪视频中对应的部分
        video_subclip = video_clip.subclip(current_time, current_time + audio_duration)

        # 将音频添加到视频剪辑中
        video_subclip = video_subclip.set_audio(audio_clip)

        if not subtitle.startswith('/'):
            # 将字幕添加到视频上
            video_subclip = CompositeVideoClip([video_subclip] + txt_clips)

        for picConfig in backPicture:
            if picConfig['begin'] <= round <= picConfig['end']:
                picName = picConfig['name']
                print(f'添加图片{picName}')
                image_clip = ImageClip(f'pic/{picName}').set_duration(audio_duration)
                width, height = image_clip.size
                resize_factor = 3 / 5
                if 'factor' in picConfig:
                    resize_factor = picConfig['factor']
                new_width = int(width * resize_factor)
                new_height = int(height * resize_factor)
                image_clip = image_clip.resize((new_width, new_height))
                # 默认是在左下角
                if 'posx' not in picConfig or 'posy' not in picConfig:
                    image_clip = image_clip.set_position(("left", "bottom"))
                else:
                    image_clip = image_clip.set_position((picConfig['posx'], picConfig['posy']))
                video_subclip = CompositeVideoClip([video_subclip, image_clip])

        # 添加到最终视频列表中
        final_clips.append(video_subclip)



        # 更新当前时间
        current_time += audio_duration

    # 合并所有剪辑
    final_video = concatenate_videoclips(final_clips)

    # 添加背景音乐
    if backMusic:
        back_audio_path = f'{output_audio}/'+backMusic
        print(f'add background music ', back_audio_path)
        # 加载音频文件
        back_audio_clip = AudioFileClip(back_audio_path)
        back_audio_clip = back_audio_clip.set_duration(current_time)
        back_audio_clip = back_audio_clip.volumex(0.2)
        final_audio = CompositeAudioClip([final_video.audio, back_audio_clip])
        final_video = final_video.set_audio(final_audio)

    # 输出目录确保存在
    # output_dir = 'final_output'
    # os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{output_name}")

    # 输出最终视频文件
    final_video.write_videofile(output_file, codec='libx264', fps=24)

    return output_file


"""
curl --location 'http://127.0.0.1:9880?text=test&text_language=zh&cut_punc=.'
"""


def genAudioandTitleFromAI(config: ConfigParser, port: int, reGen : bool):
    output_name = config.get_project()
    scriptPath = config.get_script()
    scripts = read_txt_to_list(scriptPath)
    print(scripts)
    # 遍历每一段脚本
    for index, script in enumerate(scripts):
        # 构建API请求URL
        url = f"http://127.0.0.1:{port}"
        params = {
            'text': script,
            'text_language': 'zh',
            'cut_punc': '。，',
            'speed' : '1.2'
        }
        # 跳过已经生成的内容
        if os.path.exists(f'{output_audio}/{output_name}_{index + 1}.mp3') and not reGen:
            continue

        # 处理指令
        if script[0] == '/':
            if script.startswith('/music'):
                findMusic = script.split('/music ')[1]
                print(f'寻找背景音效 {findMusic}')
                shutil.copy(f'{output_audio}/{findMusic}', f"{output_audio}/{output_name}_{index + 1}.mp3")
                print('复制成功')
                continue

        # 跳过换行符号
        script.replace('\\\\','')

        # 发送请求
        response = requests.get(url, params=params)

        # 检查响应状态
        if response.status_code == 200:
            # 保存音频文件
            audio_file_path = os.path.join(output_audio, f"{output_name}_{index + 1}.mp3")
            with open(audio_file_path, 'wb') as audio_file:
                audio_file.write(response.content)
            print(f"Audio file saved: {audio_file_path}")
        else:
            print(f"Failed to generate audio for script {index + 1}: {response.status_code}")

reGen = True

config = ConfigParser('scripts/6e.yaml')
genPic(config)

genAudioandTitleFromAI(config,port,reGen)
output_video = generateVideo(config)
print("Video saved to:", config.get_output_file())
