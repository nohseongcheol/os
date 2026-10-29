#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/부팅시험.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'mbaal_bataaxal', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'def_ligeey', 'cancel': 'Bayyi_sëfu_xayma', 'cmd_byte': 'ndigel_okte', 'reply': 'tontu', 'points': '지점들', 'server': 'dëggu_xëyma', 'data': 'mbir', 'prompt': 'xaar_jëf', 'enter': 'dugal_851ea840', 'imported': '들여온파일', 'send': 'Yónnee', 'main': 'daw', 'ROOT': '기준', 'text': 'Tekst', 'first_gui': '첫화면', 'pixel': 'piksel', 'java_class': '자바클래스', 'upload': 'toxalsi_Fisiye_yi', 'pixels_file': 'piksel_bara_denc', 'pixels_data': 'piksel_mbir', 'edit': 'soppi_xëyma', 'receive_until': '표시까지받기', 'selector': 'tànnkat', 'size': 'tolluwaay', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'lëkkalekat', 'line': 'buum', 'report': 'wéral_tënk', 'work': '작업경로', 'x': 'rëddu_iks_yi', 'python_checks': '파이썬검사', 'download': 'yebbi', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'yokkute', 'content': 'Këmb_xëyma', 'block': 'mbir_gatandu', 'marker': '확인표시', 'command': 'ndigel', 'expected': '예상결과', 'shell': 'Wëreef', 'drawing': 'deseñ_Yoonu_jëmale', 'f': 'bara_denc_dugal_xabaar', 'transcript': '대화기록', 'offset': 'Randal_xëyma', 'path': 'Yoonu_jëmale', 'screenshot': 'Jàppug_nataalu_ekaraŋ_bi', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'dawal_xëyma', 'cmd': '명령인수', 'name': 'tur_253d1510', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
