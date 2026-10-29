#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/부팅시험.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'ማሕበራዊ_ኔትወርክ_መልእኽቲ', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'ተግብር_ዕማም', 'cancel': 'ግደፍ_ስርሒት', 'cmd_byte': 'ትእዛዝ_ባይት', 'reply': 'መልስ', 'points': '지점들', 'server': 'ኣገልጋሊ_ዋጋ', 'data': 'ሓበሬታ', 'prompt': 'ናይ_ቀጽል_ምልክት', 'enter': 'የእትው_851ea840', 'imported': '들여온파일', 'send': 'ለኣኽ', 'main': 'ኣኺድ', 'ROOT': '기준', 'text': 'ጽሑፍ', 'first_gui': '첫화면', 'pixel': 'ንጣብ', 'java_class': '자바클래스', 'upload': 'ስቐል_ፋይላት', 'pixels_file': 'ንጣብ_ፋይል', 'pixels_data': 'ንጣብ_ሓበሬታ', 'edit': 'ምዕራይ_ዋጋ', 'receive_until': '표시까지받기', 'selector': 'መራፂ', 'size': 'መጠን', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'ዓሚል', 'line': 'መስመር', 'report': 'ምርግጋፅ_ጸብጻብ', 'work': '작업경로', 'x': '가로좌표', 'python_checks': '파이썬검사', 'download': 'ምውራድ', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'መስርሕ', 'content': 'ትሕዝቶ_ዋጋ', 'block': 'ሓበሬታ_ምዕጋት', 'marker': '확인표시', 'command': 'ትእዛዝ', 'expected': '예상결과', 'shell': 'ሽፋን', 'drawing': 'ስእሊ_መገዲ', 'f': 'ፋይል_ምእታው', 'transcript': '대화기록', 'offset': 'ሽፋን_ዋጋ', 'path': 'መገዲ', 'screenshot': 'ምንፃል_መርዓዪ', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ወሓዚ_ዋጋ', 'cmd': '명령인수', 'name': 'ሽም', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
