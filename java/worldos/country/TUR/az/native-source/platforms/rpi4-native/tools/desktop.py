#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/iş_masası_baxmaq.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('iş_masası_baxmaq', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('iş_masası_baxmaq')
    대응 = {'count': 'daxiletmə_COUNT', 'special': '특수글쇠', 'error': 'XƏTA', 'exact': 'EXACT_VALUE', 'network': 'Şəbəkə', 'closed': '닫힘', 'length': 'uzunluq_VALUE', 'opened': '열림', 'ftp_port': '파일전송접속번호', 'server': 'server_VALUE', 'resources': 'Resurslar', 'data': 'verilənlər', 'shift': 'SHIFT_düyməsi', 'send': 'göndərmək', 'run_desktop': 'icra_iş_masası', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'host', 'text': 'Mətn', 'korean': '한글여부', 'port': '접속번호', 'signum': '신호번호', 'version': 'versiya_nömrəsi', 'parser': 'parser', 'bridge': 'körpü', 'kind': 'sahə_VALUE', 'tail': '끝부분', 'size': 'Böyüklük', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_koordinat', 'prefix': '앞부분', 'client': 'müştəri', 'char': 'simvol_verilənlər_4d9f8719', 'work': '작업경로', 'Keyboard': 'klaviatura', 'x': 'x_koordinatı', 'down': '누르는중', 'net': 'Şəbəkə_körpü_daxiletmə', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'arqument_ARRAY', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Proses', 'Desktop': 'QOŞUN_iş_masası', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'Əmr', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'Cığır', 'cp': 'simvol_kodlaşdırma', 'terminate': '종료시키기', 'security': 'Təhlükəsizlik', 'vnc_port': '원격화면접속번호', 'body': 'əsas_mətn', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'Açar_simvol', 'output': '출력결과', 'keyboard': 'klaviatura_daxiletmə', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'oxucu', 'NetworkBridge': 'Şəbəkə_körpü', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
