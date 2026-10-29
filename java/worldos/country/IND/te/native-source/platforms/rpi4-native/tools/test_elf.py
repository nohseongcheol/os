#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/실행파일시험.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'ప్రమాణం_డేటా', 'expected': '예상결과', 'phoff': 'అనువర్తనం_శీర్షిక_ఆఫ్_సెట్', 'offset': 'ఆఫ్_సెట్_మూల్యం', 'invalid': 'చెల్లని_డేటా', 'path': 'పాత్', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'ప్రమాణం', 'format_': 'ఆకృతి_b87fd068', 'main': 'నడుపుము', 'content': 'విషయం_మూల్యం', 'source': '원본자료', 'name': 'పేరు', 'reference': 'పోలిక_ఆధారరేఖ', 'ROOT': 'ప్రొజెక్ట్_మూలం', 'value': 'మూల్యం', 'report': 'నిర్ధారణ_నివేదిక'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
