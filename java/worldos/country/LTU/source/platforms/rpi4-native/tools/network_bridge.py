#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/tiltas_3de4fe3a.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('tiltas_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('tiltas_3de4fe3a')
    susiejimas_VALUE = {'response': 'atsakas', 'parts': 'kelias_komponentas', 's': 'eilutė_duomenys', 'i': '순번', 'close': 'Užverti', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'įrašas_VALUE', 'flags': 'konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba', 'ftp_port': 'failo_perdavimas_prievado_numeris', 'args': 'argumentas_ARRAY', 'server': 'serveris_VALUE', 'data': 'duomenys', 'ethernet_input': '이더넷입력', 'trace_packet': 'sekti_paketas', 'GATEWAY': 'šliuzas_aparatūra_ADDRESS', 'rule': 'filtras_VALUE', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'organizuoti', 'ack': '확인번호', 'serial_port': 'COM_prievadas_numeris', 'readers': '읽기대상들', 'guest': 'svečias', 'destination': 'vieta_duomenys_ADDRESS', 'ethernet_port': 'eterneto_prievadas', 'b': 'SECOND_VALUE', 'MAC': 'absoliutusis_adresas', 'arp': 'ADDRESS_skiriamoji_geba_paketas', 'writable': '쓸수있음', 'direction': '방향', 'seq': 'tvarka_numeris', 'frame': '실행틀', 'loop': 'Ciklas_VALUE', 'port': 'prievado_numeris', 'offset': 'OFFSET_VALUE', 'readable': '읽을수있음', 'c': 'simbolio_kodas', 'p': 'duomenys_padėtis', 'writers': '쓰기대상들', 'IP': 'interneto_adresas_VALUE', 'e': '보조항목', 'n': 'prekė_COUNT', 'packet': 'paketas_duomenys', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'tiltas_3de4fe3a', 'window': 'Langas', 'capture': 'įrašyti'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
