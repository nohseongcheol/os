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
from 꾸러미중계 import pakej_repositori, nyahmampat
from laksanakan_perintah import projek_akar


def ujian_roda(Nama, 파일들, kes_VALUE='Root-Is-Purelib: true\n', 의존성=''):
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as pakej:
        pakej.writestr(Nama + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + kes_VALUE)
        pakej.writestr(Nama + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Nama + '\nVersion: 1.0\n' + 의존성)
        for LALUAN, Kandungan_VALUE in 파일들.items():
            pakej.writestr(LALUAN, Kandungan_VALUE)
    return data.getvalue()


def cek_hos():
    정상 = ujian_roda('jkoros-fixture', {'mod.py': 'VALUE=42\n'})
    assert nyahmampat('jkoros_fixture-1.0-py3-none-any.whl', 정상, 'jkoros-fixture', '1.0') == {'mod.py': 'VALUE=42\n'.encode()}
    for data in (
            ujian_roda('jkoros-fixture', {'../escape.py': ''}),
            ujian_roda('jkoros-fixture', {'/abs.py': ''}),
            ujian_roda('jkoros-fixture', {'big.py': 'x' * 16385}),
            ujian_roda('jkoros-fixture', {'mod.so': ''}),
            ujian_roda('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            ujian_roda('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            nyahmampat('jkoros_fixture-1.0-py3-none-any.whl', data, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel LALUAN·Saiz·C sambungan_VALUE·의존성 tolak_VALUE')


def 빈접속번호():
    with socket.socket() as 소켓:
        소켓.bind(('127.0.0.1', 0))
        return 소켓.getsockname()[1]


def Jalan():
    penghurai_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    penghurai_48ee4b1b.add_argument('--host-only', action='store_true')
    인수 = penghurai_48ee4b1b.parse_args()
    cek_hos()
    if 인수.host_only:
        return
    ukuran_laluan = projek_akar/'build/verification/pip'
    ukuran_laluan.mkdir(parents=True, exist_ok=True)
    Storan_laluan = ukuran_laluan/'cache'
    Storan_laluan.mkdir(exist_ok=True)
    # sebenar_data PyPI 배포 Fail. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    pakej_repositori(projek_akar/'build/pip-cache').Sediakan('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(projek_akar/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Storan_laluan/('micropython-bisect==3.3.3'+꼬리)))
    실물기록 = json.loads((Storan_laluan/'micropython-bisect==3.3.3.json').read_text())
    assert 실물기록['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Nama, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,나):\n return 가+나\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'VALUE=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        data = ujian_roda(Nama, 파일들)
        (Storan_laluan/(Nama+'==1.0.archive')).write_bytes(data)
        (Storan_laluan/(Nama+'==1.0.json')).write_text(json.dumps({'name': Nama, 'version': '1.0',
            'filename': Nama.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(data).hexdigest()}))
    sahkan = {'passed': False, 'kernel_sha256': hashlib.sha256((projek_akar/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 실물기록, 'checks': []}
    nombor_port = 빈접속번호()
    Proses = subprocess.Popen(['python3', str(projek_akar/'alat/laksanakan_perintah.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(nombor_port), '--pip-cache', str(Storan_laluan), '--ftp-port', str(빈접속번호())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector()
    선택기.register(Proses.stdout, selectors.EVENT_READ)
    대화기록 = bytearray()
    def 기다리기(tayang_VALUE=b'jkoros-native> '):
        Kandungan_VALUE = bytearray()
        끝 = time.monotonic()+120
        while tayang_VALUE not in Kandungan_VALUE:
            if time.monotonic() > 끝 or Proses.poll() is not None:
                raise AssertionError('게스트 balas 없음: '+Kandungan_VALUE.decode('utf-8','replace'))
            for pemasukan_VALUE, _ in 선택기.select(.1):
                조각 = pemasukan_VALUE.fileobj.read(4096)
                Kandungan_VALUE.extend(조각)
                대화기록.extend(조각)
        return Kandungan_VALUE.decode('utf-8', 'replace').replace('\r\n','\n')
    def cangkerang(Perintah, tayang_VALUE=b'jkoros-native> '):
        Proses.stdin.write(Perintah.encode()+b'\n')
        Proses.stdin.flush()
        return 기다리기(tayang_VALUE)
    def laksanakan_perintah(Perintah, 예상, status_VALUE=0):
        Kandungan_VALUE = cangkerang(Perintah)
        assert 예상 in Kandungan_VALUE and '\nexit '+str(status_VALUE)+'\n' in Kandungan_VALUE, Kandungan_VALUE
        sahkan['checks'].append(Perintah)
        return Kandungan_VALUE
    def Upload_Fail(Nama, data):
        cangkerang('load '+Nama, b'hex> ')
        for jawatan_INDEX in range(0, len(data), 64):
            cangkerang(data[jawatan_INDEX:jawatan_INDEX+64].hex(), b'hex> ')
        assert 'LOADED' in cangkerang('.')
    try:
        기다리기()
        laksanakan_perintah('pip --help', 'MicroPython sumber_pepohon 설치기')
        Upload_Fail('오류시험.py', (projek_akar/'ujian/PYTHON/한국어오류시험.py').read_bytes())
        laksanakan_perintah('python 오류시험.py', 'Melayu Fail pengecualian tentu_sahkan')
        laksanakan_perintah('pip install micropython-bisect==3.3.3 --port '+str(nombor_port), 'pasang_VALUE 완료: micropython-bisect 3.3.3')
        laksanakan_perintah('python -c \'from bisect import insort as 순서대로넣기; VALUE=[1,5]; 순서대로넣기(VALUE,3); print(VALUE)\'', '[1, 3, 5]')
        laksanakan_perintah('python -m pip list', 'micropython-bisect 3.3.3')
        laksanakan_perintah('pip install micropython-bisect==3.3.3 --port '+str(nombor_port), '이미 설치됨:')
        laksanakan_perintah('pip install jkoros-fixture==1.0 --port '+str(nombor_port), 'pasang_VALUE 완료: jkoros-fixture')
        laksanakan_perintah('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        laksanakan_perintah('pip install jkoros-syntax==1.0 --port '+str(nombor_port), 'pakej RALAT:', 1)
        laksanakan_perintah('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 RALAT 보존")\'', '구문 RALAT 보존')
        Upload_Fail('공간시험.py', (projek_akar/'ujian/PYTHON/pakej_ruang_nama_ujian.py').read_bytes())
        laksanakan_perintah('python 공간시험.py '+str(nombor_port), 'pakej e_mel_rantau 부족 kembalikan_penghubung tentu_sahkan')
        laksanakan_perintah('pip uninstall jkoros-fixture', 'alih_keluar_pemasukan 완료: jkoros-fixture')
        laksanakan_perintah('pip uninstall micropython-bisect', 'alih_keluar_pemasukan 완료: micropython-bisect')
        laksanakan_perintah('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("alih_keluar_pemasukan tentu_sahkan")\'', 'alih_keluar_pemasukan tentu_sahkan')
        sahkan['passed'] = True
        print('PASS: PyPI 실물 pasang_VALUE·import·laksanakan_perintah, Melayu pengecualian, 패키지 direktori_VALUE, kegagalan_VALUE kembalikan_penghubung, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Keluar_aplikasi 키로 QEMU를 끝내면 실행기의 중계 문맥도 정리된다.
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
        선택기.close()
        Proses.stdin.close()
        Proses.stdout.close()
        (ukuran_laluan/'serial.log').write_bytes(대화기록)
        (ukuran_laluan/'report.json').write_text(json.dumps(sahkan, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    Jalan()
