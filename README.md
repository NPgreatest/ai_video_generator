# auto_dingzhen

An auto video generator based on `moviepy, GPT-SoVITS`

Example Video(ai sun):
https://www.bilibili.com/video/BV1fNayeFExG/

Example Video(ai dingzhen):
https://www.bilibili.com/video/BV1JAayeaEiw/

## The needs of use script to generate video:

1. integrate video clip
2. integrate audio clip
3. embedding text
4. put picture
5. easy effects

## example of video config

```JSON

{
  "video_clips": [
    {
      "source": "intro.mp4",
      "start": 0.0,
      "end": 10.0,
      "position": [0, 0],
      "scale": 1.0,
      "video_begin": 0.0
    },
    {
      "source": "scene1.mp4",
      "start": 5.0,
      "end": 20.0,
      "position": [100, 100],
      "scale": 0.8,
      "video_begin": 2.0
    }
  ],
  "audio_tracks": [
    {
      "source": "xxx1.wav",
      "start": 0.0,
      "end": 30.0,
      "volume": 0.5,
      "audio_start": 0.0
    },
    {
      "source": "xxx2.wav",
      "start": 30.0,
      "end": 40.0,
      "volume": 0.7,
      "audio_start": 0.0
    }
  ],
  "image_clips": [
    {
      "source": "logo.png",
      "start": 0.0,
      "end": 30.0,
      "position": [500, 50],
      "scale": 1.0
    },
    {
      "source": "watermark.png",
      "start": 10.0,
      "end": 40.0,
      "position": [200, 300],
      "scale": 0.5
    }
  ],
  "text_overlays": [
    {
      "content": "Welcome to the show",
      "position": ["center", "top"],
      "font": "Arial",
      "size": 40,
      "color": "white",
      "start": 2.0,
      "end": 10.0
    }
  ],
  "effects": [
    {
      "type": "brightness",
      "value": 1.2,
      "start": 0.0,
      "end": 10.0
    },
    {
      "type": "blur",
      "value": 5,
      "start": 5.0,
      "end": 15.0
    }
  ]
}




```