import tools
import os

_TEXT_COLLECTION_URL = 'http://web-corpora.net/bashcorpus/2011.tar.bz2'
_COMPRESSION_TYPE = '.tar.bz2'


def _file_opening():
    for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__) +
                                                             tools.download_file(_TEXT_COLLECTION_URL, _COMPRESSION_TYPE))):
        for name in files:
            if not name.startswith('.'):
                print(name)

_file_opening()