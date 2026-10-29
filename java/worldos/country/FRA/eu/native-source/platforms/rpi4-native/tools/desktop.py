#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/mahaigain_ikusi.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('mahaigain_ikusi', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('mahaigain_ikusi')
    대응 = {'count': 'sarrera_ZENBATU', 'special': '특수글쇠', 'error': 'errorea', 'exact': 'BERDIN_balio', 'network': 'sare', 'closed': '닫힘', 'length': 'luzera_balio', 'opened': '열림', 'ftp_port': 'fitxategi_transferitu_ataka_zenbaki', 'server': 'zerbitzari_balio', 'resources': 'Baliabideak', 'data': 'datuak', 'shift': 'MAIUS_tekla', 'send': 'bidali', 'run_desktop': 'exekutatu_mahaigain', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'Ostalari', 'text': 'Testua', 'korean': '한글여부', 'port': 'ataka_zenbaki', 'signum': '신호번호', 'version': '판번호', 'parser': 'analizatzaile', 'bridge': 'zubi', 'kind': 'Kategoria_balio', 'tail': '끝부분', 'size': 'Tamaina', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_koordenatu', 'prefix': '앞부분', 'client': 'bezero', 'char': 'karaktere_datuak', 'work': '작업경로', 'Keyboard': 'teklatu', 'x': 'X_koordenatu', 'down': '누르는중', 'net': 'sare_zubi_sarrera', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'arg_matrize', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Prozesua', 'Desktop': 'KONEKTATU_mahaigain', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'ALDATU_MODA', 'command': 'Komandoa', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'KTRL', 'path': 'Bide_izena', 'cp': 'karaktere_kodeketa', 'terminate': '종료시키기', 'security': 'segurtasun', 'vnc_port': '원격화면접속번호', 'body': 'testu_nagusi', 'index': 'BEGIRATU_INDIZE', 'exited': '종료됨', 'keysym': 'gako_ikur', 'output': '출력결과', 'keyboard': 'teklatu_sarrera', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'irakurle', 'NetworkBridge': 'sare_zubi', 'gui': '그림화면', 'worker': 'prozesatze_ataza'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
