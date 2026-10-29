#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/파일전송시험.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'càrrega_dades', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'dades', 'proc': 'Procés', 'code': 'instrucció_SEQÜÈNCIA', 'linux': '리눅스파일', 'archive': 'Arxiu', 'main': 'Executa_2', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'estàtic_font', 'java_source': '자바원문', 'echo': 'eco_servidor_introducció', 'ROOT': 'Project_rel', 'text': 'SMS', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Ordre', 'out': 'mesura_dades', 'expected': '예상결과', 'server_source': 'servidor_font', 'shell': 'shell', 'upload': 'pujar_Fitxers', 'transcript': '대화기록', 'port': 'número_de_port', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'pont', 'selector': '준비선택기', 'end': 'finalitzar_DESPLAÇAMENT', 'e': '보조항목', 'ftp': 'transferència_de_fitxers_connexió', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'homòleg_VALOR', 'result': 'RESULTAT', 'unchanged': '보존자료', 'line': 'línia', 'server_tcp_port': 'servidor_flux_port', 'source': '원본자료', 'NetworkBridge': 'xarxa_pont', 'jar': '자바꾸러미', 'receive': 'rebre_correu', 'report': 'validació_informe'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
