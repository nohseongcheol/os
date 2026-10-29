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
from изпълнявам_команда import проект_корен
from COSL배포 import обвързвам_участник


def 해시계산(ПЪТ):
    стойност = hashlib.sha256()
    with ПЪТ.open('rb') as Файл_запис:
        for блок_с_данни in iter(lambda: Файл_запис.read(1024 * 1024), b''): стойност.update(блок_с_данни)
    return стойност.hexdigest()


def Стартиране():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD 부팅 HDMI/프레임버퍼 Размер')
    разделителна_способност_стойност = анализатор_48ee4b1b.parse_args().resolution
    너비, 높이 = map(int, разделителна_способност_стойност.split('x'))
    화면무리, 화면방식 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[разделителна_способност_стойност]
    фърмуер_стойност = проект_корен / 'vendor/pi4-firmware.tar.gz'
    예상결과 = фърмуер_стойност.with_name(фърмуер_стойност.name + '.sha256')
    лиценз = проект_корен / 'vendor/LICENCE.broadcom'
    if not фърмуер_стойност.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi 부팅 펌웨어 Група_стойност 필요: ' + str(фърмуер_стойност))
    if 해시계산(фърмуер_стойност) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 Група_стойност SHA256 불일치')
    if not лиценз.is_file():
        raise SystemExit('부팅 펌웨어 라이선스 Файл 없음: ' + str(лиценз))
    배포경로 = проект_корен / 'dist'
    배포경로.mkdir(exist_ok=True)
    재연결꾸러미 = обвързвам_участник()
    общо_капацитет, Стартиране = 128 * 1024 * 1024, 2048
    섹터개수 = общо_капацитет // 512 - Стартиране
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(проект_корен / 'build')) as 작업경로:
        етап_стойност = Path(작업경로)
        부팅경로 = етап_стойност / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        Файл_Списък = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(фърмуер_стойност)) as Архив:
            for Име in Файл_Списък:
                член = Архив.getmember('./' + Име)
                if not член.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + Име)
                with Архив.extractfile(член) as 원본주소, (부팅경로 / Име).open('wb') as местоназначение_стойност_позиция:
                    shutil.copyfileobj(원본주소, местоназначение_стойност_позиция)
        shutil.copyfile(str(проект_корен / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        Настройки = (проект_корен / '부팅/config.txt').read_text()
        Настройки = Настройки.replace('hdmi_group=2', 'hdmi_group=' + str(화면무리)).replace('hdmi_mode=4', 'hdmi_mode=' + str(화면방식))
        Настройки = Настройки.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(높이))
        (부팅경로 / 'config.txt').write_text(Настройки)
        shutil.copyfile(str(лиценз), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(проект_корен / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for Име in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(проект_корен.parents[1] / Име), str(부팅경로 / Име))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, Име in ((проект_корен/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (проект_корен/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (проект_корен/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (проект_корен/'vendor/LICENSE.genet','LICENSE.genet'),
                             (проект_корен/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (проект_корен/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (проект_корен/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (проект_корен/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/Име))
        for Име in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(проект_корен / 'vendor' / Име), str(부팅경로 / Име))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 Инструменти/изпълнявам_команда.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 Инструменти/изпълнявам_команда.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/안내.md.\n')
        дял_Файл = етап_стойност / 'boot.fat'
        with дял_Файл.open('wb') as Файл_запис: Файл_запис.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(Стартиране), '-n', 'JKJAVA', str(дял_Файл)])
        subprocess.check_call(['mcopy', '-i', str(дял_Файл), '-s'] + [str(данни_позиция) for данни_позиция in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 компилация_система 결과와 같은지 확인한다.
        추출자료 = етап_стойност / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(дял_Файл), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(проект_корен / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 ядро_стойност SHA256 불일치')
        снимка = етап_стойност / 'jkoros-native-rpi4.img'
        образец_част_с_ОС_системна_част = bytearray(512)
        образец_част_с_ОС_системна_част[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', Стартиране, 섹터개수)
        образец_част_с_ОС_системна_част[510:512] = b'\x55\xaa'
        with снимка.open('wb') as мярка_данни:
            мярка_данни.truncate(общо_капацитет); мярка_данни.write(образец_част_с_ОС_системна_част); мярка_данни.seek(Стартиране * 512)
            with дял_Файл.open('rb') as 원본주소: shutil.copyfileobj(원본주소, мярка_данни)
        пакет_манифест = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
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
                    'java_gui_example': '/example/java/창예제.java; run: java 창예제',
                    'framebuffer_resolution': [너비, 높이], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': фърмуер_стойност.name, 'source_sha256': 해시계산(фърмуер_стойност),
                    'image_sha256': 해시계산(снимка), 'boot_files': {}}
        for данни_позиция in sorted(부팅경로.rglob('*')):
            if данни_позиция.is_file(): пакет_манифест['boot_files'][str(данни_позиция.relative_to(부팅경로))] = 해시계산(данни_позиция)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux компилация_снимка/потребител 디스크는 건드리지 않는다.
        os.replace(str(снимка), str(배포경로 / снимка.name))
        압축기준 = етап_стойност / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(압축기준), 'zip', str(부팅경로))
        os.replace(str(압축기준) + '.zip', str(배포경로 / 'jkoros-native-rpi4-boot.zip'))
        (배포경로 / 'manifest.json').write_text(json.dumps(пакет_манифест, indent=2) + '\n')
    print('генерирам:', 배포경로 / 'jkoros-native-rpi4.img')
    print('действителен_данни Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    Стартиране()
