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
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ
from COSL배포 import 묶기


def 해시계산(ಮಾರ್ಗ):
    ಮೌಲ್ಯ = hashlib.sha256()
    with ಮಾರ್ಗ.open('rb') as ಫೈಲ್_ನಮೂದು:
        for ಡೇಟಾ_ನಿರ್ಬಂಧಿಸು in iter(lambda: ಫೈಲ್_ನಮೂದು.read(1024 * 1024), b''): ಮೌಲ್ಯ.update(ಡೇಟಾ_ನಿರ್ಬಂಧಿಸು)
    return ಮೌಲ್ಯ.hexdigest()


def ಚಲಾಯಿಸು_2():
    ಪಾರ್ಸರ್_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD 부팅 HDMI/프레임버퍼 ಗಾತ್ರ')
    ರಿಸೊಲ್ಯೂಶನ್_ಮೌಲ್ಯ = ಪಾರ್ಸರ್_48ee4b1b.parse_args().resolution
    너비, 높이 = map(int, ರಿಸೊಲ್ಯೂಶನ್_ಮೌಲ್ಯ.split('x'))
    화면무리, 화면방식 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[ರಿಸೊಲ್ಯೂಶನ್_ಮೌಲ್ಯ]
    기초제어프로그램 = ಬಿಂಬಿಸು_ಮೂಲ / 'vendor/pi4-firmware.tar.gz'
    예상결과 = 기초제어프로그램.with_name(기초제어프로그램.name + '.sha256')
    ಪರವಾನಗಿ = ಬಿಂಬಿಸು_ಮೂಲ / 'vendor/LICENCE.broadcom'
    if not 기초제어프로그램.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi 부팅 펌웨어 ಸಮೂಹ_ಮೌಲ್ಯ 필요: ' + str(기초제어프로그램))
    if 해시계산(기초제어프로그램) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 ಸಮೂಹ_ಮೌಲ್ಯ SHA256 불일치')
    if not ಪರವಾನಗಿ.is_file():
        raise SystemExit('부팅 펌웨어 라이선스 ಕಡತ 없음: ' + str(ಪರವಾನಗಿ))
    배포경로 = ಬಿಂಬಿಸು_ಮೂಲ / 'dist'
    배포경로.mkdir(exist_ok=True)
    재연결꾸러미 = 묶기()
    총량, ಚಲಾಯಿಸು_2 = 128 * 1024 * 1024, 2048
    섹터개수 = 총량 // 512 - ಚಲಾಯಿಸು_2
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(ಬಿಂಬಿಸು_ಮೂಲ / 'build')) as 작업경로:
        ಹಂತ_ಮೌಲ್ಯ = Path(작업경로)
        부팅경로 = ಹಂತ_ಮೌಲ್ಯ / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        ಫೈಲ್_ಪಟ್ಟಿ = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(기초제어프로그램)) as ಅರ್ಖೀವ್:
            for ಹೆಸರು in ಫೈಲ್_ಪಟ್ಟಿ:
                ಸದಸ್ಯ = ಅರ್ಖೀವ್.getmember('./' + ಹೆಸರು)
                if not ಸದಸ್ಯ.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + ಹೆಸರು)
                with ಅರ್ಖೀವ್.extractfile(ಸದಸ್ಯ) as 원본주소, (부팅경로 / ಹೆಸರು).open('wb') as ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ_ಹುದ್ದೆ:
                    shutil.copyfileobj(원본주소, ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ_ಹುದ್ದೆ)
        shutil.copyfile(str(ಬಿಂಬಿಸು_ಮೂಲ / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        ಸಿದ್ಧತೆಗಳು = (ಬಿಂಬಿಸು_ಮೂಲ / '부팅/config.txt').read_text()
        ಸಿದ್ಧತೆಗಳು = ಸಿದ್ಧತೆಗಳು.replace('hdmi_group=2', 'hdmi_group=' + str(화면무리)).replace('hdmi_mode=4', 'hdmi_mode=' + str(화면방식))
        ಸಿದ್ಧತೆಗಳು = ಸಿದ್ಧತೆಗಳು.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(높이))
        (부팅경로 / 'config.txt').write_text(ಸಿದ್ಧತೆಗಳು)
        shutil.copyfile(str(ಪರವಾನಗಿ), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(ಬಿಂಬಿಸು_ಮೂಲ / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for ಹೆಸರು in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(ಬಿಂಬಿಸು_ಮೂಲ.parents[1] / ಹೆಸರು), str(부팅경로 / ಹೆಸರು))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, ಹೆಸರು in ((ಬಿಂಬಿಸು_ಮೂಲ/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (ಬಿಂಬಿಸು_ಮೂಲ/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (ಬಿಂಬಿಸು_ಮೂಲ/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (ಬಿಂಬಿಸು_ಮೂಲ/'vendor/LICENSE.genet','LICENSE.genet'),
                             (ಬಿಂಬಿಸು_ಮೂಲ/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (ಬಿಂಬಿಸು_ಮೂಲ/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (ಬಿಂಬಿಸು_ಮೂಲ/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (ಬಿಂಬಿಸು_ಮೂಲ/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/ಹೆಸರು))
        for ಹೆಸರು in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(ಬಿಂಬಿಸು_ಮೂಲ / 'vendor' / ಹೆಸರು), str(부팅경로 / ಹೆಸರು))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 ಪರಿಕರಗಳು/ಪೂರೈಸು_ಆದೇಶ.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 ಪರಿಕರಗಳು/ಪೂರೈಸು_ಆದೇಶ.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/README_ಫೈಲ್_eb81d7d9.md.\n')
        ವಿಭಜನೆ_ಫೈಲ್ = ಹಂತ_ಮೌಲ್ಯ / 'boot.fat'
        with ವಿಭಜನೆ_ಫೈಲ್.open('wb') as ಫೈಲ್_ನಮೂದು: ಫೈಲ್_ನಮೂದು.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(ಚಲಾಯಿಸು_2), '-n', 'JKJAVA', str(ವಿಭಜನೆ_ಫೈಲ್)])
        subprocess.check_call(['mcopy', '-i', str(ವಿಭಜನೆ_ಫೈಲ್), '-s'] + [str(ಡೇಟಾ_ಹುದ್ದೆ) for ಡೇಟಾ_ಹುದ್ದೆ in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ 결과와 같은지 확인한다.
        추출자료 = ಹಂತ_ಮೌಲ್ಯ / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(ವಿಭಜನೆ_ಫೈಲ್), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(ಬಿಂಬಿಸು_ಮೂಲ / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 ಕರ್ನಲ್_ಮೌಲ್ಯ SHA256 불일치')
        ಇಮೇಜ್ = ಹಂತ_ಮೌಲ್ಯ / 'jkoros-native-rpi4.img'
        주부트기록 = bytearray(512)
        주부트기록[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', ಚಲಾಯಿಸು_2, 섹터개수)
        주부트기록[510:512] = b'\x55\xaa'
        with ಇಮೇಜ್.open('wb') as ಮಾಪನ_ಡೇಟಾ:
            ಮಾಪನ_ಡೇಟಾ.truncate(총량); ಮಾಪನ_ಡೇಟಾ.write(주부트기록); ಮಾಪನ_ಡೇಟಾ.seek(ಚಲಾಯಿಸು_2 * 512)
            with ವಿಭಜನೆ_ಫೈಲ್.open('rb') as 원본주소: shutil.copyfileobj(원본주소, ಮಾಪನ_ಡೇಟಾ)
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
                    'source_archive': 기초제어프로그램.name, 'source_sha256': 해시계산(기초제어프로그램),
                    'image_sha256': 해시계산(ಇಮೇಜ್), 'boot_files': {}}
        for ಡೇಟಾ_ಹುದ್ದೆ in sorted(부팅경로.rglob('*')):
            if ಡೇಟಾ_ಹುದ್ದೆ.is_file(): 꾸러미명세['boot_files'][str(ಡೇಟಾ_ಹುದ್ದೆ.relative_to(부팅경로))] = 해시계산(ಡೇಟಾ_ಹುದ್ದೆ)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux ಬಿಲ್ಡ್_ಇಮೇಜ್/ಬಳಕೆದಾರ 디스크는 건드리지 않는다.
        os.replace(str(ಇಮೇಜ್), str(배포경로 / ಇಮೇಜ್.name))
        압축기준 = ಹಂತ_ಮೌಲ್ಯ / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(압축기준), 'zip', str(부팅경로))
        os.replace(str(압축기준) + '.zip', str(배포경로 / 'jkoros-native-rpi4-boot.zip'))
        (배포경로 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('ರಚಿಸಿ:', 배포경로 / 'jkoros-native-rpi4.img')
    print('ನಿಜವಾದ_ಡೇಟಾ Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    ಚಲಾಯಿಸು_2()
