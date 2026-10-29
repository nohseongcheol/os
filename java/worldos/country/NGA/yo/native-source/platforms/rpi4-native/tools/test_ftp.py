#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/파일전송시험.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'ojúlówó_détà_détà', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'détà', 'proc': 'Ìlànà', 'code': 'ìtọ́sọ́nà_ÀTẸ̀LÉRA', 'linux': '리눅스파일', 'archive': 'Ìpamọ_ọlọ́jọ́pípẹ́', 'main': 'Rọ́ọ̀nù', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'ìdágún_orísun', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': '기준', 'text': 'SMS', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'Àṣẹ', 'out': '결과자료', 'expected': '예상결과', 'server_source': 'apèsè_orísun', 'shell': 'ṣẹ́ẹ̀lì', 'upload': 'fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì', 'transcript': '대화기록', 'port': '접속번호', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'afará', 'selector': 'olùyàn', 'end': 'parí_Ìtayọ', 'e': '보조항목', 'ftp': 'fáìlì_ṣàgbélọ_Ìsomọ́', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'ọ̀gbà_iye', 'result': '결과', 'unchanged': '보존자료', 'line': 'ìlà', 'server_tcp_port': 'apèsè_Stream_ojú', 'source': '원본자료', 'NetworkBridge': 'Alásopọ̀_afará', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'Àfọwọ́sí_ìjábọ̀'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
