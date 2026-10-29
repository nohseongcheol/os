#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/파일전송시험.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'selekanyo_sa_tshedimosetso_tshedimosetso', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'tshedimosetso', 'proc': 'Thulaganyo', 'code': 'taelo_TATELANO', 'linux': '리눅스파일', 'archive': 'boloka', 'main': 'dirisa', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'e_e_emeng_Motswedi', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'SMS', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Taelo', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'sefara_Motswedi', 'shell': 'setlhalosataelo', 'upload': 'laisa_Difaele', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'leborogo', 'selector': 'setlhophi', 'end': 'kgaola_Baya_ka_Tekatekanyo', 'e': '보조항목', 'ftp': 'faele_fudusa_Kgolagano', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'semphato_Boleng', 'result': '결과', 'unchanged': '보존자료', 'line': 'Mola', 'server_tcp_port': 'sefara_moela_gorogisetsa', 'source': '원본자료', 'NetworkBridge': 'Neteweke_leborogo', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'netefatso_pego'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
