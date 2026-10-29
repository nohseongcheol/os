#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/원격한글시험.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'నడుపుము', 'profile': 'ప్రొఫైల్', 'focused': 'కేంద్రీకరించబడింది', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'సర్వర్_మూల్యం', 'log': 'లాగ్_వరుస', 'args': 'కారకం_శ్రేణి', 'deadline': '마감시각', 'data': 'డేటా', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'నడుపుము', 'ready': '준비완료', 'found': 'శోధన_ప్రమాణం', 'guest': 'అతిథి', 'ROOT': 'ప్రొజెక్ట్_మూలం', 'marker': '확인표시', 'text': 'పాఠ్యము', 'out': 'ప్రమాణం_డేటా', 'env': '환경', 'f': 'ఫైలు_ప్రవేశం', 'port': 'పోర్ట్_సంఖ్య', 'offset': 'ఆఫ్_సెట్_మూల్యం', 'version': '판번호', 'p': 'డేటా_స్థాయి', 'selector': 'సెలక్టర్', 'xvfb': 'వర్చువల్_ప్రదర్శన', 'display': 'ప్రదర్శన', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'పేరు', 'window': 'విండో', 'report': 'నిర్ధారణ_నివేదిక', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
