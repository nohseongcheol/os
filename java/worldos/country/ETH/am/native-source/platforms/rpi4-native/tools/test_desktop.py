#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/바탕화면시험.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'ኤክስ_አስተባባሪ', 'typing': '글자입력', 'message': '알림문', 'start': 'ማስኬጃ', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'ምልክት_ad6f1a96', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'ሂደቶች', 'data': 'ውሂብ', 'main': 'ማስኬጃ', 'w': '너비값', 'init': '초기값', 'block': 'ውሂብ_አግድ', 'ROOT': 'አሳይ_ስር', 'text': 'ጽሁፍ', 'marker': '확인표시', 'report': 'ማረጋገጥ_ዘገባ', 'until': '까지', 'clipboard': 'ትግበራ_እሴት', 'dst': 'መድረሻ_አድራሻ', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'የወደብ_ቁጥር', 'offset': 'ዝንፍ_እሴት', 'h': '높이값', 'src': '원본주소', 'event': 'ፍጻሜ', 'encoding': 'የቁምፊ_ጥምር', 'size': 'መጠን', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'ምልክት_እሴት', 'client': 'ተገልጋይ', 'char': 'ቁምፊ_ውሂብ', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
