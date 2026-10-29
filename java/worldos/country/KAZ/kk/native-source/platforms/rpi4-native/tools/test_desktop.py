#!/usr/bin/env python3
"""기존 Жол_2 호환 енгізу_ұпай. нақты_деректер 구현: ../Құралдар/바탕화면시험.py"""
import importlib as 가져오기
import sys as операциялық_жүйе_мән
from pathlib import Path as Жол_2
операциялық_жүйе_мән.path.insert(0, str(Жол_2(__file__).resolve().parents[1] / 'Құралдар'))
if __name__ == '__main__':
    import runpy as бағдарлама_іске_қосу_құралы
    бағдарлама_іске_қосу_құралы.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_координатасы', 'typing': '글자입력', 'message': '알림문', 'start': 'Орындау_2', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': 'басу_Кілт', 'rectangles': '사각형들', 'sym': 'символ', 'j': '안쪽순번', 'deadline': 'ең_соңғы_мерзім_уақыт', 'proc': 'Үрдіс', 'data': 'деректер', 'main': 'Орындау_2', 'w': '너비값', 'init': '초기값', 'block': 'деректер_блогы', 'ROOT': 'жоба_түбір', 'text': 'Мәтін', 'marker': '확인표시', 'report': 'тексерім_есеп', 'until': '까지', 'clipboard': 'аралық_сақтағыш_мән', 'dst': 'тағайындау_мекенжай', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'порт_нөмірі', 'offset': 'жылжыту_мән_450fc799', 'h': '높이값', 'src': '원본주소', 'event': 'Оқиға', 'encoding': 'таңбалар_жиыны', 'size': 'Өлшемі', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_түймешігі_координата', 'output': '출력결과', 'symbol': 'символ_мән', 'client': 'клиент', 'char': 'символдық_деректер', 'rgb': '빛삼원색'}
    for 이전, ток_элемент in 대응.items():
        if hasattr(구현, ток_элемент): globals()[이전] = getattr(구현, ток_элемент)
