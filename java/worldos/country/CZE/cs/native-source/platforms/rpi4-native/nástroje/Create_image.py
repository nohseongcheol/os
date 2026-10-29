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
from Provést_příkaz import akce_kořen
from COSL배포 import vázat_účastník


def 해시계산(cesta_2):
    HODNOTA = hashlib.sha256()
    with cesta_2.open('rb') as Soubor_položka:
        for datový_blok in iter(lambda: Soubor_položka.read(1024 * 1024), b''): HODNOTA.update(datový_blok)
    return HODNOTA.hexdigest()


def Spustit_2():
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD spuštění_stroje HDMI/프레임버퍼 Velikost')
    řešení_HODNOTA = analyzátor_48ee4b1b.parse_args().resolution
    너비, výška_HODNOTA = map(int, řešení_HODNOTA.split('x'))
    화면무리, 화면방식 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[řešení_HODNOTA]
    firmware_HODNOTA = akce_kořen / 'vendor/pi4-firmware.tar.gz'
    예상결과 = firmware_HODNOTA.with_name(firmware_HODNOTA.name + '.sha256')
    licence = akce_kořen / 'vendor/LICENCE.broadcom'
    if not firmware_HODNOTA.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi spuštění_stroje 펌웨어 Skupina_HODNOTA 필요: ' + str(firmware_HODNOTA))
    if 해시계산(firmware_HODNOTA) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 Skupina_HODNOTA SHA256 불일치')
    if not licence.is_file():
        raise SystemExit('spuštění_stroje 펌웨어 라이선스 název_souboru 없음: ' + str(licence))
    distribuce_cesta = akce_kořen / 'dist'
    distribuce_cesta.mkdir(exist_ok=True)
    재연결꾸러미 = vázat_účastník()
    celkem_kapacita, Spustit_2 = 128 * 1024 * 1024, 2048
    섹터개수 = celkem_kapacita // 512 - Spustit_2
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(akce_kořen / 'build')) as 작업경로:
        fáze_HODNOTA = Path(작업경로)
        부팅경로 = fáze_HODNOTA / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        seznam_souborů = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(firmware_HODNOTA)) as Archiv:
            for Název in seznam_souborů:
                člen = Archiv.getmember('./' + Název)
                if not člen.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + Název)
                with Archiv.extractfile(člen) as 원본주소, (부팅경로 / Název).open('wb') as cíl_HODNOTA_pozice:
                    shutil.copyfileobj(원본주소, cíl_HODNOTA_pozice)
        shutil.copyfile(str(akce_kořen / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        Nastavení = (akce_kořen / 'spuštění_stroje/config.txt').read_text()
        Nastavení = Nastavení.replace('hdmi_group=2', 'hdmi_group=' + str(화면무리)).replace('hdmi_mode=4', 'hdmi_mode=' + str(화면방식))
        Nastavení = Nastavení.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(výška_HODNOTA))
        (부팅경로 / 'config.txt').write_text(Nastavení)
        shutil.copyfile(str(licence), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(akce_kořen / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for Název in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(akce_kořen.parents[1] / Název), str(부팅경로 / Název))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, Název in ((akce_kořen/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (akce_kořen/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (akce_kořen/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (akce_kořen/'vendor/LICENSE.genet','LICENSE.genet'),
                             (akce_kořen/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (akce_kořen/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (akce_kořen/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (akce_kořen/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/Název))
        for Název in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(akce_kořen / 'vendor' / Název), str(부팅경로 / Název))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 nástroje/Provést_příkaz.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 nástroje/Provést_příkaz.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/안내.md.\n')
        oddíl_Soubor = fáze_HODNOTA / 'boot.fat'
        with oddíl_Soubor.open('wb') as Soubor_položka: Soubor_položka.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(Spustit_2), '-n', 'JKJAVA', str(oddíl_Soubor)])
        subprocess.check_call(['mcopy', '-i', str(oddíl_Soubor), '-s'] + [str(data_pozice) for data_pozice in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 BLD_Systém 결과와 같은지 확인한다.
        추출자료 = fáze_HODNOTA / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(oddíl_Soubor), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(akce_kořen / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 jádro_HODNOTA SHA256 불일치')
        image = fáze_HODNOTA / 'jkoros-native-rpi4.img'
        hlavní_spouštěcí_záznam = bytearray(512)
        hlavní_spouštěcí_záznam[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', Spustit_2, 섹터개수)
        hlavní_spouštěcí_záznam[510:512] = b'\x55\xaa'
        with image.open('wb') as KV_data:
            KV_data.truncate(celkem_kapacita); KV_data.write(hlavní_spouštěcí_záznam); KV_data.seek(Spustit_2 * 512)
            with oddíl_Soubor.open('rb') as 원본주소: shutil.copyfileobj(원본주소, KV_data)
        sada_manifest = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
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
                    'java_gui_example': '/example/java/UkázkaOkna.java; run: java UkázkaOkna',
                    'framebuffer_resolution': [너비, výška_HODNOTA], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': firmware_HODNOTA.name, 'source_sha256': 해시계산(firmware_HODNOTA),
                    'image_sha256': 해시계산(image), 'boot_files': {}}
        for data_pozice in sorted(부팅경로.rglob('*')):
            if data_pozice.is_file(): sada_manifest['boot_files'][str(data_pozice.relative_to(부팅경로))] = 해시계산(data_pozice)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux BLD_image/uživatelský_prostor 디스크는 건드리지 않는다.
        os.replace(str(image), str(distribuce_cesta / image.name))
        Archiv_BASE = fáze_HODNOTA / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(Archiv_BASE), 'zip', str(부팅경로))
        os.replace(str(Archiv_BASE) + '.zip', str(distribuce_cesta / 'jkoros-native-rpi4-boot.zip'))
        (distribuce_cesta / 'manifest.json').write_text(json.dumps(sada_manifest, indent=2) + '\n')
    print('generovat:', distribuce_cesta / 'jkoros-native-rpi4.img')
    print('skutečný_data Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    Spustit_2()
