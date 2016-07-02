import bs4
import re
import pymystem3
import os
import json
import multiprocessing
import threading
import queue
import time





def _proccess_of_annotating(distance_dict,path):
#   try:
#        with open(os.path.splitext(path)[0] + '_annotated.xml', 'r', encoding='utf-8') as _opened_notation:
#            _add_to_speed_dict(speed_dict, _opened_notation)
#    except FileNotFoundError:
    distance_dict = dict.fromkeys(distance_dict, 0)
    _annotate(path, distance_dict)
    with open(os.path.splitext(path)[0] + '_dictionary.json', 'w', encoding='utf-8') as _distance_dict_file:
        json.dump(distance_dict, _distance_dict_file, ensure_ascii=False, indent=2)
    return None

def _file_opening(distance_dict):
    threads_opened = []
    for root, dirs, files in os.walk("2011"):
        for name in files:
            if not name.startswith('.') and os.path.splitext(name)[1]=='.txt':
                path = os.path.join(root,name)
                _proccess_of_annotating(distance_dict,path)
#                threads_opened.append(threading.Thread(target=_proccess_of_annotating,args=(distance_dict,path)))


def _append_to_tag(input_object, parent_tag , child_tag):
    getattr(input_object, parent_tag).append(input_object.new_tag(child_tag))
    return None


def _transform_input_text_to_soup(name_of_text):
    _input_file_opened = open(name_of_text, encoding='utf-8')
    input_soup = bs4.BeautifulSoup(_input_file_opened, "lxml")
    _input_file_opened.close()
    return input_soup


def _output_soup_init(input_soup):
    output_soup = bs4.BeautifulSoup('', "lxml")
    output_soup.append(output_soup.new_tag("html"))
    _append_to_tag(output_soup, "html", "head")
    _append_to_tag(output_soup, "head", "title")
    output_soup.title.append(input_soup.author.string)
    _append_to_tag(output_soup, "html", "body")
    _append_to_tag(output_soup, "body", "p")
    return output_soup





def _soup_parsing(output_soup,input_soup,freq_dictionary):
    _stemmer = pymystem3.Mystem()
    _line_counter = 0
    _word_counter = -1
    _words_array = re.findall(r"[а-яА-ЯёЁ]+|\n", input_soup.text)
    _words_set = set(_words_array)
    _some_threads = []
    _word_annotation_dict = {}
    new_q = queue.Queue()
    start = time.clock()
    thread_num = 8
    for i in range(thread_num):
        t = threading.Thread(target=_get_word_annotation, args=(new_q, _word_annotation_dict, _stemmer))
        t.start()
        _some_threads.append(t)
    for word in _words_set:
        new_q.put(word)
    # for word in _words_array:
    #     if word == '\n':
    #         _line_counter += 1
    #         _append_to_tag(output_soup, "body", "p")
    #     else:
    #         _word_counter += 1
    #         t = threading.Thread(target=_add_word_with_annotation,args=(_line_counter,_word_counter,
    #                                                                   word,_stemmer,output_soup,
    #                                                                   freq_dictionary))
    #         t.start()
    #         try:
    #             freq_dictionary[word.lower()] += 1
    #         except KeyError:
    #             freq_dictionary[word.lower()] = 1
    #         _some_threads.append(t)
    new_q.join()
    for i in range(thread_num):
        new_q.put(None)
    for t in _some_threads:
        t.join()
    stop= time.clock()
    print(stop-start)
    return output_soup


def _get_word_annotation(new_q, dic,stemmer):
    while True:
        word = new_q.get()
        if word is None:
            break
        try:
            dic[word] = stemmer.analyze(word)[0]['analysis'][0]
        except KeyError:
            dic[word] = ''
        new_q.task_done()
    return None


def _add_word_with_annotation(line_num,word_num,word,stemmer,soup,freq_dictionary):
    try:

        soup.find_all("p")[line_num].append(soup.new_tag("w"))
        soup.find_all("w")[word_num].append(bs4.NavigableString(word))
        soup.find_all("w")[word_num]['lex'] = stemmer.analyze(word)[0]['analysis'][0]['lex']
        soup.find_all("w")[word_num]['gr'] = stemmer.analyze(word)[0]['analysis'][0]['gr']
    except IndexError:
        return None
    return None


def _overwrite_soup_to_file(filename, soup):
    with open(os.path.splitext(filename)[0]+'_annotated.xml','w',encoding='utf-8') as output_file:
        output_file.write(soup.prettify())


def _annotate(text_name,freq_dictionary):
    _soup = _transform_input_text_to_soup(text_name)
    _new_soup = _soup_parsing(_output_soup_init(_soup), _soup, freq_dictionary)
    _overwrite_soup_to_file(text_name, _new_soup)


if __name__ == '__main__':
    _distance_dict = {}
    _speed_dictionary = {}
    _file_opening(_distance_dict)