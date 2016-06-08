import requests
import tarfile
import os
import pip


def install(package):
    pip.main(['install', package])


BYTES_IN_MEGABYTES = 1024 * 1024
BYTES_IN_KILOBYTES = 1024
DEFAULT_BYTE_MULTI = 1
DEFAULT_BYTE_MULTI_MESSAGE = ' bytes'
_DEFAULT_CHUNK_SIZE = 128

# TODO COMPRESSION DEPENDENCIES FUCK EM LITERALLY


def download_file(url, compression=None):
    try:
        import checksumdir
    except ImportError:
        install('checksumdir')
        import checksumdir
    _file_requested = _get_req_obj(url)
    _local_filename = url.split('/')[-1]
    try:
        if os.stat(_local_filename).st_size != _file_requested.headers.get('content-length'):
            print('dude what')
    except FileNotFoundError:
        with open(_local_filename, 'wb') as _file_downloaded:
            _chunk_size = _get_size_spec_val_dic(_file_requested)['chunk-size']
            for idx, chunk in enumerate(_file_requested.iter_content(_chunk_size)):
                _download_status(idx, _chunk_size, _get_size_spec_val_dic(_file_requested))
                if chunk:
                    _file_downloaded.write(chunk)
    extract_tar_compressed(_local_filename)
    return _local_filename


def _get_req_obj(url):
    url = url.strip('/')
    return requests.get(url, stream=True)


def _get_size_spec_val_dic(req_obj):
    _byte_multi_message = DEFAULT_BYTE_MULTI_MESSAGE
    _byte_multi = DEFAULT_BYTE_MULTI
    _chunk_size = _DEFAULT_CHUNK_SIZE
    _total_size = req_obj.headers.get('content-length')
    if type(_total_size) is not type(None) :
        _total_size = int(_total_size)
        if _total_size > 5 * BYTES_IN_MEGABYTES :
            _byte_multi = BYTES_IN_MEGABYTES
            _byte_multi_message = ' MBs'
            _chunk_size = 4096
        elif _total_size> 5 * BYTES_IN_KILOBYTES :
            _byte_multi = BYTES_IN_KILOBYTES
            _byte_multi_message = ' KBs'
            _chunk_size = 512
    _size_spec_val_dic = {'total-size': _total_size, 'byte-multi': _byte_multi, 'byte-multi-msg': _byte_multi_message,
                          'chunk-size': _chunk_size}
    return _size_spec_val_dic


def _download_status(block_num, block_size, size_spec_val_dic):
    _read_so_far = block_num * block_size
    if size_spec_val_dic['total-size'] is not None:
        _total_size = size_spec_val_dic['total-size']
        _percent_so_far = _read_so_far / _total_size
        _download_status_message = "{:.0%} {:.1f} / {:.1f}".format(_percent_so_far,
                                                                   _read_so_far / size_spec_val_dic['byte-multi'],
                                                                   _total_size / size_spec_val_dic['byte-multi'])
    else:
        _download_status_message = "{:}".format(_read_so_far/size_spec_val_dic['byte-multi'])
    print('\r' + _download_status_message + size_spec_val_dic['byte-multi-msg'] + " downloaded.", end='')
    return None


def extract_tar_compressed(file_name):
    with tarfile.open(file_name, "r") as _compressed_file:
        _compressed_file.extractall()
    return None
