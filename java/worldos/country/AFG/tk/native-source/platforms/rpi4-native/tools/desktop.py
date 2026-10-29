#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/iş_stoly_görkez.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('iş_stoly_görkez', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('iş_stoly_görkez')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'Hata', 'exact': '정확한값', 'network': 'Tor', 'closed': '닫힘', 'length': 'dowamlylyk_baha', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'serwer_baha', 'resources': 'Gorlar', 'data': 'maglumat', 'shift': 'SHIFT_klawişasy', 'send': 'iber', 'run_desktop': 'işe_goýber_iş_stoly', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'esasy', 'text': 'Metin', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': '판번호', 'parser': '인수해석기', 'bridge': '연결다리', 'kind': 'kategoriýa_baha', 'tail': '끝부분', 'size': 'Ululyk', 'previous_buttons': '이전단추', 'key': '누름값', 'y': '세로좌표', 'prefix': '앞부분', 'client': 'müşderi', 'char': 'nyşan_maglumat_4d9f8719', 'work': '작업경로', 'Keyboard': 'klawiatura', 'x': 'x_koordinatasy', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Proses', 'Desktop': 'Birikme_iş_stoly', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'calşyr_reje', 'command': 'buýruk', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'Ýol', 'cp': 'nyşan_kodlaşdyrma', 'terminate': '종료시키기', 'security': 'Gorag', 'vnc_port': '원격화면접속번호', 'body': 'göwre_teksti', 'index': '색인', 'exited': '종료됨', 'keysym': 'açar_nyşan', 'output': '출력결과', 'keyboard': 'klawiatura_girizmeklik', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'okyjy', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
