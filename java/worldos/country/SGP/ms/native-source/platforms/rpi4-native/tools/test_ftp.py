#!/usr/bin/env python3
"""기존 LALUAN 호환 titik_permulaan. sebenar_data pelaksanaan: ../alat/ujian_FTP.py"""
import importlib as TAKE_VALUE
import sys as sistem_pengendalian_VALUE
from pathlib import Path as LALUAN
sistem_pengendalian_VALUE.path.insert(0, str(LALUAN(__file__).resolve().parents[1] / 'alat'))
if __name__ == '__main__':
    import runpy as aplikasi_pelancar
    aplikasi_pelancar.run_module('ujian_FTP', run_name='__main__', alter_sys=True)
else:
    pelaksanaan = TAKE_VALUE.import_module('ujian_FTP')
    대응 = {'timeout': '시간제한', 'payload': 'muat_beban_data', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'data', 'proc': 'Proses', 'code': 'suruhan_jujukan', 'linux': '리눅스파일', 'archive': 'Arkib', 'main': 'Jalan', 'net_source': '통신원문', 'temporary': '임시자원', 'static_source': 'statik_sumber', 'java_source': '자바원문', 'echo': '되돌림서버항목', 'ROOT': 'projek_akar', 'text': 'Teks', 'marker': 'penanda', 'EchoFixture': '되돌림시험서버', 'command': 'Perintah', 'out': 'ukuran_data', 'expected': '예상결과', 'server_source': 'pelayan_sumber', 'shell': 'cangkerang', 'upload': 'Upload_Fail', 'transcript': '대화기록', 'port': 'nombor_port', 'native': 'asal', 'elf': 'fail_boleh_laku', 'server_udp_port': '서버전문접속번호', 'packed': '묶인자료', 'bridge': 'penghubung', 'selector': '준비선택기', 'end': 'tamat_Ofset', 'e': '보조항목', 'ftp': 'pemindahan_fail_hubungan', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'rakan_VALUE', 'result': 'ukuran', 'unchanged': '보존자료', 'line': 'baris', 'server_tcp_port': 'pelayan_strim_port', 'source': '원본자료', 'NetworkBridge': 'rangkaian_penghubung', 'jar': '자바꾸러미', 'receive': '수신하기', 'report': 'pensahihan_lapor'}
    for 이전, 현재 in 대응.items():
        if hasattr(pelaksanaan, 현재): globals()[이전] = getattr(pelaksanaan, 현재)
