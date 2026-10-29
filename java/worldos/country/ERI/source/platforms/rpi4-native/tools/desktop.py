#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/ዴስክቶፕ_ትርኢት.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('ዴስክቶፕ_ትርኢት', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ዴስክቶፕ_ትርኢት')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'ጌጋ', 'exact': '정확한값', 'network': 'ማሕበራዊ_ኔትወርክ', 'closed': '닫힘', 'length': 'ንውሓት_ዋጋ', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'ኣገልጋሊ_ዋጋ', 'resources': 'ጸጋታት', 'data': 'ሓበሬታ', 'shift': 'SHIFT_መፍትሕ', 'send': 'ለኣኽ', 'run_desktop': 'ኣኺድ_ዴስክቶፕ', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'አዐንግድ', 'text': 'ጽሑፍ', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': '연결다리', 'kind': 'መደብ_ዋጋ', 'tail': '끝부분', 'size': 'መጠን', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'ዓሚል', 'char': 'ፊደል_ሓበሬታ', 'work': '작업경로', 'Keyboard': 'ናይ_መፍትሕ_ሰሌዳ', 'x': '가로좌표', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'ሓባሪ_ቁጽሪ_ተርታ', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'መስርሕ', 'Desktop': 'ኣላግብ_ዴስክቶፕ', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'ቀይር_ኹነት', 'command': 'ትእዛዝ', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'ቁጽጽር_መፍትሕ', 'path': 'መገዲ', 'cp': 'ፊደል_ምምስጣር', 'terminate': '종료시키기', 'security': 'ሓለዋ', 'vnc_port': '원격화면접속번호', 'body': 'ዋና_ጽሑፍ', 'index': '색인', 'exited': '종료됨', 'keysym': 'መፍትሕ_ምልክት', 'output': '출력결과', 'keyboard': 'ናይ_መፍትሕ_ሰሌዳ_ምእታው', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'ኣንባቢ', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
