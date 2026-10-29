#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/అమలు_చేయి_ఫైలు.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('అమలు_చేయి_ఫైలు', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('అమలు_చేయి_ఫైలు')
    대응 = {'timeout': '시간제한', 's': 'అక్షరసరం_డేటా', 'i': '순번', 'match': '일치', 'files': 'ఫైలు_జాబితా', 'program': 'అనువర్తనం', 'executable': '실행가능파일', 'args': 'కారకం_శ్రేణి', 'chunk': '조각', 'data': 'డేటా', 'proc': 'క్రమణం', 'send': 'పంపు', 'main': 'నడుపుము', 'marker': '확인표시', 'command': 'ఆదేశము', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'అమలు_చేయి_ఆదేశం', 'p': 'డేటా_స్థాయి', 'parser': 'పార్సర్', 'options': 'ఐచ్ఛికాలు', 'kind': 'వర్గం_మూల్యం', 'selector': 'సెలక్టర్', 'upload_data': 'అప్_లోడ్_డేటా', 'end': 'ముగించు_ఆఫ్_సెట్', 'n': '개수', 'd': 'గమ్యం_డేటా', 'key': '누름값', 'output': '출력결과', 'line': 'పంక్తి', 'name': 'పేరు', 'upload_name': 'అప్_లోడ్_పేరు', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
