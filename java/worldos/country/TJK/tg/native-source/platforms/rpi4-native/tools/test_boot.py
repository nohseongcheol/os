#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/부팅시험.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Шабака_паём', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Иҷро_кардан', 'cancel': 'бекор_кардан_кор', 'cmd_byte': 'фармон_байт', 'reply': 'ҷавоб_додан', 'points': '지점들', 'server': 'сервер_қимат', 'data': 'иттилоот', 'prompt': 'сатри_фармон', 'enter': 'ворид_кардан', 'imported': '들여온파일', 'send': 'фиристодан', 'main': 'порча', 'ROOT': '기준', 'text': 'Матн', 'first_gui': '첫화면', 'pixel': 'пиксел', 'java_class': '자바클래스', 'upload': 'бор_кардан_Файлҳо', 'pixels_file': 'пиксел_файл', 'pixels_data': 'пиксел_иттилоот', 'edit': 'таҳрир_қимат', 'receive_until': '표시까지받기', 'selector': 'интихобкунанда', 'size': 'андоза_кардан', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'муштарӣ', 'line': 'хат', 'report': 'санҷиши_эътибор_гузориш', 'work': '작업경로', 'x': 'координатаи_х', 'python_checks': '파이썬검사', 'download': 'боргирӣ', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Раванд', 'content': 'Мӯҳтаво_қимат', 'block': 'иттилоот_манъ_кардан', 'marker': '확인표시', 'command': 'фармон', 'expected': '예상결과', 'shell': 'восит', 'drawing': 'нақша_масир', 'f': 'файл_ворида', 'transcript': '대화기록', 'offset': 'Интиқолшавӣ_қимат', 'path': 'масир', 'screenshot': 'буридаи_экран', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ҷараён_қимат', 'cmd': '명령인수', 'name': 'Ном', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
