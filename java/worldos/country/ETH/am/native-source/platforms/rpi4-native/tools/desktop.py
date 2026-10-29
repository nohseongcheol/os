#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/ዴስክቶፕ_እየው.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('ዴስክቶፕ_እየው', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ዴስክቶፕ_እየው')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'ስህተት', 'exact': '정확한값', 'network': 'መረብ', 'closed': '닫힘', 'length': 'ርዝመት_እሴት', 'opened': '열림', 'ftp_port': 'ፋይል_ትልልፍ_የወደብ_ቁጥር', 'server': 'አገልጋይ_እሴት', 'resources': 'ሃብቶች', 'data': 'ውሂብ', 'shift': 'SHIFT_ቁልፍ', 'send': 'ላክ', 'run_desktop': 'አሂድ_ዴስክቶፕ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'አዘጋጅ_b78e430d', 'text': 'ጽሁፍ', 'korean': '한글여부', 'port': 'የወደብ_ቁጥር', 'signum': '신호번호', 'version': '판번호', 'parser': 'አግልሎ_ማስቀመጥ', 'bridge': 'ድልድይ', 'kind': 'ምድብ_እሴት', 'tail': '끝부분', 'size': 'መጠን', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'ተገልጋይ', 'char': 'ቁምፊ_ውሂብ', 'work': '작업경로', 'Keyboard': 'የቁልፍ_ሰሌዳ', 'x': 'ኤክስ_አስተባባሪ', 'down': '누르는중', 'net': 'መረብ_ድልድይ_ምዝግብ', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'ነጋሪ_እሴት_ድርድር', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'ሂደቶች', 'Desktop': 'አገናኝ_ዴስክቶፕ', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'ቀይር_ሁነታ', 'command': 'ትእዛዝ', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL_ቁልፍ', 'path': 'መተላለፊያ', 'cp': 'ቁምፊ_በኮድ_መክተት', 'terminate': '종료시키기', 'security': 'መድህን', 'vnc_port': '원격화면접속번호', 'body': 'የጽሁፍ_አካል', 'index': 'ፍለጋ_መረጃ_ጠቆመ', 'exited': '종료됨', 'keysym': 'ቁልፍ_ምልክት', 'output': '출력결과', 'keyboard': 'የቁልፍ_ሰሌዳ_ምዝግብ', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'አንባቢ', 'NetworkBridge': 'መረብ_ድልድይ', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
