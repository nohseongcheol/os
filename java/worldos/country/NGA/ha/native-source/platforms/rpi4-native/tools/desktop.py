#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/destof_s.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('destof_s', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('destof_s')
    대응 = {'count': '항목수', 'special': '특수글쇠', 'error': 'Kuskure', 'exact': '정확한값', 'network': 'Hanyar_sadarwa', 'closed': '닫힘', 'length': 'Tsawo_Daraja', 'opened': '열림', 'ftp_port': 'Fayil_Gusar_da_lambar_kafa', 'server': 'Saba_Daraja', 'resources': 'Albarkatu', 'data': 'Tarin_bayani', 'shift': 'Makullin_matsawas', 'send': 'Aika', 'run_desktop': 'Gudanar_da_destof', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'sauka', 'text': 'SMS', 'korean': '한글여부', 'port': 'lambar_kafa', 'signum': '신호번호', 'version': '판번호', 'parser': 'tatsar_manhaja', 'bridge': '연결다리', 'kind': 'ɓangare_Daraja', 'tail': '끝부분', 'size': 'Girma', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Maɓallin_Y_Mai_tsarawa', 'prefix': '앞부분', 'client': 'abokin_hulda', 'char': 'Harafi_Tarin_bayani', 'work': '작업경로', 'Keyboard': 'kibod', 'x': 'gamayyar_x', 'down': '누르는중', 'net': '통신다리항목', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'Tubalin_aiki_TSARI', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'haryar_aikin_na_ura', 'Desktop': 'HAƊI_destof', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'Sauya_yanayin_aiki', 'command': 'Umarni', 'sock': '소켓', 'frame': '실행틀', 'ctrl': 'CTRL', 'path': 'Hanyar_shiga', 'cp': 'Harafi_Juyar_da_bayanai_zuwa_lamba', 'terminate': '종료시키기', 'security': 'Tsaro', 'vnc_port': '원격화면접속번호', 'body': 'Gundarin_zube', 'index': '색인', 'exited': '종료됨', 'keysym': 'Makulli_alama', 'output': '출력결과', 'keyboard': 'kibod_Mashigar_bayanai', 'interrupted': '가로채기됨', 'listener': '수신창구', 'reader': 'Manazarci', 'NetworkBridge': '통신다리', 'gui': '그림화면', 'worker': '처리작업'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
