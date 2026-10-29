#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/파일전송시험.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'ibitwarwa_amakurushingiro', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'amakurushingiro', 'proc': 'Inzira_a7054519', 'code': 'ibwiriza_URUKURIKIRANE', 'linux': '리눅스파일', 'archive': 'gushyingura', 'main': 'ihuriro', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'kitayega_inkomoko', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'Umwandiko', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Icyo_wifuza', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'seriveri_inkomoko', 'shell': 'insomamabwiriza', 'upload': 'gukurura_Dosiye', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': '연결다리', 'selector': 'muhitamo', 'end': 'kurangiza_Ofuseti', 'e': '보조항목', 'ftp': 'dosiye_iyimura_kwihuza', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'Mugenzi_agaciro', 'result': '결과', 'unchanged': '보존자료', 'line': 'umurongo', 'server_tcp_port': 'seriveri_Stream_poti', 'source': '원본자료', 'NetworkBridge': '통신다리', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'iyemeza_raporo'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
