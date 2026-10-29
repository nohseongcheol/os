#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/부팅시험.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'መረብ_ኢሜይል', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'መፈጸሚያ', 'cancel': 'ሰርዝ_ክወና', 'cmd_byte': 'ትእዛዝ_ባይት', 'reply': 'መልስ', 'points': '지점들', 'server': 'አገልጋይ_እሴት', 'data': 'ውሂብ', 'prompt': 'ጥሪ', 'enter': 'አስገባ_851ea840', 'imported': '들여온파일', 'send': 'ላክ', 'main': 'ማስኬጃ', 'ROOT': 'አሳይ_ስር', 'text': 'ጽሁፍ', 'first_gui': '첫화면', 'pixel': 'ፒክስል', 'java_class': '자바클래스', 'upload': 'መጫን_ፋይሎች', 'pixels_file': 'ፒክስል_ፋይል', 'pixels_data': 'ፒክስል_ውሂብ', 'edit': 'አርትዕ_እሴት', 'receive_until': '표시까지받기', 'selector': 'መራጭ', 'size': 'መጠን', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': 'ልኬት', 'samples': '예제들', 'client': 'ተገልጋይ', 'line': 'መስመር', 'report': 'ማረጋገጥ_ዘገባ', 'work': '작업경로', 'x': 'ኤክስ_አስተባባሪ', 'python_checks': '파이썬검사', 'download': 'ወራጅ', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'ሂደቶች', 'content': 'ይዘት_እሴት', 'block': 'ውሂብ_አግድ', 'marker': '확인표시', 'command': 'ትእዛዝ', 'expected': '예상결과', 'shell': 'ሼል', 'drawing': 'ስዕል_ዱካ', 'f': 'ፋይል_ምዝግብ', 'transcript': '대화기록', 'offset': 'ዝንፍ_እሴት', 'path': 'መተላለፊያ', 'screenshot': 'ማያ_ቅንጠባ', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ልቀቅ_እሴት', 'cmd': '명령인수', 'name': 'ስም', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
