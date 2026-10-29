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
from ejecutarComando import raízProyecto
from DistribuciónCOSL import EmpaquetarEjecutables


def calcularResumenHash(ruta):
    valor = hashlib.sha256()
    with ruta.open('rb') as entradaElementoArchivo:
        for bloqueDatos in iter(lambda: entradaElementoArchivo.read(1024 * 1024), b''): valor.update(bloqueDatos)
    return valor.hexdigest()


def ponerEnMarcha():
    Analizador = argparse.ArgumentParser(description=__doc__)
    Analizador.add_argument('--resolution', choices=('640x480', '1280x720', '1920x1080'), default='640x480', help='SD Arranque HDMI/프레임버퍼 tamaño')
    valorResolución = Analizador.parse_args().resolution
    valorAnchura, valorAltura = map(int, valorResolución.split('x'))
    grupoPantalla, modoPantalla = {'640x480': (2, 4), '1280x720': (1, 4), '1920x1080': (1, 16)}[valorResolución]
    valorProgramaFijo = raízProyecto / 'vendor/pi4-firmware.tar.gz'
    esperado = valorProgramaFijo.with_name(valorProgramaFijo.name + '.sha256')
    licencia = raízProyecto / 'vendor/LICENCE.broadcom'
    if not valorProgramaFijo.is_file() or not esperado.is_file():
        raise SystemExit('공식 Pi Arranque 펌웨어 valorGrupo valorNecesario: ' + str(valorProgramaFijo))
    if calcularResumenHash(valorProgramaFijo) != esperado.read_text().split()[0]:
        raise SystemExit('펌웨어 valorGrupo SHA256 불일치')
    if not licencia.is_file():
        raise SystemExit('Arranque 펌웨어 라이선스 Archivo métodoAusente: ' + str(licencia))
    rutaDistribución = raízProyecto / 'dist'
    rutaDistribución.mkdir(exist_ok=True)
    paqueteReenlazar = EmpaquetarEjecutables()
    capacidadTotal, ponerEnMarcha = 128 * 1024 * 1024, 2048
    númeroElementosSector = capacidadTotal // 512 - ponerEnMarcha
    with tempfile.TemporaryDirectory(prefix='image-', dir=str(raízProyecto / 'build')) as rutaTrabajoEnCurso:
        valorEtapa = Path(rutaTrabajoEnCurso)
        rutaArranque = valorEtapa / 'boot'
        (rutaArranque / 'overlays').mkdir(parents=True)
        listaArchivo = ['start4.elf', 'fixup4.dat', 'bcm2711-rpi-4-b.dtb', 'overlays/disable-bt.dtbo']
        with tarfile.open(str(valorProgramaFijo)) as archivoComprimido:
            for nombre in listaArchivo:
                miembro = archivoComprimido.getmember('./' + nombre)
                if not miembro.isfile(): raise SystemExit('펌웨어에 일반 파일이 아님: ' + nombre)
                with archivoComprimido.extractfile(miembro) as direcciónOriginal, (rutaArranque / nombre).open('wb') as posiciónValorDestino:
                    shutil.copyfileobj(direcciónOriginal, posiciónValorDestino)
        shutil.copyfile(str(raízProyecto / 'build/kernel8.img'), str(rutaArranque / 'kernel8.img'))
        ajustes = (raízProyecto / 'Arranque/config.txt').read_text()
        ajustes = ajustes.replace('hdmi_group=2', 'hdmi_group=' + str(grupoPantalla)).replace('hdmi_mode=4', 'hdmi_mode=' + str(modoPantalla))
        ajustes = ajustes.replace('framebuffer_width=640', 'framebuffer_width=' + str(valorAnchura)).replace('framebuffer_height=480', 'framebuffer_height=' + str(valorAltura))
        (rutaArranque / 'config.txt').write_text(ajustes)
        shutil.copyfile(str(licencia), str(rutaArranque / 'LICENCE.broadcom'))
        shutil.copyfile(str(raízProyecto / 'vendor/LICENSE.micropython'), str(rutaArranque / 'LICENSE.micropython'))
        for nombre in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            shutil.copyfile(str(raízProyecto.parents[1] / nombre), str(rutaArranque / nombre))
        shutil.copyfile(str(paqueteReenlazar), str(rutaArranque / paqueteReenlazar.name))
        for datosOriginal, nombre in ((raízProyecto/'vendor/lwip/COPYING','LICENSE.lwip'),
                             (raízProyecto/'vendor/libassh/COPYING','LICENSE.libassh'),
                             (raízProyecto/'vendor/bearssl/LICENSE.txt','LICENSE.bearssl'),
                             (raízProyecto/'vendor/LICENSE.genet','LICENSE.genet'),
                             (raízProyecto/'vendor/tinycc/COPYING','LICENSE.tinycc'),
                             (raízProyecto/'vendor/uzlib/uzlib.h','LICENSE.uzlib'),
                             (raízProyecto/'vendor/LICENSE.libgcc-runtime','LICENSE.libgcc-runtime'),
                             (raízProyecto/'vendor/LICENSE.gcc-gpl3','LICENSE.gcc-gpl3')):
            shutil.copyfile(str(datosOriginal), str(rutaArranque/nombre))
        for nombre in ('LICENSE.fonts-noto-cjk', 'LICENSE.fonts-dejavu-core', 'terminal-font.json'):
            shutil.copyfile(str(raízProyecto / 'vendor' / nombre), str(rutaArranque / nombre))
        (rutaArranque / 'README.txt').write_text('JKOROS own Java AOT kernel for Raspberry Pi 4.\n'
            'COSL commercial terms apply to author-owned code; third-party terms take precedence.\n'
            'LGPL libassh/TinyCC sources and relink material: jkoros-native-relink.tar.gz (included).\n'
            'This product includes software developed by Bill Paul.\n'
            'Guest subset javac/JVM/JAR, jaot static-subset native compiler, TinyCC, MicroPython, ELF64/C++.\n'
            'Guest lwIP TCP/UDP/ARP, Pi4 GENET + DHCP (physical hardware untested), QEMU UART1 SLIP. No Wi-Fi.\n'
            'Native SSH :22 and VNC :5900 auto-start. Separate device passwords: build/remote/access.json on build PC.\n'
            'QEMU: python3 Herramientas/ejecutarComando.py --remote --network-host 0.0.0.0; intérpreteComandosAsegurar :2222, VNC :5903.\n'
            'SSH shares the kernel console. VNC pixels are not encrypted. No RDP/SFTP/SSH forwarding.\n'
            'ELF names need no suffix; run --linux FILE opts into limited static ARM64 Linux syscall ABI.\n'
            'No Linux kernel/full OpenJDK/CPython/full Swing. UART 115200 8N1. Commands: help, vi FILE, terminal, gui.\n'
            'QEMU GUI + network: python3 Herramientas/ejecutarComando.py --desktop --network --resolution 1920x1080; Remmina VNC 127.0.0.1:5902.\n'
            'Guest ftpd start: localhost FTP 2121. Korean examples: example java | example c | example python.\n'
            'All 13 examples are ready at boot in /example/java, /example/c and /example/python (64 RAM files).\n'
            'Remmina Hangul: F9 / Shift+Space / Hangul key toggles EN/KO two-set input. Guest help ko.\n'
            'RAM files are volatile. See platforms/rpi4-native/Guía.md.\n')
        archivoPartición = valorEtapa / 'boot.fat'
        with archivoPartición.open('wb') as entradaElementoArchivo: entradaElementoArchivo.truncate(númeroElementosSector * 512)
        subprocess.check_call(['mkfs.vfat', '-F', '32', '-h', str(ponerEnMarcha), '-n', 'JKJAVA', str(archivoPartición)])
        subprocess.check_call(['mcopy', '-i', str(archivoPartición), '-s'] + [str(posiciónDatos) for posiciónDatos in sorted(rutaArranque.iterdir())] + ['::/'])
        # 이미지에서 꺼낸 커널이 construirSistema 결과와 igual 확인한다.
        extraído = valorEtapa / 'checked-kernel.img'
        subprocess.check_call(['mcopy', '-i', str(archivoPartición), '::/kernel8.img', str(extraído)])
        if calcularResumenHash(extraído) != calcularResumenHash(raízProyecto / 'build/kernel8.img'):
            raise SystemExit('FAT 이미지에서 읽은 valorNúcleo SHA256 불일치')
        imagen = valorEtapa / 'jkoros-native-rpi4.img'
        RegistroEntradaArranqueMaestro = bytearray(512)
        RegistroEntradaArranqueMaestro[446:462] = struct.pack('<B3sB3sII', 0x80, b'\xfe\xff\xff', 0x0c, b'\xfe\xff\xff', ponerEnMarcha, númeroElementosSector)
        RegistroEntradaArranqueMaestro[510:512] = b'\x55\xaa'
        with imagen.open('wb') as datosResultado:
            datosResultado.truncate(capacidadTotal); datosResultado.write(RegistroEntradaArranqueMaestro); datosResultado.seek(ponerEnMarcha * 512)
            with archivoPartición.open('rb') as direcciónOriginal: shutil.copyfileobj(direcciónOriginal, datosResultado)
        manifiestoPaquete = {'target': 'Pi4 own Java kernel, protected user execution', 'linux': False,
                    'license': 'COSL with third-party/LGPL carve-outs',
                    'relink_archive': paqueteReenlazar.name, 'relink_sha256': calcularResumenHash(paqueteReenlazar),
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
                    'java_gui_example': '/example/java/EjemploVentana.java; run: java EjemploVentana',
                    'framebuffer_resolution': [valorAnchura, valorAltura], 'framebuffer_format': 'RGB32',
                    'vi': 'EL0 vi command subset', 'cooperative_user_sessions': 4, 'full_swing': False,
                    'shell': 'directories, scripts, variables, sequential 16 KiB pipes, redirects',
                    'qemu_input': 'host VNC-to-UART bridge', 'native_usb_input': False,
                    'qemu_desktop_and_network': True, 'korean_examples': ['java', 'c', 'python'],
                    'example_count': 13, 'example_sources': 'jkoros/example',
                    'examples_ready_at_boot': True, 'ram_file_slots': 64,
                    'vnc_hangul_input': 'two-set, F9 / Shift+Space / Hangul key, EN/KO title indicator',
                    'physical_board_tested': False, 'data_persistence': False,
                    'source_archive': valorProgramaFijo.name, 'source_sha256': calcularResumenHash(valorProgramaFijo),
                    'image_sha256': calcularResumenHash(imagen), 'boot_files': {}}
        for posiciónDatos in sorted(rutaArranque.rglob('*')):
            if posiciónDatos.is_file(): manifiestoPaquete['boot_files'][str(posiciónDatos.relative_to(rutaArranque))] = calcularResumenHash(posiciónDatos)
        # 네이티브 산출물 이름으로만 교체: 기존 Linux construirImagen/Usuario 디스크는 건드리지 않는다.
        os.replace(str(imagen), str(rutaDistribución / imagen.name))
        baseArchivoComprimido = valorEtapa / 'jkoros-native-rpi4-boot'
        shutil.make_archive(str(baseArchivoComprimido), 'zip', str(rutaArranque))
        os.replace(str(baseArchivoComprimido) + '.zip', str(rutaDistribución / 'jkoros-native-rpi4-boot.zip'))
        (rutaDistribución / 'manifest.json').write_text(json.dumps(manifiestoPaquete, indent=2) + '\n')
    print('generar:', rutaDistribución / 'jkoros-native-rpi4.img')
    print('datosEfectivo Pi4 펌웨어 부팅은 아직 미검증. QEMU는 kernel8.img를 직접 적재합니다.')


if __name__ == '__main__':
    ponerEnMarcha()
