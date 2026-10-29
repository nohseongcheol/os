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
from ينفذ_أمر import يعرض_جذر
from COSL배포 import يربط_المشارك


def 해시계산(مسار):
    قيمة = hashlib.sha256()
    with مسار.open('rb') as ملف_إدخال_3d0c1245:
        for بيانات_حظر in iter(lambda: ملف_إدخال_3d0c1245.read(1024 * 1024), b''): قيمة.update(بيانات_حظر)
    return قيمة.hexdigest()


def تشغيل():
    المحلل_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    المحلل_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD إقلاع_الآلة HDMI/프레임버퍼 حجم')
    دقة_قيمة = المحلل_48ee4b1b.parse_args().resolution
    너비, ارتفاع_قيمة = map(int, دقة_قيمة.split('x'))
    화면무리, 화면방식 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[دقة_قيمة]
    برنامج_ثابت_قيمة = يعرض_جذر / 'vendor/pi4-firmware.tar.gz'
    예상결과 = برنامج_ثابت_قيمة.with_name(برنامج_ثابت_قيمة.name + '.sha256')
    ترخيص = يعرض_جذر / 'vendor/LICENCE.broadcom'
    if not برنامج_ثابت_قيمة.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi إقلاع_الآلة 펌웨어 يجمع_قيمة 필요: ' + str(برنامج_ثابت_قيمة))
    if 해시계산(برنامج_ثابت_قيمة) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 يجمع_قيمة SHA256 불일치')
    if not ترخيص.is_file():
        raise SystemExit('إقلاع_الآلة 펌웨어 라이선스 ملف 없음: ' + str(ترخيص))
    توزيع_مسار = يعرض_جذر / 'dist'
    توزيع_مسار.mkdir(exist_ok=True)
    재연결꾸러미 = يربط_المشارك()
    إجمالي_قدرة, تشغيل = 128 * 1024 * 1024, 2048
    섹터개수 = إجمالي_قدرة // 512 - تشغيل
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(يعرض_جذر / 'build')) as 작업경로:
        لوحة_قيمة = Path(작업경로)
        부팅경로 = لوحة_قيمة / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        ملف_قائمة = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(برنامج_ثابت_قيمة)) as أرشيف:
            for اسم in ملف_قائمة:
                عضو = أرشيف.getmember('./' + اسم)
                if not عضو.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + اسم)
                with أرشيف.extractfile(عضو) as 원본주소, (부팅경로 / اسم).open('wb') as وجهة_قيمة_منصب:
                    shutil.copyfileobj(원본주소, وجهة_قيمة_منصب)
        shutil.copyfile(str(يعرض_جذر / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        إعدادات = (يعرض_جذر / 'إقلاع_الآلة/config.txt').read_text()
        إعدادات = إعدادات.replace('hdmi_group=2', 'hdmi_group=' + str(화면무리)).replace('hdmi_mode=4', 'hdmi_mode=' + str(화면방식))
        إعدادات = إعدادات.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(ارتفاع_قيمة))
        (부팅경로 / 'config.txt').write_text(إعدادات)
        shutil.copyfile(str(ترخيص), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(يعرض_جذر / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for اسم in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(يعرض_جذر.parents[1] / اسم), str(부팅경로 / اسم))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, اسم in ((يعرض_جذر/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (يعرض_جذر/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (يعرض_جذر/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (يعرض_جذر/'vendor/LICENSE.genet','LICENSE.genet'),
                             (يعرض_جذر/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (يعرض_جذر/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (يعرض_جذر/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (يعرض_جذر/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/اسم))
        for اسم in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(يعرض_جذر / 'vendor' / اسم), str(부팅경로 / اسم))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 أدوات/ينفذ_أمر.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 أدوات/ينفذ_أمر.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/안내.md.\n')
        قسم_ملف = لوحة_قيمة / 'boot.fat'
        with قسم_ملف.open('wb') as ملف_إدخال_3d0c1245: ملف_إدخال_3d0c1245.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(تشغيل), '-n', 'JKJAVA', str(قسم_ملف)])
        subprocess.check_call(['mcopy', '-i', str(قسم_ملف), '-s'] + [str(بيانات_منصب) for بيانات_منصب in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 بنية_نظام 결과와 같은지 확인한다.
        추출자료 = لوحة_قيمة / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(قسم_ملف), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(يعرض_جذر / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 نواة_قيمة SHA256 불일치')
        صورة = لوحة_قيمة / 'jkoros-native-rpi4.img'
        سجل_الإقلاع_الرئيسي = bytearray(512)
        سجل_الإقلاع_الرئيسي[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', تشغيل, 섹터개수)
        سجل_الإقلاع_الرئيسي[510:512] = b'\x55\xaa'
        with صورة.open('wb') as مقياس_بيانات:
            مقياس_بيانات.truncate(إجمالي_قدرة); مقياس_بيانات.write(سجل_الإقلاع_الرئيسي); مقياس_بيانات.seek(تشغيل * 512)
            with قسم_ملف.open('rb') as 원본주소: shutil.copyfileobj(원본주소, مقياس_بيانات)
        يُجمع_بيان = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
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
                    'java_gui_example': '/example/java/مثالنافذة.java; run: java مثالنافذة',
                    'framebuffer_resolution': [너비, ارتفاع_قيمة], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': برنامج_ثابت_قيمة.name, 'source_sha256': 해시계산(برنامج_ثابت_قيمة),
                    'image_sha256': 해시계산(صورة), 'boot_files': {}}
        for بيانات_منصب in sorted(부팅경로.rglob('*')):
            if بيانات_منصب.is_file(): يُجمع_بيان['boot_files'][str(بيانات_منصب.relative_to(부팅경로))] = 해시계산(بيانات_منصب)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux بنية_صورة/فضاء_المستخدم 디스크는 건드리지 않는다.
        os.replace(str(صورة), str(توزيع_مسار / صورة.name))
        أرشيف_أساس = لوحة_قيمة / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(أرشيف_أساس), 'zip', str(부팅경로))
        os.replace(str(أرشيف_أساس) + '.zip', str(توزيع_مسار / 'jkoros-native-rpi4-boot.zip'))
        (توزيع_مسار / 'manifest.json').write_text(json.dumps(يُجمع_بيان, indent=2) + '\n')
    print('إنشاء:', توزيع_مسار / 'jkoros-native-rpi4.img')
    print('الفعلي_بيانات Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    تشغيل()
