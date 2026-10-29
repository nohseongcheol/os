#!/usr/bin/env python3
"""기존 sökväg_2 호환 startpunkt. verklig_data implementation: ../verktyg/Dator_vy.py"""
import importlib as TA_värde
import sys as operativsystem_värde
from pathlib import Path as sökväg_2
operativsystem_värde.path.insert(0, str(sökväg_2(__file__).resolve().parents[1] / 'verktyg'))
if __name__ == '__main__':
    import runpy as app_Startbild
    app_Startbild.run_module('Dator_vy', run_name='__main__', alter_sys=True)
else:
    implementation = TA_värde.import_module('Dator_vy')
    mappning_värde = {'count': 'post_ANTAL', 'special': '특수글쇠', 'error': 'fel', 'exact': 'EXAKT_värde', 'network': 'nätverk', 'closed': 'informationsteknik_stängd', 'length': 'längd_värde', 'opened': '열림', 'ftp_port': 'filöverföring_portnummer', 'server': 'server_värde', 'resources': 'Resurser', 'data': 'data', 'shift': 'SKIFT_tangenten', 'send': 'skicka', 'run_desktop': 'köra_Dator', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'värd', 'text': 'text', 'korean': '한글여부', 'port': 'portnummer', 'signum': 'signal_nummer', 'version': 'versionsnummer', 'parser': 'parser', 'bridge': 'brygga', 'kind': 'område_värde', 'tail': '끝부분', 'size': 'Storlek', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_koordinat', 'prefix': 'avstånd_del', 'client': 'klient', 'char': 'teckendata', 'work': '작업경로', 'Keyboard': 'tangentbord', 'x': 'x_koordinat', 'down': '누르는중', 'net': 'brygga_post', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_MATRIS', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Process', 'Desktop': 'ANSLUT_Dator', 'buttons': '단추들', 'thread': 'arbete', 'pressed': '눌림', 'previous': 'Föregående', 'toggle': 'byta_läge', 'command': 'kommando', 'sock': 'socket_värde', 'frame': 'körning_ram', 'ctrl': 'CTRL', 'path': 'sökväg_2', 'cp': 'teckenkodning', 'terminate': 'avsluta', 'security': 'Säkerhet', 'vnc_port': '원격화면접속번호', 'body': 'brödtext', 'index': 'LETAUPP_INDEX', 'exited': '종료됨', 'keysym': 'Nyckel_symbol', 'output': 'utleverans', 'keyboard': 'tangentbord_post', 'interrupted': '가로채기됨', 'listener': 'få_port', 'reader': 'Läsare', 'NetworkBridge': 'brygga_3de4fe3a', 'gui': 'ritning_skärmbild', 'worker': 'bearbetning_uppgift'}
    for Föregående_objekt, aktuellt_objekt in mappning_värde.items():
        if hasattr(implementation, aktuellt_objekt): globals()[Föregående_objekt] = getattr(implementation, aktuellt_objekt)
