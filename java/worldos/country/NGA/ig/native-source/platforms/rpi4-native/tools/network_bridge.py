#!/usr/bin/env python3
"""기존 ụzọ_ozi 호환 ndebà_akara. ǹdịnezie_datà 구현: ../Ngwaọrụ/통신다리.py"""
import importlib as 가져오기
import sys as OS_valuu
from pathlib import Path as ụzọ_ozi
OS_valuu.path.insert(0, str(ụzọ_ozi(__file__).resolve().parents[1] / 'Ngwaọrụ'))
if __name__ == '__main__':
    import runpy as app_ihengosi_ndi_app
    app_ihengosi_ndi_app.run_module('통신다리', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('통신다리')
    대응 = {'response': '응답자료', 'parts': 'ụzọ_ozi_ǹsòmebe', 's': 'ùsòròokwū_datà', 'i': '순번', 'close': 'Mechie', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ndebà_valuu', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'agụment_MKPOKỌTA', 'server': 'savà_valuu', 'data': 'datà', 'ethernet_input': '이더넷입력', 'trace_packet': '전문추적', 'GATEWAY': 'ụzọmbànye_ngwaike_àdreèsì', 'rule': 'm̀yọ̀_valuu', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'usu', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': '커널실행', 'destination': 'ebemwèga_datà_àdreèsì', 'ethernet_port': 'Etāneèt_pọọt', 'b': '둘째값', 'MAC': 'ngwa_komputa_àdreèsì', 'arp': 'àdreèsì_ụcha_ngosịpụta_ngwùgwù', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'òkirikiri_valuu', 'port': '접속번호', 'offset': 'Nnokwata_valuu', 'readable': '읽을수있음', 'c': 'koòdù_nkeakàrà', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'adreesi_ịntaneèt_valuu', 'e': '보조항목', 'n': '개수', 'packet': 'ngwùgwù_datà', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': '통신다리', 'window': 'windò', 'capture': 'See'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
