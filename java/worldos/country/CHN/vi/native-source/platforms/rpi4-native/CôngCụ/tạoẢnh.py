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
from thựcThiLệnh import gốcCâyDựÁn
from BảnPhânPhốiCOSL import GóiTệpThựcThi


def tínhMãBăm(đườngDẫn):
    giáTrị = hashlib.sha256()
    with đườngDẫn.open('rb') as mụcTệp:
        for khốiDữLiệu in iter(lambda: mụcTệp.read(1024 * 1024), b''): giáTrị.update(khốiDữLiệu)
    return giáTrị.hexdigest()


def chạy():
    BộPhânTích = argparse.ArgumentParser(description=__doc__)
    BộPhânTích.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD KhởiĐộng HDMI/프레임버퍼 cỡ')
    giáTrịĐộPhânGiải = BộPhânTích.parse_args().resolution
    giáTrịRộng, giáTrịCao = map(int, giáTrịĐộPhânGiải.split('x'))
    nhómMànHình, chếĐộMànHình = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[giáTrịĐộPhânGiải]
    giáTrịPhầnSụn = gốcCâyDựÁn / 'vendor/pi4-firmware.tar.gz'
    dựKiến = giáTrịPhầnSụn.with_name(giáTrịPhầnSụn.name + '.sha256')
    giấyPhép = gốcCâyDựÁn / 'vendor/LICENCE.broadcom'
    if not giáTrịPhầnSụn.is_file() or not dựKiến.is_file():
        raise SystemExit('공식 Pi KhởiĐộng 펌웨어 giáTrịNhóm giáTrịCầnĐến: ' + str(giáTrịPhầnSụn))
    if tínhMãBăm(giáTrịPhầnSụn) != dựKiến.read_text().split()[0]:
        raise SystemExit('펌웨어 giáTrịNhóm SHA256 불일치')
    if not giấyPhép.is_file():
        raise SystemExit('KhởiĐộng 펌웨어 라이선스 Tệp phươngThứcThiếu: ' + str(giấyPhép))
    đườngDẫnBảnPhânPhối = gốcCâyDựÁn / 'dist'
    đườngDẫnBảnPhânPhối.mkdir(exist_ok=True)
    góiGộpLiênKếtLại = GóiTệpThựcThi()
    sứcChứaTổngCộng, chạy = 128 * 1024 * 1024, 2048
    sốLượngCungTừ = sứcChứaTổngCộng // 512 - chạy
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(gốcCâyDựÁn / 'build')) as đườngDẫnĐangLàmViệc:
        giáTrịGiaiĐoạn = Path(đườngDẫnĐangLàmViệc)
        đườngDẫnKhởiĐộng = giáTrịGiaiĐoạn / 'boot'
        (đườngDẫnKhởiĐộng / 'overlays').mkdir(parents=True)
        danhSáchTệp = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(giáTrịPhầnSụn)) as khoLưuTrữ:
            for tên in danhSáchTệp:
                thànhViên = khoLưuTrữ.getmember('./' + tên)
                if not thànhViên.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + tên)
                with khoLưuTrữ.extractfile(thànhViên) as địaChỉNguyênBản, (đườngDẫnKhởiĐộng / tên).open('wb') as vịTríGiáTrịĐích:
                    shutil.copyfileobj(địaChỉNguyênBản, vịTríGiáTrịĐích)
        shutil.copyfile(str(gốcCâyDựÁn / 'build/kernel8.img'), str(đườngDẫnKhởiĐộng / 'kernel8.img'))
        cácThiếtLập = (gốcCâyDựÁn / 'KhởiĐộng/config.txt').read_text()
        cácThiếtLập = cácThiếtLập.replace('hdmi_group=2', 'hdmi_group=' + str(nhómMànHình)).replace('hdmi_mode=4', 'hdmi_mode=' + str(chếĐộMànHình))
        cácThiếtLập = cácThiếtLập.replace('framebuffer_width=640', 'framebuffer_width=' + str(giáTrịRộng)).replace('framebuffer_height=480', 'framebuffer_height=' + str(giáTrịCao))
        (đườngDẫnKhởiĐộng / 'config.txt').write_text(cácThiếtLập)
        shutil.copyfile(str(giấyPhép), str(đườngDẫnKhởiĐộng / 'LICENCE.broadcom'))
        shutil.copyfile(str(gốcCâyDựÁn / 'vendor/LICENSE.micropython'), str(đườngDẫnKhởiĐộng / 'LICENSE.micropython'))
        for tên in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(gốcCâyDựÁn.parents[1] / tên), str(đườngDẫnKhởiĐộng / tên))
        shutil.copyfile(str(góiGộpLiênKếtLại), str(đườngDẫnKhởiĐộng / góiGộpLiênKếtLại.name))
        for dữLiệuNguyênBản, tên in ((gốcCâyDựÁn/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (gốcCâyDựÁn/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (gốcCâyDựÁn/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (gốcCâyDựÁn/'vendor/LICENSE.genet','LICENSE.genet'),
                             (gốcCâyDựÁn/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (gốcCâyDựÁn/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (gốcCâyDựÁn/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (gốcCâyDựÁn/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(dữLiệuNguyênBản), str(đườngDẫnKhởiĐộng/tên))
        for tên in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(gốcCâyDựÁn / 'vendor' / tên), str(đườngDẫnKhởiĐộng / tên))
        (đườngDẫnKhởiĐộng / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 CôngCụ/thựcThiLệnh.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 CôngCụ/thựcThiLệnh.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/HướngDẫn.md.\n')
        tệpPhânVùng = giáTrịGiaiĐoạn / 'boot.fat'
        with tệpPhânVùng.open('wb') as mụcTệp: mụcTệp.truncate(sốLượngCungTừ * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(chạy), '-n', 'JKJAVA', str(tệpPhânVùng)])
        subprocess.check_call(['mcopy', '-i', str(tệpPhânVùng), '-s'] + [str(vịTríDữLiệu) for vịTríDữLiệu in sorted(đườngDẫnKhởiĐộng.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 xâyDựngHệThống 결과와 bằng 확인한다.
        đãTríchXuất = giáTrịGiaiĐoạn / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(tệpPhânVùng), '::/kernel8.img', str(đãTríchXuất)])
        if tínhMãBăm(đãTríchXuất) != tínhMãBăm(gốcCâyDựÁn / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 giáTrịNhân SHA256 불일치')
        ảnh = giáTrịGiaiĐoạn / 'jkoros-native-rpi4.img'
        BảnGhiKhởiĐộngChủĐạo = bytearray(512)
        BảnGhiKhởiĐộngChủĐạo[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', chạy, sốLượngCungTừ)
        BảnGhiKhởiĐộngChủĐạo[510:512] = b'\x55\xaa'
        with ảnh.open('wb') as dữLiệuKếtQuả:
            dữLiệuKếtQuả.truncate(sứcChứaTổngCộng); dữLiệuKếtQuả.write(BảnGhiKhởiĐộngChủĐạo); dữLiệuKếtQuả.seek(chạy * 512)
            with tệpPhânVùng.open('rb') as địaChỉNguyênBản: shutil.copyfileobj(địaChỉNguyênBản, dữLiệuKếtQuả)
        bảnKêGóiGộp = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
                    'license': 'COSL with third-party/LGPL carve-outs',
                    'relink_archive': góiGộpLiênKếtLại.name, 'relink_sha256': tínhMãBăm(góiGộpLiênKếtLại),
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
                    'java_gui_example': '/example/java/VíDụCửaSổ.java; run: java VíDụCửaSổ',
                    'framebuffer_resolution': [giáTrịRộng, giáTrịCao], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': giáTrịPhầnSụn.name, 'source_sha256': tínhMãBăm(giáTrịPhầnSụn),
                    'image_sha256': tínhMãBăm(ảnh), 'boot_files': {}}
        for vịTríDữLiệu in sorted(đườngDẫnKhởiĐộng.rglob('*')):
            if vịTríDữLiệu.is_file(): bảnKêGóiGộp['boot_files'][str(vịTríDữLiệu.relative_to(đườngDẫnKhởiĐộng))] = tínhMãBăm(vịTríDữLiệu)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux xâyDựngẢnh/NgườiDùng 디스크는 건드리지 않는다.
        os.replace(str(ảnh), str(đườngDẫnBảnPhânPhối / ảnh.name))
        cơSởKhoLưuTrữ = giáTrịGiaiĐoạn / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(cơSởKhoLưuTrữ), 'zip', str(đườngDẫnKhởiĐộng))
        os.replace(str(cơSởKhoLưuTrữ) + '.zip', str(đườngDẫnBảnPhânPhối / 'jkoros-native-rpi4-boot.zip'))
        (đườngDẫnBảnPhânPhối / 'manifest.json').write_text(json.dumps(bảnKêGóiGộp, indent=2) + '\n')
    print('sinh:', đườngDẫnBảnPhânPhối / 'jkoros-native-rpi4.img')
    print('dữLiệuThựcTế Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    chạy()
