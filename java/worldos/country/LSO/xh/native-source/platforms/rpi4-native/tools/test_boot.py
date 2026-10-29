#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/부팅시험.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Inethiwekhi_umyalezo', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'ukwenza_umsebenzi', 'cancel': 'rhoxisa_isibalo', 'cmd_byte': 'umyalelo_ibhayithi', 'reply': 'phendula', 'points': '지점들', 'server': 'iseva_ixabiso', 'data': 'iingcombolo', 'prompt': 'imo_yokulinda', 'enter': 'ngenisa', 'imported': '들여온파일', 'send': 'thumela', 'main': 'Phumeza', 'ROOT': '기준', 'text': 'Umbhalo', 'first_gui': '첫화면', 'pixel': 'i_pel', 'java_class': '자바클래스', 'upload': 'layisha_Iifayile', 'pixels_file': 'i_pel_ifayile', 'pixels_data': 'i_pel_iingcombolo', 'edit': 'hlela_ixabiso', 'receive_until': '표시까지받기', 'selector': 'umkhethi', 'size': 'Ubukhulu', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'iklayenti', 'line': 'umgca', 'report': 'uqinisekiso_ingxelo', 'work': '작업경로', 'x': 'isilungelelanisi_x', 'python_checks': '파이썬검사', 'download': 'khuphela', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Inkqubo', 'content': 'Isiqulatho_ixabiso', 'block': 'iingcombolo_thintela', 'marker': '확인표시', 'command': 'Umyalelo', 'expected': '예상결과', 'shell': 'isiniki_myalelo', 'drawing': 'umzobo_indlela', 'f': 'ifayile_ufako_nkcukacha', 'transcript': '대화기록', 'offset': 'Ukulinganisa_ixabiso', 'path': 'INDLELA', 'screenshot': 'ukuklipha_isikrini', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_ixabiso', 'cmd': '명령인수', 'name': 'Igama', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
