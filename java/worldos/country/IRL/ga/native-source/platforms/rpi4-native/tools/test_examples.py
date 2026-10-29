#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/예제시험.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    대응 = {'count': 'iontráil_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': 'comhad_traschur_uimhir_phoirt', 'data': 'sonraí', 'graphics_command': 'grafaic_ordú', 'main': 'Rith_2', 'row': 'ró_suíomh', 'init': '초기값', 'target': 'sprioc', 'ROOT': 'teilgean_fréamh', 'text': 'Téacs', 'binary': 'dénártha', 'out': 'tomhas_sonraí', 'entry': 'iontráil_pointe', 'got': 'RECEIVED_COUNT', 'port': 'uimhir_phoirt', 'graphics_start': 'Start_líníocht', 'col': 'colún_suíomh', 'begin': 'Start_OFFSET', 'kind': 'catagóir_VALUE', 'selector': 'roghnóir', 'n': 'mír_COUNT', 'key': '누름값', 'y': '세로좌표', 'client': 'cliant', 'line': 'Líne', 'report': 'bailíochtú_tuairisc', 'language': 'Teanga', 'x': 'x_chomhordanáid', 'start': 'Rith_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'seol_Liosta', 'payload': 'pálasta_sonraí', 'proc': 'Próiseas', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'ainm_tábla', 'content': 'Inneachar_VALUE', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'comhad_iontráil_ainm', 'shell': 'blaosc', 'color': '색상', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'run': 'Rith_ordú', 'c': 'pointe_cóid', 'path': 'CONAIR', 'encoding': 'tacar_carachtar', 'end': 'cuir_deireadh_le_OFFSET', 'ftp': 'comhad_traschur_nasc', 'pixels': '화소들', 'symbol': 'siombail_VALUE', 'source': '원본자료', 'name': 'Ainm', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
