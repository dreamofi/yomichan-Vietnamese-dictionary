#yomichan Vietnamese dictionary generator

## Introduction

This is a simple script to add Vietnamese pronunciation and meaning to Yomichan English Kanjidic2 and Jmdict dictionaries from the SQLite database in ./SQLiteDB. The content of the SQLite db was obtained from open source dictionaries over the internet such as ODVP Vietnamese-Japanese dictionary.
The script was tested on a Core i5 2500 machine, 12gb Ram, running on MXLinux 18.3, Python3.7.

## Usage

Please install ray packge before running the script:

```
pip install ray setproctitle
```

Just run the yomichanViDictGenerator.py. In case you want to use the latest english dictionaries released by Yomichan, grab the zip files and extract them to relevant folders in yomichanJsonInput.

After the script finishes, locate to the index.json in 'yomichanJsonOutput/jmdict_vietnamese' and 'yomichanJsonOutput/kanjidic_vietnamese', then change the title so that the output dictionary can be imported alongside English dictionaries. For example: change the title of "JMdict (English)" to "JMDict (Vietnamese)".

Then compress the files in 'yomichanJsonOutput/jmdict_vietnamese' and 'yomichanJsonOutput/kanjidic_vietnamese' in zip format (Note: don't zip the folder, all the files must be in root directory of the zip).

If you just want the Vietnamese versions of kanjidic and jmdict, then download the files in this repo's 'vietnameseDict', then import it into Yomichan.

## Note

The script was made to fit my simple need, so it is quite barebone. As such, feel free to change it to meet your need.
