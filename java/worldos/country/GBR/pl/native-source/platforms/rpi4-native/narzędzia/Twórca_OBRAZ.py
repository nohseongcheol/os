#!/usr/bin/env python3
"""SD용 MBR/FAT32 이미지만 생성한다. 물리 디스크는 열지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tarfile
import tempfile
from Wykonaj_polecenie import Project_korzeń
from COSL배포 import BIND_uczestnik


def 해시계산(ścieżka_2):
    WARTOŚĆ = hashlib.sha256()
    with ścieżka_2.open('rb') as Plik_wpis:
        for blok_danych in iter(lambda: Plik_wpis.read(1024 * 1024), b''): WARTOŚĆ.update(blok_danych)
    return WARTOŚĆ.hexdigest()


def Uruchom_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD rozruch_maszyny HDMI/프레임버퍼 Rozmiar')
    rozdzielczość_WARTOŚĆ = parser_48ee4b1b.parse_args().resolution
    너비, wysokość_WARTOŚĆ = map(int, rozdzielczość_WARTOŚĆ.split('x'))
    화면무리, 화면방식 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[rozdzielczość_WARTOŚĆ]
    oprogramowanie_układowe_WARTOŚĆ = Project_korzeń / 'vendor/pi4-firmware.tar.gz'
    예상결과 = oprogramowanie_układowe_WARTOŚĆ.with_name(oprogramowanie_układowe_WARTOŚĆ.name + '.sha256')
    licencja = Project_korzeń / 'vendor/LICENCE.broadcom'
    if not oprogramowanie_układowe_WARTOŚĆ.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi rozruch_maszyny 펌웨어 grupa_WARTOŚĆ 필요: ' + str(oprogramowanie_układowe_WARTOŚĆ))
    if 해시계산(oprogramowanie_układowe_WARTOŚĆ) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 grupa_WARTOŚĆ SHA256 불일치')
    if not licencja.is_file():
        raise SystemExit('rozruch_maszyny 펌웨어 라이선스 nazwa_pliku 없음: ' + str(licencja))
    dystrybucja_ścieżka = Project_korzeń / 'dist'
    dystrybucja_ścieżka.mkdir(exist_ok=True)
    재연결꾸러미 = BIND_uczestnik()
    suma_pojemność, Uruchom_2 = 128 * 1024 * 1024, 2048
    섹터개수 = suma_pojemność // 512 - Uruchom_2
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(Project_korzeń / 'build')) as 작업경로:
        etap_WARTOŚĆ = Path(작업경로)
        부팅경로 = etap_WARTOŚĆ / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        lista_plików = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(oprogramowanie_układowe_WARTOŚĆ)) as Archiwum:
            for Nazwa in lista_plików:
                członek = Archiwum.getmember('./' + Nazwa)
                if not członek.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + Nazwa)
                with Archiwum.extractfile(członek) as 원본주소, (부팅경로 / Nazwa).open('wb') as cel_WARTOŚĆ_stanowisko:
                    shutil.copyfileobj(원본주소, cel_WARTOŚĆ_stanowisko)
        shutil.copyfile(str(Project_korzeń / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        Ustawienia = (Project_korzeń / 'rozruch_maszyny/config.txt').read_text()
        Ustawienia = Ustawienia.replace('hdmi_group=2', 'hdmi_group=' + str(화면무리)).replace('hdmi_mode=4', 'hdmi_mode=' + str(화면방식))
        Ustawienia = Ustawienia.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(wysokość_WARTOŚĆ))
        (부팅경로 / 'config.txt').write_text(Ustawienia)
        shutil.copyfile(str(licencja), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(Project_korzeń / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for Nazwa in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(Project_korzeń.parents[1] / Nazwa), str(부팅경로 / Nazwa))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, Nazwa in ((Project_korzeń/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (Project_korzeń/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (Project_korzeń/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (Project_korzeń/'vendor/LICENSE.genet','LICENSE.genet'),
                             (Project_korzeń/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (Project_korzeń/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (Project_korzeń/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (Project_korzeń/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/Nazwa))
        for Nazwa in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(Project_korzeń / 'vendor' / Nazwa), str(부팅경로 / Nazwa))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 narzędzia/Wykonaj_polecenie.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 narzędzia/Wykonaj_polecenie.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/plik_README_eb81d7d9.md.\n')
        partycja_Plik = etap_WARTOŚĆ / 'boot.fat'
        with partycja_Plik.open('wb') as Plik_wpis: Plik_wpis.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(Uruchom_2), '-n', 'JKJAVA', str(partycja_Plik)])
        subprocess.check_call(['mcopy', '-i', str(partycja_Plik), '-s'] + [str(dane_stanowisko) for dane_stanowisko in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 BLD_System 결과와 같은지 확인한다.
        추출자료 = etap_WARTOŚĆ / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(partycja_Plik), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(Project_korzeń / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 jądro_WARTOŚĆ SHA256 불일치')
        OBRAZ = etap_WARTOŚĆ / 'jkoros-native-rpi4.img'
        główny_rekord_rozruchowy = bytearray(512)
        główny_rekord_rozruchowy[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', Uruchom_2, 섹터개수)
        główny_rekord_rozruchowy[510:512] = b'\x55\xaa'
        with OBRAZ.open('wb') as KR_dane:
            KR_dane.truncate(suma_pojemność); KR_dane.write(główny_rekord_rozruchowy); KR_dane.seek(Uruchom_2 * 512)
            with partycja_Plik.open('rb') as 원본주소: shutil.copyfileobj(원본주소, KR_dane)
        pakiet_manifest = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
                    'license': 'COSL with third-party/LGPL carve-outs',
                    'relink_archive': 재연결꾸러미.name, 'relink_sha256': 해시계산(재연결꾸러미),
                    'user_abi': 1, 'elf_extension_required': False, 'linux_static_elf_subset': True,
                    'full_linux_binary_compatibility': False,
                    'openjdk': False, 'guest_java': 'jkoros JVM 0.4 subset/JAR with Korean library and native Swing subset',
                    'guest_c_compiler': 'TinyCC ARM64, own ABI', 'guest_aot': 'static Java int/reference subset to native ARM64 ELF',
                    'all_class_or_jar_compatible': False,
                    'python': 'MicroPython 1.24.1 integer build', 'cpython': False,
                    'network': 'lwIP IPv4 TCP/UDP/ARP/ICMP; GENET v5 DHCP or QEMU UART1 SLIP', 'ftp': 'guest anonymous passive RAM service',
                    'genet_ethernet': True, 'physical_network_tested': False,
                    'ssh': 'native libassh server :22, shared console', 'vnc': 'native authenticated RFB 3.8 :5900', 'rdp': False,
                    'gui': 'four resizable terminal windows and native Swing subset peers',
                    'terminal_resize': 'hover corner; hold left mouse button and drag; live shell/vi grid',
                    'java_gui_example': '/example/java/PrzykładOkna.java; run: java PrzykładOkna',
                    'framebuffer_resolution': [너비, wysokość_WARTOŚĆ], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': oprogramowanie_układowe_WARTOŚĆ.name, 'source_sha256': 해시계산(oprogramowanie_układowe_WARTOŚĆ),
                    'image_sha256': 해시계산(OBRAZ), 'boot_files': {}}
        for dane_stanowisko in sorted(부팅경로.rglob('*')):
            if dane_stanowisko.is_file(): pakiet_manifest['boot_files'][str(dane_stanowisko.relative_to(부팅경로))] = 해시계산(dane_stanowisko)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux BLD_OBRAZ/przestrzeń_użytkownika 디스크는 건드리지 않는다.
        os.replace(str(OBRAZ), str(dystrybucja_ścieżka / OBRAZ.name))
        Archiwum_baza = etap_WARTOŚĆ / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(Archiwum_baza), 'zip', str(부팅경로))
        os.replace(str(Archiwum_baza) + '.zip', str(dystrybucja_ścieżka / 'jkoros-native-rpi4-boot.zip'))
        (dystrybucja_ścieżka / 'manifest.json').write_text(json.dumps(pakiet_manifest, indent=2) + '\n')
    print('generować:', dystrybucja_ścieżka / 'jkoros-native-rpi4.img')
    print('rzeczywisty_dane Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    Uruchom_2()
