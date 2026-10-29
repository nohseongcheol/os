#!/usr/bin/env python3
"""hospedar javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from compilar_usuario_espazo import crear_usuario_espazo
from compilar_Rede import crear_Rede
from 예제빌드 import 예제만들기
from compilar_remoto import crear_remoto

Project_raíz = Path(__file__).resolve().parents[1]
repositorio_raíz = Project_raíz.parents[1]
compilar_camiño = Project_raíz / 'build'


def executar_comando(argumento_MATRIZ):
    subprocess.check_call([str(첫째값) for 첫째값 in argumento_MATRIZ], cwd=str(Project_raíz))


def Executar_2():
    compilar_camiño.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    obxecto_Ficheiro_convertedor = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arquivo_ferramenta = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Ferramentas in ('javac', 시언어번역기, 시플플번역기, 연결편집기, obxecto_Ficheiro_convertedor, Arquivo_ferramenta):
        if not shutil.which(Ferramentas):
            raise SystemExit('필요한 compilar_sistema Ferramentas 없음: ' + Ferramentas)
    tipo_de_letra_información = json.loads((Project_raíz / 'vendor/terminal-font.json').read_text())
    tipo_de_letra_datos = (Project_raíz / 'vendor/terminal-font.bin').read_bytes()
    if len(tipo_de_letra_datos) != 65616 * 32 or hashlib.sha256(tipo_de_letra_datos).hexdigest() != tipo_de_letra_información['sha256']:
        raise SystemExit('Terminal tipo_de_letra_VALOR Tamaño/SHA256 불일치')
    exportar_táboa = {'jshell_interactive': '셸입출력.Tecnoloxía_da_información_TI_interactivo', 'jshell_output': '셸입출력.Saída', 'jshell_input': '셸입출력.입력', 'java_task': 'kernel.작업', 'jfs_path_start': 'Memoria_Ficheiros.camiño_START',
               'jfs_path_byte': 'Memoria_Ficheiros.camiño_byte', 'jfs_open': 'Memoria_Ficheiros.Abrir',
               'jfs_read': 'Memoria_Ficheiros.Lectura', 'jfs_write': 'Memoria_Ficheiros.Escritura',
               'jfs_seek': 'Memoria_Ficheiros.buscar_cargo', 'jfs_close': 'Memoria_Ficheiros.Pechar',
               'jfs_size': 'Memoria_Ficheiros.Tamaño', 'jfs_unlink': 'Memoria_Ficheiros.borrar_introdución',
               'jfs_truncate': 'Memoria_Ficheiros.conxunto_duración'}
    exportar_táboa.update({'jfs_entry_count': 'Memoria_Ficheiros.파일한도', 'jfs_entry_length': 'Memoria_Ficheiros.공개이름길이', 'jfs_entry_byte': 'Memoria_Ficheiros.공개이름바이트', 'jfs_entry_size': 'Memoria_Ficheiros.공개파일크기'})
    exportar_táboa.update({'jdraw_prepare': '화면합성.준비', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.clip',
        'jdraw_clip_value': '화면합성.clip_VALOR', 'jdraw_begin': '화면합성.Executar_2',
        'jdraw_end': '화면합성.fin', 'jdraw_pixel': '화면합성.píxel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.punteiro'})
    exportar_táboa.update({'jfs_mkdir': 'Memoria_Ficheiros.crear_directorio', 'jfs_rmdir': 'Memoria_Ficheiros.eliminar_directorio', 'jfs_kind': 'Memoria_Ficheiros.항목종류'})
    exportar_táboa.update({'jnet_socket': '되돌림망.crear_introdución', 'jnet_bind': '되돌림망.ligar_extremo',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.enviar',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.remitente_extremo', 'jnet_close': '되돌림망.Pechar'})
    exportar_táboa.update({'jstream_create': 'fluxo_Rede.crear_introdución', 'jstream_bind': 'fluxo_Rede.ligar_extremo', 'jstream_listen': 'fluxo_Rede.agardar_extremo', 'jstream_connect': 'fluxo_Rede.Conectar', 'jstream_accept': 'fluxo_Rede.aceptar_conexión', 'jstream_read': 'fluxo_Rede.Lectura', 'jstream_write': 'fluxo_Rede.Escritura', 'jstream_port': 'fluxo_Rede.창구읽기', 'jstream_peer': 'fluxo_Rede.상대창구읽기', 'jstream_close': 'fluxo_Rede.Pechar'})
    for símbolo_VALOR in list(exportar_táboa):
        if símbolo_VALOR.startswith('jstream_') or símbolo_VALOR.startswith('jnet_') and símbolo_VALOR not in ('jnet_put', 'jnet_get'):
            exportar_táboa[símbolo_VALOR.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = exportar_táboa.pop(símbolo_VALOR)
    예제들 = ['public final class paquete { public static void 준비() {']
    for CAMIÑO in sorted((Project_raíz / '예제').iterdir()):
        if CAMIÑO.is_file():
            예제들.append('명령해석기.estático_Ficheiro(%s, %s);' %
                (json.dumps(CAMIÑO.name), json.dumps(CAMIÑO.read_text(encoding='utf-8'), ensure_ascii=True)))
    (compilar_camiño / 'paquete.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Project_raíz, repositorio_raíz, executar_comando)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(compilar_camiño)) as 작업경로:
        Clase_camiño = Path(작업경로)
        executar_comando(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Clase_camiño, '-sourcepath', Clase_camiño, '-d', Clase_camiño] + sorted((Project_raíz / 'FONTE').glob('*.java')) + [compilar_camiño / 'paquete.java', compilar_camiño / '예제꾸러미.java'])
        # Ficheiro·shell·Xanela 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argumento_MATRIZ = ['sh', repositorio_raíz / 'compiler/미리번역.sh', '--entry', 'kernel.Executar_2', '--heap-words', '1048576', '-o', compilar_camiño / 'kernel-java.c']
        for símbolo_VALOR, 메소드 in sorted(exportar_táboa.items()):
            argumento_MATRIZ += ['--export', símbolo_VALOR + '=' + 메소드]
        executar_comando(argumento_MATRIZ + sorted(Clase_camiño.glob('*.class')))
    (compilar_camiño / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    configuración_Servizo_de_transferencia_intelixente_en_segundo_plano = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = repositorio_raíz / 'posix-kor/arm64-native'
    crear_usuario_espazo(Project_raíz, repositorio_raíz, 시언어번역기, 시플플번역기, 연결편집기, Arquivo_ferramenta, configuración_Servizo_de_transferencia_intelixente_en_segundo_plano, executar_comando)
    Rede = crear_Rede(Project_raíz, 시언어번역기, Arquivo_ferramenta, configuración_Servizo_de_transferencia_intelixente_en_segundo_plano, executar_comando)
    원격사용 = crear_remoto(Project_raíz, 시언어번역기, Arquivo_ferramenta, configuración_Servizo_de_transferencia_intelixente_en_segundo_plano, executar_comando)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', compilar_camiño]
    빌드작업 = [(시언어번역기, [], compilar_camiño / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_raíz / 'máquina/Terminal.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_raíz / 'máquina/widget.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], compilar_camiño / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_raíz / 'máquina/Panel.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_raíz / 'máquina/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_raíz / 'máquina/usuario.c', 'user.o'),
            (시언어번역기, [], Project_raíz / '부팅/introdución_p_VALOR.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Conectar.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Project_raíz / '시험/Ficheiro_Chamadas.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [Ficheiro_introdución for Ficheiro_introdución in configuración_Servizo_de_transferencia_intelixente_en_segundo_plano if Ficheiro_introdución != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else configuración_Servizo_de_transferencia_intelixente_en_segundo_plano
        executar_comando([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', compilar_camiño / 출력결과])
    executar_comando([Arquivo_ferramenta, 'rcs', compilar_camiño / 'libposix-kor-arm64.a', compilar_camiño / 'posix.o'])
    executar_comando([연결편집기, '--gc-sections', '-T', Project_raíz / '부팅/Ligar_deseño.ld', '-Map', compilar_camiño / 'kernel.map', '-o', compilar_camiño / 'kernel.elf'] +
        [compilar_camiño / Nome for Nome in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', compilar_camiño / 'libposix-kor-arm64.a', Rede, 원격사용, compilar_camiño / 'remote/libassh.a', compilar_camiño / 'remote/libbearssl.a', '--end-group'])
    executar_comando([obxecto_Ficheiro_convertedor, '-O', 'binary', compilar_camiño / 'kernel.elf', compilar_camiño / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Galego.자체', 'korean_exceptions': 20,
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
    for Nome in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Nome] = hashlib.sha256((compilar_camiño / Nome).read_bytes()).hexdigest()
    (compilar_camiño / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', compilar_camiño / 'kernel8.img')


if __name__ == '__main__':
    Executar_2()
