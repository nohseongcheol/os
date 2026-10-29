#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/원격한글시험.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Sebenzisa', 'profile': 'Iphrofayili', 'focused': 'Okugxilile', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'Iseva_inani', 'log': 'loga_umugqa', 'args': 'i_agumenti_AMALUNGU_AFANAYO', 'deadline': '마감시각', 'data': 'imininingwane', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'Sebenzisa', 'ready': '준비완료', 'found': '찾은결과', 'guest': 'isivakashi', 'ROOT': '기준', 'marker': '확인표시', 'text': 'Itekisi', 'out': '결과자료', 'env': '환경', 'f': 'ifayela_okufakwayo', 'port': '접속번호', 'offset': 'I_ofisethi_inani', 'version': '판번호', 'p': '자료위치', 'selector': 'isiqoki', 'xvfb': 'utalagu_bonisa', 'display': 'isibonisi', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Igama', 'window': 'ifasitela', 'report': 'ukufakazisa_umbiko', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
