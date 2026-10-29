#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': 'video_münasibət', 'msg': 'Şəbəkə_mesaj', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'icra_etmək_tapşırıq', 'cancel': 'imtina_etmək_əməliyyat', 'cmd_byte': 'əmr_bayt', 'reply': 'cavab', 'points': '지점들', 'server': 'server_VALUE', 'data': 'verilənlər', 'prompt': 'dəvət', 'enter': 'daxil_etmək', 'imported': '들여온파일', 'send': 'göndərmək', 'main': 'İcra_Et', 'ROOT': 'Project_kök', 'text': 'Mətn', 'first_gui': '첫화면', 'pixel': 'piksel', 'java_class': '자바클래스', 'upload': 'Upload_Fayllar', 'pixels_file': 'piksel_fayl', 'pixels_data': 'piksel_verilənlər', 'edit': 'redaktə_VALUE', 'receive_until': '표시까지받기', 'selector': 'seçici', 'size': 'Böyüklük', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': 'Y_koordinat', 'result': 'ölçü', 'samples': '예제들', 'client': 'müştəri', 'line': 'Giriş', 'report': 'yoxlama_hesabat', 'work': '작업경로', 'x': 'x_koordinatı', 'python_checks': '파이썬검사', 'download': 'yüklə', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Proses', 'content': 'Məzmun_VALUE', 'block': 'verilənlər_blokla', 'marker': '확인표시', 'command': 'Əmr', 'expected': '예상결과', 'shell': 'örtük', 'drawing': 'rəsm_yol', 'f': 'fayl_daxiletmə', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'path': 'Cığır', 'screenshot': 'ekran_şəkli', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'axın_VALUE', 'cmd': '명령인수', 'name': 'Ad', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
