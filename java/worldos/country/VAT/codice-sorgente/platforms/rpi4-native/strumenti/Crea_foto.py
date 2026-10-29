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
from Esegui_comando import azione_radice
from COSL배포 import BIND_endpoint


def calcolare_hash(percorso):
    VALORE = hashlib.sha256()
    with percorso.open('rb') as File_voce:
        for blocco_di_dati in iter(lambda: File_voce.read(1024 * 1024), b''): VALORE.update(blocco_di_dati)
    return VALORE.hexdigest()


def avvia():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD avvio_macchina HDMI/프레임버퍼 Dimensione')
    risoluzione_VALORE = parser_48ee4b1b.parse_args().resolution
    너비, altezza_VALORE = map(int, risoluzione_VALORE.split('x'))
    schermata_gruppo, schermata_MODA = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[risoluzione_VALORE]
    firmware_VALORE = azione_radice / 'vendor/pi4-firmware.tar.gz'
    예상결과 = firmware_VALORE.with_name(firmware_VALORE.name + '.sha256')
    licenza = azione_radice / 'vendor/LICENCE.broadcom'
    if not firmware_VALORE.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi avvio_macchina 펌웨어 gruppo_VALORE 필요: ' + str(firmware_VALORE))
    if calcolare_hash(firmware_VALORE) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 gruppo_VALORE SHA256 불일치')
    if not licenza.is_file():
        raise SystemExit('avvio_macchina 펌웨어 라이선스 file 없음: ' + str(licenza))
    distribuzione_percorso = azione_radice / 'dist'
    distribuzione_percorso.mkdir(exist_ok=True)
    재연결꾸러미 = BIND_endpoint()
    totale_capacità, avvia = 128 * 1024 * 1024, 2048
    settore_CONTA_NUMERI = totale_capacità // 512 - avvia
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(azione_radice / 'build')) as 작업경로:
        area_VALORE_29ee1bb7 = Path(작업경로)
        부팅경로 = area_VALORE_29ee1bb7 / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        elenco_file = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(firmware_VALORE)) as Archivio:
            for Nome in elenco_file:
                membro = Archivio.getmember('./' + Nome)
                if not membro.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + Nome)
                with Archivio.extractfile(membro) as 원본주소, (부팅경로 / Nome).open('wb') as meta_VALORE_funzione:
                    shutil.copyfileobj(원본주소, meta_VALORE_funzione)
        shutil.copyfile(str(azione_radice / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        Impostazioni = (azione_radice / 'avvio_macchina/config.txt').read_text()
        Impostazioni = Impostazioni.replace('hdmi_group=2', 'hdmi_group=' + str(schermata_gruppo)).replace('hdmi_mode=4', 'hdmi_mode=' + str(schermata_MODA))
        Impostazioni = Impostazioni.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(altezza_VALORE))
        (부팅경로 / 'config.txt').write_text(Impostazioni)
        shutil.copyfile(str(licenza), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(azione_radice / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for Nome in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(azione_radice.parents[1] / Nome), str(부팅경로 / Nome))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, Nome in ((azione_radice/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (azione_radice/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (azione_radice/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (azione_radice/'vendor/LICENSE.genet','LICENSE.genet'),
                             (azione_radice/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (azione_radice/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (azione_radice/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (azione_radice/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/Nome))
        for Nome in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(azione_radice / 'vendor' / Nome), str(부팅경로 / Nome))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 strumenti/Esegui_comando.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 strumenti/Esegui_comando.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/README_eb81d7d9.md.\n')
        partizione_File = area_VALORE_29ee1bb7 / 'boot.fat'
        with partizione_File.open('wb') as File_voce: File_voce.truncate(settore_CONTA_NUMERI * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(avvia), '-n', 'JKJAVA', str(partizione_File)])
        subprocess.check_call(['mcopy', '-i', str(partizione_File), '-s'] + [str(dati_funzione) for dati_funzione in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 costruire 결과와 같은지 확인한다.
        추출자료 = area_VALORE_29ee1bb7 / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(partizione_File), '::/kernel8.img', str(추출자료)])
        if calcolare_hash(추출자료) != calcolare_hash(azione_radice / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 kernel_VALORE SHA256 불일치')
        foto = area_VALORE_29ee1bb7 / 'jkoros-native-rpi4.img'
        record_principale_di_avvio = bytearray(512)
        record_principale_di_avvio[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', avvia, settore_CONTA_NUMERI)
        record_principale_di_avvio[510:512] = b'\x55\xaa'
        with foto.open('wb') as KR_dati:
            KR_dati.truncate(totale_capacità); KR_dati.write(record_principale_di_avvio); KR_dati.seek(avvia * 512)
            with partizione_File.open('rb') as 원본주소: shutil.copyfileobj(원본주소, KR_dati)
        aggregare_manifesto = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
                    'license': 'COSL with third-party/LGPL carve-outs',
                    'relink_archive': 재연결꾸러미.name, 'relink_sha256': calcolare_hash(재연결꾸러미),
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
                    'java_gui_example': '/example/java/EsempioFinestra.java; run: java EsempioFinestra',
                    'framebuffer_resolution': [너비, altezza_VALORE], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': firmware_VALORE.name, 'source_sha256': calcolare_hash(firmware_VALORE),
                    'image_sha256': calcolare_hash(foto), 'boot_files': {}}
        for dati_funzione in sorted(부팅경로.rglob('*')):
            if dati_funzione.is_file(): aggregare_manifesto['boot_files'][str(dati_funzione.relative_to(부팅경로))] = calcolare_hash(dati_funzione)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux BLD_foto/spazio_utente 디스크는 건드리지 않는다.
        os.replace(str(foto), str(distribuzione_percorso / foto.name))
        Archivio_BASE = area_VALORE_29ee1bb7 / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(Archivio_BASE), 'zip', str(부팅경로))
        os.replace(str(Archivio_BASE) + '.zip', str(distribuzione_percorso / 'jkoros-native-rpi4-boot.zip'))
        (distribuzione_percorso / 'manifest.json').write_text(json.dumps(aggregare_manifesto, indent=2) + '\n')
    print('generare:', distribuzione_percorso / 'jkoros-native-rpi4.img')
    print('effettivo_dati Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    avvia()
