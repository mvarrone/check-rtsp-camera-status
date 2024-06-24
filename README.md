# ip-cameras-private

## Python 3 script able to check the availability of several IP Cameras via RTSP

### Details

* ProcessPoolExecutor used in order to connect to the cameras in parallel and reduce the amount of time needed to complete this task
* It provides some stats at the end of the execution. Check [sample_execution_results.txt](https://github.com/mvarrone/check-rtsp-camera-status/blob/master/sample_execution_results.txt)
* Each camera is represented as a Python 3 dictionary, stored in the *credentials.json* file. This file is a **list** of dictionaries containing the following structure for a fake set of parameters:

*Example:*

```python
[
        {
                "protocol": "rtsp",
                "username": "admin1",
                "password": "password1",
                "domain": "domain1.dyndns.org",
                "port": 554,
                "path": "/Streaming/Channels/",
                "camera_number": 101
        },
        {
                "protocol": "rtsp",
                "username": "user",
                "password": "password2",
                "domain": "domain2.dyndns.org",
                "port": 554,
                "path": "/Streaming/Channels/",
                "camera_number": 401
        }
]
```

### RTSP IP Camera URL example

```python
rtsp://admin:password@domain.dyndns.org:554/Streaming/Channels/101
```

Again, this URL is not a valid *RTSP* url. 

Same for [sample_execution_results.txt](https://github.com/mvarrone/check-rtsp-camera-status/blob/master/sample_execution_results.txt): In this file, sensitive parameters are faked

## Requirements

- *Python 3.12.2*
- *ffmpeg*

```bash
ffmpeg version 2024-04-29-git-cf4af4bca0-full_build-www.gyan.dev Copyright (c) 2000-2024 the FFmpeg developers

built with gcc 13.2.0 (Rev5, Built by MSYS2 project)
configuration: --enable-gpl --enable-version3 --enable-static --disable-w32threads --disable-autodetect --enable-fontconfig --enable-iconv --enable-gnutls --enable-libxml2 --enable-gmp --enable-bzlib --enable-lzma --enable-libsnappy --enable-zlib --enable-librist --enable-libsrt --enable-libssh --enable-libzmq --enable-avisynth --enable-libbluray --enable-libcaca --enable-sdl2 --enable-libaribb24 --enable-libaribcaption --enable-libdav1d --enable-libdavs2 --enable-libuavs3d --enable-libxevd --enable-libzvbi --enable-librav1e --enable-libsvtav1 --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxavs2 --enable-libxeve --enable-libxvid --enable-libaom --enable-libjxl --enable-libopenjpeg --enable-libvpx --enable-mediafoundation --enable-libass --enable-frei0r --enable-libfreetype --enable-libfribidi --enable-libharfbuzz --enable-liblensfun --enable-libvidstab --enable-libvmaf --enable-libzimg --enable-amf --enable-cuda-llvm --enable-cuvid --enable-dxva2 --enable-d3d11va --enable-d3d12va --enable-ffnvcodec --enable-libvpl --enable-nvdec --enable-nvenc --enable-vaapi --enable-libshaderc --enable-vulkan --enable-libplacebo --enable-opencl --enable-libcdio --enable-libgme --enable-libmodplug --enable-libopenmpt --enable-libopencore-amrwb --enable-libmp3lame --enable-libshine --enable-libtheora --enable-libtwolame --enable-libvo-amrwbenc --enable-libcodec2 --enable-libilbc --enable-libgsm --enable-libopencore-amrnb --enable-libopus --enable-libspeex --enable-libvorbis --enable-ladspa --enable-libbs2b --enable-libflite --enable-libmysofa --enable-librubberband --enable-libsoxr --enable-chromaprint
libavutil      59. 16.101 / 59. 16.101
libavcodec     61.  5.103 / 61.  5.103
libavformat    61.  3.103 / 61.  3.103
libavdevice    61.  2.100 / 61.  2.100
libavfilter    10.  2.101 / 10.  2.101
libswscale      8.  2.100 /  8.  2.100
libswresample   5.  2.100 /  5.  2.100
libpostproc    58.  2.100 / 58.  2.100
```