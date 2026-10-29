#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/원격한글시험.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Rọ́ọ̀nù', 'profile': 'Ìrísí_Olùlò', 'focused': 'Fojúsùn', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'apèsè_iye', 'log': 'àkọsílẹ̀_ìṣe_ìlà_ìbú', 'args': 'ágúmẹ́ntì_ÀRÉÈ', 'deadline': '마감시각', 'data': 'détà', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Rọ́ọ̀nù', 'ready': '준비완료', 'found': '찾은결과', 'guest': 'àlejò', 'ROOT': '기준', 'marker': '확인표시', 'text': 'SMS', 'out': '결과자료', 'env': '환경', 'f': 'fáìlì_ìgbéwọlé', 'port': '접속번호', 'offset': 'Ìtayọ_iye', 'version': '판번호', 'p': '자료위치', 'selector': 'olùyàn', 'xvfb': 'àfojúunúṣe_ṣàfihàn', 'display': 'aṣàfihàn', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Orúkọ', 'window': 'wínńdò', 'report': 'Àfọwọ́sí_ìjábọ̀', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
