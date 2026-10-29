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
from Executar_comando import ação_raiz
from COSL배포 import BIND_empresa


def calcular_hash(caminho):
    VALOR = hashlib.sha256()
    with caminho.open('rb') as Arquivo_entrada:
        for bloco_de_dados in iter(lambda: Arquivo_entrada.read(1024 * 1024), b''): VALOR.update(bloco_de_dados)
    return VALOR.hexdigest()


def iniciar():
    analisador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analisador_48ee4b1b.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD arranque_da_máquina HDMI/프레임버퍼 Tamanho')
    resolução_VALOR = analisador_48ee4b1b.parse_args().resolution
    너비, altura_VALOR = map(int, resolução_VALOR.split('x'))
    tela_Grupo, tela_MODO = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[resolução_VALOR]
    firmware_VALOR = ação_raiz / 'vendor/pi4-firmware.tar.gz'
    예상결과 = firmware_VALOR.with_name(firmware_VALOR.name + '.sha256')
    licença = ação_raiz / 'vendor/LICENCE.broadcom'
    if not firmware_VALOR.is_file() or not 예상결과.is_file():
        raise SystemExit('공식 Pi arranque_da_máquina 펌웨어 Grupo_VALOR 필요: ' + str(firmware_VALOR))
    if calcular_hash(firmware_VALOR) != 예상결과.read_text().split()[0]:
        raise SystemExit('펌웨어 Grupo_VALOR SHA256 불일치')
    if not licença.is_file():
        raise SystemExit('arranque_da_máquina 펌웨어 라이선스 ficheiro 없음: ' + str(licença))
    distribuição_caminho = ação_raiz / 'dist'
    distribuição_caminho.mkdir(exist_ok=True)
    재연결꾸러미 = BIND_empresa()
    total_capacidade, iniciar = 128 * 1024 * 1024, 2048
    섹터개수 = total_capacidade // 512 - iniciar
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(ação_raiz / 'build')) as 작업경로:
        fase_VALOR = Path(작업경로)
        부팅경로 = fase_VALOR / 'boot'
        (부팅경로 / 'overlays').mkdir(parents=True)
        lista_de_arquivos = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(firmware_VALOR)) as arquivo:
            for Nome in lista_de_arquivos:
                membro = arquivo.getmember('./' + Nome)
                if not membro.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + Nome)
                with arquivo.extractfile(membro) as 원본주소, (부팅경로 / Nome).open('wb') as destino_VALOR_cargo:
                    shutil.copyfileobj(원본주소, destino_VALOR_cargo)
        shutil.copyfile(str(ação_raiz / 'build/kernel8.img'), str(부팅경로 / 'kernel8.img'))
        Definições = (ação_raiz / 'arranque_da_máquina/config.txt').read_text()
        Definições = Definições.replace('hdmi_group=2', 'hdmi_group=' + str(tela_Grupo)).replace('hdmi_mode=4', 'hdmi_mode=' + str(tela_MODO))
        Definições = Definições.replace('framebuffer_width=640', 'framebuffer_width=' + str(너비)).replace('framebuffer_height=480', 'framebuffer_height=' + str(altura_VALOR))
        (부팅경로 / 'config.txt').write_text(Definições)
        shutil.copyfile(str(licença), str(부팅경로 / 'LICENCE.broadcom'))
        shutil.copyfile(str(ação_raiz / 'vendor/LICENSE.micropython'), str(부팅경로 / 'LICENSE.micropython'))
        for Nome in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(ação_raiz.parents[1] / Nome), str(부팅경로 / Nome))
        shutil.copyfile(str(재연결꾸러미), str(부팅경로 / 재연결꾸러미.name))
        for 원본자료, Nome in ((ação_raiz/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (ação_raiz/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (ação_raiz/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (ação_raiz/'vendor/LICENSE.genet','LICENSE.genet'),
                             (ação_raiz/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (ação_raiz/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (ação_raiz/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (ação_raiz/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(원본자료), str(부팅경로/Nome))
        for Nome in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(ação_raiz / 'vendor' / Nome), str(부팅경로 / Nome))
        (부팅경로 / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 ferramentas/Executar_comando.py --remote --network-host 0.0.0.0; SSH :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 ferramentas/Executar_comando.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/LEIAME_eb81d7d9.md.\n')
        partição_Arquivo = fase_VALOR / 'boot.fat'
        with partição_Arquivo.open('wb') as Arquivo_entrada: Arquivo_entrada.truncate(섹터개수 * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(iniciar), '-n', 'JKJAVA', str(partição_Arquivo)])
        subprocess.check_call(['mcopy', '-i', str(partição_Arquivo), '-s'] + [str(dados_cargo) for dados_cargo in sorted(부팅경로.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 construir 결과와 같은지 확인한다.
        추출자료 = fase_VALOR / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(partição_Arquivo), '::/kernel8.img', str(추출자료)])
        if calcular_hash(추출자료) != calcular_hash(ação_raiz / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 kernel_VALOR SHA256 불일치')
        foto = fase_VALOR / 'jkoros-native-rpi4.img'
        registo_principal_de_arranque = bytearray(512)
        registo_principal_de_arranque[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', iniciar, 섹터개수)
        registo_principal_de_arranque[510:512] = b'\x55\xaa'
        with foto.open('wb') as RC_dados:
            RC_dados.truncate(total_capacidade); RC_dados.write(registo_principal_de_arranque); RC_dados.seek(iniciar * 512)
            with partição_Arquivo.open('rb') as 원본주소: shutil.copyfileobj(원본주소, RC_dados)
        grupo_manifesto = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
                    'license': 'COSL with third-party/LGPL carve-outs',
                    'relink_archive': 재연결꾸러미.name, 'relink_sha256': calcular_hash(재연결꾸러미),
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
                    'java_gui_example': '/example/java/ExemploJanela.java; run: java ExemploJanela',
                    'framebuffer_resolution': [너비, altura_VALOR], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': firmware_VALOR.name, 'source_sha256': calcular_hash(firmware_VALOR),
                    'image_sha256': calcular_hash(foto), 'boot_files': {}}
        for dados_cargo in sorted(부팅경로.rglob('*')):
            if dados_cargo.is_file(): grupo_manifesto['boot_files'][str(dados_cargo.relative_to(부팅경로))] = calcular_hash(dados_cargo)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux BLD_foto/espaço_do_utilizador 디스크는 건드리지 않는다.
        os.replace(str(foto), str(distribuição_caminho / foto.name))
        arquivo_BASE = fase_VALOR / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(arquivo_BASE), 'zip', str(부팅경로))
        os.replace(str(arquivo_BASE) + '.zip', str(distribuição_caminho / 'jkoros-native-rpi4-boot.zip'))
        (distribuição_caminho / 'manifest.json').write_text(json.dumps(grupo_manifesto, indent=2) + '\n')
    print('gerar:', distribuição_caminho / 'jkoros-native-rpi4.img')
    print('real_dados Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    iniciar()
