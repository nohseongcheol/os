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
from 命令実行 import 計画根
from COSL配布 import 実行束梱包


def ハッシュ計算(経路):
    値 = hashlib.sha256()
    with 経路.open('rb') as ファイル入口:
        for データブロック in iter(lambda: ファイル入口.read(1024 * 1024), b''): 値.update(データブロック)
    return 値.hexdigest()


def 起動処理():
    構文解析器 = argparse.ArgumentParser(description=__doc__)
    構文解析器.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD 起動 HDMI/프레임버퍼 容量')
    解像度値 = 構文解析器.parse_args().resolution
    幅値, 高さ値 = map(int, 解像度値.split('x'))
    画面集合, 画面方式 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[解像度値]
    機器制御コード値 = 計画根 / 'vendor/pi4-firmware.tar.gz'
    期待 = 機器制御コード値.with_name(機器制御コード値.name + '.sha256')
    利用許諾 = 計画根 / 'vendor/LICENCE.broadcom'
    if not 機器制御コード値.is_file() or not 期待.is_file():
        raise SystemExit('공식 Pi 起動 펌웨어 集合値 必要値: ' + str(機器制御コード値))
    if ハッシュ計算(機器制御コード値) != 期待.read_text().split()[0]:
        raise SystemExit('펌웨어 集合値 SHA256 불일치')
    if not 利用許諾.is_file():
        raise SystemExit('起動 펌웨어 라이선스 ファイル 未存在メソッド: ' + str(利用許諾))
    配布経路 = 計画根 / 'dist'
    配布経路.mkdir(exist_ok=True)
    再連結束 = 実行束梱包()
    合計容積, 起動処理 = 128 * 1024 * 1024, 2048
    扇区個数 = 合計容積 // 512 - 起動処理
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(計画根 / 'build')) as 作業中経路:
        工程値 = Path(作業中経路)
        起動経路 = 工程値 / 'boot'
        (起動経路 / 'overlays').mkdir(parents=True)
        ファイル一覧 = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(機器制御コード値)) as 書庫:
            for 名前 in ファイル一覧:
                成員 = 書庫.getmember('./' + 名前)
                if not 成員.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + 名前)
                with 書庫.extractfile(成員) as 原本番地, (起動経路 / 名前).open('wb') as 宛先値位置:
                    shutil.copyfileobj(原本番地, 宛先値位置)
        shutil.copyfile(str(計画根 / 'build/kernel8.img'), str(起動経路 / 'kernel8.img'))
        設定値 = (計画根 / '起動/config.txt').read_text()
        設定値 = 設定値.replace('hdmi_group=2', 'hdmi_group=' + str(画面集合)).replace('hdmi_mode=4', 'hdmi_mode=' + str(画面方式))
        設定値 = 設定値.replace('framebuffer_width=640', 'framebuffer_width=' + str(幅値)).replace('framebuffer_height=480', 'framebuffer_height=' + str(高さ値))
        (起動経路 / 'config.txt').write_text(設定値)
        shutil.copyfile(str(利用許諾), str(起動経路 / 'LICENCE.broadcom'))
        shutil.copyfile(str(計画根 / 'vendor/LICENSE.micropython'), str(起動経路 / 'LICENSE.micropython'))
        for 名前 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(計画根.parents[1] / 名前), str(起動経路 / 名前))
        shutil.copyfile(str(再連結束), str(起動経路 / 再連結束.name))
        for 原本データ, 名前 in ((計画根/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (計画根/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (計画根/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (計画根/'vendor/LICENSE.genet','LICENSE.genet'),
                             (計画根/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (計画根/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (計画根/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (計画根/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(原本データ), str(起動経路/名前))
        for 名前 in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(計画根 / 'vendor' / 名前), str(起動経路 / 名前))
        (起動経路 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 道具/命令実行.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 道具/命令実行.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/案内.md.\n')
        分割ファイル = 工程値 / 'boot.fat'
        with 分割ファイル.open('wb') as ファイル入口: ファイル入口.truncate(扇区個数 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(起動処理), '-n', 'JKJAVA', str(分割ファイル)])
        subprocess.check_call(['mcopy', '-i', str(分割ファイル), '-s'] + [str(データ位置) for データ位置 in sorted(起動経路.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 システム構築 결과와 等価 확인한다.
        抽出済み = 工程値 / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(分割ファイル), '::/kernel8.img', str(抽出済み)])
        if ハッシュ計算(抽出済み) != ハッシュ計算(計画根 / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 中核値 SHA256 불일치')
        イメージ = 工程値 / 'jkoros-native-rpi4.img'
        主担当起動記録 = bytearray(512)
        主担当起動記録[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', 起動処理, 扇区個数)
        主担当起動記録[510:512] = b'\x55\xaa'
        with イメージ.open('wb') as 結果データ:
            結果データ.truncate(合計容積); 結果データ.write(主担当起動記録); 結果データ.seek(起動処理 * 512)
            with 分割ファイル.open('rb') as 原本番地: shutil.copyfileobj(原本番地, 結果データ)
        束管理目録 = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
                    'license': 'COSL with third-party/LGPL carve-outs',
                    'relink_archive': 再連結束.name, 'relink_sha256': ハッシュ計算(再連結束),
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
                    'java_gui_example': '/example/java/窓例.java; run: java 窓例',
                    'framebuffer_resolution': [幅値, 高さ値], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': 機器制御コード値.name, 'source_sha256': ハッシュ計算(機器制御コード値),
                    'image_sha256': ハッシュ計算(イメージ), 'boot_files': {}}
        for データ位置 in sorted(起動経路.rglob('*')):
            if データ位置.is_file(): 束管理目録['boot_files'][str(データ位置.relative_to(起動経路))] = ハッシュ計算(データ位置)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux イメージ構築/利用者 디스크는 건드리지 않는다.
        os.replace(str(イメージ), str(配布経路 / イメージ.name))
        書庫基底 = 工程値 / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(書庫基底), 'zip', str(起動経路))
        os.replace(str(書庫基底) + '.zip', str(配布経路 / 'jkoros-native-rpi4-boot.zip'))
        (配布経路 / 'manifest.json').write_text(json.dumps(束管理目録, indent=2) + '\n')
    print('生成:', 配布経路 / 'jkoros-native-rpi4.img')
    print('実際データ Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    起動処理()
