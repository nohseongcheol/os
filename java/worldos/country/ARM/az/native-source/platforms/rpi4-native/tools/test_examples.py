#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/예제시험.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제시험')
    대응 = {'count': 'daxiletmə_COUNT', 'exact': 'EXACT_VALUE', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'verilənlər', 'graphics_command': 'qrafik_elementlər_əmr', 'main': 'İcra_Et', 'row': 'ROW_yerinə_qoymaq', 'init': '초기값', 'target': 'hədəf', 'ROOT': 'Project_kök', 'text': 'Mətn', 'binary': 'ikili', 'out': 'ölçü_verilənlər', 'entry': 'daxiletmə_p', 'got': 'RECEIVED_COUNT', 'port': '접속번호', 'graphics_start': 'Başla_rəsm', 'col': 'sütun_yerinə_qoymaq', 'begin': 'Başla_OFFSET', 'kind': 'sahə_VALUE', 'selector': 'seçici', 'n': 'element_COUNT', 'key': '누름값', 'y': 'Y_koordinat', 'client': 'müştəri', 'line': 'Giriş', 'report': 'yoxlama_hesabat', 'language': 'Dil', 'x': 'x_koordinatı', 'start': 'İcra_Et', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'göndərmək_Siyahı', 'payload': 'faydalı_yük_verilənlər', 'proc': 'Proses', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'ad_cədvəl', 'content': 'Məzmun_VALUE', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'fayl_daxiletmə_ad', 'shell': 'örtük', 'color': '색상', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'run': 'icra_etmək_əmr', 'c': 'simvol_kodu', 'path': 'Cığır', 'encoding': 'simvol_dəsti', 'end': 'bitirmək_OFFSET', 'ftp': 'fayl_ötürmə_qoşulma', 'pixels': '화소들', 'symbol': 'simvol_VALUE', 'source': '원본자료', 'name': 'Ad', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
