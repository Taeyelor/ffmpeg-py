import json
import os
import platform
import zipfile
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
            if not os.path.exists('ffmpeg-5.0.1-essentials_build.zip'):
                os.system('curl https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-5.0.1-essentials_build.zip -O ffmpeg-5.0.1-essentials_build.zip')
            with zipfile.ZipFile('ffmpeg-5.0.1-essentials_build.zip', 'r') as zip_ref:
                zip_ref.extractall('ffmpeg_runner')
            os.remove('ffmpeg-5.0.1-essentials_build.zip')

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

    def select_videos(self, indexes):
        self.__videos = indexes

    def select_audios(self, indexes):
        self.__audios = indexes

    def select_subtitles(self, indexes):
        self.__subtitles = indexes

    def x265(self, activate: bool):
        self.__x265 = activate

    def get_source_subtitles(self):
        map = subprocess.Popen(['ffmpeg_runner/ffmpeg-5.0.1-essentials_build/bin/ffprobe', '-select_streams', 's', '-show_entries', 'stream=index:stream_tags', '-of', 'json', self.__input_file[0]], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return json.loads(map.stdout.read())['streams']

    def get_source_audios(self):
        map = subprocess.Popen(['ffmpeg_runner/ffmpeg-5.0.1-essentials_build/bin/ffprobe', '-select_streams', 'a', '-show_entries', 'stream=index:stream_tags', '-of', 'json', self.__input_file[0]], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return json.loads(map.stdout.read())['streams']

    def get_source_videos(self):
        print('Videos:')
        map = subprocess.Popen(['ffmpeg_runner/ffmpeg-5.0.1-essentials_build/bin/ffprobe', '-select_streams', 'v', '-show_entries', 'stream=index:stream_tags', '-of', 'json', self.__input_file[0]], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        return json.loads(map.stdout.read())['streams']

    def encoding(self):
        if not self.__ffmpeg_check():
            self.__ffmpeg_donwload() 

        if not os.path.exists(self.__output_path):
            os.mkdir(self.__output_path)

        run = [
            'ffmpeg_runner/ffmpeg-5.0.1-essentials_build/bin/ffmpeg', 
            '-y',
            '-i',
            f'{self.__input_file[0]}', 
            '-crf',
            f'{self.__crf}',
            '-preset',
            f'{self.__preset}'
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

        print(run)

        subprocess.run(run)

    def concat(self):
        if not self.__ffmpeg_check():
            self.__ffmpeg_donwload() 

        if not os.path.exists(self.__output_path):
            os.mkdir(self.__output_path)

        inputes = ''

        for input in self.__input_file:
            inputes += f'{input}|'

        inputes = inputes[:-1]

        run = [
            'ffmpeg_runner/ffmpeg-5.0.1-essentials_build/bin/ffmpeg', 
            '-y',
            '-i',
            f'concat:{inputes}',
        ]

        run.extend(['-c', 'copy', f'{self.__output_path}/{self.__output_name}'])

        print(run)

        subprocess.run(run)