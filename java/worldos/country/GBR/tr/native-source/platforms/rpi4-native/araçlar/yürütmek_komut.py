#!/usr/bin/env python3
import argparse
from contextlib import ExitStack
import os
import re
from pathlib import Path
import shutil
import subprocess
import atexit
import tempfile

işlem_kök = Path(__file__).resolve().parents[1]
rastgele_Dosyalar = []


def _난수정리():
    for yol in rastgele_Dosyalar:
        try:
            os.unlink(yol)
        except FileNotFoundError:
            pass


atexit.register(_난수정리)


def 원격난수인수():
    # QEMU raspi4b에는 RNG200이 없다. 실행마다 OS CSPRNG로 새 씨앗을 준다.
    with tempfile.NamedTemporaryFile(prefix='jkoros-entropy-', delete=False) as dosya:
        dosya.write(b'JKRENRG1' + os.urandom(32))
        rastgele_Dosyalar.append(dosya.name)
    return ['-device', 'loader,file={},addr=0x01ff0000,force-raw=on'.format(dosya.name)]


def 모의기계():
    if os.environ.get('QEMU_AARCH64'):
        return [os.environ['QEMU_AARCH64']]
    konak = işlem_kök.parent / 'rpi4/build/host'
    yükleyici = konak / 'lib/ld-musl-x86_64.so.1'
    ikili = konak / 'usr/bin/qemu-system-aarch64'
    if yükleyici.is_file() and ikili.is_file():
        return [str(yükleyici), '--library-path', str(konak / 'usr/lib') + ':' + str(konak / 'lib'),
                str(ikili), '-L', str(konak / 'usr/share/qemu')]
    ikili = shutil.which('qemu-system-aarch64')
    if not ikili:
        raise SystemExit('raspi4b Destek_değer QEMU 필요. QEMU_AARCH64로 경로를 지정하세요.')
    return [ikili]


def 해상도읽기(metin):
    if not re.fullmatch(r'[0-9]{3,4}x[0-9]{3,4}', metin):
        raise argparse.ArgumentTypeError('çözme_değer biçim_değer: 1920x1080')
    너비, 높이 = map(int, metin.split('x'))
    if not (640 <= 너비 <= 1920 and 480 <= 높이 <= 1080):
        raise argparse.ArgumentTypeError('Destek_değer klip: 너비 640~1920, 높이 480~1080')
    return 너비, 높이


def komut(çözme_değer=(640, 480)):
    Arka_Plan_değer = 모의기계()
    지원목록 = subprocess.check_output(Arka_Plan_değer + ['-machine', 'help'], universal_newlines=True)
    if 'raspi4b ' not in 지원목록:
        raise SystemExit('이 QEMU는 raspi4b를 지원하지 않습니다. 최신 QEMU 경로를 QEMU_AARCH64로 지정하세요.')
    너비, 높이 = 해상도읽기('{}x{}'.format(*çözme_değer))
    return Arka_Plan_değer + ['-M', 'raspi4b', '-smp', '4', '-m', '2G',
                   '-global', 'bcm2835-fb.xres=' + str(너비),
                   '-global', 'bcm2835-fb.yres=' + str(높이), '-kernel',
                   str(işlem_kök / 'build/kernel8.img'), '-no-reboot'] + 원격난수인수()


