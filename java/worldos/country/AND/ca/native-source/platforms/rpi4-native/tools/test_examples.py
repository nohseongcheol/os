#!/usr/bin/env python3
"""기존 Camí 호환 introducció_p. real_dades 구현: ../Eines/예제시험.py"""
import importlib as PREN_VALOR
import sys as sistema_operatiu_VALOR
from pathlib import Path as Camí
sistema_operatiu_VALOR.path.insert(0, str(Camí(__file__).resolve().parents[1] / 'Eines'))
if __name__ == '__main__':
    import runpy as programa_iniciador
    programa_iniciador.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = PREN_VALOR.import_module('예제시험')
    대응 = {'count': 'introducció_COMPT', 'exact': 'IGUAL_VALOR', 'expected_file': '예상파일', 'ftp_port': 'transferència_de_fitxers_número_de_port', 'data': 'dades', 'graphics_command': 'gràfics_ordre', 'main': 'Executa_2', 'row': 'FILA_càrrec', 'init': '초기값', 'target': 'objectiu', 'ROOT': 'Project_rel', 'text': 'SMS', 'binary': 'binari', 'out': 'mesura_dades', 'entry': 'introducció_p', 'got': 'CANTIDAD_RECIBIDA_COMPT', 'port': 'número_de_port', 'graphics_start': 'Inici_dibuix', 'col': 'COLUMNA_càrrec', 'begin': 'Inici_DESPLAÇAMENT', 'kind': 'Categoria_VALOR', 'selector': '준비선택기', 'n': 'element_COMPT', 'key': '누름값', 'y': 'Y_coordenada', 'client': 'client', 'line': 'línia', 'report': 'validació_informe', 'language': 'Idioma', 'x': 'X_coordenada', 'start': 'Executa_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'enviar_Llista', 'payload': 'càrrega_dades', 'proc': 'Procés', 'w': '너비값', 'temporary': '임시자원', 'echo': 'eco_servidor_introducció', 'label': 'nom_taula', 'content': 'contingut_VALOR', 'argument': '전달값', 'EchoServers': 'eco_Servidors', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'arxiu_introducció_nom', 'shell': 'shell', 'color': '색상', 'transcript': '대화기록', 'offset': 'DESPLAÇAMENT_VALOR', 'h': '높이값', 'run': 'Executa_ordre', 'c': 'codi_de_caràcter', 'path': 'Camí', 'encoding': 'joc_de_caràcters', 'end': 'finalitzar_DESPLAÇAMENT', 'ftp': 'transferència_de_fitxers_connexió', 'pixels': '화소들', 'symbol': 'símbol_VALOR', 'source': '원본자료', 'name': 'Nom', 'receive': 'rebre_correu', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
