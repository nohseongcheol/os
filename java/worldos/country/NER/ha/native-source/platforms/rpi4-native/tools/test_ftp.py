#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/파일전송시험.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'Kumshinbayanai_Tarin_bayani', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'Tarin_bayani', 'proc': 'haryar_aikin_na_ura', 'code': 'Sharadi_JERI', 'linux': '리눅스파일', 'archive': 'Rumbun_ajiya', 'main': 'Tafiyar_da', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'Tsaye_cik_tushe', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'SMS', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Umarni', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'Saba_tushe', 'shell': 'Mai_fayyace_umani', 'upload': 'lodawa_Fayiloli', 'transcript': '대화기록', 'port': 'lambar_kafa', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': '연결다리', 'selector': 'mai_zabe', 'end': 'Ƙarshe_Sassautawa', 'e': '보조항목', 'ftp': 'Fayil_Gusar_da_haɗi', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'Fiya_Daraja', 'result': '결과', 'unchanged': '보존자료', 'line': 'Layi', 'server_tcp_port': 'Saba_watsuwa_fot', 'source': '원본자료', 'NetworkBridge': '통신다리', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'amincewa_Rahoto'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
