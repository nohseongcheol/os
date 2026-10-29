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
from ดําเนินการ_คําสั่ง import แสดง_ราก
from COSL배포 import ผูก_ปลายทาง


def 해시계산(เส้นทาง):
    ค่า = hashlib.sha256()
    with เส้นทาง.open('rb') as แฟ้ม_รายการ_3d0c1245:
        for ข้อมูล_บล็อก in iter(lambda: แฟ้ม_รายการ_3d0c1245.read(1024 * 1024), b''): ค่า.update(ข้อมูล_บล็อก)
    return ค่า.hexdigest()


def เรียกใช้งาน():
    ตัวแยกวิเคราะห์_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD 부팅 HDMI/프레임버퍼 ขนาด')
    ความละเอียด_ค่า = ตัวแยกวิเคราะห์_48ee4b1b.parse_args().resolution
    너비, 높이 = map(int, ความละเอียด_ค่า.split('x'))
    화면무리, 화면방식 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[ความละเอียด_ค่า]
    เฟิร์มแวร์_ค่า = แสดง_ราก / 'vendor/pi4-firmware.tar.gz'
    예상결과 = เฟิร์มแวร์_ค่า.with_name(เฟิร์มแวร์_ค่า.name + '.sha256')
    สิทธิการใช้งาน = แสดง_ราก / 'vendor/LICENCE.broadcom'
    if not เฟิร์มแวร์_ค่า.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi 부팅 펌웨어 กลุ่ม_ค่า 필요: ' + str(เฟิร์มแวร์_ค่า))
    if 해시계산(เฟิร์มแวร์_ค่า) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 กลุ่ม_ค่า SHA256 불일치')
    if not สิทธิการใช้งาน.is_file():
        raise SystemExit('부팅 펌웨어 라이선스 แฟ้ม 없음: ' + str(สิทธิการใช้งาน))
    การกระจาย_พาธ = แสดง_ราก / 'dist'
    การกระจาย_พาธ.mkdir(exist_ok=True)
    재연결꾸러미 = ผูก_ปลายทาง()
    รวม_ความจุ, เรียกใช้งาน = 128 * 1024 * 1024, 2048
    섹터개수 = รวม_ความจุ // 512 - เรียกใช้งาน
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(แสดง_ราก / 'build')) as 작업경로:
        สเตจ_ค่า = Path(작업경로)
        부팅경로 = สเตจ_ค่า / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        แฟ้ม_รายการ = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(เฟิร์มแวร์_ค่า)) as เก็บถาวร:
            for ชื่อ in แฟ้ม_รายการ:
                สมาชิก = เก็บถาวร.getmember('./' + ชื่อ)
                if not สมาชิก.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + ชื่อ)
                with เก็บถาวร.extractfile(สมาชิก) as 원본주소, (부팅경로 / ชื่อ).open('wb') as ปลายทาง_ค่า_ตําแหน่ง:
                    shutil.copyfileobj(원본주소, ปลายทาง_ค่า_ตําแหน่ง)
        shutil.copyfile(str(แสดง_ราก / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        ตั้งค่า = (แสดง_ราก / '부팅/config.txt').read_text()
        ตั้งค่า = ตั้งค่า.replace('hdmi_group=2', 'hdmi_group=' + str(화면무리)).replace('hdmi_mode=4', 'hdmi_mode=' + str(화면방식))
        ตั้งค่า = ตั้งค่า.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(높이))
        (부팅경로 / 'config.txt').write_text(ตั้งค่า)
        shutil.copyfile(str(สิทธิการใช้งาน), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(แสดง_ราก / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for ชื่อ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(แสดง_ราก.parents[1] / ชื่อ), str(부팅경로 / ชื่อ))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, ชื่อ in ((แสดง_ราก/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (แสดง_ราก/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (แสดง_ราก/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (แสดง_ราก/'vendor/LICENSE.genet','LICENSE.genet'),
                             (แสดง_ราก/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (แสดง_ราก/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (แสดง_ราก/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (แสดง_ราก/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/ชื่อ))
        for ชื่อ in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(แสดง_ราก / 'vendor' / ชื่อ), str(부팅경로 / ชื่อ))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 เครื่องมือ/ดําเนินการ_คําสั่ง.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 เครื่องมือ/ดําเนินการ_คําสั่ง.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/안내.md.\n')
        พาร์ติชัน_แฟ้ม = สเตจ_ค่า / 'boot.fat'
        with พาร์ติชัน_แฟ้ม.open('wb') as แฟ้ม_รายการ_3d0c1245: แฟ้ม_รายการ_3d0c1245.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(เรียกใช้งาน), '-n', 'JKJAVA', str(พาร์ติชัน_แฟ้ม)])
        subprocess.check_call(['mcopy', '-i', str(พาร์ติชัน_แฟ้ม), '-s'] + [str(ข้อมูล_ตําแหน่ง) for ข้อมูล_ตําแหน่ง in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 สร้าง 결과와 같은지 확인한다.
        추출자료 = สเตจ_ค่า / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(พาร์ติชัน_แฟ้ม), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(แสดง_ราก / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 เคอร์เนล_ค่า SHA256 불일치')
        รูป = สเตจ_ค่า / 'jkoros-native-rpi4.img'
        มาสเตอร์บูตเรกคอร์ด = bytearray(512)
        มาสเตอร์บูตเรกคอร์ด[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', เรียกใช้งาน, 섹터개수)
        มาสเตอร์บูตเรกคอร์ด[510:512] = b'\x55\xaa'
        with รูป.open('wb') as เมตริก_ข้อมูล:
            เมตริก_ข้อมูล.truncate(รวม_ความจุ); เมตริก_ข้อมูล.write(มาสเตอร์บูตเรกคอร์ด); เมตริก_ข้อมูล.seek(เรียกใช้งาน * 512)
            with พาร์ติชัน_แฟ้ม.open('rb') as 원본주소: shutil.copyfileobj(원본주소, เมตริก_ข้อมูล)
        รวม_ไฟล์กํากับ = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
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
                    'source_archive': เฟิร์มแวร์_ค่า.name, 'source_sha256': 해시계산(เฟิร์มแวร์_ค่า),
                    'image_sha256': 해시계산(รูป), 'boot_files': {}}
        for ข้อมูล_ตําแหน่ง in sorted(부팅경로.rglob('*')):
            if ข้อมูล_ตําแหน่ง.is_file(): รวม_ไฟล์กํากับ['boot_files'][str(ข้อมูล_ตําแหน่ง.relative_to(부팅경로))] = 해시계산(ข้อมูล_ตําแหน่ง)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux รุ่น_รูป/ผู้ใช้ 디스크는 건드리지 않는다.
        os.replace(str(รูป), str(การกระจาย_พาธ / รูป.name))
        เก็บถาวร_ฐาน = สเตจ_ค่า / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(เก็บถาวร_ฐาน), 'zip', str(부팅경로))
        os.replace(str(เก็บถาวร_ฐาน) + '.zip', str(การกระจาย_พาธ / 'jkoros-native-rpi4-boot.zip'))
        (การกระจาย_พาธ / 'manifest.json').write_text(json.dumps(รวม_ไฟล์กํากับ, indent=2) + '\n')
    print('สร้าง_167eff27:', การกระจาย_พาธ / 'jkoros-native-rpi4.img')
    print('ค่าจริง_ข้อมูล Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    เรียกใช้งาน()
