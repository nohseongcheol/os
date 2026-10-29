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
from Jalankan_perintah import Tugas_akar
from COSL배포 import ikat_peserta


def 해시계산(jalur):
    VALUE = hashlib.sha256()
    with jalur.open('rb') as file_entri:
        for blok_data in iter(lambda: file_entri.read(1024 * 1024), b''): VALUE.update(blok_data)
    return VALUE.hexdigest()


def jalankan():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD awal_mesin HDMI/프레임버퍼 Ukuran')
    resolusi_VALUE = parser_48ee4b1b.parse_args().resolution
    너비, 높이 = map(int, resolusi_VALUE.split('x'))
    화면무리, 화면방식 = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[resolusi_VALUE]
    기초제어프로그램 = Tugas_akar / 'vendor/pi4-firmware.tar.gz'
    예상결과 = 기초제어프로그램.with_name(기초제어프로그램.name + '.sha256')
    lisensi = Tugas_akar / 'vendor/LICENCE.broadcom'
    if not 기초제어프로그램.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi awal_mesin 펌웨어 grup_VALUE 필요: ' + str(기초제어프로그램))
    if 해시계산(기초제어프로그램) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 grup_VALUE SHA256 불일치')
    if not lisensi.is_file():
        raise SystemExit('awal_mesin 펌웨어 라이선스 berkas 없음: ' + str(lisensi))
    배포경로 = Tugas_akar / 'dist'
    배포경로.mkdir(exist_ok=True)
    재연결꾸러미 = ikat_peserta()
    total_kapasitas, jalankan = 128 * 1024 * 1024, 2048
    섹터개수 = total_kapasitas // 512 - jalankan
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(Tugas_akar / 'build')) as 작업경로:
        tahap_VALUE = Path(작업경로)
        부팅경로 = tahap_VALUE / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        file_Daftar = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(기초제어프로그램)) as Arsip:
            for Nama_2 in file_Daftar:
                anggota = Arsip.getmember('./' + Nama_2)
                if not anggota.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + Nama_2)
                with Arsip.extractfile(anggota) as 원본주소, (부팅경로 / Nama_2).open('wb') as tujuan_VALUE_posisi:
                    shutil.copyfileobj(원본주소, tujuan_VALUE_posisi)
        shutil.copyfile(str(Tugas_akar / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        Konfigurasi = (Tugas_akar / 'awal_mesin/config.txt').read_text()
        Konfigurasi = Konfigurasi.replace('hdmi_group=2', 'hdmi_group=' + str(화면무리)).replace('hdmi_mode=4', 'hdmi_mode=' + str(화면방식))
        Konfigurasi = Konfigurasi.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(높이))
        (부팅경로 / 'config.txt').write_text(Konfigurasi)
        shutil.copyfile(str(lisensi), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(Tugas_akar / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for Nama_2 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(Tugas_akar.parents[1] / Nama_2), str(부팅경로 / Nama_2))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, Nama_2 in ((Tugas_akar/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (Tugas_akar/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (Tugas_akar/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (Tugas_akar/'vendor/LICENSE.genet','LICENSE.genet'),
                             (Tugas_akar/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (Tugas_akar/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (Tugas_akar/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (Tugas_akar/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/Nama_2))
        for Nama_2 in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(Tugas_akar / 'vendor' / Nama_2), str(부팅경로 / Nama_2))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 alat/Jalankan_perintah.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 alat/Jalankan_perintah.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/baca_saya_eb81d7d9.md.\n')
        partisi_file = tahap_VALUE / 'boot.fat'
        with partisi_file.open('wb') as file_entri: file_entri.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(jalankan), '-n', 'JKJAVA', str(partisi_file)])
        subprocess.check_call(['mcopy', '-i', str(partisi_file), '-s'] + [str(data_posisi) for data_posisi in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 bangun 결과와 같은지 확인한다.
        추출자료 = tahap_VALUE / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(partisi_file), '::/kernel8.img', str(추출자료)])
        if 해시계산(추출자료) != 해시계산(Tugas_akar / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 kernel_VALUE SHA256 불일치')
        foto = tahap_VALUE / 'jkoros-native-rpi4.img'
        rekaman_awal_utama = bytearray(512)
        rekaman_awal_utama[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', jalankan, 섹터개수)
        rekaman_awal_utama[510:512] = b'\x55\xaa'
        with foto.open('wb') as KR_data:
            KR_data.truncate(total_kapasitas); KR_data.write(rekaman_awal_utama); KR_data.seek(jalankan * 512)
            with partisi_file.open('rb') as 원본주소: shutil.copyfileobj(원본주소, KR_data)
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
                    'java_gui_example': '/example/java/ContohJendela.java; run: java ContohJendela',
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
                    'image_sha256': 해시계산(foto), 'boot_files': {}}
        for data_posisi in sorted(부팅경로.rglob('*')):
            if data_posisi.is_file(): 꾸러미명세['boot_files'][str(data_posisi.relative_to(부팅경로))] = 해시계산(data_posisi)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux build_foto/ruang_pengguna 디스크는 건드리지 않는다.
        os.replace(str(foto), str(배포경로 / foto.name))
        Arsip_BASE = tahap_VALUE / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(Arsip_BASE), 'zip', str(부팅경로))
        os.replace(str(Arsip_BASE) + '.zip', str(배포경로 / 'jkoros-native-rpi4-boot.zip'))
        (배포경로 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('buat:', 배포경로 / 'jkoros-native-rpi4.img')
    print('aktual_data Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    jalankan()
