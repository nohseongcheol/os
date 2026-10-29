#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/바탕화면시험.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('바탕화면시험')
    대응 = {'x': 'X_coordenada', 'typing': '글자입력', 'message': '알림문', 'start': 'Executar_2', 'down': '누르는중', 'exact': 'EXACTO_VALOR', 'i': '순번', 'press': 'pulsar_Chave', 'rectangles': '사각형들', 'sym': 'símbolo', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Proceso', 'data': 'datos', 'main': 'Executar_2', 'w': '너비값', 'init': '초기값', 'block': 'datos_bloquear', 'ROOT': 'Project_raíz', 'text': 'Texto', 'marker': '확인표시', 'report': 'validación_informe', 'until': '까지', 'clipboard': 'portapapeis_VALOR', 'dst': 'destino_ENDEREZO', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'número_do_porto', 'offset': 'DESPRAZAMENTO_VALOR', 'h': '높이값', 'src': '원본주소', 'event': 'Evento', 'encoding': 'conxunto_de_caracteres', 'size': 'Tamaño', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_coordenada', 'output': '출력결과', 'symbol': 'símbolo_VALOR', 'client': 'cliente', 'char': 'carácter_datos', 'rgb': '빛삼원색'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
