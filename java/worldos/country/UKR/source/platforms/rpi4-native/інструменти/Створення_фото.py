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
from Виконати_команда import Дії_корінь
from COSL배포 import зв_язувати_учасник


def 해시계산(шлях):
    значення = hashlib.sha256()
    with шлях.open('rb') as Файл_запис:
        for блок_даних in iter(lambda: Файл_запис.read(1024 * 1024), b''): значення.update(блок_даних)
    return значення.hexdigest()


def запустити():
    аналізатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатор_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD запуск_машини HDMI/프레임버퍼 Розмір')
    роздільна_здатність_значення = аналізатор_48ee4b1b.parse_args().resolution
    너비, 높이 = map(int, роздільна_здатність_значення.split('x'))
    화면무리, 화면방식 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[роздільна_здатність_значення]
    мікропрограма_значення = Дії_корінь / 'vendor/pi4-firmware.tar.gz'
    예상결과 = мікропрограма_значення.with_name(мікропрограма_значення.name + '.sha256')
    ліцензія = Дії_корінь / 'vendor/LICENCE.broadcom'
    if not мікропрограма_значення.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi запуск_машини 펌웨어 Група_значення 필요: ' + str(мікропрограма_значення))
    if 해시계산(мікропрограма_значення) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 Група_значення SHA256 불일치')
    if not ліцензія.is_file():
        raise SystemExit('запуск_машини 펌웨어 라이선스 файл 없음: ' + str(ліцензія))
    배포경로 = Дії_корінь / 'dist'
    배포경로.mkdir(exist_ok=True)
    재연결꾸러미 = зв_язувати_учасник()
    усього_ресурс, запустити = 128 * 1024 * 1024, 2048
    섹터개수 = усього_ресурс // 512 - запустити
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(Дії_корінь / 'build')) as 작업경로:
        етап_значення = Path(작업경로)
        부팅경로 = етап_значення / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        Файл_список = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(мікропрограма_значення)) as Архів:
            for Назва in Файл_список:
                елемент = Архів.getmember('./' + Назва)
                if not елемент.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + Назва)
                with Архів.extractfile(елемент) as 원본주소, (부팅경로 / Назва).open('wb') as місце_значення_посада:
                    shutil.copyfileobj(원본주소, місце_значення_посада)
        shutil.copyfile(str(Дії_корінь / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        Налаштування = (Дії_корінь / 'запуск_машини/config.txt').read_text()
        Налаштування = Налаштування.replace('hdmi_group=2', 'hdmi_group=' + str(화면무리)).replace('hdmi_mode=4', 'hdmi_mode=' + str(화면방식))
        Налаштування = Налаштування.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(높이))
        (부팅경로 / 'config.txt').write_text(Налаштування)
        shutil.copyfile(str(ліцензія), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(Дії_корінь / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for Назва in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(Дії_корінь.parents[1] / Назва), str(부팅경로 / Назва))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, Назва in ((Дії_корінь/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (Дії_корінь/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (Дії_корінь/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (Дії_корінь/'vendor/LICENSE.genet','LICENSE.genet'),
                             (Дії_корінь/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (Дії_корінь/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (Дії_корінь/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (Дії_корінь/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/Назва))
        for Назва in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(Дії_корінь / 'vendor' / Назва), str(부팅경로 / Назва))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 інструменти/Виконати_команда.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 інструменти/Виконати_команда.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/файл_Readme_eb81d7d9.md.\n')
        розділ_Файл = етап_значення / 'boot.fat'
        with розділ_Файл.open('wb') as Файл_запис: Файл_запис.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(запустити), '-n', 'JKJAVA', str(розділ_Файл)])
        subprocess.check_call(['mcopy', '-i', str(розділ_Файл), '-s'] + [str(дані_посада) for дані_посада in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 збирання 결과와 같은지 확인한다.
        추출자료 = етап_значення / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(розділ_Файл), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(Дії_корінь / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 ядро_значення SHA256 불일치')
        фото = етап_значення / 'jkoros-native-rpi4.img'
        головний_завантажувальний_запис = bytearray(512)
        головний_завантажувальний_запис[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', запустити, 섹터개수)
        головний_завантажувальний_запис[510:512] = b'\x55\xaa'
        with фото.open('wb') as КР_дані:
            КР_дані.truncate(усього_ресурс); КР_дані.write(головний_завантажувальний_запис); КР_дані.seek(запустити * 512)
            with розділ_Файл.open('rb') as 원본주소: shutil.copyfileobj(원본주소, КР_дані)
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
                    'java_gui_example': '/example/java/ПрикладВікна.java; run: java ПрикладВікна',
                    'framebuffer_resolution': [너비, 높이], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': мікропрограма_значення.name, 'source_sha256': 해시계산(мікропрограма_значення),
                    'image_sha256': 해시계산(фото), 'boot_files': {}}
        for дані_посада in sorted(부팅경로.rglob('*')):
            if дані_посада.is_file(): 꾸러미명세['boot_files'][str(дані_посада.relative_to(부팅경로))] = 해시계산(дані_посада)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux збірка_фото/простір_користувача 디스크는 건드리지 않는다.
        os.replace(str(фото), str(배포경로 / фото.name))
        압축기준 = етап_значення / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(압축기준), 'zip', str(부팅경로))
        os.replace(str(압축기준) + '.zip', str(배포경로 / 'jkoros-native-rpi4-boot.zip'))
        (배포경로 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('генерувати:', 배포경로 / 'jkoros-native-rpi4.img')
    print('фактично_дані Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    запустити()
