#!/usr/bin/env python3
"""기존 caminho 호환 ponto_de_entrada. real_dados implementação: ../ferramentas/ponte_3de4fe3a.py"""
import importlib as PEGAR_VALOR
import sys as SO_VALOR
from pathlib import Path as caminho
SO_VALOR.path.insert(0, str(caminho(__file__).resolve().parents[1] / 'ferramentas'))
if __name__ == '__main__':
    import runpy as app_Launcher
    app_Launcher.run_module('ponte_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    implementação = PEGAR_VALOR.import_module('ponte_3de4fe3a')
    mapeamento_VALOR = {'response': 'réplica', 'parts': 'caminho_componente', 's': 'cadeia_dados', 'i': '순번', 'close': 'Fechar', 'forward': '전달규칙', 'slip_input': 'protocolo_SLIP_entrada', 'self': '자신', 'item': 'entrada_VALOR_962f286b', 'flags': 'Configuração_BITS', 'ftp_port': 'transferência_de_arquivo_número_da_porta', 'args': 'argumento_MATRIZ', 'server': 'servidor_VALOR', 'data': 'dados', 'ethernet_input': 'Ethernet_entrada', 'trace_packet': 'rastrear_pacote', 'GATEWAY': 'gateway_hardware_email', 'rule': 'regra_VALOR', 'protocol': 'rede_ABI', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'host', 'ack': '확인번호', 'serial_port': 'porta_COM_número', 'readers': '읽기대상들', 'guest': 'convidado', 'destination': 'destino_dados_email', 'ethernet_port': 'porta_de_rede', 'b': 'SEGUNDO_VALOR', 'MAC': 'endereço_real', 'arp': 'resolução_de_endereço_pacote', 'writable': 'gravável', 'direction': 'direção', 'seq': 'ordem_número', 'frame': 'execução_quadro', 'loop': 'Ciclo_VALOR', 'port': 'número_da_porta', 'offset': 'DESLOC_VALOR', 'readable': '읽을수있음', 'c': 'ponto_de_código', 'p': 'dados_cargo', 'writers': '쓰기대상들', 'IP': 'endereço_na_Internet_VALOR', 'e': '보조항목', 'n': 'item_CONT_NÚM', 'packet': 'pacote_dados', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'ponte_3de4fe3a', 'window': 'Janela', 'capture': 'Captura'}
    for Anterior_item, em_dia_item in mapeamento_VALOR.items():
        if hasattr(implementação, em_dia_item): globals()[Anterior_item] = getattr(implementação, em_dia_item)
