#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/바탕화면시험.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': '가로좌표', 'typing': '글자입력', 'message': '알림문', 'start': 'ኣኺድ', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'ምልክት', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'መስርሕ', 'data': 'ሓበሬታ', 'main': 'ኣኺድ', 'w': '너비값', 'init': '초기값', 'block': 'ሓበሬታ_ምዕጋት', 'ROOT': '기준', 'text': 'ጽሑፍ', 'marker': '확인표시', 'report': 'ምርግጋፅ_ጸብጻብ', 'until': '까지', 'clipboard': 'ናይ_ቅንጣብ_ሰሌዳ_ዋጋ', 'dst': 'መዓልቦ_ኣድራሻ', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'ሽፋን_ዋጋ', 'h': '높이값', 'src': '원본주소', 'event': 'ፍጻመ', 'encoding': 'እኩባት_ፊደላት', 'size': 'መጠን', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'ምልክት_ዋጋ', 'client': 'ዓሚል', 'char': 'ፊደል_ሓበሬታ', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
