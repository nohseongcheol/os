#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/예제시험.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'ፋይል_ትልልፍ_የወደብ_ቁጥር', 'data': 'ውሂብ', 'graphics_command': 'ግራፊክስ_ትእዛዝ', 'main': 'ማስኬጃ', 'row': 'ረድፍ_በቦታ_አስቀመጠ', 'init': '초기값', 'target': 'ዓላማ', 'ROOT': 'አሳይ_ስር', 'text': 'ጽሁፍ', 'binary': 'ባይነሪ', 'out': 'ልኬት_ውሂብ', 'entry': 'ምዝግብ_ቦታ', 'got': '받은수', 'port': 'የወደብ_ቁጥር', 'graphics_start': 'ጀምር_ስዕል', 'col': 'አምድ_በቦታ_አስቀመጠ', 'begin': 'ጀምር_ዝንፍ', 'kind': 'ምድብ_እሴት', 'selector': 'መራጭ', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'ተገልጋይ', 'line': 'መስመር', 'report': 'ማረጋገጥ_ዘገባ', 'language': 'ቋንቋ', 'x': 'ኤክስ_አስተባባሪ', 'start': 'ማስኬጃ', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'ላክ_ዝርዝር', 'payload': 'የክፍያ_ጫና_ውሂብ', 'proc': 'ሂደቶች', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'ስም_ሰንጠረዥ', 'content': 'ይዘት_እሴት', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'ፋይል_ምዝግብ_ስም', 'shell': 'ሼል', 'color': '색상', 'transcript': '대화기록', 'offset': 'ዝንፍ_እሴት', 'h': '높이값', 'run': 'ፈጽም_ትእዛዝ', 'c': 'የቁምፊ_ኮድ', 'path': 'መተላለፊያ', 'encoding': 'የቁምፊ_ጥምር', 'end': 'ጨርስ_ዝንፍ', 'ftp': 'ፋይል_ትልልፍ_ግንኙነት', 'pixels': '화소들', 'symbol': 'ምልክት_እሴት', 'source': '원본자료', 'name': 'ስም', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
