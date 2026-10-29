#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 입력·RAM 되돌림을 Asli 커널에서 검사한다."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import selectors
import shutil
import socket
import subprocess
import time
import zipfile
from 꾸러미중계 import paket_repositori, 압축풀기
from Jalankan_perintah import Tugas_akar


def 시험휠(Nama_2, 파일들, kasus_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as paket:
        paket.writestr(Nama_2 + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + kasus_VALUE)
        paket.writestr(Nama_2 + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Nama_2 + '\nVersion: 1.0\n' + 의존성)
        for jalur, Isi_VALUE in 파일들.items():
            paket.writestr(jalur, Isi_VALUE)
    return data.getvalue()


def cek_host():
    정상 = 시험휠('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert 압축풀기('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for data in (
            시험휠('jkoros-fixture', {'../escape.py': ''}),
            시험휠('jkoros-fixture', {'/abs.py': ''}),
            시험휠('jkoros-fixture', {'big.py': 'x' * 16385}),
            시험휠('jkoros-fixture', {'mod.so': ''}),
            시험휠('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            시험휠('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            압축풀기('jkoros_fixture-1.0-py3-none-any.whl', data, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel jalur·Ukuran·C ekstensi_VALUE·의존성 tolak_VALUE')


def kosong_nomor_port():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def jalankan():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--host-only', action='store_true')
    argumen = parser_48ee4b1b.parse_args()
    cek_host()
    if argumen.host_only:
        return
    KR_jalur = Tugas_akar/'build/verification/pip'
    KR_jalur.mkdir(parents=True, exist_ok=True)
    Storage_jalur = KR_jalur/'cache'
    Storage_jalur.mkdir(exist_ok=True)
    # aktual_data PyPI 배포 berkas. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    paket_repositori(Tugas_akar/'build/pip-cache').Siapkan('micropython-bisect==3.3.3')
    for ekor_VALUE in ('.archive', '.json'):
        shutil.copyfile(str(Tugas_akar/'build/pip-cache'/('micropython-bisect==3.3.3'+ekor_VALUE)), str(Storage_jalur/('micropython-bisect==3.3.3'+ekor_VALUE)))
    실물기록 = json.loads((Storage_jalur/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Nama_2, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,SECOND_operand):\n return 가+SECOND_operand\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        data = 시험휠(Nama_2, 파일들)
        (Storage_jalur/(Nama_2+'==1.0.archive')).write_bytes(data)
        (Storage_jalur/(Nama_2+'==1.0.json')).write_text(json.dumps({'name': Nama_2, 'version': '1.0',
            'filename': Nama_2.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(data).hexdigest()}))
    validasi = {'passed': False, 'kernel_sha256': hashlib.sha256((Tugas_akar/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    nomor_port = kosong_nomor_port()
    Proses = subprocess.Popen(['python3', str(Tugas_akar/'alat/Jalankan_perintah.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(nomor_port), '--pip-cache', str(Storage_jalur), '--ftp-port', str(kosong_nomor_port())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    pemilih_a916db4e = selectors.DefaultSelector()
    pemilih_a916db4e.register(Proses.stdout, selectors.EVENT_READ)
    transkrip = bytearray()
    def 기다리기(show_VALUE=b'jkoros-native> '):
        Isi_VALUE = bytearray()
        끝 = time.monotonic()+120
        while show_VALUE not in Isi_VALUE:
            if time.monotonic() > 끝 or Proses.poll() is not None:
                raise AssertionError('게스트 balas 없음: '+Isi_VALUE.decode('utf-8','replace'))
            for entri_VALUE, _ in pemilih_a916db4e.select(.1):
                조각 = entri_VALUE.fileobj.read(4096)
                Isi_VALUE.extend(조각)
                transkrip.extend(조각)
        return Isi_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def shell(perintah, show_VALUE=b'jkoros-native> '):
        Proses.stdin.write(perintah.encode()+b'\n')
        Proses.stdin.flush()
        return 기다리기(show_VALUE)
    def Jalankan_perintah(perintah, 예상, Status_VALUE=0):
        Isi_VALUE = shell(perintah)
        assert 예상 in Isi_VALUE and '\nexit '+str(Status_VALUE)+'\n' in Isi_VALUE, Isi_VALUE
        validasi['checks'].append(perintah)
        return Isi_VALUE
    def Upload_File(Nama_2, data):
        shell('load '+Nama_2, b'hex> ')
        for posisi_INDEX in range(0, len(data), 64):
            shell(data[posisi_INDEX:posisi_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in shell('.')
    try:
        기다리기()
        Jalankan_perintah('pip --help', 'MicroPython sumber_pohon 설치기')
        Upload_File('오류시험.py', (Tugas_akar/'pengujian/PYTHON/한국어오류시험.py').read_bytes())
        Jalankan_perintah('python 오류시험.py', 'Indonesia berkas pengecualian periksa')
        Jalankan_perintah('pip install micropython-bisect==3.3.3 --port '+str(nomor_port), 'instal_VALUE 완료: micropython-bisect 3.3.3')
        Jalankan_perintah('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        Jalankan_perintah('python -m pip list', 'micropython-bisect 3.3.3')
        Jalankan_perintah('pip install micropython-bisect==3.3.3 --port '+str(nomor_port), '이미 설치됨:')
        Jalankan_perintah('pip install jkoros-fixture==1.0 --port '+str(nomor_port), 'instal_VALUE 완료: jkoros-fixture')
        Jalankan_perintah('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        Jalankan_perintah('pip install jkoros-syntax==1.0 --port '+str(nomor_port), 'paket galat:', 1)
        Jalankan_perintah('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 galat 보존")\'', '구문 galat 보존')
        Upload_File('공간시험.py', (Tugas_akar/'pengujian/PYTHON/꾸러미공간시험.py').read_bytes())
        Jalankan_perintah('python 공간시험.py '+str(nomor_port), 'paket surel_wilayah 부족 kembalikan_bridge periksa')
        Jalankan_perintah('pip uninstall jkoros-fixture', 'hapus_entri 완료: jkoros-fixture')
        Jalankan_perintah('pip uninstall micropython-bisect', 'hapus_entri 완료: micropython-bisect')
        Jalankan_perintah('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("hapus_entri periksa")\'', 'hapus_entri periksa')
        validasi['passed'] = True
        print('PASS: PyPI 실물 instal_VALUE·import·Jalankan_perintah, Indonesia pengecualian, 패키지 Direktori_VALUE, kegagalan_VALUE kembalikan_bridge, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Keluar_apl 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
            Proses.stdin.write(b'\x01x')
            Proses.stdin.flush()
            Proses.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Proses.terminate()
            try:
                Proses.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Proses.kill()
                Proses.wait()
        if Proses.poll() is None:
            Proses.kill()
            Proses.wait()
        pemilih_a916db4e.close()
        Proses.stdin.close()
        Proses.stdout.close()
        (KR_jalur/'serial.log').write_bytes(transkrip)
        (KR_jalur/'report.json').write_text(json.dumps(validasi, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    jalankan()
