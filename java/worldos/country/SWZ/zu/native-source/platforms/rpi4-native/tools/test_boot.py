#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/부팅시험.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'iNethiwekhi_umlayezo', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'yenza_umsebenzi', 'cancel': 'khansela_umsebenzi', 'cmd_byte': 'umyalo_ibhayithi', 'reply': 'phendula', 'points': '지점들', 'server': 'Iseva_inani', 'data': 'imininingwane', 'prompt': 'ozokusebenzisa', 'enter': 'faka_851ea840', 'imported': '들여온파일', 'send': 'Thumela', 'main': 'Sebenzisa', 'ROOT': '기준', 'text': 'Itekisi', 'first_gui': '첫화면', 'pixel': 'i_pel', 'java_class': '자바클래스', 'upload': 'layisha_Amafayela', 'pixels_file': 'i_pel_ifayela', 'pixels_data': 'i_pel_imininingwane', 'edit': 'hlela_inani', 'receive_until': '표시까지받기', 'selector': 'isiqoki', 'size': 'Ubungako', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'iklayenti', 'line': 'umugqa', 'report': 'ukufakazisa_umbiko', 'work': '작업경로', 'x': 'okuxhumanisa_u_x', 'python_checks': '파이썬검사', 'download': 'ehlisa', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Inqubo', 'content': 'Okuqukethwe_inani', 'block': 'imininingwane_vimbela', 'marker': '확인표시', 'command': 'Umlayelo', 'expected': '예상결과', 'shell': 'isihumushi_miyalelo', 'drawing': 'umdwebo_umzila', 'f': 'ifayela_okufakwayo', 'transcript': '대화기록', 'offset': 'I_ofisethi_inani', 'path': 'Indlela_2', 'screenshot': 'ukuthwebula_ingxenye_yesikrini', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_inani', 'cmd': '명령인수', 'name': 'Igama', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
