#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/Inethiwekhi_ibhulorho.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('Inethiwekhi_ibhulorho', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Inethiwekhi_ibhulorho')
    대응 = {'response': '응답자료', 'parts': 'indlela_inxenye_yento', 's': 'uluhlu_lweekharektha_iingcombolo', 'i': '순번', 'close': 'Vala', 'forward': '전달규칙', 'slip_input': '직렬전문입력', 'self': '자신', 'item': 'ufako_nkcukacha_ixabiso', 'flags': '설정비트', 'ftp_port': '파일전송접속번호', 'args': 'isiniki_myalelo_ULUHLU', 'server': 'iseva_ixabiso', 'data': 'iingcombolo', 'ethernet_input': '이더넷입력', 'trace_packet': 'ithreyisi_ipakethe', 'GATEWAY': '관문기계주소', 'rule': 'umgaqo_ixabiso', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'umsingathi', 'ack': '확인번호', 'serial_port': '직렬접속번호', 'readers': '읽기대상들', 'guest': 'undwendwe', 'destination': 'indawo_ekuyiwa_kuyo_iingcombolo_idilesi', 'ethernet_port': 'i_Ithanethi_iphothi', 'b': '둘째값', 'MAC': 'umatshini_idilesi', 'arp': 'idilesi_isisombululo_ipakethe', 'writable': '쓸수있음', 'direction': '방향', 'seq': '순서번호', 'frame': '실행틀', 'loop': 'Umjikelo_ixabiso', 'port': '접속번호', 'offset': 'Ukulinganisa_ixabiso', 'readable': '읽을수있음', 'c': 'ikhowudi_yekharakhtha', 'p': '자료위치', 'writers': '쓰기대상들', 'IP': 'idilesi_yeintanethi_ixabiso', 'e': '보조항목', 'n': '개수', 'packet': 'ipakethe_iingcombolo', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'Inethiwekhi_ibhulorho', 'window': 'i_window', 'capture': 'bamba'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
