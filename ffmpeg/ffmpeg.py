import json
import os
import platform
import zipfile
import tarfile
import subprocess

class FFmpeg:
    __threads = 1
    __input_file = []
    __output_path = None
    __output_name = None
    __subtitle_file = []
    __crf = 22
    __preset = 'medium'
    __x265 = False
    __videos = []
    __audios = []
    __subtitles = []
    __scale = None
    __tune = 'film'
    __ffmpeg_file = ''
    __ffprobe_file= ''

    def __init__(self, input_file, output_path, output_name):
        self.__input_file = input_file
        self.__output_path = output_path
        self.__output_name = output_name

    def __ffmpeg_check(self):
        if os.path.exists('ffmpeg_runner'):
            return True

        return False

    def __ffmpeg_donwload(self):
        os_name = platform.system()
        print(f'OS: {os_name}')
        if os_name == 'Windows':
            print('Downloading ffmpeg...')
            if not os.path.exists('ffmpeg-5.0.1-essentials_build.zip'):
                os.system('curl https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-5.0.1-essentials_build.zip -O ffmpeg-5.0.1-essentials_build.zip')
            with zipfile.ZipFile('ffmpeg-5.0.1-essentials_build.zip', 'r') as zip_ref:
                zip_ref.extractall('ffmpeg_runner')
            os.remove('ffmpeg-5.0.1-essentials_build.zip')
            self.__ffmpeg_file = 'ffmpeg_runner/ffmpeg-5.0.1-essentials_build/bin/ffmpeg'
            self.__ffprobe_file = 'ffmpeg_runner/ffmpeg-5.0.1-essentials_build/bin/ffprobe'
            print('Download complete.')
        elif os_name == 'Linux':
            print('Downloading ffmpeg...')
            if not os.path.exists('ffmpeg-5.0.1-essentials_build.zip'):
                os.system('curl https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -O ffmpeg-release-amd64-static.tar.xz')
            with tarfile.open('ffmpeg-release-amd64-static.tar.xz') as tar_ref:
                tar_ref.extractall('ffmpeg_runner')
            os.remove('ffmpeg-release-amd64-static.tar.xz')
            self.__ffmpeg_file = 'ffmpeg_runner/ffmpeg-5.0.1-amd64-static/ffmpeg'
            self.__ffprobe_file = 'ffmpeg_runner/ffmpeg-5.0.1-amd64-static/ffprobe'
            print('Download complete.')


    def ffmpeg_exists(self):
        if not self.__ffmpeg_check():
            self.__ffmpeg_donwload()

    def set_threads(self, count):
        self.__threads = count

    def get_threads(self):
        return self.__threads

    def add_subtitle(self, file):
        self.__subtitle_file.append(file)


    def get_subtitle(self):
        return self.__subtitle_file

    def set_crf(self, crf):
        self.__crf = crf

    def get_crf(self):
        return self.__crf

    def set_preset(self, preset):
        if preset not in ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow', 'placebo']:
            print('Invalid preset')
            return

        self.__preset = preset

    def get_preset(self):
        return self.__preset

    def set_scale(self, scale):
        if scale not in ['360', '480', '720', '1080']:
            print('Invalid scale')
            return

        self.__scale = scale

    def set_tune(self, tune):
        if tune not in ['film', 'animation', 'grain', 'stillimage', 'fastdecode', 'zerolatency', 'psnr', 'ssim']:
            print('Invalid tune')
            return

        self.__tune = tune

    def get_tune(self):
        return self.__tune

    def select_videos(self, indexes):
        self.__videos = indexes

    def select_audios(self, indexes):
        self.__audios = indexes

    def select_subtitles(self, indexes):
        self.__subtitles = indexes

    def x265(self, activate: bool):
        self.__x265 = activate

    def get_source_subtitles(self):
        map = subprocess.Popen([self.__ffprobe_file, '-select_streams', 's', '-show_entries', 'stream=index:stream_tags', '-of', 'json', self.__input_file[0]], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return json.loads(map.stdout.read())['streams']

    def get_source_audios(self):
        map = subprocess.Popen([self.__ffprobe_file, '-select_streams', 'a', '-show_entries', 'stream=index:stream_tags', '-of', 'json', self.__input_file[0]], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return json.loads(map.stdout.read())['streams']

    def get_source_videos(self):
        print('Videos:')
        map = subprocess.Popen([self.__ffprobe_file, '-select_streams', 'v', '-show_entries', 'stream=index:stream_tags', '-of', 'json', self.__input_file[0]], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return json.loads(map.stdout.read())['streams']

    def encoding(self):
        if not self.__ffmpeg_check():
            self.__ffmpeg_donwload() 

        if not os.path.exists(self.__output_path):
            os.mkdir(self.__output_path)

        run = [
            self.__ffmpeg_file, 
            '-y',
            '-i',
            f'{self.__input_file[0]}', 
            '-crf',
            f'{self.__crf}',
            '-preset',
            f'{self.__preset}',
            '-tune',
            f'{self.__tune}',
            '-c:a',
            'aac',
            '-b:a',
            '128k'
        ]

        if(self.__x265):
            run.extend(['-c:v', 'libx265'])

        if len(self.__subtitle_file) > 0 and self.__scale is None:
            run.append('-vf')
            ass = ''

            for subtitle in self.__subtitle_file:
                ass += f'ass={subtitle},'

            ass = ass[:-1] 

            run.append(ass)

        if self.__scale is not None and len(self.__subtitle_file) == 0:
            run.extend(['-vf', f'scale={self.__scale}:trunc(ow/a/2)*2'])

        if self.__scale is not None and len(self.__subtitle_file) > 0:
            ass = ''

            for subtitle in self.__subtitle_file:
                ass += f'ass={subtitle},'

            ass = ass[:-1] 

            run.extend(['-vf', f"scale={self.__scale}:trunc(ow/a/2)*2,{ass}"])
        if len(self.__videos) > 0:
            for i in range(0, len(self.__videos)):
                run.extend(['-map', f'0:{self.__videos[i]}'])

        if len(self.__audios) > 0:
            for i in range(0, len(self.__audios)):
                run.extend(['-map', f'0:{self.__audios[i]}'])

        if len(self.__subtitles) > 0:
            for i in range(0, len(self.__audios)):
                run.extend(['-map', f'0:{self.__audios[i]}'])

        
        run.extend(['-threads', f'{self.__threads}'])
        
        run.append(f'{self.__output_path}/{self.__output_name}')

        subprocess.run(run)

    def concat(self):
        if not self.__ffmpeg_check():
            self.__ffmpeg_donwload() 

        if not os.path.exists(self.__output_path):
            os.mkdir(self.__output_path)

        file = open(f"./inputs.txt", "w")
        file.write(f"file {self.__input_file[0]}\nfile {self.__input_file[1]}")
        file.close()

        run = [
            self.__ffmpeg_file, 
            '-y',
            '-f',
            'concat',
            '-i',
            f'./inputs.txt',
            '-segment_time_metadata',
            '1',
            '-vf',
            'select=concatdec_select',
            '-af',
            'aselect=concatdec_select,aresample=async=1',
            f'{self.__output_path}/{self.__output_name}'
        ]

        subprocess.run(run)