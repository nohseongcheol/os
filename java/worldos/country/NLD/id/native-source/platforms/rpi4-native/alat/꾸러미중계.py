#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost 중계. 게스트는 TCP로 받은 소스를 직접 instal_VALUE·실행한다."""
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

Tugas_akar = Path(__file__).resolve().parents[1]


def urai_permintaan(permintaan):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', permintaan)
    if not 맞음:
        raise ValueError('paket Nama_2 또는 Nama_2==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def validasi_jalur_f98b46e1(Nama_2, penginstalan_jalur=True):
    jalur = PurePosixPath(Nama_2)
    if jalur.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Nama_2.split('/')):
        raise ValueError('허용하지 않는 paket jalur: ' + Nama_2)
    if '\\' in Nama_2 or any(ord(karakter_VALUE) < 32 or ord(karakter_VALUE) == 127 for karakter_VALUE in Nama_2):
        raise ValueError('잘못된 paket jalur 문자')
    if penginstalan_jalur and (len(('/lib/' + Nama_2).encode()) > 63 or Nama_2 in ('Indonesia.py', 'paket.py')):
        raise ValueError('paket jalur 제한 또는 nilai_default pustaka 충돌: ' + Nama_2)
    return Nama_2


def 압축풀기(file_entri_nama, data, Nama_2, versi_VALUE):
    파일들 = {}
    명세들 = []
    def tambah_entri(jalur, Isi_VALUE):
        validasi_jalur_f98b46e1(jalur)
        if jalur in 파일들:
            raise ValueError('중복 paket jalur: ' + jalur)
        if len(Isi_VALUE) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + jalur)
        Isi_VALUE.decode('utf-8')
        파일들[jalur] = Isi_VALUE
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 sumber_pohon 16개·total_VALUE 64 KiB 이하여야 합니다.')
    if file_entri_nama.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(data)) as paket:
            항목들 = paket.infolist()
            if len(항목들) > 256 or sum(entri_VALUE.file_size for entri_VALUE in 항목들) > 1048576:
                raise ValueError('Arsip_VALUE lepas_Storage Ukuran 제한 초과')
            kasus_Daftar = [entri_VALUE for entri_VALUE in 항목들 if entri_VALUE.filename.endswith('.dist-info/WHEEL')]
            if len(kasus_Daftar) != 1:
                raise ValueError('wheel kasus_VALUE 명세가 필요합니다.')
            kasus_VALUE = email.parser.Parser().parsestr(paket.read(kasus_Daftar[0]).decode())
            if kasus_VALUE.get('Root-Is-Purelib', '').lower() != 'true' or not file_entri_nama.endswith('-none-any.whl'):
                raise ValueError('C ekstensi_VALUE·플랫폼 전용 wheel은 지원하지 않습니다.')
            for entri_VALUE in 항목들:
                jalur = entri_VALUE.filename.rstrip('/')
                validasi_jalur_f98b46e1(jalur, False)
                if (entri_VALUE.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if entri_VALUE.filename.endswith('/'):
                    continue
                if '.dist-info/' in jalur:
                    if jalur.endswith('/METADATA'):
                        명세들.append(paket.read(entri_VALUE).decode())
                    continue
                if not jalur.endswith('.py') or '.data/' in jalur:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + jalur)
                tambah_entri(jalur, paket.read(entri_VALUE))
    elif file_entri_nama.endswith('.tar.gz') and Nama_2.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Jalankan_perintah 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(data), mode='r|gz') as paket:
            뿌리들 = set()
            entri_COUNT = 0
            total_ukuran = 0
            for entri_VALUE in paket:
                entri_COUNT += 1
                total_ukuran += entri_VALUE.size
                if entri_COUNT > 256 or total_ukuran > 1048576:
                    raise ValueError('Arsip_VALUE lepas_Storage Ukuran 제한 초과')
                validasi_jalur_f98b46e1(entri_VALUE.name, False)
                부분들 = entri_VALUE.name.split('/')
                뿌리들.add(부분들[0])
                if entri_VALUE.isdir():
                    continue
                if not entri_VALUE.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython sumber_pohon 배포형')
                jalur = '/'.join(부분들[1:])
                Isi_VALUE = paket.extractfile(entri_VALUE).read()
                if jalur.endswith('PKG-INFO'):
                    명세들.append(Isi_VALUE.decode())
                elif jalur.endswith('.py') and jalur not in ('setup.py',):
                    tambah_entri(jalur, Isi_VALUE)
                elif '.egg-info/' not in jalur and not jalur.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + jalur)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 akar_VALUE 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* sumber_pohon 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 배포 메타데이터가 필요합니다.')
    spes = email.parser.Parser().parsestr(명세들[0])
    if urai_permintaan(spes.get('Name', ''))[0] != Nama_2 or spes.get('Version') != versi_VALUE:
        raise ValueError('배포 메타데이터의 Nama_2·버전 불일치')
    if spes.get_all('Requires-Dist') or spes.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(surel, 한도):
    if not surel.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS 배포 주소만 허용합니다.')
    with urllib.request.urlopen(surel, timeout=30) as balas:
        if not balas.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 배포 surel gerak_VALUE')
        data = balas.read(한도 + 1)
    if len(data) > 한도:
        raise ValueError('배포 berkas Ukuran 제한 초과')
    return data


