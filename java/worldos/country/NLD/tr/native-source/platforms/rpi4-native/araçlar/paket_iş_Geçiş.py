#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost Geçiş_değer. 게스트는 TCP로 받은 소스를 직접 yükle_değer·실행한다."""
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

işlem_kök = Path(__file__).resolve().parents[1]


def ayrıştırmak_istek(istek):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', istek)
    if not 맞음:
        raise ValueError('paket_iş İsim 또는 İsim==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def doğrulamak_yol(İsim, yükleme_yol=True):
    yol = PurePosixPath(İsim)
    if yol.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in İsim.split('/')):
        raise ValueError('허용하지 않는 paket_iş yol: ' + İsim)
    if '\\' in İsim or any(ord(karakter_değer) < 32 or ord(karakter_değer) == 127 for karakter_değer in İsim):
        raise ValueError('잘못된 paket_iş yol 문자')
    if yükleme_yol and (len(('/lib/' + İsim).encode()) > 63 or İsim in ('Türkçe.py', 'paket_iş.py')):
        raise ValueError('paket_iş yol 제한 또는 varsayılan_değer kitaplık 충돌: ' + İsim)
    return İsim


def sıkıştırılmışı_açmak(Dosya_girdi_ad, veri, İsim, sürüm_değer):
    파일들 = {}
    명세들 = []
    def Ekleme_girdi(yol, içerik_değer):
        doğrulamak_yol(yol)
        if yol in 파일들:
            raise ValueError('중복 paket_iş yol: ' + yol)
        if len(içerik_değer) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + yol)
        içerik_değer.decode('utf-8')
        파일들[yol] = içerik_değer
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 kaynak_ağaç 16개·toplam_değer 64 KiB 이하여야 합니다.')
    if Dosya_girdi_ad.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(veri)) as paket_iş:
            항목들 = paket_iş.infolist()
            if len(항목들) > 256 or sum(girdi_değer.file_size for girdi_değer in 항목들) > 1048576:
                raise ValueError('Arşiv_değer sürüm_Depolama Boyut 제한 초과')
            iş_Liste = [girdi_değer for girdi_değer in 항목들 if girdi_değer.filename.endswith('.dist-info/WHEEL')]
            if len(iş_Liste) != 1:
                raise ValueError('wheel sözleşme_değeri 명세가 필요합니다.')
            sözleşme_değeri = email.parser.Parser().parsestr(paket_iş.read(iş_Liste[0]).decode())
            if sözleşme_değeri.get('Root-Is-Purelib', '').lower() != 'true' or not Dosya_girdi_ad.endswith('-none-any.whl'):
                raise ValueError('C uzantı_değer·플랫폼 전용 wheel은 지원하지 않습니다.')
            for girdi_değer in 항목들:
                yol = girdi_değer.filename.rstrip('/')
                doğrulamak_yol(yol, False)
                if (girdi_değer.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 수 없습니다.')
                if girdi_değer.filename.endswith('/'):
                    continue
                if '.dist-info/' in yol:
                    if yol.endswith('/METADATA'):
                        명세들.append(paket_iş.read(girdi_değer).decode())
                    continue
                if not yol.endswith('.py') or '.data/' in yol:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + yol)
                Ekleme_girdi(yol, paket_iş.read(girdi_değer))
    elif Dosya_girdi_ad.endswith('.tar.gz') and İsim.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py yürütmek_komut 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(veri), mode='r|gz') as paket_iş:
            뿌리들 = set()
            girdi_BAĞ_DEĞ_SAY = 0
            toplam_boyutlandırmak = 0
            for girdi_değer in paket_iş:
                girdi_BAĞ_DEĞ_SAY += 1
                toplam_boyutlandırmak += girdi_değer.size
                if girdi_BAĞ_DEĞ_SAY > 256 or toplam_boyutlandırmak > 1048576:
                    raise ValueError('Arşiv_değer sürüm_Depolama Boyut 제한 초과')
                doğrulamak_yol(girdi_değer.name, False)
                부분들 = girdi_değer.name.split('/')
                뿌리들.add(부분들[0])
                if girdi_değer.isdir():
                    continue
                if not girdi_değer.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython kaynak_ağaç 배포형')
                yol = '/'.join(부분들[1:])
                içerik_değer = paket_iş.extractfile(girdi_değer).read()
                if yol.endswith('PKG-INFO'):
                    명세들.append(içerik_değer.decode())
                elif yol.endswith('.py') and yol not in ('setup.py',):
                    Ekleme_girdi(yol, içerik_değer)
                elif '.egg-info/' not in yol and not yol.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + yol)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 kök_değer 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* kaynak_ağaç 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 dağıtım_değer 메타데이터가 필요합니다.')
    명세 = email.parser.Parser().parsestr(명세들[0])
    if ayrıştırmak_istek(명세.get('Name', ''))[0] != İsim or 명세.get('Version') != sürüm_değer:
        raise ValueError('dağıtım_değer 메타데이터의 İsim·버전 불일치')
    if 명세.get_all('Requires-Dist') or 명세.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def 웹읽기(ADRES, 한도):
    if not ADRES.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS dağıtım_değer 주소만 허용합니다.')
    with urllib.request.urlopen(ADRES, timeout=30) as yanıt:
        if not yanıt.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 dağıtım_değer ADRES taşımak_değer_83b651b8')
        veri = yanıt.read(한도 + 1)
    if len(veri) > 한도:
        raise ValueError('dağıtım_değer dosya Boyut 제한 초과')
    return veri


