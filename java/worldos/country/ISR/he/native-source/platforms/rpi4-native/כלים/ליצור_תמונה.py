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
from לבצע_פקודה import לשקף_בסיס
from COSL배포 import לאגד_משתתף


def 해시계산(נתיב):
    ערך = hashlib.sha256()
    with נתיב.open('rb') as קובץ_ערך:
        for נתונים_בלוק in iter(lambda: קובץ_ערך.read(1024 * 1024), b''): ערך.update(נתונים_בלוק)
    return ערך.hexdigest()


def הפעלה():
    מנתח_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    מנתח_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD 부팅 HDMI/프레임버퍼 גודל')
    רזולוציה_ערך = מנתח_48ee4b1b.parse_args().resolution
    너비, גובה_ערך = map(int, רזולוציה_ערך.split('x'))
    화면무리, 화면방식 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[רזולוציה_ערך]
    קושחה_ערך = לשקף_בסיס / 'vendor/pi4-firmware.tar.gz'
    예상결과 = קושחה_ערך.with_name(קושחה_ערך.name + '.sha256')
    רשיון = לשקף_בסיס / 'vendor/LICENCE.broadcom'
    if not קושחה_ערך.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi 부팅 펌웨어 לקבץ_ערך 필요: ' + str(קושחה_ערך))
    if 해시계산(קושחה_ערך) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 לקבץ_ערך SHA256 불일치')
    if not רשיון.is_file():
        raise SystemExit('부팅 펌웨어 라이선스 קובץ 없음: ' + str(רשיון))
    הפצה_נתיב = לשקף_בסיס / 'dist'
    הפצה_נתיב.mkdir(exist_ok=True)
    재연결꾸러미 = לאגד_משתתף()
    סך_הכל_קיבולת, הפעלה = 128 * 1024 * 1024, 2048
    섹터개수 = סך_הכל_קיבולת // 512 - הפעלה
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(לשקף_בסיס / 'build')) as 작업경로:
        במה_ערך = Path(작업경로)
        부팅경로 = במה_ערך / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        קובץ_רשימה = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(קושחה_ערך)) as ארכיון:
            for שם in קובץ_רשימה:
                חבר = ארכיון.getmember('./' + שם)
                if not חבר.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + שם)
                with ארכיון.extractfile(חבר) as 원본주소, (부팅경로 / שם).open('wb') as יעד_ערך_עמדה:
                    shutil.copyfileobj(원본주소, יעד_ערך_עמדה)
        shutil.copyfile(str(לשקף_בסיס / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        הגדרות = (לשקף_בסיס / '부팅/config.txt').read_text()
        הגדרות = הגדרות.replace('hdmi_group=2', 'hdmi_group=' + str(화면무리)).replace('hdmi_mode=4', 'hdmi_mode=' + str(화면방식))
        הגדרות = הגדרות.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(גובה_ערך))
        (부팅경로 / 'config.txt').write_text(הגדרות)
        shutil.copyfile(str(רשיון), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(לשקף_בסיס / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for שם in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(לשקף_בסיס.parents[1] / שם), str(부팅경로 / שם))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, שם in ((לשקף_בסיס/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (לשקף_בסיס/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (לשקף_בסיס/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (לשקף_בסיס/'vendor/LICENSE.genet','LICENSE.genet'),
                             (לשקף_בסיס/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (לשקף_בסיס/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (לשקף_בסיס/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (לשקף_בסיס/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/שם))
        for שם in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(לשקף_בסיס / 'vendor' / שם), str(부팅경로 / שם))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 כלים/לבצע_פקודה.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 כלים/לבצע_פקודה.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/안내.md.\n')
        מחיצה_קובץ = במה_ערך / 'boot.fat'
        with מחיצה_קובץ.open('wb') as קובץ_ערך: קובץ_ערך.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(הפעלה), '-n', 'JKJAVA', str(מחיצה_קובץ)])
        subprocess.check_call(['mcopy', '-i', str(מחיצה_קובץ), '-s'] + [str(נתונים_עמדה) for נתונים_עמדה in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 בנייה 결과와 같은지 확인한다.
        추출자료 = במה_ערך / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(מחיצה_קובץ), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(לשקף_בסיס / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 ליבה_ערך SHA256 불일치')
        תמונה = במה_ערך / 'jkoros-native-rpi4.img'
        רשומת_אתחול_ראשית = bytearray(512)
        רשומת_אתחול_ראשית[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', הפעלה, 섹터개수)
        רשומת_אתחול_ראשית[510:512] = b'\x55\xaa'
        with תמונה.open('wb') as תוצאה_נתונים:
            תוצאה_נתונים.truncate(סך_הכל_קיבולת); תוצאה_נתונים.write(רשומת_אתחול_ראשית); תוצאה_נתונים.seek(הפעלה * 512)
            with מחיצה_קובץ.open('rb') as 원본주소: shutil.copyfileobj(원본주소, תוצאה_נתונים)
        חבילה_מניפסט = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
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
                    'java_gui_example': '/example/java/דוגמתחלון.java; run: java דוגמתחלון',
                    'framebuffer_resolution': [너비, גובה_ערך], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': קושחה_ערך.name, 'source_sha256': 해시계산(קושחה_ערך),
                    'image_sha256': 해시계산(תמונה), 'boot_files': {}}
        for נתונים_עמדה in sorted(부팅경로.rglob('*')):
            if נתונים_עמדה.is_file(): חבילה_מניפסט['boot_files'][str(נתונים_עמדה.relative_to(부팅경로))] = 해시계산(נתונים_עמדה)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux בנה_תמונה/משתמש 디스크는 건드리지 않는다.
        os.replace(str(תמונה), str(הפצה_נתיב / תמונה.name))
        압축기준 = במה_ערך / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(압축기준), 'zip', str(부팅경로))
        os.replace(str(압축기준) + '.zip', str(הפצה_נתיב / 'jkoros-native-rpi4-boot.zip'))
        (הפצה_נתיב / 'manifest.json').write_text(json.dumps(חבילה_מניפסט, indent=2) + '\n')
    print('יצר:', הפצה_נתיב / 'jkoros-native-rpi4.img')
    print('בפועל_נתונים Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    הפעלה()
