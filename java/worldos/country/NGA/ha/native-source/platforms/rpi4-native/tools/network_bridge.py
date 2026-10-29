#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/통신다리.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('통신다리', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('통신다리')
    대응 = {'response': '응답자료', 'parts': 'Hanyar_shiga_Ƙunshiyar_na_urori', 's': 'Zare_Tarin_bayani', 'i': '순번', 'close': 'Rufe', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'Mashigar_bayanai_Daraja', 'flags': 'saiti_Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango', 'ftp_port': 'Fayil_Gusar_da_lambar_kafa', 'args': 'Tubalin_aiki_TSARI', 'server': 'Saba_Daraja', 'data': 'Tarin_bayani', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': 'Mashiga_kayan_haɗi_na_kwamfuta_imel', 'rule': 'mataci_Daraja', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'sauka', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'baƙo', 'destination': 'Zangon_ƙarshe_Tarin_bayani_imel', 'ethernet_port': 'Wayar_kwamfuta_ta_yanar_gizo_fot', 'b': '둘째값', 'MAC': 'cikakken_gurbin_adireshi', 'arp': 'imel_Kyawon_tarkacen_hoto_makunshi', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Aikin_na_ura_a_kai_a_kai_Daraja', 'port': 'lambar_kafa', 'offset': 'Sassautawa_Daraja', 'readable': '읽을수있음', 'c': 'Lambar_sirrin_harafi', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'Adireshin_yanar_gizo_Daraja', 'e': '보조항목', 'n': '개수', 'packet': 'makunshi_Tarin_bayani', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': '통신다리', 'window': 'taga', 'capture': 'ɗauka'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
