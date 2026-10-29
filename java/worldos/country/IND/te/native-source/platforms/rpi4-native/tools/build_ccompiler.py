#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'ప్రమాణం_డేటా', 'builtins': '내장연산', 'header': 'శీర్షిక_మూల్యం', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'అమలు_చేయి_ఆదేశం', 'flags': 'నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ', 'path': 'పాత్', 'p': 'డేటా_స్థాయి', 'cc': '시언어번역기', 'obj': 'గమ్యఫైల్', 'flag': 'సెట్టింగ్_లు_మూల్యం', 'ld': '연결편집기', 'objects': 'గమ్యం_ఫైల్_లు', 'repo': 'రిపోజిటరీ_పథం', 'v': '임시값', 'upstream': 'అప్_స్ట్రీమ్', 'root': 'మూలం_ఇమెయిల్', 'assets': '탑재자료', 'source': '원본자료', 'name': 'పేరు', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
