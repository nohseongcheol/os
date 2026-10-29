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
from Uitvoeren_opdracht import Taken_wortel
from COSL배포 import BIND_eindpunt


def 해시계산(pad):
    WAARDE = hashlib.sha256()
    with pad.open('rb') as Bestand_invoer:
        for gegevensblok in iter(lambda: Bestand_invoer.read(1024 * 1024), b''): WAARDE.update(gegevensblok)
    return WAARDE.hexdigest()


def starten():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD machineopstart HDMI/프레임버퍼 Grootte')
    resolutie_WAARDE = parser_48ee4b1b.parse_args().resolution
    너비, hoogte_WAARDE = map(int, resolutie_WAARDE.split('x'))
    scherm_Groep, scherm_MODUS = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[resolutie_WAARDE]
    firmware_WAARDE = Taken_wortel / 'vendor/pi4-firmware.tar.gz'
    예상결과 = firmware_WAARDE.with_name(firmware_WAARDE.name + '.sha256')
    licentie = Taken_wortel / 'vendor/LICENCE.broadcom'
    if not firmware_WAARDE.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi machineopstart 펌웨어 Groep_WAARDE 필요: ' + str(firmware_WAARDE))
    if 해시계산(firmware_WAARDE) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 Groep_WAARDE SHA256 불일치')
    if not licentie.is_file():
        raise SystemExit('machineopstart 펌웨어 라이선스 bestand 없음: ' + str(licentie))
    distributie_pad = Taken_wortel / 'dist'
    distributie_pad.mkdir(exist_ok=True)
    재연결꾸러미 = BIND_eindpunt()
    totaal_capaciteit, starten = 128 * 1024 * 1024, 2048
    섹터개수 = totaal_capaciteit // 512 - starten
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(Taken_wortel / 'build')) as 작업경로:
        fase_WAARDE = Path(작업경로)
        부팅경로 = fase_WAARDE / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        bestandslijst = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(firmware_WAARDE)) as Archief:
            for Naam in bestandslijst:
                lid = Archief.getmember('./' + Naam)
                if not lid.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + Naam)
                with Archief.extractfile(lid) as 원본주소, (부팅경로 / Naam).open('wb') as doel_WAARDE_functie:
                    shutil.copyfileobj(원본주소, doel_WAARDE_functie)
        shutil.copyfile(str(Taken_wortel / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        Instellingen = (Taken_wortel / 'machineopstart/config.txt').read_text()
        Instellingen = Instellingen.replace('hdmi_group=2', 'hdmi_group=' + str(scherm_Groep)).replace('hdmi_mode=4', 'hdmi_mode=' + str(scherm_MODUS))
        Instellingen = Instellingen.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(hoogte_WAARDE))
        (부팅경로 / 'config.txt').write_text(Instellingen)
        shutil.copyfile(str(licentie), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(Taken_wortel / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for Naam in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(Taken_wortel.parents[1] / Naam), str(부팅경로 / Naam))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, Naam in ((Taken_wortel/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (Taken_wortel/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (Taken_wortel/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (Taken_wortel/'vendor/LICENSE.genet','LICENSE.genet'),
                             (Taken_wortel/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (Taken_wortel/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (Taken_wortel/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (Taken_wortel/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/Naam))
        for Naam in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(Taken_wortel / 'vendor' / Naam), str(부팅경로 / Naam))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 hulpmiddelen/Uitvoeren_opdracht.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 hulpmiddelen/Uitvoeren_opdracht.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/LEESMIJ_eb81d7d9.md.\n')
        partitie_Bestand = fase_WAARDE / 'boot.fat'
        with partitie_Bestand.open('wb') as Bestand_invoer: Bestand_invoer.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(starten), '-n', 'JKJAVA', str(partitie_Bestand)])
        subprocess.check_call(['mcopy', '-i', str(partitie_Bestand), '-s'] + [str(gegevens_functie) for gegevens_functie in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 bouwen 결과와 같은지 확인한다.
        추출자료 = fase_WAARDE / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(partitie_Bestand), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(Taken_wortel / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 kernel_WAARDE SHA256 불일치')
        kopie = fase_WAARDE / 'jkoros-native-rpi4.img'
        hoofdopstartrecord = bytearray(512)
        hoofdopstartrecord[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', starten, 섹터개수)
        hoofdopstartrecord[510:512] = b'\x55\xaa'
        with kopie.open('wb') as HR_gegevens:
            HR_gegevens.truncate(totaal_capaciteit); HR_gegevens.write(hoofdopstartrecord); HR_gegevens.seek(starten * 512)
            with partitie_Bestand.open('rb') as 원본주소: shutil.copyfileobj(원본주소, HR_gegevens)
        bundel_manifest = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
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
                    'java_gui_example': '/example/java/Venstervoorbeeld.java; run: java Venstervoorbeeld',
                    'framebuffer_resolution': [너비, hoogte_WAARDE], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': firmware_WAARDE.name, 'source_sha256': 해시계산(firmware_WAARDE),
                    'image_sha256': 해시계산(kopie), 'boot_files': {}}
        for gegevens_functie in sorted(부팅경로.rglob('*')):
            if gegevens_functie.is_file(): bundel_manifest['boot_files'][str(gegevens_functie.relative_to(부팅경로))] = 해시계산(gegevens_functie)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux build_kopie/gebruikersruimte 디스크는 건드리지 않는다.
        os.replace(str(kopie), str(distributie_pad / kopie.name))
        Archief_BASIS = fase_WAARDE / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(Archief_BASIS), 'zip', str(부팅경로))
        os.replace(str(Archief_BASIS) + '.zip', str(distributie_pad / 'jkoros-native-rpi4-boot.zip'))
        (distributie_pad / 'manifest.json').write_text(json.dumps(bundel_manifest, indent=2) + '\n')
    print('genereren:', distributie_pad / 'jkoros-native-rpi4.img')
    print('werkelijk_gegevens Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    starten()
