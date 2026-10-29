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
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ
from सीओएसएल_वितरण import बाइंड_करा_संचारटोक


def गणनाकरा_हॅश(मार्ग):
    मूल्य = hashlib.sha256()
    with मार्ग.open('rb') as संचिका_प्रविष्टी:
        for डेटा_अवरोधित_करा in iter(lambda: संचिका_प्रविष्टी.read(1024 * 1024), b''): मूल्य.update(डेटा_अवरोधित_करा)
    return मूल्य.hexdigest()


def सुरू_करा():
    व्याकरणविश्लेषक_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    व्याकरणविश्लेषक_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD प्रणालीप्रारंभ HDMI/프레임버퍼 आकार')
    बिंदूघनता_मूल्य = व्याकरणविश्लेषक_48ee4b1b.parse_args().resolution
    रुंदी_मूल्य, उंची_मूल्य = map(int, बिंदूघनता_मूल्य.split('x'))
    पडदा_समूह, पडदा_मोड = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[बिंदूघनता_मूल्य]
    उपकरणसूत्र_मूल्य = प्रोजेक्ट_मूळ / 'vendor/pi4-firmware.tar.gz'
    अपेक्षित = उपकरणसूत्र_मूल्य.with_name(उपकरणसूत्र_मूल्य.name + '.sha256')
    परवाना = प्रोजेक्ट_मूळ / 'vendor/LICENCE.broadcom'
    if not उपकरणसूत्र_मूल्य.is_file() or not अपेक्षित.is_file():
        raise SystemExit('공식 Pi प्रणालीप्रारंभ 펌웨어 समूह_मूल्य आवश्यक_मूल्य: ' + str(उपकरणसूत्र_मूल्य))
    if गणनाकरा_हॅश(उपकरणसूत्र_मूल्य) != अपेक्षित.read_text().split()[0]:
        raise SystemExit('펌웨어 समूह_मूल्य SHA256 불일치')
    if not परवाना.is_file():
        raise SystemExit('प्रणालीप्रारंभ 펌웨어 라이선스 फाइल अनुपस्थित_पद्धत: ' + str(परवाना))
    वितरण_पथ = प्रोजेक्ट_मूळ / 'dist'
    वितरण_पथ.mkdir(exist_ok=True)
    पुनर्जोडणी_बंडल = बाइंड_करा_संचारटोक()
    एकूण_धारणक्षमता, सुरू_करा = 128 * 1024 * 1024, 2048
    त्रिज्यखंड_संख्या = एकूण_धारणक्षमता // 512 - सुरू_करा
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(प्रोजेक्ट_मूळ / 'build')) as कार्यरत_पथ:
        टप्पा_मूल्य = Path(कार्यरत_पथ)
        प्रणालीप्रारंभ_पथ = टप्पा_मूल्य / 'boot'
        (प्रणालीप्रारंभ_पथ / 'overlays').mkdir(parents=True)
        संचिका_यादी = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(उपकरणसूत्र_मूल्य)) as संग्रह:
            for नाव in संचिका_यादी:
                सदस्य = संग्रह.getmember('./' + नाव)
                if not सदस्य.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + नाव)
                with संग्रह.extractfile(सदस्य) as मूळ_पत्ता_4c9bece9, (प्रणालीप्रारंभ_पथ / नाव).open('wb') as गंतव्यस्थान_मूल्य_स्थान:
                    shutil.copyfileobj(मूळ_पत्ता_4c9bece9, गंतव्यस्थान_मूल्य_स्थान)
        shutil.copyfile(str(प्रोजेक्ट_मूळ / 'build/kernel8.img'), str(प्रणालीप्रारंभ_पथ / 'kernel8.img'))
        संयोजना = (प्रोजेक्ट_मूळ / 'प्रणालीप्रारंभ/config.txt').read_text()
        संयोजना = संयोजना.replace('hdmi_group=2', 'hdmi_group=' + str(पडदा_समूह)).replace('hdmi_mode=4', 'hdmi_mode=' + str(पडदा_मोड))
        संयोजना = संयोजना.replace('framebuffer_width=640', 'framebuffer_width=' + str(रुंदी_मूल्य)).replace('framebuffer_height=480', 'framebuffer_height=' + str(उंची_मूल्य))
        (प्रणालीप्रारंभ_पथ / 'config.txt').write_text(संयोजना)
        shutil.copyfile(str(परवाना), str(प्रणालीप्रारंभ_पथ / 'LICENCE.broadcom'))
        shutil.copyfile(str(प्रोजेक्ट_मूळ / 'vendor/LICENSE.micropython'), str(प्रणालीप्रारंभ_पथ / 'LICENSE.micropython'))
        for नाव in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(प्रोजेक्ट_मूळ.parents[1] / नाव), str(प्रणालीप्रारंभ_पथ / नाव))
        shutil.copyfile(str(पुनर्जोडणी_बंडल), str(प्रणालीप्रारंभ_पथ / पुनर्जोडणी_बंडल.name))
        for मूळ_डेटा, नाव in ((प्रोजेक्ट_मूळ/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (प्रोजेक्ट_मूळ/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (प्रोजेक्ट_मूळ/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (प्रोजेक्ट_मूळ/'vendor/LICENSE.genet','LICENSE.genet'),
                             (प्रोजेक्ट_मूळ/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (प्रोजेक्ट_मूळ/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (प्रोजेक्ट_मूळ/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (प्रोजेक्ट_मूळ/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(मूळ_डेटा), str(प्रणालीप्रारंभ_पथ/नाव))
        for नाव in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(प्रोजेक्ट_मूळ / 'vendor' / नाव), str(प्रणालीप्रारंभ_पथ / नाव))
        (प्रणालीप्रारंभ_पथ / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 साधने/आज्ञा_कार्यवाही_करा.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 साधने/आज्ञा_कार्यवाही_करा.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/वापरमार्गदर्शिका_eb81d7d9.md.\n')
        विभाजन_संचिका = टप्पा_मूल्य / 'boot.fat'
        with विभाजन_संचिका.open('wb') as संचिका_प्रविष्टी: संचिका_प्रविष्टी.truncate(त्रिज्यखंड_संख्या * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(सुरू_करा), '-n', 'JKJAVA', str(विभाजन_संचिका)])
        subprocess.check_call(['mcopy', '-i', str(विभाजन_संचिका), '-s'] + [str(डेटा_स्थान) for डेटा_स्थान in sorted(प्रणालीप्रारंभ_पथ.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 सिस्टम_बांधणी 결과와 समान 확인한다.
        बाहेरकाढलेले = टप्पा_मूल्य / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(विभाजन_संचिका), '::/kernel8.img', str(बाहेरकाढलेले)])
        if गणनाकरा_हॅश(बाहेरकाढलेले) != गणनाकरा_हॅश(प्रोजेक्ट_मूळ / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 गाभा_मूल्य SHA256 불일치')
        चित्र = टप्पा_मूल्य / 'jkoros-native-rpi4.img'
        मुख्य_प्रणालीप्रारंभ_नोंद = bytearray(512)
        मुख्य_प्रणालीप्रारंभ_नोंद[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', सुरू_करा, त्रिज्यखंड_संख्या)
        मुख्य_प्रणालीप्रारंभ_नोंद[510:512] = b'\x55\xaa'
        with चित्र.open('wb') as मोजमाप_डेटा:
            मोजमाप_डेटा.truncate(एकूण_धारणक्षमता); मोजमाप_डेटा.write(मुख्य_प्रणालीप्रारंभ_नोंद); मोजमाप_डेटा.seek(सुरू_करा * 512)
            with विभाजन_संचिका.open('rb') as मूळ_पत्ता_4c9bece9: shutil.copyfileobj(मूळ_पत्ता_4c9bece9, मोजमाप_डेटा)
        बंडल_सूचीलेख = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
                    'license': 'COSL with third-party/LGPL carve-outs',
                    'relink_archive': पुनर्जोडणी_बंडल.name, 'relink_sha256': गणनाकरा_हॅश(पुनर्जोडणी_बंडल),
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
                    'java_gui_example': '/example/java/खिडकीउदाहरण.java; run: java खिडकीउदाहरण',
                    'framebuffer_resolution': [रुंदी_मूल्य, उंची_मूल्य], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': उपकरणसूत्र_मूल्य.name, 'source_sha256': गणनाकरा_हॅश(उपकरणसूत्र_मूल्य),
                    'image_sha256': गणनाकरा_हॅश(चित्र), 'boot_files': {}}
        for डेटा_स्थान in sorted(प्रणालीप्रारंभ_पथ.rglob('*')):
            if डेटा_स्थान.is_file(): बंडल_सूचीलेख['boot_files'][str(डेटा_स्थान.relative_to(प्रणालीप्रारंभ_पथ))] = गणनाकरा_हॅश(डेटा_स्थान)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux चित्र_बांधणी/प्रयोक्ता 디스크는 건드리지 않는다.
        os.replace(str(चित्र), str(वितरण_पथ / चित्र.name))
        संग्रह_पाया = टप्पा_मूल्य / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(संग्रह_पाया), 'zip', str(प्रणालीप्रारंभ_पथ))
        os.replace(str(संग्रह_पाया) + '.zip', str(वितरण_पथ / 'jkoros-native-rpi4-boot.zip'))
        (वितरण_पथ / 'manifest.json').write_text(json.dumps(बंडल_सूचीलेख, indent=2) + '\n')
    print('तयार_करा:', वितरण_पथ / 'jkoros-native-rpi4.img')
    print('वास्तविक_डेटा Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    सुरू_करा()
