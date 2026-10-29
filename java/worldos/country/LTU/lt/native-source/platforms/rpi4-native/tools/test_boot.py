#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    susiejimas_VALUE = {'timeout': '시간제한', 'response': 'atsakas', 'msg': 'tinklas_žinutė', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Vykdyti', 'cancel': 'Atšaukti_operacija', 'cmd_byte': 'komanda_baitas', 'reply': 'atsakyti', 'points': '지점들', 'server': 'serveris_VALUE', 'data': 'duomenys', 'prompt': 'raginimas', 'enter': 'įvesti', 'imported': '들여온파일', 'send': 'siųsti', 'main': 'Paleisti', 'ROOT': 'Project_šaknis', 'text': 'Tekstas', 'first_gui': '첫화면', 'pixel': 'pikselis', 'java_class': '자바클래스', 'upload': 'Upload_Failai', 'pixels_file': 'pikselis_Failas', 'pixels_data': 'pikselis_duomenys', 'edit': 'redaguoti_VALUE', 'receive_until': '표시까지받기', 'selector': 'išrinkiklis', 'size': 'Dydis', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': '세로좌표', 'result': 'REZULTATAS', 'samples': '예제들', 'client': 'klientas', 'line': 'Eilutė', 'report': 'tikrinimas_pranešti', 'work': '작업경로', 'x': 'x_koordinatė', 'python_checks': '파이썬검사', 'download': 'atsisiųsti', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'terminas_TIME', 'proc': 'Procesas', 'content': 'Turinys_VALUE', 'block': 'duomenų_blokas', 'marker': 'žymeklis', 'command': 'Komanda', 'expected': '예상결과', 'shell': 'apvalkalas', 'drawing': 'piešinys_kelias', 'f': 'Failas_įrašas', 'transcript': 'transkribavimas', 'offset': 'OFFSET_VALUE', 'path': 'KELIAS', 'screenshot': 'ekrano_kopija', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': 'išeiga', 'stream': 'Stream_VALUE', 'cmd': '명령인수', 'name': 'Pavadinimas_2', 'qmp': '모의제어접속'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
