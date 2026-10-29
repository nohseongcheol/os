#!/usr/bin/env python3
"""Anfitrión javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from construirEspacioUsuario import crearEspacioUsuario
from construirRed import crearRed
from construirColecciónEjemplos import crearColecciónEjemplos
from construirRemoto import crearRemoto

raízProyecto = Path(__file__).resolve().parents[1]
raízRepositorio = raízProyecto.parents[1]
construirRuta = raízProyecto / 'build'


def ejecutarComando(arregloArgumento):
    subprocess.check_call([str(valorPrimero) for valorPrimero in arregloArgumento], cwd=str(raízProyecto))


def ponerEnMarcha():
    construirRuta.mkdir(exist_ok=True)
    CompiladorC = os.environ.get('ARM64_CC', 'clang')
    compiladorCpp = os.environ.get('ARM64_CXX', 'clang++')
    herramientaEnlazador = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    convertidorArchivoObjeto = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    herramientaArchivoComprimido = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Herramientas in ('javac', CompiladorC, compiladorCpp, herramientaEnlazador, convertidorArchivoObjeto, herramientaArchivoComprimido):
        if not shutil.which(Herramientas):
            raise SystemExit('필요한 construirSistema Herramientas métodoAusente: ' + Herramientas)
    informaciónFuenteTipográfica = json.loads((raízProyecto / 'vendor/terminal-font.json').read_text())
    datosFuenteTipográfica = (raízProyecto / 'vendor/terminal-font.bin').read_bytes()
    if len(datosFuenteTipográfica) != 65616 * 32 or hashlib.sha256(datosFuenteTipográfica).hexdigest() != informaciónFuenteTipográfica['sha256']:
        raise SystemExit('terminal valorFuenteTipográfica tamaño/SHA256 불일치')
    tablaExportar = {'jshell_interactive': 'EntradaSalidaIntérpreteComandos.esInteractivo', 'jshell_output': 'EntradaSalidaIntérpreteComandos.Salida', 'jshell_input': 'EntradaSalidaIntérpreteComandos.valorEntrada', 'java_task': 'Núcleo.Tarea', 'jfs_path_start': 'ArchivosMemoria.iniciarRuta',
               'jfs_path_byte': 'ArchivosMemoria.byteRuta', 'jfs_open': 'ArchivosMemoria.abrir',
               'jfs_read': 'ArchivosMemoria.leer', 'jfs_write': 'ArchivosMemoria.escribir',
               'jfs_seek': 'ArchivosMemoria.posicionarPosición', 'jfs_close': 'ArchivosMemoria.cerrar',
               'jfs_size': 'ArchivosMemoria.tamaño', 'jfs_unlink': 'ArchivosMemoria.borrarEntradaElemento',
               'jfs_truncate': 'ArchivosMemoria.establecerLongitud'}
    tablaExportar.update({'jfs_entry_count': 'ArchivosMemoria.límiteArchivo', 'jfs_entry_length': 'ArchivosMemoria.longitudNombreExportado', 'jfs_entry_byte': 'ArchivosMemoria.byteNombreExportado', 'jfs_entry_size': 'ArchivosMemoria.tamañoArchivoExportado'})
    tablaExportar.update({'jdraw_prepare': 'ComponedorBúferImagen.preparar', 'jdraw_width': 'ComponedorBúferImagen.obtenerAnchura',
        'jdraw_height': 'ComponedorBúferImagen.obtenerAltura', 'jdraw_count_low': 'ComponedorBúferImagen.obtenerBajoContador',
        'jdraw_count_high': 'ComponedorBúferImagen.obtenerAltoContador', 'jdraw_clip': 'ComponedorBúferImagen.recortar',
        'jdraw_clip_value': 'ComponedorBúferImagen.valorRecortar', 'jdraw_begin': 'ComponedorBúferImagen.ponerEnMarcha',
        'jdraw_end': 'ComponedorBúferImagen.terminar', 'jdraw_pixel': 'ComponedorBúferImagen.píxel',
        'jdraw_rectangle': 'ComponedorBúferImagen.rellenarRectángulo', 'jdraw_pointer': 'ComponedorBúferImagen.puntero'})
    tablaExportar.update({'jfs_mkdir': 'ArchivosMemoria.crearDirectorio', 'jfs_rmdir': 'ArchivosMemoria.eliminarDirectorio', 'jfs_kind': 'ArchivosMemoria.claseTipoEntradaElemento'})
    tablaExportar.update({'jnet_socket': 'RedBucleRetorno.crearEntradaElemento', 'jnet_bind': 'RedBucleRetorno.EmpaquetarEjecutables',
        'jnet_put': 'RedBucleRetorno.ponerDatos', 'jnet_get': 'RedBucleRetorno.leerDatos', 'jnet_send': 'RedBucleRetorno.enviar',
        'jnet_recv': 'RedBucleRetorno.recibir', 'jnet_port': 'RedBucleRetorno.leerPuertoExtremo', 'jnet_address': 'RedBucleRetorno.leerDirección',
        'jnet_peer': 'RedBucleRetorno.extremoEmisor', 'jnet_close': 'RedBucleRetorno.cerrar'})
    tablaExportar.update({'jstream_create': 'RedFlujo.crearEntradaElemento', 'jstream_bind': 'RedFlujo.EmpaquetarEjecutables', 'jstream_listen': 'RedFlujo.escucharExtremo', 'jstream_connect': 'RedFlujo.conectar', 'jstream_accept': 'RedFlujo.aceptarConexión', 'jstream_read': 'RedFlujo.leer', 'jstream_write': 'RedFlujo.escribir', 'jstream_port': 'RedFlujo.leerPuertoExtremo', 'jstream_peer': 'RedFlujo.leerPuertoParRed', 'jstream_close': 'RedFlujo.cerrar'})
    for valorSímbolo in list(tablaExportar):
        if valorSímbolo.startswith('jstream_') or valorSímbolo.startswith('jnet_') and valorSímbolo not in ('jnet_put', 'jnet_get'):
            tablaExportar[valorSímbolo.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = tablaExportar.pop(valorSímbolo)
    entradasEjemplo = ['public final class Paquete { public static void preparar() {']
    for ruta in sorted((raízProyecto / 'Ejemplos').iterdir()):
        if ruta.is_file():
            entradasEjemplo.append('IntérpreteComandos.archivoEstático(%s, %s);' %
                (json.dumps(ruta.name), json.dumps(ruta.read_text(encoding='utf-8'), ensure_ascii=True)))
    (construirRuta / 'Paquete.java').write_text('\n'.join(entradasEjemplo + ['}}']), encoding='utf-8')
    crearColecciónEjemplos(raízProyecto, raízRepositorio, ejecutarComando)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(construirRuta)) as rutaTrabajoEnCurso:
        rutaClase = Path(rutaTrabajoEnCurso)
        ejecutarComando(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', rutaClase, '-sourcepath', rutaClase, '-d', rutaClase] + sorted((raízProyecto / 'fuente').glob('*.java')) + [construirRuta / 'Paquete.java', construirRuta / 'PaqueteEjemplo.java'])
        # Archivo·intérpreteComandos·ventana 세션·통신과 Java Pantalla 합성 배열을 construirTodos 수용한다.
        arregloArgumento = ['sh', raízRepositorio / 'compiler/tiempoDeAnticipado.sh', '--entry', 'Núcleo.ponerEnMarcha', '--heap-words', '1048576', '-o', construirRuta / 'kernel-java.c']
        for valorSímbolo, entradaElementoMétodo in sorted(tablaExportar.items()):
            arregloArgumento += ['--export', valorSímbolo + '=' + entradaElementoMétodo]
        ejecutarComando(arregloArgumento + sorted(rutaClase.glob('*.class')))
    (construirRuta / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    bitsConfiguración = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    pOSIX = raízRepositorio / 'posix-kor/arm64-native'
    crearEspacioUsuario(raízProyecto, raízRepositorio, CompiladorC, compiladorCpp, herramientaEnlazador, herramientaArchivoComprimido, bitsConfiguración, ejecutarComando)
    red = crearRed(raízProyecto, CompiladorC, herramientaArchivoComprimido, bitsConfiguración, ejecutarComando)
    usarRemoto = crearRemoto(raízProyecto, CompiladorC, herramientaArchivoComprimido, bitsConfiguración, ejecutarComando)
    inclusiones = ['-I', pOSIX / 'Encabezados', '-I', construirRuta]
    construirTrabajos = [(CompiladorC, [], construirRuta / 'terminal-font.S', 'font.o'),
            (CompiladorC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], raízProyecto / 'máquina/terminal.c', 'terminal.o'),
            (CompiladorC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], raízProyecto / 'máquina/ComponenteVisual.c', 'widgets.o'),
            (CompiladorC, ['-std=c11'], construirRuta / 'kernel-java.c', 'java.o'),
            (CompiladorC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], raízProyecto / 'máquina/Placa.c', 'board.o'),
            (CompiladorC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], raízProyecto / 'máquina/dibujoPantalla.c', 'drawing.o'),
            (CompiladorC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], raízProyecto / 'máquina/Usuario.c', 'user.o'),
            (CompiladorC, [], raízProyecto / 'Arranque/valorPuntoEntradaElemento.S', 'entry.o'),
            (CompiladorC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], pOSIX / 'conectar.c', 'posix.o'),
            (compiladorCpp, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], raízProyecto / 'Pruebas/LlamadasArchivo.cpp', 'cpp.o')]
    for herramientaCompilador, regiónAdicional, datosOriginal, salida in construirTrabajos:
        configuraciónOriginal = [entradaElementoArchivo for entradaElementoArchivo in bitsConfiguración if entradaElementoArchivo != '-mgeneral-regs-only'] if datosOriginal.suffix == '.S' else bitsConfiguración
        ejecutarComando([herramientaCompilador] + configuraciónOriginal + regiónAdicional + inclusiones + ['-c', datosOriginal, '-o', construirRuta / salida])
    ejecutarComando([herramientaArchivoComprimido, 'rcs', construirRuta / 'libposix-kor-arm64.a', construirRuta / 'posix.o'])
    ejecutarComando([herramientaEnlazador, '--gc-sections', '-T', raízProyecto / 'Arranque/DisposiciónEnlace.ld', '-Map', construirRuta / 'kernel.map', '-o', construirRuta / 'kernel.elf'] +
        [construirRuta / nombre for nombre in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', construirRuta / 'libposix-kor-arm64.a', red, usarRemoto, construirRuta / 'remote/libassh.a', construirRuta / 'remote/libbearssl.a', '--end-group'])
    ejecutarComando([convertidorArchivoObjeto, '-O', 'binary', construirRuta / 'kernel.elf', construirRuta / 'kernel8.img'])
    manifiestoPaquete = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'español.propio', 'korean_exceptions': 20,
                                 'full_awt_swing': False, 'swing_subset': ['JFrame','JPanel','JLabel','JButton','JTextField','ActionListener','SwingUtilities.invokeLater'], 'java_se_certified': False},
                'python': 'MicroPython 1.24.1 integer build', 'cpython': False,
                'pip': {'kind': 'source installer with host PyPI HTTPS relay', 'commands': ['install','list','uninstall'], 'cpython_pip': False, 'dependencies': False, 'persistent': False},
                'korean_c_api': 'independent structs, enum constants and real function symbols',
                'framebuffer': {'format': 'RGB32', 'default': [640,480], 'maximum': [1920,1080], 'boot_configurable': True, 'size_syscall': 22},
                'shell': 'UTF-8 editor/history, directories, variables, scripts, sequential pipes, redirects, ELF execution',
                'system_commands': ['ipconfig','ip','ifconfig','ping','route','netstat','ss','ps','top','free','df','uptime','poweroff'],
                'system_status': 'real lwIP interface/endpoints, native task/session PIDs, AOT heap pools, RAM filesystem slots',
                'ip_configuration': 'GENET DHCP on real Pi4; static IPv4/netmask/gateway; volatile; close active sockets before address changes',
                'ping': 'real ICMPv4 echo, numeric addresses, count/timeout/RTT; no DNS resolver',
                'poweroff': 'BCM2835 PM firmware-halt watchdog; QEMU guest shutdown; physical Pi untested',
                'pipe_capacity_bytes': 16384, 'posix_shell_complete': False,
                'ram_files': {'count': 64, 'bytes_each': 16384, 'directories': 16, 'persistent': False},
                'user_abi': 1, 'user_elf64': True, 'elf_extension_required': False,
                'linux_static_elf_subset': True, 'full_linux_binary_compatibility': False,
                'mmu': True, 'user_timeout_seconds': 2, 'cooperative_user_sessions': 4,
                'interactive_wait_renews_deadline': True, 'vi': 'native EL0 UTF-8 vi subset',
                'network': 'lwIP 2.2.0 IPv4 TCP/UDP/ARP/ICMP; GENET v5 Ethernet or UART1 SLIP', 'external_network': True,
                'external_network_transport': 'Pi4 GENET (hardware untested); QEMU auxiliary UART SLIP bridge',
                'ftp': 'guest service, passive binary transfers, anonymous root RAM workspace',
                'genet_ethernet': True, 'genet_driver_status': 'implemented; MMIO/MDIO model tests only', 'physical_network_tested': False,
                'ssh': {'implementation': 'guest libassh 1.1 / LGPL-2.1-or-later', 'port': 22, 'password_auth': True, 'console': 'shared kernel shell', 'independent_sessions': False, 'sftp': False, 'port_forwarding': False},
                'vnc': {'implementation': 'guest RFB 3.8 / VNC authentication / raw incremental tiles', 'port': 5900, 'encrypted_pixels': False, 'clients': 1, 'korean_input': 'native two-set F9/Shift+Space'},
                'rdp': False,
                'gui': 'four native terminal windows and Swing subset peers; guest VNC server with native input; optional QEMU VNC bridge',
                'native_usb_input': False, 'full_swing': False, 'swing_subset': True, 'sha256': {}}
    for nombre in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        manifiestoPaquete['sha256'][nombre] = hashlib.sha256((construirRuta / nombre).read_bytes()).hexdigest()
    (construirRuta / 'build.json').write_text(json.dumps(manifiestoPaquete, indent=2) + '\n')
    print('esTerminado:', construirRuta / 'kernel8.img')


if __name__ == '__main__':
    ponerEnMarcha()
