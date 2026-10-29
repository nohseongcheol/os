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
from εκτελώ_εντολή import έργο_ρίζα
from COSL배포 import συνδέω_τελικό_σημείο_bbe6b410


def 해시계산(ΔΙΑΔΡΟΜΗ):
    τιμή = hashlib.sha256()
    with ΔΙΑΔΡΟΜΗ.open('rb') as Αρχείο_καταχώρηση:
        for μπλοκ_δεδομένων in iter(lambda: Αρχείο_καταχώρηση.read(1024 * 1024), b''): τιμή.update(μπλοκ_δεδομένων)
    return τιμή.hexdigest()


def Εκτέλεση_2():
    ανάλυση_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ανάλυση_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD 부팅 HDMI/프레임버퍼 Μέγεθος')
    ανάλυση_τιμή = ανάλυση_48ee4b1b.parse_args().resolution
    너비, ύψος_τιμή = map(int, ανάλυση_τιμή.split('x'))
    화면무리, 화면방식 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[ανάλυση_τιμή]
    기초제어프로그램 = έργο_ρίζα / 'vendor/pi4-firmware.tar.gz'
    예상결과 = 기초제어프로그램.with_name(기초제어프로그램.name + '.sha256')
    Άδεια_Χρήσης = έργο_ρίζα / 'vendor/LICENCE.broadcom'
    if not 기초제어프로그램.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi 부팅 펌웨어 Ομάδα_τιμή 필요: ' + str(기초제어프로그램))
    if 해시계산(기초제어프로그램) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 Ομάδα_τιμή SHA256 불일치')
    if not Άδεια_Χρήσης.is_file():
        raise SystemExit('부팅 펌웨어 라이선스 Αρχείο 없음: ' + str(Άδεια_Χρήσης))
    배포경로 = έργο_ρίζα / 'dist'
    배포경로.mkdir(exist_ok=True)
    재연결꾸러미 = συνδέω_τελικό_σημείο_bbe6b410()
    σύνολο_Δυνατότητα, Εκτέλεση_2 = 128 * 1024 * 1024, 2048
    섹터개수 = σύνολο_Δυνατότητα // 512 - Εκτέλεση_2
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(έργο_ρίζα / 'build')) as 작업경로:
        σκηνή_τιμή = Path(작업경로)
        부팅경로 = σκηνή_τιμή / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        λίστα_αρχείων = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(기초제어프로그램)) as Αρχειοθήκη:
            for Όνομα in λίστα_αρχείων:
                μέλος = Αρχειοθήκη.getmember('./' + Όνομα)
                if not μέλος.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + Όνομα)
                with Αρχειοθήκη.extractfile(μέλος) as 원본주소, (부팅경로 / Όνομα).open('wb') as προορισμός_τιμή_θέση:
                    shutil.copyfileobj(원본주소, προορισμός_τιμή_θέση)
        shutil.copyfile(str(έργο_ρίζα / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        Ρυθμίσεις = (έργο_ρίζα / '부팅/config.txt').read_text()
        Ρυθμίσεις = Ρυθμίσεις.replace('hdmi_group=2', 'hdmi_group=' + str(화면무리)).replace('hdmi_mode=4', 'hdmi_mode=' + str(화면방식))
        Ρυθμίσεις = Ρυθμίσεις.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(ύψος_τιμή))
        (부팅경로 / 'config.txt').write_text(Ρυθμίσεις)
        shutil.copyfile(str(Άδεια_Χρήσης), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(έργο_ρίζα / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for Όνομα in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(έργο_ρίζα.parents[1] / Όνομα), str(부팅경로 / Όνομα))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, Όνομα in ((έργο_ρίζα/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (έργο_ρίζα/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (έργο_ρίζα/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (έργο_ρίζα/'vendor/LICENSE.genet','LICENSE.genet'),
                             (έργο_ρίζα/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (έργο_ρίζα/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (έργο_ρίζα/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (έργο_ρίζα/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/Όνομα))
        for Όνομα in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(έργο_ρίζα / 'vendor' / Όνομα), str(부팅경로 / Όνομα))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 Εργαλεία/εκτελώ_εντολή.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 Εργαλεία/εκτελώ_εντολή.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/αρχείο_readme_eb81d7d9.md.\n')
        διαμέρισμα_Αρχείο = σκηνή_τιμή / 'boot.fat'
        with διαμέρισμα_Αρχείο.open('wb') as Αρχείο_καταχώρηση: Αρχείο_καταχώρηση.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(Εκτέλεση_2), '-n', 'JKJAVA', str(διαμέρισμα_Αρχείο)])
        subprocess.check_call(['mcopy', '-i', str(διαμέρισμα_Αρχείο), '-s'] + [str(δεδομένα_θέση) for δεδομένα_θέση in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 δομή_Σύστημα 결과와 같은지 확인한다.
        추출자료 = σκηνή_τιμή / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(διαμέρισμα_Αρχείο), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(έργο_ρίζα / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 πυρήνας_τιμή SHA256 불일치')
        εικόνα = σκηνή_τιμή / 'jkoros-native-rpi4.img'
        κύρια_εγγραφή_εκκίνησης = bytearray(512)
        κύρια_εγγραφή_εκκίνησης[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', Εκτέλεση_2, 섹터개수)
        κύρια_εγγραφή_εκκίνησης[510:512] = b'\x55\xaa'
        with εικόνα.open('wb') as μέτρηση_δεδομένα:
            μέτρηση_δεδομένα.truncate(σύνολο_Δυνατότητα); μέτρηση_δεδομένα.write(κύρια_εγγραφή_εκκίνησης); μέτρηση_δεδομένα.seek(Εκτέλεση_2 * 512)
            with διαμέρισμα_Αρχείο.open('rb') as 원본주소: shutil.copyfileobj(원본주소, μέτρηση_δεδομένα)
        πακέτο_διακήρυξη = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
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
                    'java_gui_example': '/example/java/ΠαράδειγμαΠαραθύρου.java; run: java ΠαράδειγμαΠαραθύρου',
                    'framebuffer_resolution': [너비, ύψος_τιμή], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': 기초제어프로그램.name, 'source_sha256': 해시계산(기초제어프로그램),
                    'image_sha256': 해시계산(εικόνα), 'boot_files': {}}
        for δεδομένα_θέση in sorted(부팅경로.rglob('*')):
            if δεδομένα_θέση.is_file(): πακέτο_διακήρυξη['boot_files'][str(δεδομένα_θέση.relative_to(부팅경로))] = 해시계산(δεδομένα_θέση)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux δομή_εικόνα/χρήστης 디스크는 건드리지 않는다.
        os.replace(str(εικόνα), str(배포경로 / εικόνα.name))
        압축기준 = σκηνή_τιμή / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(압축기준), 'zip', str(부팅경로))
        os.replace(str(압축기준) + '.zip', str(배포경로 / 'jkoros-native-rpi4-boot.zip'))
        (배포경로 / 'manifest.json').write_text(json.dumps(πακέτο_διακήρυξη, indent=2) + '\n')
    print('δημιουργώ:', 배포경로 / 'jkoros-native-rpi4.img')
    print('πραγματικός_δεδομένα Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    Εκτέλεση_2()
