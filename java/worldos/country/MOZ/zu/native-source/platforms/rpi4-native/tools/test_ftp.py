#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/파일전송시험.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'ukulayisha_okukhokhelwayo_imininingwane', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'imininingwane', 'proc': 'Inqubo', 'code': 'umyalelo_UKULANDELANA', 'linux': '리눅스파일', 'archive': 'londoloza', 'main': 'Sebenzisa', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'ngaguquki_umthombo', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'Itekisi', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Umlayelo', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'Iseva_umthombo', 'shell': 'isihumushi_miyalelo', 'upload': 'layisha_Amafayela', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'ibhuloho', 'selector': 'isiqoki', 'end': 'yekisa_I_ofisethi', 'e': '보조항목', 'ftp': 'ifayela_dlulisa_uxhumano', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'untanga_inani', 'result': '결과', 'unchanged': '보존자료', 'line': 'umugqa', 'server_tcp_port': 'Iseva_Stream_intuba', 'source': '원본자료', 'NetworkBridge': 'iNethiwekhi_ibhuloho', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'ukufakazisa_umbiko'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
