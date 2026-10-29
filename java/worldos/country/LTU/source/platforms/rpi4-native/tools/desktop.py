#!/usr/bin/env python3
"""기존 KELIAS 호환 įrašas_p. faktinis_duomenys 구현: ../Įrankiai/darbalaukis_rodyti.py"""
import importlib as TAKE_VALUE
import sys as operacinė_sistema_VALUE
from pathlib import Path as KELIAS
operacinė_sistema_VALUE.path.insert(0, str(KELIAS(__file__).resolve().parents[1] / 'Įrankiai'))
if __name__ == '__main__':
    import runpy as programa_programų_skydelis
    programa_programų_skydelis.run_module('darbalaukis_rodyti', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('darbalaukis_rodyti')
    susiejimas_VALUE = {'count': 'įrašas_COUNT', 'special': '특수글쇠', 'error': 'KLAIDA', 'exact': 'EXACT_VALUE', 'network': 'tinklas', 'closed': 'informacinės_technologijos_uždaryta', 'length': '길이', 'opened': '열림', 'ftp_port': 'failo_perdavimas_prievado_numeris', 'server': 'serveris_VALUE', 'resources': 'Ištekliai', 'data': 'duomenys', 'shift': '윗글쇠', 'send': 'siųsti', 'run_desktop': 'vykdyti_darbalaukis', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'organizuoti', 'text': 'Tekstas', 'korean': '한글여부', 'port': 'prievado_numeris', 'signum': 'signalas_numeris', 'version': 'versijos_numeris', 'parser': 'analizatorius', 'bridge': 'tiltas', 'kind': 'sritis_VALUE', 'tail': '끝부분', 'size': 'Dydis', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'klientas', 'char': 'simbolių_duomenys', 'work': '작업경로', 'Keyboard': 'klaviatūra', 'x': 'x_koordinatė', 'down': '누르는중', 'net': 'tiltas_įrašas', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argumentas_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Procesas', 'Desktop': 'ryšys_darbalaukis', 'buttons': '단추들', 'thread': 'darbininkas', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'Komanda', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'valdymas_Raktas', 'path': 'KELIAS', 'cp': 'simbolių_koduotė', 'terminate': '종료시키기', 'security': 'Sauga', 'vnc_port': '원격화면접속번호', 'body': 'pagrindinis_tekstas', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'Raktas_simbolis', 'output': 'išeiga', 'keyboard': 'klaviatūra_įrašas', 'interrupted': '가로채기됨', 'listener': 'gauti_jungtis', 'reader': 'Skaitytuvė', 'NetworkBridge': 'tiltas_3de4fe3a', 'gui': '그림화면', 'worker': 'apdorojimas_užduotis'}
    for 이전, dabartinis_prekė in susiejimas_VALUE.items():
        if hasattr(구현, dabartinis_prekė): globals()[이전] = getattr(구현, dabartinis_prekė)
