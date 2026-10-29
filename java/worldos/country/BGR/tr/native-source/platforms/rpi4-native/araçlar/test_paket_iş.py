#!/usr/bin/env python3
"""PyPI 실물 배포와 부정 artış_değer·RAM 되돌림을 Öz 커널에서 검사한다."""
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
from paket_iş_Geçiş import paket_iş_depo, sıkıştırılmışı_açmak
from yürütmek_komut import işlem_kök


def test_çark(İsim, 파일들, sözleşme_değeri='Root-Is-Purelib: true\n', 의존성=''):
    veri = io.BytesIO()
    with zipfile.ZipFile(veri, 'w', zipfile.ZIP_DEFLATED) as paket_iş:
        paket_iş.writestr(İsim + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + sözleşme_değeri)
        paket_iş.writestr(İsim + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + İsim + '\nVersion: 1.0\n' + 의존성)
        for yol, içerik_değer in 파일들.items():
            paket_iş.writestr(yol, içerik_değer)
    return veri.getvalue()


def çek_konak():
    bilgi_teknolojisi_normal = test_çark('jkoros-fixture', {'mod.py': 'değer=42\n'})
    assert sıkıştırılmışı_açmak('jkoros_fixture-1.0-py3-none-any.whl', bilgi_teknolojisi_normal, 'jkoros-fixture', '1.0') == {'mod.py': 'değer=42\n'.encode()}
    for veri in (
            test_çark('jkoros-fixture', {'../escape.py': ''}),
            test_çark('jkoros-fixture', {'/abs.py': ''}),
            test_çark('jkoros-fixture', {'big.py': 'x' * 16385}),
            test_çark('jkoros-fixture', {'mod.so': ''}),
            test_çark('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            test_çark('jkoros-fixture', {'mod.py': ''}, 의존성='Requires-Dist: requests\n')):
        try:
            sıkıştırılmışı_açmak('jkoros_fixture-1.0-py3-none-any.whl', veri, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel yol·Boyut·C uzantı_değer·의존성 reddetmek_değer')


def boş_bağlantı_noktası_numarası():
    with socket.socket() as yuva_değer:
        yuva_değer.bind(('127.0.0.1', 0))
        return yuva_değer.getsockname()[1]


def çalıştır():
    ayrıştırıcı_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ayrıştırıcı_48ee4b1b.add_argument('--host-only', action='store_true')
    bağımsız_değişkenler = ayrıştırıcı_48ee4b1b.parse_args()
    çek_konak()
    if bağımsız_değişkenler.host_only:
        return
    KR_yol = işlem_kök/'build/verification/pip'
    KR_yol.mkdir(parents=True, exist_ok=True)
    Depolama_yol = KR_yol/'cache'
    Depolama_yol.mkdir(exist_ok=True)
    # fiili_veri PyPI dağıtım_değer dosya. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    paket_iş_depo(işlem_kök/'build/pip-cache').Hazırlan('micropython-bisect==3.3.3')
    for 꼬리 in ('.archive', '.json'):
        shutil.copyfile(str(işlem_kök/'build/pip-cache'/('micropython-bisect==3.3.3'+꼬리)), str(Depolama_yol/('micropython-bisect==3.3.3'+꼬리)))
    donanım_LOG = json.loads((Depolama_yol/'micropython-bisect==3.3.3.json').read_text())
    assert donanım_LOG['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for İsim, 파일들 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .계산 import 더하기\n', '검증꾸러미/계산.py': 'def 더하기(가,SANİYE_işlenen):\n return 가+SANİYE_işlenen\n'}),
            ('jkoros-space', {'space%d.py' % 수: 'değer=1\n' for 수 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        veri = test_çark(İsim, 파일들)
        (Depolama_yol/(İsim+'==1.0.archive')).write_bytes(veri)
        (Depolama_yol/(İsim+'==1.0.json')).write_text(json.dumps({'name': İsim, 'version': '1.0',
            'filename': İsim.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(veri).hexdigest()}))
    doğrulamak_5fb2b747 = {'passed': False, 'kernel_sha256': hashlib.sha256((işlem_kök/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': donanım_LOG, 'checks': []}
    bağlantı_noktası_numarası = boş_bağlantı_noktası_numarası()
    Süreç = subprocess.Popen(['python3', str(işlem_kök/'araçlar/yürütmek_komut.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(bağlantı_noktası_numarası), '--pip-cache', str(Depolama_yol), '--ftp-port', str(boş_bağlantı_noktası_numarası())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    seçici_a916db4e = selectors.DefaultSelector()
    seçici_a916db4e.register(Süreç.stdout, selectors.EVENT_READ)
    döküm = bytearray()
    def 기다리기(şov_değer=b'jkoros-native> '):
        içerik_değer = bytearray()
        끝 = time.monotonic()+120
        while şov_değer not in içerik_değer:
            if time.monotonic() > 끝 or Süreç.poll() is not None:
                raise AssertionError('게스트 yanıt 없음: '+içerik_değer.decode('utf-8','replace'))
            for girdi_değer, _ in seçici_a916db4e.select(.1):
                parça_değer = girdi_değer.fileobj.read(4096)
                içerik_değer.extend(parça_değer)
                döküm.extend(parça_değer)
        return içerik_değer.decode('utf-8', 'replace').replace('\r\n','\n')
    def kabuk(komut, şov_değer=b'jkoros-native> '):
        Süreç.stdin.write(komut.encode()+b'\n')
        Süreç.stdin.flush()
        return 기다리기(şov_değer)
    def yürütmek_komut(komut, 예상, Durum_değer=0):
        içerik_değer = kabuk(komut)
        assert 예상 in içerik_değer and '\nexit '+str(Durum_değer)+'\n' in içerik_değer, içerik_değer
        doğrulamak_5fb2b747['checks'].append(komut)
        return içerik_değer
    def yükle_Dosyalar(İsim, veri):
        kabuk('load '+İsim, b'hex> ')
        for konum_dizini in range(0, len(veri), 64):
            kabuk(veri[konum_dizini:konum_dizini+64].hex(), b'hex> ')
        assert 'LOADED' in kabuk('.')
    try:
        기다리기()
        yürütmek_komut('pip --help', 'MicroPython kaynak_ağaç 설치기')
        yükle_Dosyalar('오류시험.py', (işlem_kök/'sınamalar/PYTHON/한국어오류시험.py').read_bytes())
        yürütmek_komut('python 오류시험.py', 'Türkçe dosya özel_durum doğrulamak')
        yürütmek_komut('pip install micropython-bisect==3.3.3 --port '+str(bağlantı_noktası_numarası), 'yükle_değer 완료: micropython-bisect 3.3.3')
        yürütmek_komut('python -c \'from bisect import insort as 순서대로넣기; değer=[1,5]; 순서대로넣기(değer,3); print(değer)\'', '[1, 3, 5]')
        yürütmek_komut('python -m pip list', 'micropython-bisect 3.3.3')
        yürütmek_komut('pip install micropython-bisect==3.3.3 --port '+str(bağlantı_noktası_numarası), '이미 설치됨:')
        yürütmek_komut('pip install jkoros-fixture==1.0 --port '+str(bağlantı_noktası_numarası), 'yükle_değer 완료: jkoros-fixture')
        yürütmek_komut('python -c \'from 검증꾸러미 import 더하기; print(더하기(20,22))\'', '\n42\n')
        yürütmek_komut('pip install jkoros-syntax==1.0 --port '+str(bağlantı_noktası_numarası), 'paket_iş hata:', 1)
        yürütmek_komut('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 hata 보존")\'', '구문 hata 보존')
        yükle_Dosyalar('공간시험.py', (işlem_kök/'sınamalar/PYTHON/paket_iş_kök_test.py').read_bytes())
        yürütmek_komut('python 공간시험.py '+str(bağlantı_noktası_numarası), 'paket_iş ADRES_bölge 부족 İade_köprü doğrulamak')
        yürütmek_komut('pip uninstall jkoros-fixture', 'kaldırmak_girdi 완료: jkoros-fixture')
        yürütmek_komut('pip uninstall micropython-bisect', 'kaldırmak_girdi 완료: micropython-bisect')
        yürütmek_komut('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("kaldırmak_girdi doğrulamak")\'', 'kaldırmak_girdi doğrulamak')
        doğrulamak_5fb2b747['passed'] = True
        print('PASS: PyPI 실물 yükle_değer·import·yürütmek_komut, Türkçe özel_durum, 패키지 dizin_değer, hata_değer İade_köprü, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 Çıkış_program 키로 QEMU를 끝내면 실행기의 Geçiş_değer 문맥도 정리된다.
            Süreç.stdin.write(b'\x01x')
            Süreç.stdin.flush()
            Süreç.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            Süreç.terminate()
            try:
                Süreç.wait(timeout=8)
            except subprocess.TimeoutExpired:
                Süreç.kill()
                Süreç.wait()
        if Süreç.poll() is None:
            Süreç.kill()
            Süreç.wait()
        seçici_a916db4e.close()
        Süreç.stdin.close()
        Süreç.stdout.close()
        (KR_yol/'serial.log').write_bytes(döküm)
        (KR_yol/'report.json').write_text(json.dumps(doğrulamak_5fb2b747, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    çalıştır()
