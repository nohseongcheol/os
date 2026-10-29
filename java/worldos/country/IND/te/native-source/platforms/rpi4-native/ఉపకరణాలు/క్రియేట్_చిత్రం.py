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
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం
from COSL배포 import 묶기


def 해시계산(పాత్):
    మూల్యం = hashlib.sha256()
    with పాత్.open('rb') as ఫైలు_ప్రవేశం:
        for డేటా_నిరోధించు in iter(lambda: ఫైలు_ప్రవేశం.read(1024 * 1024), b''): మూల్యం.update(డేటా_నిరోధించు)
    return మూల్యం.hexdigest()


def నడుపుము():
    పార్సర్_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    పార్సర్_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD 부팅 HDMI/프레임버퍼 పరిమాణం')
    స్పష్టత_మూల్యం = పార్సర్_48ee4b1b.parse_args().resolution
    너비, 높이 = map(int, స్పష్టత_మూల్యం.split('x'))
    화면무리, 화면방식 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[స్పష్టత_మూల్యం]
    기초제어프로그램 = ప్రొజెక్ట్_మూలం / 'vendor/pi4-firmware.tar.gz'
    예상결과 = 기초제어프로그램.with_name(기초제어프로그램.name + '.sha256')
    లైసెన్స్ = ప్రొజెక్ట్_మూలం / 'vendor/LICENCE.broadcom'
    if not 기초제어프로그램.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi 부팅 펌웨어 సమూహం_మూల్యం 필요: ' + str(기초제어프로그램))
    if 해시계산(기초제어프로그램) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 సమూహం_మూల్యం SHA256 불일치')
    if not లైసెన్స్.is_file():
        raise SystemExit('부팅 펌웨어 라이선스 దస్త్రం 없음: ' + str(లైసెన్స్))
    배포경로 = ప్రొజెక్ట్_మూలం / 'dist'
    배포경로.mkdir(exist_ok=True)
    재연결꾸러미 = 묶기()
    총량, నడుపుము = 128 * 1024 * 1024, 2048
    섹터개수 = 총량 // 512 - నడుపుము
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(ప్రొజెక్ట్_మూలం / 'build')) as 작업경로:
        దశ_మూల్యం = Path(작업경로)
        부팅경로 = దశ_మూల్యం / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        ఫైలు_జాబితా = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(기초제어프로그램)) as ఆర్కైవ్:
            for పేరు in ఫైలు_జాబితా:
                సభ్యుడు = ఆర్కైవ్.getmember('./' + పేరు)
                if not సభ్యుడు.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + పేరు)
                with ఆర్కైవ్.extractfile(సభ్యుడు) as 원본주소, (부팅경로 / పేరు).open('wb') as గమ్యం_మూల్యం_స్థాయి:
                    shutil.copyfileobj(원본주소, గమ్యం_మూల్యం_స్థాయి)
        shutil.copyfile(str(ప్రొజెక్ట్_మూలం / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        అమరికలు = (ప్రొజెక్ట్_మూలం / '부팅/config.txt').read_text()
        అమరికలు = అమరికలు.replace('hdmi_group=2', 'hdmi_group=' + str(화면무리)).replace('hdmi_mode=4', 'hdmi_mode=' + str(화면방식))
        అమరికలు = అమరికలు.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(높이))
        (부팅경로 / 'config.txt').write_text(అమరికలు)
        shutil.copyfile(str(లైసెన్స్), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(ప్రొజెక్ట్_మూలం / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for పేరు in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(ప్రొజెక్ట్_మూలం.parents[1] / పేరు), str(부팅경로 / పేరు))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, పేరు in ((ప్రొజెక్ట్_మూలం/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (ప్రొజెక్ట్_మూలం/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (ప్రొజెక్ట్_మూలం/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (ప్రొజెక్ట్_మూలం/'vendor/LICENSE.genet','LICENSE.genet'),
                             (ప్రొజెక్ట్_మూలం/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (ప్రొజెక్ట్_మూలం/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (ప్రొజెక్ట్_మూలం/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (ప్రొజెక్ట్_మూలం/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/పేరు))
        for పేరు in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(ప్రొజెక్ట్_మూలం / 'vendor' / పేరు), str(부팅경로 / పేరు))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 ఉపకరణాలు/అమలు_చేయి_ఆదేశం.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 ఉపకరణాలు/అమలు_చేయి_ఆదేశం.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/మార్గదర్శక_సమాచారం_eb81d7d9.md.\n')
        విభజన_ఫైలు = దశ_మూల్యం / 'boot.fat'
        with విభజన_ఫైలు.open('wb') as ఫైలు_ప్రవేశం: ఫైలు_ప్రవేశం.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(నడుపుము), '-n', 'JKJAVA', str(విభజన_ఫైలు)])
        subprocess.check_call(['mcopy', '-i', str(విభజన_ఫైలు), '-s'] + [str(డేటా_స్థాయి) for డేటా_స్థాయి in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 బిల్డ్_సిస్టం 결과와 같은지 확인한다.
        추출자료 = దశ_మూల్యం / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(విభజన_ఫైలు), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(ప్రొజెక్ట్_మూలం / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 కెర్నల్_మూల్యం SHA256 불일치')
        చిత్రం = దశ_మూల్యం / 'jkoros-native-rpi4.img'
        주부트기록 = bytearray(512)
        주부트기록[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', నడుపుము, 섹터개수)
        주부트기록[510:512] = b'\x55\xaa'
        with చిత్రం.open('wb') as ప్రమాణం_డేటా:
            ప్రమాణం_డేటా.truncate(총량); ప్రమాణం_డేటా.write(주부트기록); ప్రమాణం_డేటా.seek(నడుపుము * 512)
            with విభజన_ఫైలు.open('rb') as 원본주소: shutil.copyfileobj(원본주소, ప్రమాణం_డేటా)
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
                    'image_sha256': 해시계산(చిత్రం), 'boot_files': {}}
        for డేటా_స్థాయి in sorted(부팅경로.rglob('*')):
            if డేటా_స్థాయి.is_file(): 꾸러미명세['boot_files'][str(డేటా_స్థాయి.relative_to(부팅경로))] = 해시계산(డేటా_స్థాయి)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux బిల్డ్_చిత్రం/వినియోగదారు 디스크는 건드리지 않는다.
        os.replace(str(చిత్రం), str(배포경로 / చిత్రం.name))
        압축기준 = దశ_మూల్యం / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(압축기준), 'zip', str(부팅경로))
        os.replace(str(압축기준) + '.zip', str(배포경로 / 'jkoros-native-rpi4-boot.zip'))
        (배포경로 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('రూపొందించు:', 배포경로 / 'jkoros-native-rpi4.img')
    print('వాస్తవ_డేటా Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    నడుపుము()
