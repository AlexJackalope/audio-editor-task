import os
import argparse
import sys

from WavConverter import WavConverter, ConverterError
from WavEditor import WavEditor, WavEditorError


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


def setup_tools(dir_path, audio_path):
    converter = WavConverter
    WavEditor.clear_states()
    editor_start_file = os.path.join(dir_path, 'EditorFiles', 'source0.wav')
    try:
        converter.convert(converter, audio_path, editor_start_file)
    except ConverterError as e:
        sys.exit(e)

    editor = WavEditor(editor_start_file)
    return converter, editor


def get_dir_path():
    dir_path = os.path.dirname(__file__)
    if sys.platform == 'win32':
        dir_path = dir_path.replace("/", "\\")
    return dir_path


def prepare_concatenation(converter, audio_path, new_source_name):
    try:
        converter.convert(converter, audio_path, new_source_name)
    except (FileNotFoundError, NameError) as e:
        print(e)


def check_export_path(dir, filename):
    try:
        export_name = os.path.join(dir, filename)
    except IndexError:
        print('Input path to directory and desired filename')
        return None
    if not os.path.isdir(dir):
        print('Input directory does not exist')
        return None
    return export_name


def call_editor_method(editor, method_name, args):
    try:
        method = getattr(editor, method_name)
        method(*args)
    except AttributeError:
        print("No such command, print 'help' to see the list "
              "of available commands")
    except TypeError:
        print('Your input was wrong, print "help" to see hints')
    except WavEditorError as e:
        print(e)


def main():
    args = parse_start_args()
    dir_path = get_dir_path()
    converter, editor = setup_tools(dir_path, args.audio_path)
    print('Editor preparing ended, start calling commands.')

    files_counter = 1
    for line in sys.stdin:
        args = line.split()

        if args[0] == 'help':
            print_help()
        elif args[0] == 'concat':
            new_source_name = os.path.join(
                dir_path, 'EditorFiles', 'source' + files_counter + '.wav')
            prepare_concatenation(converter, args[1], new_source_name)
            files_counter += 1
            editor.concat(new_source_name)
        elif args[0] == 'export':
            export_name = check_export_path(args[1], args[2])
            if export_name is None:
                continue
            try:
                converter.convert(converter, editor.current_state, export_name)
            except ConverterError as e:
                print(e)
                continue
            WavEditor.clear_states()
            print("Audio successfully exported, editor's work completed")
            sys.exit()
        else:
            call_editor_method(editor, args[0], args[1:])
    print('a')


if __name__ == '__main__':
    main()
