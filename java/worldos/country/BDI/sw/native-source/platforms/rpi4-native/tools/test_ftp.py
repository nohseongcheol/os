#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/파일전송시험.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'data_muhimu_data', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'data', 'proc': 'Mchakato', 'code': 'agizo_MFUATANO', 'linux': '리눅스파일', 'archive': 'Hifadhi_eb6be19d', 'main': 'endesha', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'tuli_chanzo', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'SMS', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'amri', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'seva_chanzo', 'shell': 'sheli', 'upload': 'pakia_Faili', 'transcript': '대화기록', 'port': 'namba_ya_kituo', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'daraja', 'selector': 'kiteuzi', 'end': 'tamatia_Chipua', 'e': '보조항목', 'ftp': 'faili_hamisha_muunganisho', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'kompyuta_rika_thamani', 'result': '결과', 'unchanged': '보존자료', 'line': 'laini', 'server_tcp_port': 'seva_Stream_kituo', 'source': '원본자료', 'NetworkBridge': 'Mtandao_daraja', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'uhakikishi_ripoti'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
