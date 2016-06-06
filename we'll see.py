import urllib.request
import urllib.response
import urllib.error
import sys
import os
import tarfile


_BYTES_IN_MEGABYTES = 1024 * 1024
_TEXT_COLLECTION_URL = 'http://web-corpora.net/bashcorpus/2011.tar.bz2'


def extract_tar_bz2_compressed(file_name):
    with tarfile.open(file_name, "r") as _compressed_file:
        _compressed_file.extractall()


def _choosing_file_to_annotate():




