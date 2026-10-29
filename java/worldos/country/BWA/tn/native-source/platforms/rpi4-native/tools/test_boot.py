#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/부팅시험.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Neteweke_molaetsa', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'diragatsa_Tiro', 'cancel': 'khansela_tiro', 'cmd_byte': 'Taelo_baete', 'reply': 'araba', 'points': '지점들', 'server': 'sefara_Boleng', 'data': 'tshedimosetso', 'prompt': 'kgwetlho', 'enter': 'kwadisa', 'imported': '들여온파일', 'send': 'romela', 'main': 'dirisa', 'ROOT': '기준', 'text': 'SMS', 'first_gui': '첫화면', 'pixel': 'phele', 'java_class': '자바클래스', 'upload': 'laisa_Difaele', 'pixels_file': 'phele_faele', 'pixels_data': 'phele_tshedimosetso', 'edit': 'Tseleganya_Boleng', 'receive_until': '표시까지받기', 'selector': 'setlhophi', 'size': 'lekanya', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'sedirelwa', 'line': 'Mola', 'report': 'netefatso_pego', 'work': '작업경로', 'x': 'kgokagano_ya_x', 'python_checks': '파이썬검사', 'download': 'laisolola', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Thulaganyo', 'content': 'Diteng_Boleng', 'block': 'tshedimosetso_thibela', 'marker': '확인표시', 'command': 'Taelo', 'expected': '예상결과', 'shell': 'setlhalosataelo', 'drawing': 'sethalo_tsela', 'f': 'faele_tsenyo', 'transcript': '대화기록', 'offset': 'Baya_ka_Tekatekanyo_Boleng', 'path': 'tsela', 'screenshot': 'pontsho_ya_sekerine', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'moela_Boleng', 'cmd': '명령인수', 'name': 'leina', 'qmp': '모의제어접속'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
