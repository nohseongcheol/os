#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/예제시험.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'ఫైలు_బదిలీ_పోర్ట్_సంఖ్య', 'data': 'డేటా', 'graphics_command': 'గ్రాఫిక్స్_ఆదేశం', 'main': 'నడుపుము', 'row': 'వరుస_స్థాయి', 'init': '초기값', 'target': 'లక్ష్యం', 'ROOT': 'ప్రొజెక్ట్_మూలం', 'text': 'పాఠ్యము', 'binary': 'బైనరీ', 'out': 'ప్రమాణం_డేటా', 'entry': 'ప్రవేశం_పాయింట్', 'got': '받은수', 'port': 'పోర్ట్_సంఖ్య', 'graphics_start': 'ప్రారంభం_రేఖాచిత్రణ', 'col': 'కాలమ్_స్థాయి', 'begin': 'ప్రారంభం_ఆఫ్_సెట్', 'kind': 'వర్గం_మూల్యం', 'selector': 'సెలక్టర్', 'n': '개수', 'key': '누름값', 'y': 'Y_బటన్_సమన్వయపరుచు', 'client': 'క్లయింట్', 'line': 'పంక్తి', 'report': 'నిర్ధారణ_నివేదిక', 'language': 'భాష', 'x': 'x_నిర్దేశాంకం', 'start': 'నడుపుము', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'పంపు_జాబితా', 'payload': 'చెల్లింపుభారం_డేటా', 'proc': 'క్రమణం', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'పేరు_పట్టిక', 'content': 'విషయం_మూల్యం', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ఫైలు_ప్రవేశం_పేరు', 'shell': 'షెల్', 'color': '색상', 'transcript': '대화기록', 'offset': 'ఆఫ్_సెట్_మూల్యం', 'h': '높이값', 'run': 'అమలు_చేయి_ఆదేశం', 'c': 'అక్షర_కోడ్', 'path': 'పాత్', 'encoding': 'అక్షర_సమితి', 'end': 'ముగించు_ఆఫ్_సెట్', 'ftp': 'ఫైలు_బదిలీ_కనెక్షన్', 'pixels': '화소들', 'symbol': 'చిహ్నం_మూల్యం', 'source': '원본자료', 'name': 'పేరు', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
