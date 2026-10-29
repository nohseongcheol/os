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
from köra_kommando import åtgärd_rot
from COSL배포 import BIND_deltagare


def 해시계산(sökväg_2):
    värde = hashlib.sha256()
    with sökväg_2.open('rb') as fil_post:
        for datablock in iter(lambda: fil_post.read(1024 * 1024), b''): värde.update(datablock)
    return värde.hexdigest()


def Kör():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD maskinstart HDMI/프레임버퍼 Storlek')
    upplösning_värde = parser_48ee4b1b.parse_args().resolution
    너비, 높이 = map(int, upplösning_värde.split('x'))
    skärmbild_grupp, skärmbild_läge = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[upplösning_värde]
    inbyggd_programvara_värde = åtgärd_rot / 'vendor/pi4-firmware.tar.gz'
    예상결과 = inbyggd_programvara_värde.with_name(inbyggd_programvara_värde.name + '.sha256')
    licens = åtgärd_rot / 'vendor/LICENCE.broadcom'
    if not inbyggd_programvara_värde.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi maskinstart 펌웨어 grupp_värde 필요: ' + str(inbyggd_programvara_värde))
    if 해시계산(inbyggd_programvara_värde) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 grupp_värde SHA256 불일치')
    if not licens.is_file():
        raise SystemExit('maskinstart 펌웨어 라이선스 filnamn 없음: ' + str(licens))
    fördelning_väg = åtgärd_rot / 'dist'
    fördelning_väg.mkdir(exist_ok=True)
    재연결꾸러미 = BIND_deltagare()
    summa_kapacitet, Kör = 128 * 1024 * 1024, 2048
    섹터개수 = summa_kapacitet // 512 - Kör
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(åtgärd_rot / 'build')) as 작업경로:
        scen_värde = Path(작업경로)
        부팅경로 = scen_värde / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        fillista = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(inbyggd_programvara_värde)) as Arkiv:
            for Namn in fillista:
                medlem = Arkiv.getmember('./' + Namn)
                if not medlem.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + Namn)
                with Arkiv.extractfile(medlem) as 원본주소, (부팅경로 / Namn).open('wb') as mål_värde_placera:
                    shutil.copyfileobj(원본주소, mål_värde_placera)
        shutil.copyfile(str(åtgärd_rot / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        Inställningar = (åtgärd_rot / 'maskinstart/config.txt').read_text()
        Inställningar = Inställningar.replace('hdmi_group=2', 'hdmi_group=' + str(skärmbild_grupp)).replace('hdmi_mode=4', 'hdmi_mode=' + str(skärmbild_läge))
        Inställningar = Inställningar.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(높이))
        (부팅경로 / 'config.txt').write_text(Inställningar)
        shutil.copyfile(str(licens), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(åtgärd_rot / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for Namn in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(åtgärd_rot.parents[1] / Namn), str(부팅경로 / Namn))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, Namn in ((åtgärd_rot/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (åtgärd_rot/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (åtgärd_rot/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (åtgärd_rot/'vendor/LICENSE.genet','LICENSE.genet'),
                             (åtgärd_rot/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (åtgärd_rot/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (åtgärd_rot/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (åtgärd_rot/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/Namn))
        for Namn in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(åtgärd_rot / 'vendor' / Namn), str(부팅경로 / Namn))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 verktyg/köra_kommando.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 verktyg/köra_kommando.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/VIKTIGT_eb81d7d9.md.\n')
        partition_fil = scen_värde / 'boot.fat'
        with partition_fil.open('wb') as fil_post: fil_post.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(Kör), '-n', 'JKJAVA', str(partition_fil)])
        subprocess.check_call(['mcopy', '-i', str(partition_fil), '-s'] + [str(data_placera) for data_placera in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 version_System 결과와 같은지 확인한다.
        추출자료 = scen_värde / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(partition_fil), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(åtgärd_rot / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 kärna_värde SHA256 불일치')
        BILD = scen_värde / 'jkoros-native-rpi4.img'
        huvudstartpost = bytearray(512)
        huvudstartpost[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', Kör, 섹터개수)
        huvudstartpost[510:512] = b'\x55\xaa'
        with BILD.open('wb') as KR_data:
            KR_data.truncate(summa_kapacitet); KR_data.write(huvudstartpost); KR_data.seek(Kör * 512)
            with partition_fil.open('rb') as 원본주소: shutil.copyfileobj(원본주소, KR_data)
        bunt_manifest = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
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
                    'java_gui_example': '/example/java/Fönsterexempel.java; run: java Fönsterexempel',
                    'framebuffer_resolution': [너비, 높이], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': inbyggd_programvara_värde.name, 'source_sha256': 해시계산(inbyggd_programvara_värde),
                    'image_sha256': 해시계산(BILD), 'boot_files': {}}
        for data_placera in sorted(부팅경로.rglob('*')):
            if data_placera.is_file(): bunt_manifest['boot_files'][str(data_placera.relative_to(부팅경로))] = 해시계산(data_placera)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux version_BILD/användarutrymme 디스크는 건드리지 않는다.
        os.replace(str(BILD), str(fördelning_väg / BILD.name))
        Arkiv_BAS = scen_värde / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(Arkiv_BAS), 'zip', str(부팅경로))
        os.replace(str(Arkiv_BAS) + '.zip', str(fördelning_väg / 'jkoros-native-rpi4-boot.zip'))
        (fördelning_väg / 'manifest.json').write_text(json.dumps(bunt_manifest, indent=2) + '\n')
    print('generera:', fördelning_väg / 'jkoros-native-rpi4.img')
    print('verklig_data Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    Kör()
