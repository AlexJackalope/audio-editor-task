import os
import subprocess


class WavConverter:
    def convert(self, filename, export_path):
        try:
            in_ext = self.check_file(filename, filename)
        except (FileNotFoundError, NameError) as e:
            raise e
        out_ext = os.path.splitext(export_path)[1]
        if in_ext == '.wav' and out_ext == '.wav':
            with open(filename, 'rb') as source:
                with open(export_path, 'wb') as export:
                    export.write(source.read())
        else:
            subprocess.call(['ffmpeg', '-i', filename, export_path])

    def check_file(self, filename):
        if not os.path.isfile(filename):
            raise FileNotFoundError(filename + " file does not exist")
        ext = os.path.splitext(filename)[1]
        if ext != '.wav' and ext != '.mp3':
            raise NameError("This editor does not work with " + ext)
        return ext