def devir_paket_iş(İsim, sürüm_değer, 파일들, origin_değer):
    명세 = {'name': İsim, 'version': sürüm_değer, 'source': origin_değer, 'files': [
        {'path': yol, 'size': len(veri), 'sha256': hashlib.sha256(veri).hexdigest()}
        for yol, veri in sorted(파일들.items())]}
    머리 = json.dumps(명세, ensure_ascii=False).encode()
    if len(머리) > 8192:
        raise ValueError('paket_iş 명세 Boyut 초과')
    return b'JKP1' + struct.pack('>I', len(머리)) + 머리 + b''.join(파일들[girdi_değer['path']] for girdi_değer in 명세['files'])


class paket_iş_depo:
    def __init__(자신, yol, bilgi_teknolojisi_Çevrimdışı=False):
        자신.yol = Path(yol)
        자신.yol.mkdir(parents=True, exist_ok=True)
        자신.bilgi_teknolojisi_Çevrimdışı = bilgi_teknolojisi_Çevrimdışı

    def Hazırlan(자신, istek):
        İsim, sürüm_değer = ayrıştırmak_istek(istek)
        tuş_malzeme = İsim + ('==' + sürüm_değer if sürüm_değer else '')
        LOG_yol = 자신.yol / (tuş_malzeme + '.json')
        dağıtım_yol = 자신.yol / (tuş_malzeme + '.archive')
        if LOG_yol.is_file() and dağıtım_yol.is_file():
            LOG_KAYIT = json.loads(LOG_yol.read_text())
            veri = dağıtım_yol.read_bytes()
            if hashlib.sha256(veri).hexdigest() != LOG_KAYIT['sha256']:
                raise ValueError('저장된 dağıtım_değer 파일의 SHA-256 불일치')
        else:
            if 자신.bilgi_teknolojisi_Çevrimdışı:
                raise ValueError('bilgi_teknolojisi_Çevrimdışı 저장소에 없는 paket_iş: ' + istek)
            ADRES = 'https://pypi.org/pypi/' + İsim + ('/' + sürüm_değer if sürüm_değer else '') + '/json'
            msinfo32_exe = json.loads(웹읽기(ADRES, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            aday = [girdi_değer for girdi_değer in msinfo32_exe['urls'] if not girdi_değer.get('yanked') and girdi_değer['filename'].endswith('-none-any.whl')]
            if not aday and İsim.startswith('micropython-'):
                aday = [girdi_değer for girdi_değer in msinfo32_exe['urls'] if not girdi_değer.get('yanked') and girdi_değer['filename'].endswith('.tar.gz')]
            if not aday:
                raise ValueError('지원되는 순수 Python dağıtım_değer 파일이 없습니다.')
            seçim_değer = aday[0]
            veri = 웹읽기(seçim_değer['url'], 4194304)
            if hashlib.sha256(veri).hexdigest() != seçim_değer['digests']['sha256']:
                raise ValueError('PyPI dağıtım_değer dosya SHA-256 불일치')
            LOG_KAYIT = {'name': İsim, 'version': msinfo32_exe['info']['version'], 'filename': seçim_değer['filename'],
                    'url': seçim_değer['url'], 'sha256': seçim_değer['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            sıkıştırılmışı_açmak(LOG_KAYIT['filename'], veri, İsim, LOG_KAYIT['version'])
            dağıtım_yol.write_bytes(veri)
            LOG_yol.write_text(json.dumps(LOG_KAYIT, ensure_ascii=False, indent=2) + '\n')
        if LOG_KAYIT['name'] != İsim or sürüm_değer and LOG_KAYIT['version'] != sürüm_değer:
            raise ValueError('depo_kök İsim·버전 불일치')
        파일들 = sıkıştırılmışı_açmak(LOG_KAYIT['filename'], veri, İsim, LOG_KAYIT['version'])
        return devir_paket_iş(İsim, LOG_KAYIT['version'], 파일들, LOG_KAYIT['url'])


class paket_iş_istek(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            istek = bytearray()
            while b'\n' not in istek and len(istek) < 100:
                parça_değer = 자신.request.recv(100 - len(istek))
                if not parça_değer:
                    return
                istek.extend(parça_değer)
            if not istek.endswith(b'\n') or istek.count(b'\n') != 1:
                raise ValueError('잘못된 paket_iş istek')
            yanıt = 자신.server.depo_kök.Hazırlan(istek[:-1].decode('ascii'))
        except Exception as hata:
            머리 = json.dumps({'error': str(hata)[:500]}, ensure_ascii=False).encode()
            yanıt = b'JKP1' + struct.pack('>I', len(머리)) + 머리
        try:
            자신.request.sendall(yanıt)
        except OSError:
            pass


class paket_iş_Geçiş:
    def __init__(자신, bağlantı_noktası_numarası=8027, yol=None, bilgi_teknolojisi_Çevrimdışı=False):
        자신.sunucu_değer = socketserver.TCPServer(('127.0.0.1', bağlantı_noktası_numarası), paket_iş_istek, bind_and_activate=False)
        자신.sunucu_değer.allow_reuse_address = True
        자신.sunucu_değer.server_bind()
        자신.sunucu_değer.server_activate()
        자신.sunucu_değer.depo_kök = paket_iş_depo(yol or işlem_kök/'build/pip-cache', bilgi_teknolojisi_Çevrimdışı)
        자신.bağlantı_noktası_numarası = 자신.sunucu_değer.server_address[1]
        자신.yazışma_değer = threading.Thread(target=자신.sunucu_değer.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.yazışma_değer.start()
        return 자신

    def __exit__(자신, *bağımsız_değişkenler):
        자신.sunucu_değer.shutdown()
        자신.sunucu_değer.server_close()
        자신.yazışma_değer.join(timeout=2)


def çalıştır():
    ayrıştırıcı_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ayrıştırıcı_48ee4b1b.add_argument('--port', type=int, default=8027)
    ayrıştırıcı_48ee4b1b.add_argument('--cache', type=Path, default=işlem_kök/'build/pip-cache')
    ayrıştırıcı_48ee4b1b.add_argument('--offline', action='store_true')
    ayrıştırıcı_48ee4b1b.add_argument('--fetch', help='yürütmek_komut 없이 호환 dağıtım_değer 파일을 내려받아 검사·depo_değer')
    bağımsız_değişkenler = ayrıştırıcı_48ee4b1b.parse_args()
    if bağımsız_değişkenler.fetch:
        veri = paket_iş_depo(bağımsız_değişkenler.cache, bağımsız_değişkenler.offline).Hazırlan(bağımsız_değişkenler.fetch)
        print('paket_iş Hazırlan 완료:', bağımsız_değişkenler.fetch, len(veri), 'bayt_değer')
        return
    with paket_iş_Geçiş(bağımsız_değişkenler.port, bağımsız_değişkenler.cache, bağımsız_değişkenler.offline) as Geçiş_değer:
        print('paket_iş Geçiş_değer: 127.0.0.1:' + str(Geçiş_değer.bağlantı_noktası_numarası), flush=True)
        try:
            Geçiş_değer.yazışma_değer.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    çalıştır()
