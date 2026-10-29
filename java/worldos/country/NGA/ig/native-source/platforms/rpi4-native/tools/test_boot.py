#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/부팅시험.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Netwọọkụ_ozi', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'mee_ọrụ', 'cancel': 'kàgbuo_àrụmọrụ', 'cmd_byte': 'nnyemiwu_baịtị', 'reply': 'nzaghachi', 'points': '지점들', 'server': 'savà_valuu', 'data': 'datà', 'prompt': 'mkpalite', 'enter': 'tinye', 'imported': '들여온파일', 'send': 'zìga', 'main': 'Bido', 'ROOT': '기준', 'text': 'SMS', 'first_gui': '첫화면', 'pixel': 'pel', 'java_class': '자바클래스', 'upload': 'bùlie_Ndi_ọbọakwụkwọ', 'pixels_file': 'pel_ọbọakwụkwọ', 'pixels_data': 'pel_datà', 'edit': 'dezìmà_valuu', 'receive_until': '표시까지받기', 'selector': 'ihe_nhọpụta', 'size': 'Ụhara', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'klayènt', 'line': 'ahịrī', 'report': 'nkwèputaonòdù_akụkọ', 'work': '작업경로', 'x': 'ngakọrịta_x', 'python_checks': '파이썬검사', 'download': 'butùo', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'ùsòrò', 'content': 'ndịnà_valuu', 'block': 'datà_gbochie', 'marker': '확인표시', 'command': 'Ntiiwu', 'expected': '예상결과', 'shell': 'nkọwannyemiwu', 'drawing': 'osise_ụzọ_ozi', 'f': 'ọbọakwụkwọ_ndebà', 'transcript': '대화기록', 'offset': 'Nnokwata_valuu', 'path': 'ụzọ_ozi', 'screenshot': 'mkpagide_ihuenyo', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'agịrị_valuu', 'cmd': '명령인수', 'name': 'Aha', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
