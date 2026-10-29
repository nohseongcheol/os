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
from Utfør_kommando import speile_rot
from COSL배포 import BIND_deltaker


def 해시계산(Sti):
    VERDI = hashlib.sha256()
    with Sti.open('rb') as Fil_oppføring:
        for data_blokk in iter(lambda: Fil_oppføring.read(1024 * 1024), b''): VERDI.update(data_blokk)
    return VERDI.hexdigest()


def Kjør_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD 부팅 HDMI/프레임버퍼 Størrelse')
    oppløsning_VERDI = parser_48ee4b1b.parse_args().resolution
    너비, 높이 = map(int, oppløsning_VERDI.split('x'))
    skjermbilde_gruppe, skjermbilde_MODUS = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[oppløsning_VERDI]
    fastvare_VERDI = speile_rot / 'vendor/pi4-firmware.tar.gz'
    예상결과 = fastvare_VERDI.with_name(fastvare_VERDI.name + '.sha256')
    lisens = speile_rot / 'vendor/LICENCE.broadcom'
    if not fastvare_VERDI.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi 부팅 펌웨어 gruppe_VERDI 필요: ' + str(fastvare_VERDI))
    if 해시계산(fastvare_VERDI) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 gruppe_VERDI SHA256 불일치')
    if not lisens.is_file():
        raise SystemExit('부팅 펌웨어 라이선스 Fil 없음: ' + str(lisens))
    distribusjon_bane = speile_rot / 'dist'
    distribusjon_bane.mkdir(exist_ok=True)
    재연결꾸러미 = BIND_deltaker()
    total_kapasitet, Kjør_2 = 128 * 1024 * 1024, 2048
    섹터개수 = total_kapasitet // 512 - Kjør_2
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(speile_rot / 'build')) as 작업경로:
        fase_VERDI = Path(작업경로)
        부팅경로 = fase_VERDI / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        filliste = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(fastvare_VERDI)) as Arkiv:
            for Navn in filliste:
                medlem = Arkiv.getmember('./' + Navn)
                if not medlem.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + Navn)
                with Arkiv.extractfile(medlem) as 원본주소, (부팅경로 / Navn).open('wb') as mål_VERDI_plassere:
                    shutil.copyfileobj(원본주소, mål_VERDI_plassere)
        shutil.copyfile(str(speile_rot / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        Innstillinger = (speile_rot / '부팅/config.txt').read_text()
        Innstillinger = Innstillinger.replace('hdmi_group=2', 'hdmi_group=' + str(skjermbilde_gruppe)).replace('hdmi_mode=4', 'hdmi_mode=' + str(skjermbilde_MODUS))
        Innstillinger = Innstillinger.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(높이))
        (부팅경로 / 'config.txt').write_text(Innstillinger)
        shutil.copyfile(str(lisens), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(speile_rot / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for Navn in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(speile_rot.parents[1] / Navn), str(부팅경로 / Navn))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, Navn in ((speile_rot/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (speile_rot/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (speile_rot/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (speile_rot/'vendor/LICENSE.genet','LICENSE.genet'),
                             (speile_rot/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (speile_rot/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (speile_rot/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (speile_rot/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/Navn))
        for Navn in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(speile_rot / 'vendor' / Navn), str(부팅경로 / Navn))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 Verktøy/Utfør_kommando.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 Verktøy/Utfør_kommando.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/Viktig_fil_eb81d7d9.md.\n')
        partisjon_Fil = fase_VERDI / 'boot.fat'
        with partisjon_Fil.open('wb') as Fil_oppføring: Fil_oppføring.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(Kjør_2), '-n', 'JKJAVA', str(partisjon_Fil)])
        subprocess.check_call(['mcopy', '-i', str(partisjon_Fil), '-s'] + [str(data_plassere) for data_plassere in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 bygg_System 결과와 같은지 확인한다.
        추출자료 = fase_VERDI / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(partisjon_Fil), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(speile_rot / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 kjerne_VERDI SHA256 불일치')
        BILDE = fase_VERDI / 'jkoros-native-rpi4.img'
        MBR = bytearray(512)
        MBR[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', Kjør_2, 섹터개수)
        MBR[510:512] = b'\x55\xaa'
        with BILDE.open('wb') as KR_data:
            KR_data.truncate(total_kapasitet); KR_data.write(MBR); KR_data.seek(Kjør_2 * 512)
            with partisjon_Fil.open('rb') as 원본주소: shutil.copyfileobj(원본주소, KR_data)
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
                    'java_gui_example': '/example/java/Vinduseksempel.java; run: java Vinduseksempel',
                    'framebuffer_resolution': [너비, 높이], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': fastvare_VERDI.name, 'source_sha256': 해시계산(fastvare_VERDI),
                    'image_sha256': 해시계산(BILDE), 'boot_files': {}}
        for data_plassere in sorted(부팅경로.rglob('*')):
            if data_plassere.is_file(): bunt_manifest['boot_files'][str(data_plassere.relative_to(부팅경로))] = 해시계산(data_plassere)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux bygg_BILDE/bruker 디스크는 건드리지 않는다.
        os.replace(str(BILDE), str(distribusjon_bane / BILDE.name))
        Arkiv_grunnlag = fase_VERDI / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(Arkiv_grunnlag), 'zip', str(부팅경로))
        os.replace(str(Arkiv_grunnlag) + '.zip', str(distribusjon_bane / 'jkoros-native-rpi4-boot.zip'))
        (distribusjon_bane / 'manifest.json').write_text(json.dumps(bunt_manifest, indent=2) + '\n')
    print('generere:', distribusjon_bane / 'jkoros-native-rpi4.img')
    print('faktisk_data Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    Kjør_2()
