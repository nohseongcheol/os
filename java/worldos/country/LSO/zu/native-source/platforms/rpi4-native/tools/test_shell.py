#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/셸시험.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'okuxhumanisa_u_x', 'msg': 'iNethiwekhi_umlayezo', 'i': '순번', 'reply': 'phendula', 'call': '호출', 'args': 'i_agumenti_AMALUNGU_AFANAYO', 'chunk': '조각', 'data': 'imininingwane', 'proc': 'Inqubo', 'long_text': '긴글', 'restored': '복원자료', 'send': 'Thumela', 'file': 'Ihele', 'main': 'Sebenzisa', 'found': '찾은결과', 'ROOT': '기준', 'text': 'Itekisi', 'marker': '확인표시', 'command': 'Umlayelo', 'expected': '예상결과', 'pixel': 'i_pel', 'shell': 'isihumushi_miyalelo', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'yekisa_I_ofisethi', 'image': 'isithombe', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'iklayenti', 'line': 'umugqa', 'stream': 'Stream_inani', 'name': 'Igama', 'value': 'inani', 'receive': '수신하기', 'report': 'ukufakazisa_umbiko', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
