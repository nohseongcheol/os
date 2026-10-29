#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/부팅시험.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'నెట్_వర్క్_సందేశం', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'అమలుపరుచు', 'cancel': 'రద్దు_ఆపరేషన్', 'cmd_byte': 'ఆదేశం_బైట్', 'reply': 'ప్రత్యుత్తరం_ఇవ్వు', 'points': '지점들', 'server': 'సర్వర్_మూల్యం', 'data': 'డేటా', 'prompt': 'ప్రాంప్ట్', 'enter': 'ప్రవేశపెట్టు', 'imported': '들여온파일', 'send': 'పంపు', 'main': 'నడుపుము', 'ROOT': 'ప్రొజెక్ట్_మూలం', 'text': 'పాఠ్యము', 'first_gui': '첫화면', 'pixel': 'పెల్', 'java_class': '자바클래스', 'upload': 'అప్_లోడ్_ఫైల్_లు', 'pixels_file': 'పెల్_ఫైలు', 'pixels_data': 'పెల్_డేటా', 'edit': 'సంకలనంచేయు_మూల్యం', 'receive_until': '표시까지받기', 'selector': 'సెలక్టర్', 'size': 'పరిమాణం', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': 'Y_బటన్_సమన్వయపరుచు', 'result': 'ప్రమాణం', 'samples': '예제들', 'client': 'క్లయింట్', 'line': 'పంక్తి', 'report': 'నిర్ధారణ_నివేదిక', 'work': '작업경로', 'x': 'x_నిర్దేశాంకం', 'python_checks': '파이썬검사', 'download': 'దిగుమతి', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'క్రమణం', 'content': 'విషయం_మూల్యం', 'block': 'డేటా_నిరోధించు', 'marker': '확인표시', 'command': 'ఆదేశము', 'expected': '예상결과', 'shell': 'షెల్', 'drawing': 'రేఖాచిత్రణ_పథం', 'f': 'ఫైలు_ప్రవేశం', 'transcript': '대화기록', 'offset': 'ఆఫ్_సెట్_మూల్యం', 'path': 'పాత్', 'screenshot': 'స్క్రీన్_షాట్', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ధార_మూల్యం', 'cmd': '명령인수', 'name': 'పేరు', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
