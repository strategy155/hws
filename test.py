import requests


BYTES_IN_MEGABYTES = 1024 * 1024
BYTES_IN_KILOBYTES = 1024
DEFAULT_BYTE_MULTI = 1
DEFAULT_BYTE_MULTI_MESSAGE = ' bytes'
_DEFAULT_CHUNK_SIZE = 128


def download_file(url):
    _file_requested = _get_req_obj(url)
    _local_filename = url.split('/')[-1]
    with open(_local_filename, 'wb') as _file_downloaded:
        _chunk_size = _get_size_spec_val_dic(_file_requested)['chunk-size']
        for idx, chunk in enumerate(_file_requested.iter_content(_chunk_size)):
            _download_status(idx, _chunk_size, _get_size_spec_val_dic(_file_requested))
            if chunk: # filter out keep-alive new chunks
                _file_downloaded.write(chunk)
                #_file_downloaded.flush() commented by recommendation from J.F.Sebastian
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
    _size_spec_val_dic = {'total-size': _total_size, 'byte-multi': _byte_multi, 'byte-multi-msg': _byte_multi_message ,
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


download_file('http://web-corpora.net/bashcorpus/2011.tar.bz2')
