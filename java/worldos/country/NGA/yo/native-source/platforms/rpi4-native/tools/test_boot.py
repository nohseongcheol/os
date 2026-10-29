#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/부팅시험.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Alásopọ̀_iṣé', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'ṣiṣẹ́_iṣẹ́', 'cancel': 'paá_rẹ́_ìmú_ṣiṣẹ́', 'cmd_byte': 'àṣẹ_báìtì', 'reply': 'Fèsì', 'points': '지점들', 'server': 'apèsè_iye', 'data': 'détà', 'prompt': 'ìgún_ní_kẹ́ṣẹ́', 'enter': 'ṣàtẹ̀wọlé', 'imported': '들여온파일', 'send': 'í_meèlì', 'main': 'Rọ́ọ̀nù', 'ROOT': '기준', 'text': 'SMS', 'first_gui': '첫화면', 'pixel': 'píkísẹ̀', 'java_class': '자바클래스', 'upload': 'fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì', 'pixels_file': 'píkísẹ̀_fáìlì', 'pixels_data': 'píkísẹ̀_détà', 'edit': 'ṣàtúnṣe_iye', 'receive_until': '표시까지받기', 'selector': 'olùyàn', 'size': 'Ìwọ̀n', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'aṣojú', 'line': 'ìlà', 'report': 'Àfọwọ́sí_ìjábọ̀', 'work': '작업경로', 'x': 'ibi_ìtọ́kasí_x', 'python_checks': '파이썬검사', 'download': 'gbígbà_ẹ̀dà_fáìlì', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Ìlànà', 'content': 'Àkóónú_iye', 'block': 'détà_sèdíwọ', 'marker': '확인표시', 'command': 'Àṣẹ', 'expected': '예상결과', 'shell': 'ṣẹ́ẹ̀lì', 'drawing': 'íyàwòrán_ọ̀nà', 'f': 'fáìlì_ìgbéwọlé', 'transcript': '대화기록', 'offset': 'Ìtayọ_iye', 'path': 'ọ̀nà', 'screenshot': 'aṣòdiwọ̀n_agbàwòrán', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_iye', 'cmd': '명령인수', 'name': 'Orúkọ', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
