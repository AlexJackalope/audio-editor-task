import os
import argparse
import sys

from WavConverter import WavConverter
from WavEditor import WavEditor


def parse_start_args():
    parser = argparse.ArgumentParser(
        description="Console audio editor.\n"
                    "To start working input path to your audio "
                    "(.wav and .mp3 formats are supported)\n",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("audio_path", help="Path to audio to edit")
    return parser.parse_args()


def print_help():
    message = "Console audio editor commands:\n"\
              "* speed_chg [coefficient] - " \
              "changes audio speed with mentioned coefficient\n"\
              "* cut [start] [length] - " \
              "cuts off a fragment mentioned with length from start time\n"\
              "  (time is always written in seconds)\n"\
              "* concat [path to audio] - " \
              "adds new audio to the end of current\n"\
              "* reverb [room scale between 0 and 100] - " \
              "makes reverberation\n"\
              "* normalize - normalizes audio\n"\
              "* rollback - returns to previous step, " \
              "you can cancel only two last steps\n"\
              "To end working:\n"\
              "* export [path to export] " \
              "[export file name with .wav or .mp3 extention]"
    print(message)


def main():
    args = parse_start_args()
    converter = WavConverter
    dir_path = os.path.dirname(__file__)
    if sys.platform == 'win32':
        dir_path = dir_path.replace("/", "\\")
    editor_start_file = os.path.join(dir_path, 'EditorFiles', 'source0.wav')
    used_files_counter = 1
    try:
        converter.convert(converter, args.audio_path, editor_start_file)
    except (FileNotFoundError, NameError) as e:
        sys.exit(e)

    editor = WavEditor(editor_start_file)
    print('Editor preparing ended, start calling commands.')
    for line in sys.stdin:
        args = line.split()
        if args[0] == 'help':
            print_help()
        elif args[0] == 'concat':
            new_source_name = os.path.join(dir_path,
                                           'EditorFiles',
                                           'source' + used_files_counter +
                                           '.wav')
            used_files_counter += 1
            try:
                converter.convert(converter, args[1], new_source_name)
            except (FileNotFoundError, NameError) as e:
                print(e)
            editor.concat(new_source_name)
        elif args[0] == 'export':
            export_name = os.path.join(args[1], args[2])
            converter.convert(converter, editor.current_state, export_name)
            editor.clear_states()
            print("Audio successfully exported, editor's work completed")
            sys.exit()
        else:
            try:
                method = getattr(editor, args[0])
                method(*args[1:])
            except RuntimeError as e:
                print(e)
    print('a')


if __name__ == '__main__':
    main()
