import urllib.request
import urllib.response
import urllib.error
import sys
import os
import tarfile


_BYTES_IN_MEGABYTES = 1024 * 1024
_TEXT_COLLECTION_URL = 'http://web-corpora.net/bashcorpus/2011.tar.bz2'


def download_file(file_url):
    _file_name = file_url.split('/')[-1]
    try:
        urllib.request.urlretrieve(file_url, _file_name, _reporthook)
    except urllib.error.URLError:
        print("Internet connection is down, try later.")
        sys.exit()
    return None


def extract_tar_bz2_compressed(file_name):
    with tarfile.open(file_name, "r") as _compressed_file:
        _compressed_file.extractall()


def _reporthook(block_num, block_size, total_size):
    _read_so_far = block_num * block_size
    if total_size > 0:
        _percent_so_far = _read_so_far / total_size
        _download_status_message = "{:.2%} {:.1f} / {:.1f}".format(_percent_so_far, _read_so_far / _BYTES_IN_MEGABYTES,
                                                 total_size / _BYTES_IN_MEGABYTES) + " megabytes downloaded"
        updating_output_row(_download_status_message)
    else:
        updating_output_row("\n read {:d}\n".format(_read_so_far))
    return None


def updating_output_row(your_message):
    sys.stdout.write('\r')
    sys.stdout.write(your_message)
    sys.stdout.flush()
    return None


def _choosing_file_to_annotate():




