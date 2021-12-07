import os
import subprocess
import contextlib


class WavConverter:
    def convert(self, filename, export_path):
        self.check_file(filename, filename)
        in_ext = self.check_ext(filename, filename)
        out_ext = self.check_ext(export_path, export_path)

        if in_ext == '.wav' and out_ext == '.wav':
            with open(filename, 'rb') as source:
                with open(export_path, 'wb') as export:
                    export.write(source.read())
        else:
            with contextlib.redirect_stdout(None):
                subprocess.call(['ffmpeg', '-i', filename, export_path])

    def check_file(self, filename):
        if not os.path.isfile(filename):
            raise ConverterError(filename + " file does not exist")

    def check_ext(self, filename):
        ext = os.path.splitext(filename)[1]
        if ext != '.wav' and ext != '.mp3':
            raise ConverterError("This editor does not work with " + ext + " extention")
        return ext


class ConverterError(Exception):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        if self.message is not None:
            return self.message
        else:
            return 'ConverterError'
