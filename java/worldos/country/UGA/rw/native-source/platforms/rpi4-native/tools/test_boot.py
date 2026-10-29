#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/부팅시험.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Urusobemiyoboro_ubutumwa', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'gukora_umukoro', 'cancel': 'kureka_igikorwa', 'cmd_byte': 'ibwiriza_bayiti', 'reply': 'gusubiza', 'points': '지점들', 'server': 'seriveri_agaciro', 'data': 'amakurushingiro', 'prompt': 'integuza', 'enter': 'kwandika_851ea840', 'imported': '들여온파일', 'send': 'kohereza', 'main': 'ihuriro', 'ROOT': '기준', 'text': 'Umwandiko', 'first_gui': '첫화면', 'pixel': 'pel', 'java_class': '자바클래스', 'upload': 'gukurura_Dosiye', 'pixels_file': 'pel_dosiye', 'pixels_data': 'pel_amakurushingiro', 'edit': 'guhindura_agaciro', 'receive_until': '표시까지받기', 'selector': 'muhitamo', 'size': 'Ingano', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'umukiriya', 'line': 'umurongo', 'report': 'iyemeza_raporo', 'work': '작업경로', 'x': 'Ihuza_rya_x', 'python_checks': '파이썬검사', 'download': 'gukurura', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Inzira_a7054519', 'content': 'Ibirimo_agaciro', 'block': 'amakurushingiro_guheza', 'marker': '확인표시', 'command': 'Icyo_wifuza', 'expected': '예상결과', 'shell': 'insomamabwiriza', 'drawing': 'igishushanyo_inzira', 'f': 'dosiye_icyinjizwa', 'transcript': '대화기록', 'offset': 'Ofuseti_agaciro', 'path': 'Inzira', 'screenshot': 'guhina_mugaragaza', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_agaciro', 'cmd': '명령인수', 'name': 'Izina', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
