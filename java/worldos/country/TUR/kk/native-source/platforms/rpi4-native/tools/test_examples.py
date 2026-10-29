#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/예제시험.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'файл_тасымалдау_порт_нөмірі', 'data': 'деректер', 'graphics_command': 'графика_пәрмен', 'main': 'Орындау_2', 'row': 'жол_лауазым', 'init': '초기값', 'target': 'мақсатты_мән', 'ROOT': 'жоба_түбір', 'text': 'Мәтін', 'binary': 'екілік', 'out': 'өлшем_деректер', 'entry': 'енгізу_ұпай', 'got': '받은수', 'port': 'порт_нөмірі', 'graphics_start': 'басы_сызба', 'col': 'баған_лауазым', 'begin': 'басы_жылжыту', 'kind': 'Санат_мән', 'selector': 'селектор', 'n': '개수', 'key': '누름값', 'y': 'Y_түймешігі_координата', 'client': 'клиент', 'line': 'Жол', 'report': 'тексерім_есеп', 'language': 'Тіл', 'x': 'x_координатасы', 'start': 'Орындау_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'жіберу_Тізім', 'payload': 'жүктеме_деректер', 'proc': 'Үрдіс', 'w': '너비값', 'temporary': '임시자원', 'echo': 'экранға_шығару_сервер_енгізу', 'label': 'аты_кесте', 'content': 'мазмұн_мән', 'argument': '전달값', 'EchoServers': 'экранға_шығару_Серверлер', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'файл_енгізу_аты', 'shell': 'қоршам', 'color': '색상', 'transcript': '대화기록', 'offset': 'жылжыту_мән_450fc799', 'h': '높이값', 'run': 'орындау_пәрмен', 'c': 'таңба_коды', 'path': 'Жол_2', 'encoding': 'таңбалар_жиыны', 'end': 'тоқтату_жылжыту', 'ftp': 'файл_тасымалдау_қосылым', 'pixels': '화소들', 'symbol': 'символ_мән', 'source': '원본자료', 'name': 'Аты', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