def çalıştır():
    ayrıştırıcı = argparse.ArgumentParser(description='Öz Java Pi4 çekirdek_değer. 직렬 셸은 Ctrl+A X, --desktop은 Ctrl+C로 Çıkış_program.')
    ayrıştırıcı.add_argument('--display', default='none', help='none 또는 gtk/sdl (konak Destek_değer 필요)')
    ayrıştırıcı.add_argument('--resolution', type=해상도읽기, default=(640, 480), help='makine_başlatma 화면 Boyut. 예: 1920x1080; varsayılan_değer 640x480')
    ayrıştırıcı.add_argument('--vnc', help='예: 127.0.0.1:2 → VNC donanım_taşımak 5902. tuş_değer 입력은 UART 터미널에서 합니다.')
    ayrıştırıcı.add_argument('--desktop', action='store_true', help='VNC 키보드/한글 입력을 UART로 연결하고 GUI 터미널을 엽니다.')
    ayrıştırıcı.add_argument('--port', type=int, default=5902, help='--desktop의 localhost VNC donanım_taşımak')
    ayrıştırıcı.add_argument('--network', action='store_true', help='보조 UART SLIP와 QEMU NAT를 Bağlan; --desktop과 함께 kullanmak_değer 가능; 게스트에서 ftpd start')
    ayrıştırıcı.add_argument('--remote', action='store_true', help='--network와 게스트 SSH 2222→22, VNC 5903→5900 전달을 켭니다. --desktop 불필요')
    ayrıştırıcı.add_argument('--ftp-port', type=int, default=2121, help='--network의 localhost FTP denetim_değer donanım_taşımak (데이터 50000..50007)')
    ayrıştırıcı.add_argument('--guest-ip', default=None, help='QEMU NAT İleri_değer hedef. 기본은 ip.conf의 IP; değiştirmek_değer 시 게스트 ipconfig set으로 같은 주소를 지정합니다.')
    ayrıştırıcı.add_argument('--network-host', default='127.0.0.1', help='NAT almak_değer ADRES. 127.0.0.1: 이 PC만, 0.0.0.0 또는 PC의 LAN ADRES: dış_değer cxn_e05f319b')
    ayrıştırıcı.add_argument('--forward', action='append', default=[], help='--network Ekleme_girdi Bağlan: tcp:호스트포트:게스트포트 또는 udp:호스트포트:게스트포트')
    ayrıştırıcı.add_argument('--pip', action='store_true', help='PyPI kaynak_ağaç paket_iş Geçiş_değer çalıştır (--network 필요, MicroPython 호환 소스만)')
    ayrıştırıcı.add_argument('--pip-port', type=int, default=8027, help='paket_iş 중계의 localhost TCP donanım_taşımak')
    ayrıştırıcı.add_argument('--pip-cache', type=Path, default=işlem_kök/'build/pip-cache')
    ayrıştırıcı.add_argument('--pip-offline', action='store_true', help='이미 받은 dağıtım_değer 파일만 제공')
    bağımsız_değişken_DİZİ = ayrıştırıcı.parse_args()
    if bağımsız_değişken_DİZİ.remote:
        bağımsız_değişken_DİZİ.network=True
        bağımsız_değişken_DİZİ.forward += ['tcp:2222:22','tcp:5903:5900']
        print('게스트 SSH → {}:2222, VNC → {}:5903; parola_değer: python3 araçlar/uzak_Ayarlar.py show'.format(bağımsız_değişken_DİZİ.network_host,bağımsız_değişken_DİZİ.network_host),flush=True)
    if bağımsız_değişken_DİZİ.pip and not bağımsız_değişken_DİZİ.network: ayrıştırıcı.error('--pip는 --network와 함께 사용합니다.')
    if not 1 <= bağımsız_değişken_DİZİ.pip_port <= 65535: ayrıştırıcı.error('--pip-port 범위는 1~65535입니다.')
    if bağımsız_değişken_DİZİ.forward and not bağımsız_değişken_DİZİ.network: ayrıştırıcı.error('--forward는 --network와 함께 사용합니다.')
    with ExitStack() as kaynak_değer:
        if bağımsız_değişken_DİZİ.pip:
            from paket_iş_Geçiş import paket_iş_Geçiş
            kaynak_değer.enter_context(paket_iş_Geçiş(bağımsız_değişken_DİZİ.pip_port, bağımsız_değişken_DİZİ.pip_cache, bağımsız_değişken_DİZİ.pip_offline))
            print('paket_iş Geçiş_değer: 127.0.0.1:' + str(bağımsız_değişken_DİZİ.pip_port), flush=True)
        Çalıştır(bağımsız_değişken_DİZİ)


def Çalıştır(bağımsız_değişken_DİZİ):
    if bağımsız_değişken_DİZİ.desktop:
        if bağımsız_değişken_DİZİ.vnc or bağımsız_değişken_DİZİ.display != 'none': raise SystemExit('--desktop은 --vnc/--display와 함께 사용하지 않습니다.')
        from Masaüstü_Görünüm import çalıştırma_Masaüstü
        raise SystemExit(çalıştırma_Masaüstü(bağımsız_değişken_DİZİ.port, ağ=bağımsız_değişken_DİZİ.network, dosya_aktarımı_bağlantı_noktası_numarası=bağımsız_değişken_DİZİ.ftp_port, 전달규칙들=bağımsız_değişken_DİZİ.forward, çözme_değer=bağımsız_değişken_DİZİ.resolution, konuk_ADRES=bağımsız_değişken_DİZİ.guest_ip, konak_ADRES=bağımsız_değişken_DİZİ.network_host))
    Seçenekler = ['-display', bağımsız_değişken_DİZİ.display, '-serial', 'mon:stdio']
    if bağımsız_değişken_DİZİ.vnc:
        Seçenekler += ['-vnc', bağımsız_değişken_DİZİ.vnc]
    if bağımsız_değişken_DİZİ.network:
        from köprü_3de4fe3a import köprü_3de4fe3a
        with köprü_3de4fe3a(bağımsız_değişken_DİZİ.ftp_port, bağımsız_değişken_DİZİ.forward, konuk_ADRES=bağımsız_değişken_DİZİ.guest_ip, konak_ADRES=bağımsız_değişken_DİZİ.network_host) as köprü:
            Durum_değer = subprocess.call(komut(bağımsız_değişken_DİZİ.resolution) + Seçenekler + köprü.전달인수())
            if köprü.hata: raise SystemExit('network bridge: ' + köprü.hata)
        raise SystemExit(Durum_değer)
    raise SystemExit(subprocess.call(komut(bağımsız_değişken_DİZİ.resolution) + Seçenekler))


if __name__ == '__main__':
    çalıştır()
