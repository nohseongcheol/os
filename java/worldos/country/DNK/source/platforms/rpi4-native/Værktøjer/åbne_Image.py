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
from Udfør_kommando import To_do_rod
from COSL배포 import BIND_slutpunkt


def 해시계산(Sti):
    VÆRDI = hashlib.sha256()
    with Sti.open('rb') as fil_post:
        for datablok in iter(lambda: fil_post.read(1024 * 1024), b''): VÆRDI.update(datablok)
    return VÆRDI.hexdigest()


def Kør_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD 부팅 HDMI/프레임버퍼 Størrelse')
    opløsning_VÆRDI = parser_48ee4b1b.parse_args().resolution
    너비, 높이 = map(int, opløsning_VÆRDI.split('x'))
    skærmbillede_gruppe, skærmbillede_HYPPIGST = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[opløsning_VÆRDI]
    Firmware_VÆRDI = To_do_rod / 'vendor/pi4-firmware.tar.gz'
    예상결과 = Firmware_VÆRDI.with_name(Firmware_VÆRDI.name + '.sha256')
    licens = To_do_rod / 'vendor/LICENCE.broadcom'
    if not Firmware_VÆRDI.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi 부팅 펌웨어 gruppe_VÆRDI 필요: ' + str(Firmware_VÆRDI))
    if 해시계산(Firmware_VÆRDI) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 gruppe_VÆRDI SHA256 불일치')
    if not licens.is_file():
        raise SystemExit('부팅 펌웨어 라이선스 Fil 없음: ' + str(licens))
    distribution_sti = To_do_rod / 'dist'
    distribution_sti.mkdir(exist_ok=True)
    재연결꾸러미 = BIND_slutpunkt()
    i_alt_kapacitet, Kør_2 = 128 * 1024 * 1024, 2048
    섹터개수 = i_alt_kapacitet // 512 - Kør_2
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(To_do_rod / 'build')) as 작업경로:
        fase_VÆRDI = Path(작업경로)
        부팅경로 = fase_VÆRDI / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        filliste = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(Firmware_VÆRDI)) as Arkiv:
            for Navn in filliste:
                medlem = Arkiv.getmember('./' + Navn)
                if not medlem.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + Navn)
                with Arkiv.extractfile(medlem) as 원본주소, (부팅경로 / Navn).open('wb') as destination_VÆRDI_placere:
                    shutil.copyfileobj(원본주소, destination_VÆRDI_placere)
        shutil.copyfile(str(To_do_rod / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        Indstillinger = (To_do_rod / '부팅/config.txt').read_text()
        Indstillinger = Indstillinger.replace('hdmi_group=2', 'hdmi_group=' + str(skærmbillede_gruppe)).replace('hdmi_mode=4', 'hdmi_mode=' + str(skærmbillede_HYPPIGST))
        Indstillinger = Indstillinger.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(높이))
        (부팅경로 / 'config.txt').write_text(Indstillinger)
        shutil.copyfile(str(licens), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(To_do_rod / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for Navn in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(To_do_rod.parents[1] / Navn), str(부팅경로 / Navn))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, Navn in ((To_do_rod/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (To_do_rod/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (To_do_rod/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (To_do_rod/'vendor/LICENSE.genet','LICENSE.genet'),
                             (To_do_rod/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (To_do_rod/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (To_do_rod/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (To_do_rod/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/Navn))
        for Navn in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(To_do_rod / 'vendor' / Navn), str(부팅경로 / Navn))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 Værktøjer/Udfør_kommando.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 Værktøjer/Udfør_kommando.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/Vigtigt_eb81d7d9.md.\n')
        partition_fil = fase_VÆRDI / 'boot.fat'
        with partition_fil.open('wb') as fil_post: fil_post.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(Kør_2), '-n', 'JKJAVA', str(partition_fil)])
        subprocess.check_call(['mcopy', '-i', str(partition_fil), '-s'] + [str(data_placere) for data_placere in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 build_System 결과와 같은지 확인한다.
        추출자료 = fase_VÆRDI / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(partition_fil), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(To_do_rod / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 kerne_VÆRDI SHA256 불일치')
        Image = fase_VÆRDI / 'jkoros-native-rpi4.img'
        MBR = bytearray(512)
        MBR[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', Kør_2, 섹터개수)
        MBR[510:512] = b'\x55\xaa'
        with Image.open('wb') as KR_data:
            KR_data.truncate(i_alt_kapacitet); KR_data.write(MBR); KR_data.seek(Kør_2 * 512)
            with partition_fil.open('rb') as 원본주소: shutil.copyfileobj(원본주소, KR_data)
        bundt_manifest = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
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
                    'java_gui_example': '/example/java/Vindueseksempel.java; run: java Vindueseksempel',
                    'framebuffer_resolution': [너비, 높이], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': Firmware_VÆRDI.name, 'source_sha256': 해시계산(Firmware_VÆRDI),
                    'image_sha256': 해시계산(Image), 'boot_files': {}}
        for data_placere in sorted(부팅경로.rglob('*')):
            if data_placere.is_file(): bundt_manifest['boot_files'][str(data_placere.relative_to(부팅경로))] = 해시계산(data_placere)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux build_Image/bruger 디스크는 건드리지 않는다.
        os.replace(str(Image), str(distribution_sti / Image.name))
        Arkiv_BASIS = fase_VÆRDI / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(Arkiv_BASIS), 'zip', str(부팅경로))
        os.replace(str(Arkiv_BASIS) + '.zip', str(distribution_sti / 'jkoros-native-rpi4-boot.zip'))
        (distribution_sti / 'manifest.json').write_text(json.dumps(bundt_manifest, indent=2) + '\n')
    print('generere:', distribution_sti / 'jkoros-native-rpi4.img')
    print('faktisk_data Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    Kør_2()
