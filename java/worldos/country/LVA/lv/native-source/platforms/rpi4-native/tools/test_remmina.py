#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/원격한글시험.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('원격한글시험')
    kartēšana_VALUE = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Palaist', 'profile': 'Profils', 'focused': 'Svarīgie', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'serveris_VALUE', 'log': 'LOG_RECORD', 'args': 'arg_ARRAY', 'deadline': 'izpildes_termiņš_TIME', 'data': 'dati', 'candidate': '후보', 'logs': '기록들', 'kw': 'nosaukts_arguments', 'number': '수치', 'main': 'Palaist', 'ready': '준비완료', 'found': 'Meklēt_mērs', 'guest': 'viesis', 'ROOT': 'Project_sakne', 'marker': 'marķieris', 'text': 'Teksts', 'out': 'mērs_dati', 'env': '환경', 'f': 'Fails_ievade', 'port': 'porta_numurs', 'offset': 'Nobīde_VALUE', 'version': 'versijas_numurs', 'p': 'dati_amats', 'selector': 'atlasītājs', 'xvfb': '가상표시장치', 'display': 'displejs', 'n': 'krājums_COUNT', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'Nosaukums', 'window': 'Logs', 'report': 'validācija_ziņot', 'work': '작업경로'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
