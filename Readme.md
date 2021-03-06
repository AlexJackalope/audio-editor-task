# Аудиоредактор
___
Автор: Зайцева Александра
___
### Требования:
* Модуль pysndfx
* SoX в PATH
* ffmpeg в PATH
___
### Состав:
* Консольная версия ```main.py```
* Аудиоконвертер ```WavConverter.py```
* Wav-редактор ```WavEditor.py```
* Папка для хранения промежуточных обработанных файлов ```EditorFiles/```
* Тесты ```Tests/```
___
### Консольная версия:
Полная справка по команде ```help```
___
### Начало работы:
Для запуска в интерактивном режиме введите путь к редактируемому файла, для запуса 
скрипта с заранее описанными командами до пути добавьте флаг -s.
___
#### Команды:
* ```speed_chg [коэффициент]``` - изменение скорости,
* ```cut [начало в секундах] [длина отрывка в секундах]``` - вырезание фрагмента из аудио,
* ```concat [путь к другому аудио]``` - добавляет второй аудиофайл в конец данного,
* ```reverb [сила эффекта от 0 до 100]``` - эффект реверберации,
* ```normalize``` - эффект нормализации,
* ```export [путь к директории экспорта] [имя конечного файла с указанием расширения .wav или .mp3]``` - 
завершающая работу редактора команда экспорта.