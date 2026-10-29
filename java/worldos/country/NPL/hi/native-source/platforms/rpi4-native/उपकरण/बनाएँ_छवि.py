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
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल
from COSL배포 import बाइंड_करें_एंडपॉइंट


def 해시계산(पथ):
    मान = hashlib.sha256()
    with पथ.open('rb') as फ़ाइल_एन्ट्री:
        for डेटा_ब्_लॉक in iter(lambda: फ़ाइल_एन्ट्री.read(1024 * 1024), b''): मान.update(डेटा_ब्_लॉक)
    return मान.hexdigest()


def चलाएँ():
    पार्सर_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    पार्सर_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD 부팅 HDMI/프레임버퍼 आकार')
    रिज़ॉल्यूशन_मान = पार्सर_48ee4b1b.parse_args().resolution
    너비, 높이 = map(int, रिज़ॉल्यूशन_मान.split('x'))
    화면무리, 화면방식 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[रिज़ॉल्यूशन_मान]
    फ़र्मवेयर_मान = प्रोजेक्ट_करें_मूल / 'vendor/pi4-firmware.tar.gz'
    예상결과 = फ़र्मवेयर_मान.with_name(फ़र्मवेयर_मान.name + '.sha256')
    लाइसेंस = प्रोजेक्ट_करें_मूल / 'vendor/LICENCE.broadcom'
    if not फ़र्मवेयर_मान.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi 부팅 펌웨어 समूह_मान 필요: ' + str(फ़र्मवेयर_मान))
    if 해시계산(फ़र्मवेयर_मान) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 समूह_मान SHA256 불일치')
    if not लाइसेंस.is_file():
        raise SystemExit('부팅 펌웨어 라이선스 संचिका 없음: ' + str(लाइसेंस))
    배포경로 = प्रोजेक्ट_करें_मूल / 'dist'
    배포경로.mkdir(exist_ok=True)
    재연결꾸러미 = बाइंड_करें_एंडपॉइंट()
    총량, चलाएँ = 128 * 1024 * 1024, 2048
    섹터개수 = 총량 // 512 - चलाएँ
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(प्रोजेक्ट_करें_मूल / 'build')) as 작업경로:
        स्टेज_मान = Path(작업경로)
        부팅경로 = स्टेज_मान / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        फ़ाइल_सूची = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(फ़र्मवेयर_मान)) as संग्रह:
            for नाम in फ़ाइल_सूची:
                सदस्य = संग्रह.getmember('./' + नाम)
                if not सदस्य.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + नाम)
                with संग्रह.extractfile(सदस्य) as 원본주소, (부팅경로 / नाम).open('wb') as गंतव्य_मान_पद:
                    shutil.copyfileobj(원본주소, गंतव्य_मान_पद)
        shutil.copyfile(str(प्रोजेक्ट_करें_मूल / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        विन्यास = (प्रोजेक्ट_करें_मूल / '부팅/config.txt').read_text()
        विन्यास = विन्यास.replace('hdmi_group=2', 'hdmi_group=' + str(화면무리)).replace('hdmi_mode=4', 'hdmi_mode=' + str(화면방식))
        विन्यास = विन्यास.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(높이))
        (부팅경로 / 'config.txt').write_text(विन्यास)
        shutil.copyfile(str(लाइसेंस), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(प्रोजेक्ट_करें_मूल / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for नाम in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(प्रोजेक्ट_करें_मूल.parents[1] / नाम), str(부팅경로 / नाम))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, नाम in ((प्रोजेक्ट_करें_मूल/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (प्रोजेक्ट_करें_मूल/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (प्रोजेक्ट_करें_मूल/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (प्रोजेक्ट_करें_मूल/'vendor/LICENSE.genet','LICENSE.genet'),
                             (प्रोजेक्ट_करें_मूल/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (प्रोजेक्ट_करें_मूल/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (प्रोजेक्ट_करें_मूल/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (प्रोजेक्ट_करें_मूल/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/नाम))
        for नाम in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(प्रोजेक्ट_करें_मूल / 'vendor' / नाम), str(부팅경로 / नाम))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 उपकरण/निष्पादित_करें_आदेश.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 उपकरण/निष्पादित_करें_आदेश.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/ReadMe_फ़ाइल_eb81d7d9.md.\n')
        विभाजन_फ़ाइल = स्टेज_मान / 'boot.fat'
        with विभाजन_फ़ाइल.open('wb') as फ़ाइल_एन्ट्री: फ़ाइल_एन्ट्री.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(चलाएँ), '-n', 'JKJAVA', str(विभाजन_फ़ाइल)])
        subprocess.check_call(['mcopy', '-i', str(विभाजन_फ़ाइल), '-s'] + [str(डेटा_पद) for डेटा_पद in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 बिल्ड_सिस्टम 결과와 같은지 확인한다.
        추출자료 = स्टेज_मान / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(विभाजन_फ़ाइल), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(प्रोजेक्ट_करें_मूल / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 कर्नेल_मान SHA256 불일치')
        छवि = स्टेज_मान / 'jkoros-native-rpi4.img'
        मास्टर_बूट_रेकॉर्ड = bytearray(512)
        मास्टर_बूट_रेकॉर्ड[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', चलाएँ, 섹터개수)
        मास्टर_बूट_रेकॉर्ड[510:512] = b'\x55\xaa'
        with छवि.open('wb') as परिणाम_डेटा:
            परिणाम_डेटा.truncate(총량); परिणाम_डेटा.write(मास्टर_बूट_रेकॉर्ड); परिणाम_डेटा.seek(चलाएँ * 512)
            with विभाजन_फ़ाइल.open('rb') as 원본주소: shutil.copyfileobj(원본주소, परिणाम_डेटा)
        बंडल_सूची = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
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
                    'java_gui_example': '/example/java/खिड़कीउदाहरण.java; run: java खिड़कीउदाहरण',
                    'framebuffer_resolution': [너비, 높이], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': फ़र्मवेयर_मान.name, 'source_sha256': 해시계산(फ़र्मवेयर_मान),
                    'image_sha256': 해시계산(छवि), 'boot_files': {}}
        for डेटा_पद in sorted(부팅경로.rglob('*')):
            if डेटा_पद.is_file(): बंडल_सूची['boot_files'][str(डेटा_पद.relative_to(부팅경로))] = 해시계산(डेटा_पद)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux बिल्ड_छवि/उपयोगकर्ता 디스크는 건드리지 않는다.
        os.replace(str(छवि), str(배포경로 / छवि.name))
        압축기준 = स्टेज_मान / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(압축기준), 'zip', str(부팅경로))
        os.replace(str(압축기준) + '.zip', str(배포경로 / 'jkoros-native-rpi4-boot.zip'))
        (배포경로 / 'manifest.json').write_text(json.dumps(बंडल_सूची, indent=2) + '\n')
    print('जनरेट_करें:', 배포경로 / 'jkoros-native-rpi4.img')
    print('वास्तविक_डेटा Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    चलाएँ()
