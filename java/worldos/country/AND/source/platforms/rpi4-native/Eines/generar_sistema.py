#!/usr/bin/env python3
"""allotjar javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from generar_usuari_espai import Crear_usuari_espai
from generar_xarxa import Crear_xarxa
from 예제빌드 import 예제만들기
from generar_remot import Crear_remot

Project_rel = Path(__file__).resolve().parents[1]
dipòsit_rel = Project_rel.parents[1]
generar_camí = Project_rel / 'build'


def Executa_ordre(arg_MATRIU):
    subprocess.check_call([str(첫째값) for 첫째값 in arg_MATRIU], cwd=str(Project_rel))


def Executa_2():
    generar_camí.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    목적파일변환기 = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arxiu_eina = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Eines in ('javac', 시언어번역기, 시플플번역기, 연결편집기, 목적파일변환기, Arxiu_eina):
        if not shutil.which(Eines):
            raise SystemExit('필요한 generar_sistema Eines 없음: ' + Eines)
    tipus_de_lletra_informació = json.loads((Project_rel / 'vendor/terminal-font.json').read_text())
    tipus_de_lletra_dades = (Project_rel / 'vendor/terminal-font.bin').read_bytes()
    if len(tipus_de_lletra_dades) != 65616 * 32 or hashlib.sha256(tipus_de_lletra_dades).hexdigest() != tipus_de_lletra_informació['sha256']:
        raise SystemExit('Terminal tipus_de_lletra_VALOR Mida/SHA256 불일치')
    exportar_taula = {'jshell_interactive': '셸입출력.tecnologies_de_la_informació_interactiu', 'jshell_output': '셸입출력.Sortida', 'jshell_input': '셸입출력.입력', 'java_task': 'nucli.작업', 'jfs_path_start': 'Memòria_Fitxers.camí_Inici',
               'jfs_path_byte': 'Memòria_Fitxers.camí_byte', 'jfs_open': 'Memòria_Fitxers.Obre',
               'jfs_read': 'Memòria_Fitxers.Lectura', 'jfs_write': 'Memòria_Fitxers.Escriptura',
               'jfs_seek': 'Memòria_Fitxers.cercar_càrrec', 'jfs_close': 'Memòria_Fitxers.Tanca',
               'jfs_size': 'Memòria_Fitxers.Mida', 'jfs_unlink': 'Memòria_Fitxers.esborrar_introducció',
               'jfs_truncate': 'Memòria_Fitxers.conjunt_durada'}
    exportar_taula.update({'jfs_entry_count': 'Memòria_Fitxers.파일한도', 'jfs_entry_length': 'Memòria_Fitxers.공개이름길이', 'jfs_entry_byte': 'Memòria_Fitxers.공개이름바이트', 'jfs_entry_size': 'Memòria_Fitxers.공개파일크기'})
    exportar_taula.update({'jdraw_prepare': '화면합성.Prepara', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.clip',
        'jdraw_clip_value': '화면합성.clip_VALOR', 'jdraw_begin': '화면합성.Executa_2',
        'jdraw_end': '화면합성.fi', 'jdraw_pixel': '화면합성.píxel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.punter'})
    exportar_taula.update({'jfs_mkdir': 'Memòria_Fitxers.Crear_directori', 'jfs_rmdir': 'Memòria_Fitxers.suprimir_directori', 'jfs_kind': 'Memòria_Fitxers.항목종류'})
    exportar_taula.update({'jnet_socket': '되돌림망.Crear_introducció', 'jnet_bind': '되돌림망.enllaçar_extrem',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.tancar_dades', 'jnet_send': '되돌림망.enviar',
        'jnet_recv': '되돌림망.rebre', 'jnet_port': '되돌림망.tancar_extrem_port', 'jnet_address': '되돌림망.tancar_ADREÇA',
        'jnet_peer': '되돌림망.emissor_extrem', 'jnet_close': '되돌림망.Tanca'})
    exportar_taula.update({'jstream_create': 'flux_xarxa.Crear_introducció', 'jstream_bind': 'flux_xarxa.enllaçar_extrem', 'jstream_listen': 'flux_xarxa.escoltar_extrem', 'jstream_connect': 'flux_xarxa.Connecta', 'jstream_accept': 'flux_xarxa.acceptar_connexió', 'jstream_read': 'flux_xarxa.Lectura', 'jstream_write': 'flux_xarxa.Escriptura', 'jstream_port': 'flux_xarxa.tancar_extrem_port', 'jstream_peer': 'flux_xarxa.tancar_homòleg_port', 'jstream_close': 'flux_xarxa.Tanca'})
    for símbol_VALOR in list(exportar_taula):
        if símbol_VALOR.startswith('jstream_') or símbol_VALOR.startswith('jnet_') and símbol_VALOR not in ('jnet_put', 'jnet_get'):
            exportar_taula[símbol_VALOR.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = exportar_taula.pop(símbol_VALOR)
    예제들 = ['public final class paquet { public static void Prepara() {']
    for Camí in sorted((Project_rel / '예제').iterdir()):
        if Camí.is_file():
            예제들.append('명령해석기.estàtic_arxiu(%s, %s);' %
                (json.dumps(Camí.name), json.dumps(Camí.read_text(encoding='utf-8'), ensure_ascii=True)))
    (generar_camí / 'paquet.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Project_rel, dipòsit_rel, Executa_ordre)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(generar_camí)) as 작업경로:
        Classe_camí = Path(작업경로)
        Executa_ordre(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Classe_camí, '-sourcepath', Classe_camí, '-d', Classe_camí] + sorted((Project_rel / 'FONT').glob('*.java')) + [generar_camí / 'paquet.java', generar_camí / '예제꾸러미.java'])
        # Fitxer·shell·Finestra 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        arg_MATRIU = ['sh', dipòsit_rel / 'compiler/미리번역.sh', '--entry', 'nucli.Executa_2', '--heap-words', '1048576', '-o', generar_camí / 'kernel-java.c']
        for símbol_VALOR, 메소드 in sorted(exportar_taula.items()):
            arg_MATRIU += ['--export', símbol_VALOR + '=' + 메소드]
        Executa_ordre(arg_MATRIU + sorted(Classe_camí.glob('*.class')))
    (generar_camí / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    configuració_Servei_de_transferència_intel_ligent_en_segon_terme = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = dipòsit_rel / 'posix-kor/arm64-native'
    Crear_usuari_espai(Project_rel, dipòsit_rel, 시언어번역기, 시플플번역기, 연결편집기, Arxiu_eina, configuració_Servei_de_transferència_intel_ligent_en_segon_terme, Executa_ordre)
    xarxa = Crear_xarxa(Project_rel, 시언어번역기, Arxiu_eina, configuració_Servei_de_transferència_intel_ligent_en_segon_terme, Executa_ordre)
    remot_ús = Crear_remot(Project_rel, 시언어번역기, Arxiu_eina, configuració_Servei_de_transferència_intel_ligent_en_segon_terme, Executa_ordre)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', generar_camí]
    빌드작업 = [(시언어번역기, [], generar_camí / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_rel / 'màquina/Terminal.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_rel / 'màquina/giny.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], generar_camí / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_rel / 'màquina/Tauler.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_rel / 'màquina/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_rel / 'màquina/usuari.c', 'user.o'),
            (시언어번역기, [], Project_rel / '부팅/introducció_p_VALOR.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Connecta.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Project_rel / '시험/arxiu_Trucades.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [arxiu_introducció for arxiu_introducció in configuració_Servei_de_transferència_intel_ligent_en_segon_terme if arxiu_introducció != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else configuració_Servei_de_transferència_intel_ligent_en_segon_terme
        Executa_ordre([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', generar_camí / 출력결과])
    Executa_ordre([Arxiu_eina, 'rcs', generar_camí / 'libposix-kor-arm64.a', generar_camí / 'posix.o'])
    Executa_ordre([연결편집기, '--gc-sections', '-T', Project_rel / '부팅/enllaç_disseny.ld', '-Map', generar_camí / 'kernel.map', '-o', generar_camí / 'kernel.elf'] +
        [generar_camí / Nom for Nom in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', generar_camí / 'libposix-kor-arm64.a', xarxa, remot_ús, generar_camí / 'remote/libassh.a', generar_camí / 'remote/libbearssl.a', '--end-group'])
    Executa_ordre([목적파일변환기, '-O', 'binary', generar_camí / 'kernel.elf', generar_camí / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Català.propi', 'korean_exceptions': 20,
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
    for Nom in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Nom] = hashlib.sha256((generar_camí / Nom).read_bytes()).hexdigest()
    (generar_camí / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', generar_camí / 'kernel8.img')


if __name__ == '__main__':
    Executa_2()
