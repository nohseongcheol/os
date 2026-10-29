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
from Izvrši_naredba import akcija_korijen
from COSL배포 import BIND_sudionik


def 해시계산(PUTANJA):
    VALUE = hashlib.sha256()
    with PUTANJA.open('rb') as Datoteka_unos:
        for podatkovni_blok in iter(lambda: Datoteka_unos.read(1024 * 1024), b''): VALUE.update(podatkovni_blok)
    return VALUE.hexdigest()


def Pokreni():
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD 부팅 HDMI/프레임버퍼 Veličina')
    razlučivost_VALUE = analizator_48ee4b1b.parse_args().resolution
    너비, 높이 = map(int, razlučivost_VALUE.split('x'))
    화면무리, 화면방식 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[razlučivost_VALUE]
    oprema_VALUE = akcija_korijen / 'vendor/pi4-firmware.tar.gz'
    예상결과 = oprema_VALUE.with_name(oprema_VALUE.name + '.sha256')
    licenca = akcija_korijen / 'vendor/LICENCE.broadcom'
    if not oprema_VALUE.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi 부팅 펌웨어 Grupa_VALUE 필요: ' + str(oprema_VALUE))
    if 해시계산(oprema_VALUE) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 Grupa_VALUE SHA256 불일치')
    if not licenca.is_file():
        raise SystemExit('부팅 펌웨어 라이선스 Datoteka 없음: ' + str(licenca))
    배포경로 = akcija_korijen / 'dist'
    배포경로.mkdir(exist_ok=True)
    재연결꾸러미 = BIND_sudionik()
    ukupni_zbroj_kapacitet, Pokreni = 128 * 1024 * 1024, 2048
    섹터개수 = ukupni_zbroj_kapacitet // 512 - Pokreni
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(akcija_korijen / 'build')) as 작업경로:
        faza_VALUE = Path(작업경로)
        부팅경로 = faza_VALUE / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        Datoteka_Popis = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(oprema_VALUE)) as Arhiva:
            for Ime in Datoteka_Popis:
                član = Arhiva.getmember('./' + Ime)
                if not član.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + Ime)
                with Arhiva.extractfile(član) as 원본주소, (부팅경로 / Ime).open('wb') as odredište_VALUE_položaj:
                    shutil.copyfileobj(원본주소, odredište_VALUE_položaj)
        shutil.copyfile(str(akcija_korijen / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        Postavke = (akcija_korijen / '부팅/config.txt').read_text()
        Postavke = Postavke.replace('hdmi_group=2', 'hdmi_group=' + str(화면무리)).replace('hdmi_mode=4', 'hdmi_mode=' + str(화면방식))
        Postavke = Postavke.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(높이))
        (부팅경로 / 'config.txt').write_text(Postavke)
        shutil.copyfile(str(licenca), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(akcija_korijen / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for Ime in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(akcija_korijen.parents[1] / Ime), str(부팅경로 / Ime))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, Ime in ((akcija_korijen/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (akcija_korijen/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (akcija_korijen/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (akcija_korijen/'vendor/LICENSE.genet','LICENSE.genet'),
                             (akcija_korijen/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (akcija_korijen/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (akcija_korijen/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (akcija_korijen/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/Ime))
        for Ime in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(akcija_korijen / 'vendor' / Ime), str(부팅경로 / Ime))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 Alati/Izvrši_naredba.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 Alati/Izvrši_naredba.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/안내.md.\n')
        particija_Datoteka = faza_VALUE / 'boot.fat'
        with particija_Datoteka.open('wb') as Datoteka_unos: Datoteka_unos.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(Pokreni), '-n', 'JKJAVA', str(particija_Datoteka)])
        subprocess.check_call(['mcopy', '-i', str(particija_Datoteka), '-s'] + [str(podaci_položaj) for podaci_položaj in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 međuverzija_sustav 결과와 같은지 확인한다.
        추출자료 = faza_VALUE / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(particija_Datoteka), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(akcija_korijen / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 jezgra_sustava_VALUE SHA256 불일치')
        IMAGE = faza_VALUE / 'jkoros-native-rpi4.img'
        MBR = bytearray(512)
        MBR[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', Pokreni, 섹터개수)
        MBR[510:512] = b'\x55\xaa'
        with IMAGE.open('wb') as KR_podaci:
            KR_podaci.truncate(ukupni_zbroj_kapacitet); KR_podaci.write(MBR); KR_podaci.seek(Pokreni * 512)
            with particija_Datoteka.open('rb') as 원본주소: shutil.copyfileobj(원본주소, KR_podaci)
        꾸러미명세 = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
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
                    'java_gui_example': '/example/java/PrimjerProzora.java; run: java PrimjerProzora',
                    'framebuffer_resolution': [너비, 높이], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': oprema_VALUE.name, 'source_sha256': 해시계산(oprema_VALUE),
                    'image_sha256': 해시계산(IMAGE), 'boot_files': {}}
        for podaci_položaj in sorted(부팅경로.rglob('*')):
            if podaci_položaj.is_file(): 꾸러미명세['boot_files'][str(podaci_položaj.relative_to(부팅경로))] = 해시계산(podaci_položaj)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux međuverzija_IMAGE/korisnik 디스크는 건드리지 않는다.
        os.replace(str(IMAGE), str(배포경로 / IMAGE.name))
        Arhiva_BASE = faza_VALUE / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(Arhiva_BASE), 'zip', str(부팅경로))
        os.replace(str(Arhiva_BASE) + '.zip', str(배포경로 / 'jkoros-native-rpi4-boot.zip'))
        (배포경로 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('generirati:', 배포경로 / 'jkoros-native-rpi4.img')
    print('stvaran_podaci Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    Pokreni()