def Transfer_paket(Nama_2, versi_VALUE, 파일들, 출처):
    spes = {'name': Nama_2, 'version': versi_VALUE, 'source': 출처, 'files': [
        {'path': jalur, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        for jalur, data in sorted(파일들.items())]}
    kepala_VALUE = json.dumps(spes, ensure_ascii=False).encode()
    if len(kepala_VALUE) > 8192:
        raise ValueError('paket spes Ukuran 초과')
    return b'JKP1' + struct.pack('>I', len(kepala_VALUE)) + kepala_VALUE + b''.join(파일들[entri_VALUE['path']] for entri_VALUE in spes['files'])


class paket_repositori:
    def __init__(자신, jalur, teknologi_informasi_luring=False):
        자신.jalur = Path(jalur)
        자신.jalur.mkdir(parents=True, exist_ok=True)
        자신.teknologi_informasi_luring = teknologi_informasi_luring

    def Siapkan(자신, permintaan):
        Nama_2, versi_VALUE = urai_permintaan(permintaan)
        열쇠 = Nama_2 + ('==' + versi_VALUE if versi_VALUE else '')
        LOG_jalur = 자신.jalur / (열쇠 + '.json')
        배포경로 = 자신.jalur / (열쇠 + '.archive')
        if LOG_jalur.is_file() and 배포경로.is_file():
            LOG_baris = json.loads(LOG_jalur.read_text())
            data = 배포경로.read_bytes()
            if hashlib.sha256(data).hexdigest() != LOG_baris['sha256']:
                raise ValueError('저장된 배포 파일의 SHA-256 불일치')
        else:
            if 자신.teknologi_informasi_luring:
                raise ValueError('teknologi_informasi_luring 저장소에 없는 paket: ' + permintaan)
            surel = 'https://pypi.org/pypi/' + Nama_2 + ('/' + versi_VALUE if versi_VALUE else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(surel, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            후보 = [entri_VALUE for entri_VALUE in msinfo32_exe['urls'] if not entri_VALUE.get('yanked') and entri_VALUE['filename'].endswith('-none-any.whl')]
            if not 후보 and Nama_2.startswith('micropython-'):
                후보 = [entri_VALUE for entri_VALUE in msinfo32_exe['urls'] if not entri_VALUE.get('yanked') and entri_VALUE['filename'].endswith('.tar.gz')]
            if not 후보:
                raise ValueError('지원되는 순수 Python 배포 파일이 없습니다.')
            pilihan_VALUE = 후보[0]
            data = 웹읽기(pilihan_VALUE['url'], 4194304)
            if hashlib.sha256(data).hexdigest() != pilihan_VALUE['digests']['sha256']:
                raise ValueError('PyPI 배포 berkas SHA-256 불일치')
            LOG_baris = {'name': Nama_2, 'version': msinfo32_exe['info']['version'], 'filename': pilihan_VALUE['filename'],
                    'url': pilihan_VALUE['url'], 'sha256': pilihan_VALUE['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            압축풀기(LOG_baris['filename'], data, Nama_2, LOG_baris['version'])
            배포경로.write_bytes(data)
            LOG_jalur.write_text(json.dumps(LOG_baris, ensure_ascii=False, indent=2) + '\n')
        if LOG_baris['name'] != Nama_2 or versi_VALUE and LOG_baris['version'] != versi_VALUE:
            raise ValueError('repositori_akar Nama_2·버전 불일치')
        파일들 = 압축풀기(LOG_baris['filename'], data, Nama_2, LOG_baris['version'])
        return Transfer_paket(Nama_2, LOG_baris['version'], 파일들, LOG_baris['url'])


class paket_permintaan(socketserver.BaseRequestHandler):
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
                raise ValueError('잘못된 paket permintaan')
            balas = 자신.server.repositori_akar.Siapkan(permintaan[:-1].decode('ascii'))
        except Exception as galat:
            kepala_VALUE = json.dumps({'error': str(galat)[:500]}, ensure_ascii=False).encode()
            balas = b'JKP1' + struct.pack('>I', len(kepala_VALUE)) + kepala_VALUE
        try:
            자신.request.sendall(balas)
        except OSError:
            pass


class 꾸러미중계:
    def __init__(자신, nomor_port=8027, jalur=None, teknologi_informasi_luring=False):
        자신.server_VALUE = socketserver.TCPServer(('127.0.0.1', nomor_port), paket_permintaan, bind_and_activate=False)
        자신.server_VALUE.allow_reuse_address = True
        자신.server_VALUE.server_bind()
        자신.server_VALUE.server_activate()
        자신.server_VALUE.repositori_akar = paket_repositori(jalur or Tugas_akar/'build/pip-cache', teknologi_informasi_luring)
        자신.nomor_port = 자신.server_VALUE.server_address[1]
        자신.alur_VALUE = threading.Thread(target=자신.server_VALUE.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.alur_VALUE.start()
        return 자신

    def __exit__(자신, *argumen):
        자신.server_VALUE.shutdown()
        자신.server_VALUE.server_close()
        자신.alur_VALUE.join(timeout=2)


def jalankan():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--port', type=int, default=8027)
    parser_48ee4b1b.add_argument('--cache', type=Path, default=Tugas_akar/'build/pip-cache')
    parser_48ee4b1b.add_argument('--offline', action='store_true')
    parser_48ee4b1b.add_argument('--fetch', help='Jalankan_perintah 없이 호환 배포 파일을 내려받아 검사·Store_VALUE')
    argumen = parser_48ee4b1b.parse_args()
    if argumen.fetch:
        data = paket_repositori(argumen.cache, argumen.offline).Siapkan(argumen.fetch)
        print('paket Siapkan 완료:', argumen.fetch, len(data), 'byte_VALUE')
        return
    with 꾸러미중계(argumen.port, argumen.cache, argumen.offline) as 중계:
        print('paket 중계: 127.0.0.1:' + str(중계.nomor_port), flush=True)
        try:
            중계.alur_VALUE.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    jalankan()
