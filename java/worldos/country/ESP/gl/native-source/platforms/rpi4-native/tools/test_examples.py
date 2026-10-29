#!/usr/bin/env python3
"""기존 CAMIÑO 호환 introdución_p. real_datos 구현: ../Ferramentas/예제시험.py"""
import importlib as COLLER_VALOR
import sys as sistema_operativo_VALOR
from pathlib import Path as CAMIÑO
sistema_operativo_VALOR.path.insert(0, str(CAMIÑO(__file__).resolve().parents[1] / 'Ferramentas'))
if __name__ == '__main__':
    import runpy as apl_iniciador
    apl_iniciador.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = COLLER_VALOR.import_module('예제시험')
    대응 = {'count': 'introdución_CONTAR', 'exact': 'EXACTO_VALOR', 'expected_file': '예상파일', 'ftp_port': 'transferencia_de_ficheiros_número_do_porto', 'data': 'datos', 'graphics_command': 'gráficos_comando', 'main': 'Executar_2', 'row': 'FILA_cargo', 'init': '초기값', 'target': 'obxectivo_VALOR', 'ROOT': 'Project_raíz', 'text': 'Texto', 'binary': 'binario', 'out': 'medida_datos', 'entry': 'introdución_p', 'got': 'RECIBIDO_CONTAR', 'port': 'número_do_porto', 'graphics_start': '그림시작', 'col': 'COLUMNA_cargo', 'begin': 'START_DESPRAZAMENTO', 'kind': 'Categoría_VALOR', 'selector': '준비선택기', 'n': 'elemento_CONTAR', 'key': '누름값', 'y': 'Y_coordenada', 'client': 'cliente', 'line': 'Liña', 'report': 'validación_informe', 'language': 'Idioma', 'x': 'X_coordenada', 'start': 'Executar_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'enviar_Lista', 'payload': 'carga_datos_60367a51', 'proc': 'Proceso', 'w': '너비값', 'temporary': '임시자원', 'echo': 'eco_servidor_introdución', 'label': 'nome_táboa', 'content': 'Contido_VALOR', 'argument': '전달값', 'EchoServers': 'eco_Servidores', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'Ficheiro_introdución_nome', 'shell': 'shell', 'color': '색상', 'transcript': '대화기록', 'offset': 'DESPRAZAMENTO_VALOR', 'h': '높이값', 'run': 'executar_comando', 'c': 'código_de_carácter', 'path': 'CAMIÑO', 'encoding': 'conxunto_de_caracteres', 'end': 'finalizar_DESPRAZAMENTO', 'ftp': 'transferencia_de_ficheiros_conexión', 'pixels': '화소들', 'symbol': 'símbolo_VALOR', 'source': '원본자료', 'name': 'Nome', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, ao_corrente_elemento in 대응.items():
        if hasattr(구현, ao_corrente_elemento): globals()[이전] = getattr(구현, ao_corrente_elemento)
