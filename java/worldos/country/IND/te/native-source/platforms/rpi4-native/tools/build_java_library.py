#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'శీర్షిక_మూల్యం', 'sources': '원문목록', 'i': '순번', 'info': 'సిస్టమ్_సమాచారం', 'payload': 'చెల్లింపుభారం_డేటా', 'src': '원본주소', 'run': 'అమలు_చేయి_ఆదేశం', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'తరగతి_పథం', 'dist': '배포경로', 'archive': 'ఆర్కైవ్', 'output': '출력결과', 'root': 'మూలం_ఇమెయిల్', 'name': 'పేరు', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
