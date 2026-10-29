#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Tarmoq_xabar', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Ishga_tushirish', 'cancel': 'bekor_qilish_jarrohlik', 'cmd_byte': 'buyruq_bayt', 'reply': 'javob_berish', 'points': '지점들', 'server': 'server_VALUE', 'data': 'ma_lumotlar', 'prompt': 'so_rov', 'enter': 'kiritmoq', 'imported': '들여온파일', 'send': 'yuborish', 'main': 'Bajarish', 'ROOT': 'Project_ildiz', 'text': 'Matn', 'first_gui': '첫화면', 'pixel': 'piksel', 'java_class': '자바클래스', 'upload': 'uzatmoq_Fayllar', 'pixels_file': 'piksel_fayl', 'pixels_data': 'piksel_ma_lumotlar', 'edit': 'tahrirlamoq_VALUE', 'receive_until': '표시까지받기', 'selector': 'tanlagich', 'size': 'Hajmi', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': 'Y_tugmasi_koordinat', 'result': 'o_lchov', 'samples': '예제들', 'client': 'mijoz', 'line': 'satr', 'report': 'tasdiq_hisobot', 'work': '작업경로', 'x': 'x_koordinata', 'python_checks': '파이썬검사', 'download': 'yuklamoq', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Jarayon', 'content': 'tarkib_VALUE', 'block': 'ma_lumotlar_bloklash', 'marker': '확인표시', 'command': 'Buyruq', 'expected': '예상결과', 'shell': 'qobiq', 'drawing': 'chizish_yo_l', 'f': 'fayl_kiritish', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'path': 'yo_l', 'screenshot': 'ekran_surati', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'oqim_VALUE', 'cmd': '명령인수', 'name': 'Nomi', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
