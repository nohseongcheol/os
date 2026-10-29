#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/파일전송시험.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('파일전송시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일전송시험')
    대응 = {'timeout': '시간제한', 'payload': 'ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'ទិន្នន័យ', 'proc': 'ដំណើរការ', 'code': '명령열', 'linux': '리눅스파일', 'archive': 'ប័ណ្ណសារ', 'main': 'រត់', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'នឹង_ប្រភព', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'បញ្ចាំង_ឬស', 'text': 'អត្ថបទ', 'marker': '확인표시', 'EchoFixture': '되돌림시험서버', 'command': 'ពាក្យ_បញ្ជា', 'out': 'ការវាស់វែង_ទិន្នន័យ', 'expected': '예상결과', 'server_source': 'ម៉ាស៊ីនមេ_ប្រភព', 'shell': '셸', 'upload': 'បង្ហោះ_ឯកសារ', 'transcript': '대화기록', 'port': 'លេខរន្ធ', 'native': '자체실행파일', 'elf': '실행파일', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': '연결다리', 'selector': 'អ្នកជ្រើសរើស', 'end': 'បញ្ចប់_ការបែង_ភាគ', 'e': '보조항목', 'ftp': 'ឯកសារ_ផ្ទេរ_ការភ្ជាប់', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'សិទ្ធស្មើ_តំលៃ', 'result': 'ការវាស់វែង', 'unchanged': '보존자료', 'line': 'បន្ទាត់', 'server_tcp_port': 'ម៉ាស៊ីនមេ_ស្ទ្រីម_ច្រក', 'source': '원본자료', 'NetworkBridge': '통신다리', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'សុពលភាព_រាយការណ៍'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
