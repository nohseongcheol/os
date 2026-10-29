#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/예제시험.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'ሓበሬታ', 'graphics_command': '그림명령', 'main': 'ኣኺድ', 'row': '행위치', 'init': '초기값', 'target': 'ዕላማ', 'ROOT': '기준', 'text': 'ጽሑፍ', 'binary': 'ጽምዳዊ', 'out': '결과자료', 'entry': 'ምእታው_ነጥቢ', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'ጀምር_ስእሊ', 'col': '열위치', 'begin': 'ጀምር_ሽፋን', 'kind': 'መደብ_ዋጋ', 'selector': 'መራፂ', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'ዓሚል', 'line': 'መስመር', 'report': 'ምርግጋፅ_ጸብጻብ', 'language': 'ቋንቋ', 'x': '가로좌표', 'start': 'ኣኺድ', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'ለኣኽ_ዝርዝር', 'payload': 'ጽዕነት_ክፍሊት_ሓበሬታ', 'proc': 'መስርሕ', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'ሽም_ሰሌዳ', 'content': 'ትሕዝቶ_ዋጋ', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ፋይል_ምእታው_ሽም', 'shell': 'ሽፋን', 'color': '색상', 'transcript': '대화기록', 'offset': 'ሽፋን_ዋጋ', 'h': '높이값', 'run': 'ተግብር_ትእዛዝ', 'c': 'ኮድ_ፊደል', 'path': 'መገዲ', 'encoding': 'እኩባት_ፊደላት', 'end': 'ኣቑም_ሽፋን', 'ftp': 'ፋይል_ምስጋር_ርክብ', 'pixels': '화소들', 'symbol': 'ምልክት_ዋጋ', 'source': '원본자료', 'name': 'ሽም', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
