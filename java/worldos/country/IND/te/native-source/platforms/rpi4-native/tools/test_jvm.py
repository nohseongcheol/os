#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/자바가상기계시험.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'అక్షరసరం_డేటా', 'actual': 'వాస్తవ_ప్రమాణం', 'match': '일치', 'payload': 'చెల్లింపుభారం_డేటా', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'నడుపుము', 'ROOT': 'ప్రొజెక్ట్_మూలం', 'text': 'పాఠ్యము', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'తరగతి_పథం', 'output': '출력결과', 'result': 'ప్రమాణం', 'cmd': '명령인수', 'name': 'పేరు', 'jar': '자바꾸러미', 'report': 'నిర్ధారణ_నివేదిక', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
