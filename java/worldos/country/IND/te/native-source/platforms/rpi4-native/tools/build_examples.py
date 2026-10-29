#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/예제빌드.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'ప్రమాణం_డేటా', 'build_examples': '예제만들기', 'files': 'ఫైలు_జాబితా', 'java': '자바실행', 'run': 'అమలు_చేయి_ఆదేశం', 'path': 'పాత్', 'p': 'డేటా_స్థాయి', 'readme': 'మార్గదర్శక_సమాచారం', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'అంశం_శోధన_సూచీ', 'classes': 'తరగతి_పథం', 'repo': 'రిపోజిటరీ_పథం', 'root': 'మూలం_ఇమెయిల్', 'content': 'విషయం_మూల్యం', 'source': '원본자료', 'name': 'పేరు', 'target': 'లక్ష్యం', 'manifest': '꾸러미명세', 'language': 'భాష'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
