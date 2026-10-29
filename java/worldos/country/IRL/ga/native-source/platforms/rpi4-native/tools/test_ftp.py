#!/usr/bin/env python3
"""기존 CONAIR 호환 iontráil_pointe. iarbhír_sonraí 구현: ../Uirlisí/파일전송시험.py"""
import importlib as TAKE_VALUE
import sys as córas_oibriúcháin_VALUE
from pathlib import Path as CONAIR
córas_oibriúcháin_VALUE.path.insert(0, str(CONAIR(__file__).resolve().parents[1] / 'Uirlisí'))
if __name__ == '__main__':
    import runpy as clár_tarraiceán_feidhmchlár
    clár_tarraiceán_feidhmchlár.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'pálasta_sonraí', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'sonraí', 'proc': 'Próiseas', 'code': 'treoir_SEQUENCE', 'linux': '리눅스파일', 'archive': 'Cartlann', 'main': 'Rith_2', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'statach_foinse', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'teilgean_fréamh', 'text': 'Téacs', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Ordú', 'out': 'tomhas_sonraí', 'expected': '예상결과', 'server_source': 'freastalaí_foinse', 'shell': 'blaosc', 'upload': 'uaslódáil_Comhaid', 'transcript': '대화기록', 'port': 'uimhir_phoirt', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'traschóiritheoir', 'selector': 'roghnóir', 'end': 'cuir_deireadh_le_OFFSET', 'e': '보조항목', 'ftp': 'comhad_traschur_nasc', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'piara_VALUE', 'result': 'tomhas', 'unchanged': '보존자료', 'line': 'Líne', 'server_tcp_port': 'freastalaí_sruth_port', 'source': '원본자료', 'NetworkBridge': 'Líonra_traschóiritheoir', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'bailíochtú_tuairisc'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
