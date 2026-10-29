#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    susiejimas_VALUE = {'timeout': '시간제한', 'payload': 'mokamoji_krova_duomenys', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'duomenys', 'proc': 'Procesas', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'Archyvas', 'main': 'Paleisti', 'net_source': 'NET_šaltinis', 'temporary': '임시자원', 'static_source': '정적원문', 'java_source': '자바원문', 'echo': 'aidas_serveris_įrašas', 'ROOT': 'Project_šaknis', 'text': 'Tekstas', 'marker': 'žymeklis', 'EchoFixture': '되돌림시험서버', 'command': 'Komanda', 'out': 'KR_duomenys', 'expected': '예상결과', 'server_source': 'serveris_šaltinis', 'shell': 'apvalkalas', 'upload': 'Upload_Failai', 'transcript': 'transkribavimas', 'port': 'prievado_numeris', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': 'serveris_paketų_kelio_schema_jungtis', 'packed': '묶인자료', 'bridge': 'tiltas', 'selector': 'išrinkiklis', 'end': 'baigti_pokalbį_OFFSET', 'e': '보조항목', 'ftp': 'failo_perdavimas_ryšys', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'lygiavertis_mazgas_VALUE', 'result': 'REZULTATAS', 'unchanged': '보존자료', 'line': 'Eilutė', 'server_tcp_port': 'serveris_Stream_jungtis', 'source': '원본자료', 'NetworkBridge': 'tiltas_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'gauti_žinutė', 'report': 'tikrinimas_pranešti'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
