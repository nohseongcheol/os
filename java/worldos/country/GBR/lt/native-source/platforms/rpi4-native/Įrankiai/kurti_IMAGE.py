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
from Vykdyti_komanda import Project_šaknis
from COSL배포 import BIND_dalyvis


def 해시계산(KELIAS):
    VALUE = hashlib.sha256()
    with KELIAS.open('rb') as Failas_įrašas:
        for duomenų_blokas in iter(lambda: Failas_įrašas.read(1024 * 1024), b''): VALUE.update(duomenų_blokas)
    return VALUE.hexdigest()


def Paleisti():
    analizatorius_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatorius_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD 부팅 HDMI/프레임버퍼 Dydis')
    skiriamoji_geba_VALUE = analizatorius_48ee4b1b.parse_args().resolution
    너비, 높이 = map(int, skiriamoji_geba_VALUE.split('x'))
    화면무리, 화면방식 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[skiriamoji_geba_VALUE]
    programinė_aparatinė_įranga_VALUE = Project_šaknis / 'vendor/pi4-firmware.tar.gz'
    예상결과 = programinė_aparatinė_įranga_VALUE.with_name(programinė_aparatinė_įranga_VALUE.name + '.sha256')
    licencija = Project_šaknis / 'vendor/LICENCE.broadcom'
    if not programinė_aparatinė_įranga_VALUE.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi 부팅 펌웨어 Grupė_VALUE 필요: ' + str(programinė_aparatinė_įranga_VALUE))
    if 해시계산(programinė_aparatinė_įranga_VALUE) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 Grupė_VALUE SHA256 불일치')
    if not licencija.is_file():
        raise SystemExit('부팅 펌웨어 라이선스 Failas 없음: ' + str(licencija))
    paskirstymas_kelias = Project_šaknis / 'dist'
    paskirstymas_kelias.mkdir(exist_ok=True)
    재연결꾸러미 = BIND_dalyvis()
    bendras_pajėgumas, Paleisti = 128 * 1024 * 1024, 2048
    섹터개수 = bendras_pajėgumas // 512 - Paleisti
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(Project_šaknis / 'build')) as 작업경로:
        etapas_VALUE = Path(작업경로)
        부팅경로 = etapas_VALUE / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        Failas_Sąrašas = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(programinė_aparatinė_įranga_VALUE)) as Archyvas:
            for Pavadinimas_2 in Failas_Sąrašas:
                narys = Archyvas.getmember('./' + Pavadinimas_2)
                if not narys.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + Pavadinimas_2)
                with Archyvas.extractfile(narys) as 원본주소, (부팅경로 / Pavadinimas_2).open('wb') as vieta_VALUE_padėtis:
                    shutil.copyfileobj(원본주소, vieta_VALUE_padėtis)
        shutil.copyfile(str(Project_šaknis / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        Nustatymai = (Project_šaknis / '부팅/config.txt').read_text()
        Nustatymai = Nustatymai.replace('hdmi_group=2', 'hdmi_group=' + str(화면무리)).replace('hdmi_mode=4', 'hdmi_mode=' + str(화면방식))
        Nustatymai = Nustatymai.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(높이))
        (부팅경로 / 'config.txt').write_text(Nustatymai)
        shutil.copyfile(str(licencija), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(Project_šaknis / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for Pavadinimas_2 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(Project_šaknis.parents[1] / Pavadinimas_2), str(부팅경로 / Pavadinimas_2))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, Pavadinimas_2 in ((Project_šaknis/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (Project_šaknis/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (Project_šaknis/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (Project_šaknis/'vendor/LICENSE.genet','LICENSE.genet'),
                             (Project_šaknis/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (Project_šaknis/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (Project_šaknis/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (Project_šaknis/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/Pavadinimas_2))
        for Pavadinimas_2 in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(Project_šaknis / 'vendor' / Pavadinimas_2), str(부팅경로 / Pavadinimas_2))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 Įrankiai/Vykdyti_komanda.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 Įrankiai/Vykdyti_komanda.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/안내.md.\n')
        skaidinys_Failas = etapas_VALUE / 'boot.fat'
        with skaidinys_Failas.open('wb') as Failas_įrašas: Failas_įrašas.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(Paleisti), '-n', 'JKJAVA', str(skaidinys_Failas)])
        subprocess.check_call(['mcopy', '-i', str(skaidinys_Failas), '-s'] + [str(duomenys_padėtis) for duomenys_padėtis in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 kompiliuoti_sistema 결과와 같은지 확인한다.
        추출자료 = etapas_VALUE / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(skaidinys_Failas), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(Project_šaknis / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 branduolys_VALUE SHA256 불일치')
        IMAGE = etapas_VALUE / 'jkoros-native-rpi4.img'
        MBR = bytearray(512)
        MBR[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', Paleisti, 섹터개수)
        MBR[510:512] = b'\x55\xaa'
        with IMAGE.open('wb') as KR_duomenys:
            KR_duomenys.truncate(bendras_pajėgumas); KR_duomenys.write(MBR); KR_duomenys.seek(Paleisti * 512)
            with skaidinys_Failas.open('rb') as 원본주소: shutil.copyfileobj(원본주소, KR_duomenys)
        꾸러미명세 = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
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
                    'java_gui_example': '/example/java/LangoPavyzdys.java; run: java LangoPavyzdys',
                    'framebuffer_resolution': [너비, 높이], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': programinė_aparatinė_įranga_VALUE.name, 'source_sha256': 해시계산(programinė_aparatinė_įranga_VALUE),
                    'image_sha256': 해시계산(IMAGE), 'boot_files': {}}
        for duomenys_padėtis in sorted(부팅경로.rglob('*')):
            if duomenys_padėtis.is_file(): 꾸러미명세['boot_files'][str(duomenys_padėtis.relative_to(부팅경로))] = 해시계산(duomenys_padėtis)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux kompiliuoti_IMAGE/naudotojas 디스크는 건드리지 않는다.
        os.replace(str(IMAGE), str(paskirstymas_kelias / IMAGE.name))
        Archyvas_BASE = etapas_VALUE / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(Archyvas_BASE), 'zip', str(부팅경로))
        os.replace(str(Archyvas_BASE) + '.zip', str(paskirstymas_kelias / 'jkoros-native-rpi4-boot.zip'))
        (paskirstymas_kelias / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('generuoti:', paskirstymas_kelias / 'jkoros-native-rpi4.img')
    print('faktinis_duomenys Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    Paleisti()
