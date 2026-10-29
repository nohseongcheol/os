#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/డెస్క్_టాప్_వీక్షణ.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('డెస్క్_టాప్_వీక్షణ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('డెస్క్_టాప్_వీక్షణ')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'దోషం', 'exact': '정확한값', 'network': 'నెట్_వర్క్', 'closed': '닫힘', 'length': 'పొడవు_మూల్యం', 'opened': '열림', 'ftp_port': 'ఫైలు_బదిలీ_పోర్ట్_సంఖ్య', 'server': 'సర్వర్_మూల్యం', 'resources': 'వనరులు', 'data': 'డేటా', 'shift': 'SHIFT_మీట', 'send': 'పంపు', 'run_desktop': 'అమలు_చెయ్_డెస్క్_టాప్', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'హోస్ట్', 'text': 'పాఠ్యము', 'korean': '한글여부', 'port': 'పోర్ట్_సంఖ్య', 'signum': '신호번호', 'version': '판번호', 'parser': 'పార్సర్', 'bridge': 'బ్రిడ్జ్', 'kind': 'వర్గం_మూల్యం', 'tail': '끝부분', 'size': 'పరిమాణం', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_బటన్_సమన్వయపరుచు', 'prefix': '앞부분', 'client': 'క్లయింట్', 'char': 'అక్షరం_డేటా', 'work': '작업경로', 'Keyboard': 'కీబోర్డు', 'x': 'x_నిర్దేశాంకం', 'down': '누르는중', 'net': 'నెట్_వర్క్_బ్రిడ్జ్_ప్రవేశం', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'కారకం_శ్రేణి', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'క్రమణం', 'Desktop': 'అనుసంధానించు_డెస్క్_టాప్', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'మారు_మోడ్', 'command': 'ఆదేశము', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_మీట', 'path': 'పాత్', 'cp': 'అక్షరం_సంకేతీకరణం', 'terminate': '종료시키기', 'security': 'భద్రత', 'vnc_port': '원격화면접속번호', 'body': 'ప్రధాన_పాఠం', 'index': 'అంశం_శోధన_సూచీ', 'exited': '종료됨', 'keysym': 'కీ_చిహ్నం', 'output': '출력결과', 'keyboard': 'కీబోర్డు_ప్రవేశం', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'రీడర్', 'NetworkBridge': 'నెట్_వర్క్_బ్రిడ్జ్', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
