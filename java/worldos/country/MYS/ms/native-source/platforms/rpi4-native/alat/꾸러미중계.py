#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 pasang_VALUE·실행한다."""
import argparse
import email.parser
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import socketserver
import struct
import tarfile
import threading
import urllib.request
import zipfile

projek_akar = Path(__file__).resolve().parents[1]


def hurai_permintaan(permintaan):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', permintaan)
    if not 맞음:
        raise ValueError('pakej Nama 또는 Nama==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def sahkan_laluan(Nama, pemasangan_laluan=True):
    LALUAN = PurePosixPath(Nama)
    if LALUAN.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Nama.split('/')):
        raise ValueError('허용하지 않는 pakej LALUAN: ' + Nama)
    if '\\' in Nama or any(ord(aksara_VALUE) < 32 or ord(aksara_VALUE) == 127 for aksara_VALUE in Nama):
        raise ValueError('잘못된 pakej LALUAN 문자')
    if pemasangan_laluan and (len(('/lib/' + Nama).encode()) > 63 or Nama in ('Melayu.py', 'pakej.py')):
        raise ValueError('pakej LALUAN 제한 또는 nilai_lalai pustaka 충돌: ' + Nama)
    return Nama


def nyahmampat(fail_pemasukan_nama, data, Nama, versi_VALUE):
    파일들 = {}
    명세들 = []
    def Tambah_pemasukan(LALUAN, Kandungan_VALUE):
        sahkan_laluan(LALUAN)
        if LALUAN in 파일들:
            raise ValueError('중복 pakej LALUAN: ' + LALUAN)
        if len(Kandungan_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + LALUAN)
        Kandungan_VALUE.decode('utf-8')
        파일들[LALUAN] = Kandungan_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 sumber_pepohon 16개·합계 64 KiB 이하여야 합니다.')
    if fail_pemasukan_nama.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(data)) as pakej:
            항목들 = pakej.infolist()
            if len(항목들) > 256 or sum(pemasukan_VALUE.file_size for pemasukan_VALUE in 항목들) > 1048576:
                raise ValueError('Arkib_VALUE keluaran_Storan Saiz 제한 초과')
            kes_Senarai = [pemasukan_VALUE for pemasukan_VALUE in 항목들 if pemasukan_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(kes_Senarai) != 1:
                raise ValueError('wheel kes_VALUE 명세가 필요합니다.')
            kes_VALUE = email.parser.Parser().parsestr(pakej.read(kes_Senarai[0]).decode())
            if kes_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not fail_pemasukan_nama.endswith('-none-any.whl'):
                raise ValueError('C sambungan_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for pemasukan_VALUE in 항목들:
                LALUAN = pemasukan_VALUE.filename.rstrip('/')
                sahkan_laluan(LALUAN, False)
                if (pemasukan_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if pemasukan_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in LALUAN:
                    if LALUAN.endswith('/METADATA'):
                        명세들.append(pakej.read(pemasukan_VALUE).decode())
                    continue
                if not LALUAN.endswith('.py') or '.data/' in LALUAN:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + LALUAN)
                Tambah_pemasukan(LALUAN, pakej.read(pemasukan_VALUE))
    elif fail_pemasukan_nama.endswith('.tar.gz') and Nama.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py laksanakan_perintah 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(data), mode='r|gz') as pakej:
            뿌리들 = set()
            pemasukan_COUNT = 0
            전체크기 = 0
            for pemasukan_VALUE in pakej:
                pemasukan_COUNT += 1
                전체크기 += pemasukan_VALUE.size
                if pemasukan_COUNT > 256 or 전체크기 > 1048576:
                    raise ValueError('Arkib_VALUE keluaran_Storan Saiz 제한 초과')
                sahkan_laluan(pemasukan_VALUE.name, False)
                부분들 = pemasukan_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if pemasukan_VALUE.isdir():
                    continue
                if not pemasukan_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython sumber_pepohon 배포형')
                LALUAN = '/'.join(부분들[1:])
                Kandungan_VALUE = pakej.extractfile(pemasukan_VALUE).read()
                if LALUAN.endswith('PKG-INFO'):
                    명세들.append(Kandungan_VALUE.decode())
                elif LALUAN.endswith('.py') and LALUAN not in ('setup.py',):
                    Tambah_pemasukan(LALUAN, Kandungan_VALUE)
                elif '.egg-info/' not in LALUAN and not LALUAN.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + LALUAN)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 akar_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* sumber_pepohon 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if hurai_permintaan(명세.get('Name', ''))[0] != Nama or 명세.get('Version') != versi_VALUE:
        raise ValueError('배포 메타데이터의 Nama·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(e_mel, 한도):
    if not e_mel.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(e_mel, timeout=30) as balas:
        if not balas.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 e_mel alih_VALUE')
        data = balas.read(한도 + 1)
    if len(data) > 한도:
        raise ValueError('배포 Fail Saiz 제한 초과')
    return data


def pindah_pakej(Nama, versi_VALUE, 파일들, 출처):
    명세 = {'name': Nama, 'version': versi_VALUE, 'source': 출처, 'files': [
        {'path': LALUAN, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        for LALUAN, data in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('pakej 명세 Saiz 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[pemasukan_VALUE['path']] for pemasukan_VALUE in 명세['files'])


class pakej_repositori:
    def __init__(자신, LALUAN, teknologi_maklumat_Luar_talian=False):
        자신.LALUAN = Path(LALUAN)
        자신.LALUAN.mkdir(parents=True, exist_ok=True)
        자신.teknologi_maklumat_Luar_talian = teknologi_maklumat_Luar_talian

    def Sediakan(자신, permintaan):
        Nama, versi_VALUE = hurai_permintaan(permintaan)
        열쇠 = Nama + ('==' + versi_VALUE if versi_VALUE else '')
        LOG_laluan = 자신.LALUAN / (열쇠 + '.json')
        배포경로 = 자신.LALUAN / (열쇠 + '.archive')
        if LOG_laluan.is_file() and 배포경로.is_file():
            LOG_baris = json.loads(LOG_laluan.read_text())
            data = 배포경로.read_bytes()
            if hashlib.sha256(data).hexdigest() != LOG_baris['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.teknologi_maklumat_Luar_talian:
                raise ValueError('teknologi_maklumat_Luar_talian 저장소에 없는 pakej: ' + permintaan)
            e_mel = 'https://pypi.org/pypi/' + Nama + ('/' + versi_VALUE if versi_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(e_mel, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [pemasukan_VALUE for pemasukan_VALUE in msinfo32_exe['urls'] if not pemasukan_VALUE.get('yanked') and pemasukan_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Nama.startswith('micropython-'):
                후보 = [pemasukan_VALUE for pemasukan_VALUE in msinfo32_exe['urls'] if not pemasukan_VALUE.get('yanked') and pemasukan_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            pilihan_VALUE = 후보[0]
            data = 웹읽기(pilihan_VALUE['url'], 4194304)
            if hashlib.sha256(data).hexdigest() != pilihan_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 Fail SHA-256 불일치')
            LOG_baris = {'name': Nama, 'version': msinfo32_exe['info']['version'], 'filename': pilihan_VALUE['filename'],
                    'url': pilihan_VALUE['url'], 'sha256': pilihan_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            nyahmampat(LOG_baris['filename'], data, Nama, LOG_baris['version'])
            배포경로.write_bytes(data)
            LOG_laluan.write_text(json.dumps(LOG_baris, ensure_ascii=False, indent=2) + '\n')
        if LOG_baris['name'] != Nama or versi_VALUE and LOG_baris['version'] != versi_VALUE:
            raise ValueError('repositori_akar Nama·버전 불일치')
        파일들 = nyahmampat(LOG_baris['filename'], data, Nama, LOG_baris['version'])
        return pindah_pakej(Nama, LOG_baris['version'], 파일들, LOG_baris['url'])


class pakej_permintaan(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            permintaan = bytearray()
            while b'\n' not in permintaan and len(permintaan) < 100:
                조각 = 자신.request.recv(100 - len(permintaan))
                if not 조각:
                    return
                permintaan.extend(조각)
            if not permintaan.endswith(b'\n') or permintaan.count(b'\n') != 1:
                raise ValueError('잘못된 pakej permintaan')
            balas = 자신.server.repositori_akar.Sediakan(permintaan[:-1].decode('ascii'))
        except Exception as RALAT:
            머리 = json.dumps({'error': str(RALAT)[:500]}, ensure_ascii=False).encode()
            balas = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(balas)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, nombor_port=8027, LALUAN=None, teknologi_maklumat_Luar_talian=False):
        자신.pelayan_VALUE = socketserver.TCPServer(('127.0.0.1', nombor_port), pakej_permintaan, bind_and_activate=False)
        자신.pelayan_VALUE.allow_reuse_address = True
        자신.pelayan_VALUE.server_bind()
        자신.pelayan_VALUE.server_activate()
        자신.pelayan_VALUE.repositori_akar = pakej_repositori(LALUAN or projek_akar/'build/pip-cache', teknologi_maklumat_Luar_talian)
        자신.nombor_port = 자신.pelayan_VALUE.server_address[1]
        자신.urutan_VALUE = threading.Thread(target=자신.pelayan_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.urutan_VALUE.start()
        return 자신

    def __exit__(자신, *인수):
        자신.pelayan_VALUE.shutdown()
        자신.pelayan_VALUE.server_close()
        자신.urutan_VALUE.join(timeout=2)


def Jalan():
    penghurai_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    penghurai_48ee4b1b.add_argument('--port', type=int, default=8027)
    penghurai_48ee4b1b.add_argument('--cache', type=Path, default=projek_akar/'build/pip-cache')
    penghurai_48ee4b1b.add_argument('--offline', action='store_true')
    penghurai_48ee4b1b.add_argument('--fetch', help='laksanakan_perintah 없이 호환 배포 파일을 내려받아 검사·stor_VALUE')
    인수 = penghurai_48ee4b1b.parse_args()
    if 인수.fetch:
        data = pakej_repositori(인수.cache, 인수.offline).Sediakan(인수.fetch)
        print('pakej Sediakan 완료:', 인수.fetch, len(data), 'bait_VALUE')
        return
    with 꾸러미중계(인수.port, 인수.cache, 인수.offline) as 중계:
        print('pakej 중계: 127.0.0.1:' + str(중계.nombor_port), flush=True)
        try:
            중계.urutan_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    Jalan()
