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
from végrehajt_parancs import teendő_gyök
from COSL배포 import BIND_végpont


def 해시계산(ÚTVONAL):
    ÉRTÉK = hashlib.sha256()
    with ÚTVONAL.open('rb') as Fájl_bejegyzés:
        for adatblokk in iter(lambda: Fájl_bejegyzés.read(1024 * 1024), b''): ÉRTÉK.update(adatblokk)
    return ÉRTÉK.hexdigest()


def Futtatás():
    elemző_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    elemző_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD 부팅 HDMI/프레임버퍼 Méret')
    felbontás_ÉRTÉK = elemző_48ee4b1b.parse_args().resolution
    너비, 높이 = map(int, felbontás_ÉRTÉK.split('x'))
    화면무리, 화면방식 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[felbontás_ÉRTÉK]
    기초제어프로그램 = teendő_gyök / 'vendor/pi4-firmware.tar.gz'
    예상결과 = 기초제어프로그램.with_name(기초제어프로그램.name + '.sha256')
    licenc = teendő_gyök / 'vendor/LICENCE.broadcom'
    if not 기초제어프로그램.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi 부팅 펌웨어 Csoport_ÉRTÉK 필요: ' + str(기초제어프로그램))
    if 해시계산(기초제어프로그램) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 Csoport_ÉRTÉK SHA256 불일치')
    if not licenc.is_file():
        raise SystemExit('부팅 펌웨어 라이선스 Fájl 없음: ' + str(licenc))
    elosztás_útvonal = teendő_gyök / 'dist'
    elosztás_útvonal.mkdir(exist_ok=True)
    재연결꾸러미 = BIND_végpont()
    összesen_kapacitás, Futtatás = 128 * 1024 * 1024, 2048
    섹터개수 = összesen_kapacitás // 512 - Futtatás
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(teendő_gyök / 'build')) as 작업경로:
        fázis_ÉRTÉK = Path(작업경로)
        부팅경로 = fázis_ÉRTÉK / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        fájllista = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(기초제어프로그램)) as archív:
            for Név in fájllista:
                tag = archív.getmember('./' + Név)
                if not tag.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + Név)
                with archív.extractfile(tag) as 원본주소, (부팅경로 / Név).open('wb') as cél_ÉRTÉK_pozíció:
                    shutil.copyfileobj(원본주소, cél_ÉRTÉK_pozíció)
        shutil.copyfile(str(teendő_gyök / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        Beállítások = (teendő_gyök / '부팅/config.txt').read_text()
        Beállítások = Beállítások.replace('hdmi_group=2', 'hdmi_group=' + str(화면무리)).replace('hdmi_mode=4', 'hdmi_mode=' + str(화면방식))
        Beállítások = Beállítások.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(높이))
        (부팅경로 / 'config.txt').write_text(Beállítások)
        shutil.copyfile(str(licenc), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(teendő_gyök / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for Név in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(teendő_gyök.parents[1] / Név), str(부팅경로 / Név))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, Név in ((teendő_gyök/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (teendő_gyök/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (teendő_gyök/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (teendő_gyök/'vendor/LICENSE.genet','LICENSE.genet'),
                             (teendő_gyök/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (teendő_gyök/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (teendő_gyök/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (teendő_gyök/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/Név))
        for Név in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(teendő_gyök / 'vendor' / Név), str(부팅경로 / Név))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 Eszközök/végrehajt_parancs.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 Eszközök/végrehajt_parancs.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/fontos_fájl_eb81d7d9.md.\n')
        partíció_Fájl = fázis_ÉRTÉK / 'boot.fat'
        with partíció_Fájl.open('wb') as Fájl_bejegyzés: Fájl_bejegyzés.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(Futtatás), '-n', 'JKJAVA', str(partíció_Fájl)])
        subprocess.check_call(['mcopy', '-i', str(partíció_Fájl), '-s'] + [str(adat_pozíció) for adat_pozíció in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 épít_Rendszer 결과와 같은지 확인한다.
        추출자료 = fázis_ÉRTÉK / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(partíció_Fájl), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(teendő_gyök / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 kernel_ÉRTÉK SHA256 불일치')
        KÉP = fázis_ÉRTÉK / 'jkoros-native-rpi4.img'
        MBR = bytearray(512)
        MBR[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', Futtatás, 섹터개수)
        MBR[510:512] = b'\x55\xaa'
        with KÉP.open('wb') as KR_adat:
            KR_adat.truncate(összesen_kapacitás); KR_adat.write(MBR); KR_adat.seek(Futtatás * 512)
            with partíció_Fájl.open('rb') as 원본주소: shutil.copyfileobj(원본주소, KR_adat)
        köteg_jegyzékfájl = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
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
                    'java_gui_example': '/example/java/AblakPélda.java; run: java AblakPélda',
                    'framebuffer_resolution': [너비, 높이], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': 기초제어프로그램.name, 'source_sha256': 해시계산(기초제어프로그램),
                    'image_sha256': 해시계산(KÉP), 'boot_files': {}}
        for adat_pozíció in sorted(부팅경로.rglob('*')):
            if adat_pozíció.is_file(): köteg_jegyzékfájl['boot_files'][str(adat_pozíció.relative_to(부팅경로))] = 해시계산(adat_pozíció)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux épít_KÉP/felhasználó 디스크는 건드리지 않는다.
        os.replace(str(KÉP), str(elosztás_útvonal / KÉP.name))
        archív_ALAP = fázis_ÉRTÉK / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(archív_ALAP), 'zip', str(부팅경로))
        os.replace(str(archív_ALAP) + '.zip', str(elosztás_útvonal / 'jkoros-native-rpi4-boot.zip'))
        (elosztás_útvonal / 'manifest.json').write_text(json.dumps(köteg_jegyzékfájl, indent=2) + '\n')
    print('generálás:', elosztás_útvonal / 'jkoros-native-rpi4.img')
    print('tényleges_adat Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    Futtatás()
