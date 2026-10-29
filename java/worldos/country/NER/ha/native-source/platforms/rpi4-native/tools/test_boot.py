#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/부팅시험.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Hanyar_sadarwa_imel', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'gudanar_aiki', 'cancel': 'Soke_aiki', 'cmd_byte': 'Umarni_bayit', 'reply': 'mayar_da_martani', 'points': '지점들', 'server': 'Saba_Daraja', 'data': 'Tarin_bayani', 'prompt': 'promt', 'enter': 'Shiga', 'imported': '들여온파일', 'send': 'Aika', 'main': 'Tafiyar_da', 'ROOT': '기준', 'text': 'SMS', 'first_gui': '첫화면', 'pixel': 'pel', 'java_class': '자바클래스', 'upload': 'lodawa_Fayiloli', 'pixels_file': 'pel_Fayil', 'pixels_data': 'pel_Tarin_bayani', 'edit': 'gyaran_Daraja', 'receive_until': '표시까지받기', 'selector': 'mai_zabe', 'size': 'Girma', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': 'Maɓallin_Y_Mai_tsarawa', 'result': '결과', 'samples': '예제들', 'client': 'abokin_hulda', 'line': 'Layi', 'report': 'amincewa_Rahoto', 'work': '작업경로', 'x': 'gamayyar_x', 'python_checks': '파이썬검사', 'download': 'zazzage', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'haryar_aikin_na_ura', 'content': 'kunshiya_Daraja', 'block': 'Tarin_bayani_bulo', 'marker': '확인표시', 'command': 'Umarni', 'expected': '예상결과', 'shell': 'Mai_fayyace_umani', 'drawing': 'zane_Hanyar_shiga', 'f': 'Fayil_Mashigar_bayanai', 'transcript': '대화기록', 'offset': 'Sassautawa_Daraja', 'path': 'Hanyar_shiga', 'screenshot': 'hoton_allo', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'watsuwa_Daraja', 'cmd': '명령인수', 'name': 'Suna', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
