#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Líonra_teachtaireacht', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Rith', 'cancel': 'Cealaigh_oibríocht', 'cmd_byte': 'ordú_beart', 'reply': 'freagair', 'points': '지점들', 'server': 'freastalaí_VALUE', 'data': 'sonraí', 'prompt': 'leid', 'enter': 'iontráil', 'imported': '들여온파일', 'send': 'seol', 'main': 'Rith_2', 'ROOT': 'teilgean_fréamh', 'text': 'Téacs', 'first_gui': '첫화면', 'pixel': 'picteilín', 'java_class': '자바클래스', 'upload': 'uaslódáil_Comhaid', 'pixels_file': 'picteilín_comhad', 'pixels_data': 'picteilín_sonraí', 'edit': 'cuir_in_eagar_VALUE', 'receive_until': '표시까지받기', 'selector': 'roghnóir', 'size': 'Méid', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': '세로좌표', 'result': 'tomhas', 'samples': '예제들', 'client': 'cliant', 'line': 'Líne', 'report': 'bailíochtú_tuairisc', 'work': '작업경로', 'x': 'x_chomhordanáid', 'python_checks': '파이썬검사', 'download': 'íoslódáil', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Próiseas', 'content': 'Inneachar_VALUE', 'block': 'sonraí_bac', 'marker': '확인표시', 'command': 'Ordú', 'expected': '예상결과', 'shell': 'blaosc', 'drawing': 'líníocht_cosán', 'f': 'comhad_iontráil', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'path': 'CONAIR', 'screenshot': 'gearrthóg_scáileáin', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'sruth_VALUE', 'cmd': '명령인수', 'name': 'Ainm', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
