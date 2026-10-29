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
from 執行命令 import 項目根
from COSL分發 import 可執行束打包


def 計算哈希(路徑):
    值 = hashlib.sha256()
    with 路徑.open('rb') as 檔案條目:
        for 資料塊 in iter(lambda: 檔案條目.read(1024 * 1024), b''): 值.update(資料塊)
    return 值.hexdigest()


def 運行():
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD 啓動 HDMI/프레임버퍼 大小')
    分辨率值 = 解析器.parse_args().resolution
    寬度值, 高度值 = map(int, 分辨率值.split('x'))
    屏幕組, 屏幕模式 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[分辨率值]
    固件值 = 項目根 / 'vendor/pi4-firmware.tar.gz'
    預期 = 固件值.with_name(固件值.name + '.sha256')
    許可 = 項目根 / 'vendor/LICENCE.broadcom'
    if not 固件值.is_file() or not 預期.is_file():
        raise SystemExit('공식 Pi 啓動 펌웨어 組值 所需條件值: ' + str(固件值))
    if 計算哈希(固件值) != 預期.read_text().split()[0]:
        raise SystemExit('펌웨어 組值 SHA256 불일치')
    if not 許可.is_file():
        raise SystemExit('啓動 펌웨어 라이선스 檔案 缺失方法: ' + str(許可))
    分發路徑 = 項目根 / 'dist'
    分發路徑.mkdir(exist_ok=True)
    重新鏈接捆綁 = 可執行束打包()
    總計容量, 運行 = 128 * 1024 * 1024, 2048
    扇區個數 = 總計容量 // 512 - 運行
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(項目根 / 'build')) as 工作中路徑:
        階段值 = Path(工作中路徑)
        啓動路徑 = 階段值 / 'boot'
        (啓動路徑 / 'overlays').mkdir(parents=True)
        檔案列表 = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(固件值)) as 存檔:
            for 名稱 in 檔案列表:
                成員 = 存檔.getmember('./' + 名稱)
                if not 成員.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + 名稱)
                with 存檔.extractfile(成員) as 原始地址, (啓動路徑 / 名稱).open('wb') as 目的地址值位置:
                    shutil.copyfileobj(原始地址, 目的地址值位置)
        shutil.copyfile(str(項目根 / 'build/kernel8.img'), str(啓動路徑 / 'kernel8.img'))
        設置 = (項目根 / '啓動/config.txt').read_text()
        設置 = 設置.replace('hdmi_group=2', 'hdmi_group=' + str(屏幕組)).replace('hdmi_mode=4', 'hdmi_mode=' + str(屏幕模式))
        設置 = 設置.replace('framebuffer_width=640', 'framebuffer_width=' + str(寬度值)).replace('framebuffer_height=480', 'framebuffer_height=' + str(高度值))
        (啓動路徑 / 'config.txt').write_text(設置)
        shutil.copyfile(str(許可), str(啓動路徑 / 'LICENCE.broadcom'))
        shutil.copyfile(str(項目根 / 'vendor/LICENSE.micropython'), str(啓動路徑 / 'LICENSE.micropython'))
        for 名稱 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(項目根.parents[1] / 名稱), str(啓動路徑 / 名稱))
        shutil.copyfile(str(重新鏈接捆綁), str(啓動路徑 / 重新鏈接捆綁.name))
        for 原始資料, 名稱 in ((項目根/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (項目根/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (項目根/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (項目根/'vendor/LICENSE.genet','LICENSE.genet'),
                             (項目根/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (項目根/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (項目根/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (項目根/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(原始資料), str(啓動路徑/名稱))
        for 名稱 in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(項目根 / 'vendor' / 名稱), str(啓動路徑 / 名稱))
        (啓動路徑 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 工具集/執行命令.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 工具集/執行命令.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/指南.md.\n')
        分區檔案 = 階段值 / 'boot.fat'
        with 分區檔案.open('wb') as 檔案條目: 檔案條目.truncate(扇區個數 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(運行), '-n', 'JKJAVA', str(分區檔案)])
        subprocess.check_call(['mcopy', '-i', str(分區檔案), '-s'] + [str(資料位置) for 資料位置 in sorted(啓動路徑.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 構建系統 결과와 相等 확인한다.
        已提取 = 階段值 / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(分區檔案), '::/kernel8.img', str(已提取)])
        if 計算哈希(已提取) != 計算哈希(項目根 / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 內核值 SHA256 불일치')
        映像 = 階段值 / 'jkoros-native-rpi4.img'
        主控啓動記錄 = bytearray(512)
        主控啓動記錄[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', 運行, 扇區個數)
        主控啓動記錄[510:512] = b'\x55\xaa'
        with 映像.open('wb') as 結果資料:
            結果資料.truncate(總計容量); 結果資料.write(主控啓動記錄); 結果資料.seek(運行 * 512)
            with 分區檔案.open('rb') as 原始地址: shutil.copyfileobj(原始地址, 結果資料)
        捆綁構建清單 = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
                    'license': 'COSL with third-party/LGPL carve-outs',
                    'relink_archive': 重新鏈接捆綁.name, 'relink_sha256': 計算哈希(重新鏈接捆綁),
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
                    'java_gui_example': '/example/java/窗口例.java; run: java 窗口例',
                    'framebuffer_resolution': [寬度值, 高度值], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': 固件值.name, 'source_sha256': 計算哈希(固件值),
                    'image_sha256': 計算哈希(映像), 'boot_files': {}}
        for 資料位置 in sorted(啓動路徑.rglob('*')):
            if 資料位置.is_file(): 捆綁構建清單['boot_files'][str(資料位置.relative_to(啓動路徑))] = 計算哈希(資料位置)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux 構建映像/使用者 디스크는 건드리지 않는다.
        os.replace(str(映像), str(分發路徑 / 映像.name))
        存檔基底 = 階段值 / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(存檔基底), 'zip', str(啓動路徑))
        os.replace(str(存檔基底) + '.zip', str(分發路徑 / 'jkoros-native-rpi4-boot.zip'))
        (分發路徑 / 'manifest.json').write_text(json.dumps(捆綁構建清單, indent=2) + '\n')
    print('生成:', 分發路徑 / 'jkoros-native-rpi4.img')
    print('實際資料 Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    運行()
