#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'faydalı_yük_verilənlər', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'verilənlər', 'proc': 'Proses', 'code': 'təlimat_SEQUENCE', 'linux': '리눅스파일', 'archive': 'Arxiv', 'main': 'İcra_Et', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'statik_mənbə', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'Project_kök', 'text': 'Mətn', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Əmr', 'out': 'ölçü_verilənlər', 'expected': '예상결과', 'server_source': 'server_mənbə', 'shell': 'örtük', 'upload': 'Upload_Fayllar', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'körpü', 'selector': 'seçici', 'end': 'bitirmək_OFFSET', 'e': '보조항목', 'ftp': 'fayl_ötürmə_qoşulma', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'eynisəviyyəli_VALUE', 'result': 'ölçü', 'unchanged': '보존자료', 'line': 'Giriş', 'server_tcp_port': 'server_axın_port', 'source': '원본자료', 'NetworkBridge': 'Şəbəkə_körpü', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'yoxlama_hesabat'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
