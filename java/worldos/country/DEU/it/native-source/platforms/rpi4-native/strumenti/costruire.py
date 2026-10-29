#!/usr/bin/env python3
"""host javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from BLD_USER_Space import Crea_USER_Space
from BLD_rete import Crea_rete
from 예제빌드 import 예제만들기
from BLD_remoto import Crea_remoto

azione_radice = Path(__file__).resolve().parents[1]
radice_del_repository = azione_radice.parents[1]
BLD_percorso = azione_radice / 'build'


def Esegui_comando(argomento_array):
    subprocess.check_call([str(첫째값) for 첫째값 in argomento_array], cwd=str(azione_radice))


def avvia():
    BLD_percorso.mkdir(exist_ok=True)
    C_compilatore = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    linker_strumento = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    file_oggetto_convertitore = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Archivio_strumento = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for strumenti in ('javac', C_compilatore, 시플플번역기, linker_strumento, file_oggetto_convertitore, Archivio_strumento):
        if not shutil.which(strumenti):
            raise SystemExit('필요한 costruire strumenti 없음: ' + strumenti)
    tipo_di_carattere_info = json.loads((azione_radice / 'vendor/terminal-font.json').read_text())
    tipo_di_carattere_dati = (azione_radice / 'vendor/terminal-font.bin').read_bytes()
    if len(tipo_di_carattere_dati) != 65616 * 32 or hashlib.sha256(tipo_di_carattere_dati).hexdigest() != tipo_di_carattere_info['sha256']:
        raise SystemExit('terminale tipo_di_carattere_VALORE Dimensione/SHA256 불일치')
    esportare_tabella = {'jshell_interactive': '셸입출력.reparto_IT_interattivo', 'jshell_output': '셸입출력.uscitaTesto', 'jshell_input': '셸입출력.input_VALORE', 'java_task': 'Nucleo.작업', 'jfs_path_start': 'FileMemoria.percorso_START',
               'jfs_path_byte': 'FileMemoria.percorso_byte', 'jfs_open': 'FileMemoria.Apri',
               'jfs_read': 'FileMemoria.Lettura', 'jfs_write': 'FileMemoria.Scrittura',
               'jfs_seek': 'FileMemoria.cercare_funzione', 'jfs_close': 'FileMemoria.Chiudi',
               'jfs_size': 'FileMemoria.Dimensione', 'jfs_unlink': 'FileMemoria.cancellare_voce',
               'jfs_truncate': 'FileMemoria.set_durata'}
    esportare_tabella.update({'jfs_entry_count': 'FileMemoria.파일한도', 'jfs_entry_length': 'FileMemoria.공개이름길이', 'jfs_entry_byte': 'FileMemoria.공개이름바이트', 'jfs_entry_size': 'FileMemoria.공개파일크기'})
    esportare_tabella.update({'jdraw_prepare': '화면합성.Prepara', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.get_altezza', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.ritagliare',
        'jdraw_clip_value': '화면합성.ritagliare_VALORE', 'jdraw_begin': '화면합성.avvia',
        'jdraw_end': '화면합성.Fine', 'jdraw_pixel': '화면합성.pixel',
        'jdraw_rectangle': '화면합성.rettangolo_Riempi', 'jdraw_pointer': '화면합성.puntatore'})
    esportare_tabella.update({'jfs_mkdir': 'FileMemoria.Crea_elenco', 'jfs_rmdir': 'FileMemoria.rimuovere_elenco', 'jfs_kind': 'FileMemoria.voce_Kind'})
    esportare_tabella.update({'jnet_socket': 'loopback_rete.Crea_voce', 'jnet_bind': 'loopback_rete.BIND_endpoint',
        'jnet_put': 'loopback_rete.자료넣기', 'jnet_get': 'loopback_rete.자료읽기', 'jnet_send': 'loopback_rete.inviare',
        'jnet_recv': 'loopback_rete.ricevere', 'jnet_port': 'loopback_rete.창구읽기', 'jnet_address': 'loopback_rete.주소읽기',
        'jnet_peer': 'loopback_rete.sender_endpoint', 'jnet_close': 'loopback_rete.Chiudi'})
    esportare_tabella.update({'jstream_create': 'Stream_rete.Crea_voce', 'jstream_bind': 'Stream_rete.BIND_endpoint', 'jstream_listen': 'Stream_rete.essere_in_ascolto_endpoint', 'jstream_connect': 'Stream_rete.Connetti', 'jstream_accept': 'Stream_rete.accettare_connessione', 'jstream_read': 'Stream_rete.Lettura', 'jstream_write': 'Stream_rete.Scrittura', 'jstream_port': 'Stream_rete.창구읽기', 'jstream_peer': 'Stream_rete.상대창구읽기', 'jstream_close': 'Stream_rete.Chiudi'})
    for simbolo_VALORE in list(esportare_tabella):
        if simbolo_VALORE.startswith('jstream_') or simbolo_VALORE.startswith('jnet_') and simbolo_VALORE not in ('jnet_put', 'jnet_get'):
            esportare_tabella[simbolo_VALORE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = esportare_tabella.pop(simbolo_VALORE)
    예제들 = ['public final class aggregare { public static void Prepara() {']
    for percorso in sorted((azione_radice / '예제').iterdir()):
        if percorso.is_file():
            예제들.append('InterpreteComandi.statico_File(%s, %s);' %
                (json.dumps(percorso.name), json.dumps(percorso.read_text(encoding='utf-8'), ensure_ascii=True)))
    (BLD_percorso / 'aggregare.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(azione_radice, radice_del_repository, Esegui_comando)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(BLD_percorso)) as 작업경로:
        Corso_percorso = Path(작업경로)
        Esegui_comando(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Corso_percorso, '-sourcepath', Corso_percorso, '-d', Corso_percorso] + sorted((azione_radice / 'codiceSorgente').glob('*.java')) + [BLD_percorso / 'aggregare.java', BLD_percorso / '예제꾸러미.java'])
        # file·Shell·Finestra 세션·통신과 Java schermata 합성 배열을 모두 수용한다.
        argomento_array = ['sh', radice_del_repository / 'compiler/미리번역.sh', '--entry', 'Nucleo.avvia', '--heap-words', '1048576', '-o', BLD_percorso / 'kernel-java.c']
        for simbolo_VALORE, metodo_voce in sorted(esportare_tabella.items()):
            argomento_array += ['--export', simbolo_VALORE + '=' + metodo_voce]
        Esegui_comando(argomento_array + sorted(Corso_percorso.glob('*.class')))
    (BLD_percorso / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    configurazione_BITS = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = radice_del_repository / 'posix-kor/arm64-native'
    Crea_USER_Space(azione_radice, radice_del_repository, C_compilatore, 시플플번역기, linker_strumento, Archivio_strumento, configurazione_BITS, Esegui_comando)
    rete = Crea_rete(azione_radice, C_compilatore, Archivio_strumento, configurazione_BITS, Esegui_comando)
    remoto_usare = Crea_remoto(azione_radice, C_compilatore, Archivio_strumento, configurazione_BITS, Esegui_comando)
    포함인수 = ['-I', 포직스경로 / 'dichiarazioni', '-I', BLD_percorso]
    빌드작업 = [(C_compilatore, [], BLD_percorso / 'terminal-font.S', 'font.o'),
            (C_compilatore, ['-std=c11', '-Wall', '-Wextra', '-Werror'], azione_radice / 'computer/terminale.c', 'terminal.o'),
            (C_compilatore, ['-std=c11', '-Wall', '-Wextra', '-Werror'], azione_radice / 'computer/elemento_grafico.c', 'widgets.o'),
            (C_compilatore, ['-std=c11'], BLD_percorso / 'kernel-java.c', 'java.o'),
            (C_compilatore, ['-std=c11', '-Wall', '-Wextra', '-Werror'], azione_radice / 'computer/scheda.c', 'board.o'),
            (C_compilatore, ['-std=c11', '-Wall', '-Wextra', '-Werror'], azione_radice / 'computer/schermata_disegno.c', 'drawing.o'),
            (C_compilatore, ['-std=c11', '-Wall', '-Wextra', '-Werror'], azione_radice / 'computer/spazio_utente.c', 'user.o'),
            (C_compilatore, [], azione_radice / 'avvio_macchina/punto_di_ingresso_VALORE.S', 'entry.o'),
            (C_compilatore, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Connetti.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], azione_radice / 'prove/File_Chiamate.cpp', 'cpp.o')]
    for compilatore_strumento, 추가영역, 원본자료, output in 빌드작업:
        원본설정 = [File_voce for File_voce in configurazione_BITS if File_voce != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else configurazione_BITS
        Esegui_comando([compilatore_strumento] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', BLD_percorso / output])
    Esegui_comando([Archivio_strumento, 'rcs', BLD_percorso / 'libposix-kor-arm64.a', BLD_percorso / 'posix.o'])
    Esegui_comando([linker_strumento, '--gc-sections', '-T', azione_radice / 'avvio_macchina/disposizione_di_collegamento.ld', '-Map', BLD_percorso / 'kernel.map', '-o', BLD_percorso / 'kernel.elf'] +
        [BLD_percorso / Nome for Nome in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', BLD_percorso / 'libposix-kor-arm64.a', rete, remoto_usare, BLD_percorso / 'remote/libassh.a', BLD_percorso / 'remote/libbearssl.a', '--end-group'])
    Esegui_comando([file_oggetto_convertitore, '-O', 'binary', BLD_percorso / 'kernel.elf', BLD_percorso / 'kernel8.img'])
    aggregare_manifesto = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Italiano.nativo', 'korean_exceptions': 20,
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
        aggregare_manifesto['sha256'][Nome] = hashlib.sha256((BLD_percorso / Nome).read_bytes()).hexdigest()
    (BLD_percorso / 'build.json').write_text(json.dumps(aggregare_manifesto, indent=2) + '\n')
    print('완료:', BLD_percorso / 'kernel8.img')


if __name__ == '__main__':
    avvia()
