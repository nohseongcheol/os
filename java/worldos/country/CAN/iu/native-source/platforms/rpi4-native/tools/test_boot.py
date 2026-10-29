#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/부팅시험.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Kasuqatigiitsimajut_titiqqausiaq', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': '실행하기', 'cancel': 'qujanaarli_aulattiniq', 'cmd_byte': 'piqujijjut_byte', 'reply': '응답', 'points': '지점들', 'server': 'ikiaqqitittivik_atuutilik', 'data': 'titiqqat', 'prompt': 'inattijjut', 'enter': 'naqilli', 'imported': '들여온파일', 'send': 'nassiutili', 'main': '시작', 'ROOT': '기준', 'text': 'titiqqaq', 'first_gui': '첫화면', 'pixel': 'pel', 'java_class': '자바클래스', 'upload': '올리기', 'pixels_file': 'pel_ini', 'pixels_data': 'pel_titiqqat', 'edit': 'aaqqigiarli_atuutilik', 'receive_until': '표시까지받기', 'selector': '준비선택기', 'size': 'anininga', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'pijittiqtaq', 'line': 'titikutaak', 'report': 'naammannirainiq_unikkaaq', 'work': '작업경로', 'x': '가로좌표', 'python_checks': '파이썬검사', 'download': 'minaq', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Pivallianiq', 'content': 'Ilulingit_atuutilik', 'block': 'titiqqat_sapummili', 'marker': '확인표시', 'command': 'piqujijjut', 'expected': '예상결과', 'shell': 'piqujijjutiliriji', 'drawing': 'titiraujarniq_aqqut', 'f': 'ini_Iliniku', 'transcript': '대화기록', 'offset': '변위', 'path': 'aqqut', 'screenshot': '화면갈무리', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ingirrania_aulataup_atuutilik', 'cmd': '명령인수', 'name': 'atiq', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
