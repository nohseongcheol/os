#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/igalaujaq_takussarurli.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('igalaujaq_takussarurli', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('igalaujaq_takussarurli')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'tammarniq', 'exact': '정확한값', 'network': 'Kasuqatigiitsimajut', 'closed': '닫힘', 'length': 'takininga_atuutilik', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'ikiaqqitittivik_atuutilik', 'resources': 'Qarasaujalirijjutit', 'data': 'titiqqat', 'shift': 'SHIFT_naqigaq', 'send': 'nassiutili', 'run_desktop': '바탕화면실행', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'tuttarvik', 'text': 'titiqqaq', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': '연결다리', 'kind': 'Ataqatigiivvik_atuutilik', 'tail': '끝부분', 'size': 'anininga', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'pijittiqtaq', 'char': 'immikkuuqtuq_titiqqat', 'work': '작업경로', 'Keyboard': 'naqittaut', 'x': '가로좌표', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'aturniqarnirainiq_array', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Pivallianiq', 'Desktop': 'kasurli_igalaujaq', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'kipulli_mode', 'command': 'piqujijjut', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'aqqut', 'cp': 'immikkuuqtuq_tukiniktiri', 'terminate': '종료시키기', 'security': 'pijjaiqsimajuq', 'vnc_port': '원격화면접속번호', 'body': 'Titiqqaup_ilulilluataa', 'index': '색인', 'exited': '종료됨', 'keysym': '글쇠기호', 'output': '출력결과', 'keyboard': 'naqittaut_Iliniku', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Uqalimaarut', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
