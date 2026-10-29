#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/창시험.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'kgokagano_ya_x', 's': 'dikwalwa_tshedimosetso', 'xy': 'sebedi_sa_dintlhakopanyi', 'sel': 'setlhophi_a916db4e', 'seconds': '초단위', 'log': 'rekota_mola', 'at': '현재위치', 'send': 'romela', 'main': 'dirisa', 'req': '요청값', 'hot': 'tlhabanyetso_Boleng', 'pump': 'mokgwakamogelo_tiragalo', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'Taelo', 'shell': 'setlhalosataelo', 'f': 'faele_tsenyo', 'color': '색상', 'click': 'tobetsa_konopo', 'k': '셋째순번', 'c': 'khoutuletshwao', 'r': '반환값', 'p': '자료위치', 'done': '완료량', 'end': 'kgaola_Baya_ka_Tekatekanyo', 'command_mode': 'Taelo_mokgwa', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': '결과', 'report': 'netefatso_pego', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
