#!/usr/bin/env python3
"""hostit javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from BLD_uživatel_Space import Create_uživatel_Space
from BLD_síť import Create_síť
from 예제빌드 import 예제만들기
from BLD_vzdálený import Create_vzdálený

akce_kořen = Path(__file__).resolve().parents[1]
úložiště_kořen = akce_kořen.parents[1]
BLD_cesta = akce_kořen / 'build'


def Provést_příkaz(argument_pole):
    subprocess.check_call([str(첫째값) for 첫째값 in argument_pole], cwd=str(akce_kořen))


def Spustit_2():
    BLD_cesta.mkdir(exist_ok=True)
    C_kompilátor = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    linker_nástroj = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objekt_Soubor_převaděč = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Archiv_nástroj = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for nástroje in ('javac', C_kompilátor, 시플플번역기, linker_nástroj, objekt_Soubor_převaděč, Archiv_nástroj):
        if not shutil.which(nástroje):
            raise SystemExit('필요한 BLD_Systém nástroje 없음: ' + nástroje)
    písmo_informace = json.loads((akce_kořen / 'vendor/terminal-font.json').read_text())
    písmo_data = (akce_kořen / 'vendor/terminal-font.bin').read_bytes()
    if len(písmo_data) != 65616 * 32 or hashlib.sha256(písmo_data).hexdigest() != písmo_informace['sha256']:
        raise SystemExit('interpret_příkazů písmo_HODNOTA Velikost/SHA256 불일치')
    exportovat_tabulka = {'jshell_interactive': '셸입출력.informační_systémy_interaktivní', 'jshell_output': '셸입출력.výstupní_pozice', 'jshell_input': '셸입출력.vstup_HODNOTA', 'java_task': 'jádro.작업', 'jfs_path_start': 'Paměť_Files.cesta_START',
               'jfs_path_byte': 'Paměť_Files.cesta_bajt', 'jfs_open': 'Paměť_Files.Otevřít',
               'jfs_read': 'Paměť_Files.Čtení', 'jfs_write': 'Paměť_Files.Zápis',
               'jfs_seek': 'Paměť_Files.hledat_pozice', 'jfs_close': 'Paměť_Files.Zavřené',
               'jfs_size': 'Paměť_Files.Velikost', 'jfs_unlink': 'Paměť_Files.vymazat_položka',
               'jfs_truncate': 'Paměť_Files.sada_délka'}
    exportovat_tabulka.update({'jfs_entry_count': 'Paměť_Files.파일한도', 'jfs_entry_length': 'Paměť_Files.공개이름길이', 'jfs_entry_byte': 'Paměť_Files.공개이름바이트', 'jfs_entry_size': 'Paměť_Files.공개파일크기'})
    exportovat_tabulka.update({'jdraw_prepare': '화면합성.Připravit', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.get_výška', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.oříznout',
        'jdraw_clip_value': '화면합성.oříznout_HODNOTA', 'jdraw_begin': '화면합성.Spustit_2',
        'jdraw_end': '화면합성.Dokončit', 'jdraw_pixel': '화면합성.pixel',
        'jdraw_rectangle': '화면합성.obdélník_výplň', 'jdraw_pointer': '화면합성.ukazatel'})
    exportovat_tabulka.update({'jfs_mkdir': 'Paměť_Files.Create_Adresář', 'jfs_rmdir': 'Paměť_Files.odebrat_Adresář', 'jfs_kind': 'Paměť_Files.položka_Druh'})
    exportovat_tabulka.update({'jnet_socket': 'zpětná_smyčka_síť.Create_položka', 'jnet_bind': 'zpětná_smyčka_síť.vázat_účastník',
        'jnet_put': 'zpětná_smyčka_síť.자료넣기', 'jnet_get': 'zpětná_smyčka_síť.자료읽기', 'jnet_send': 'zpětná_smyčka_síť.poslat',
        'jnet_recv': 'zpětná_smyčka_síť.dostat', 'jnet_port': 'zpětná_smyčka_síť.창구읽기', 'jnet_address': 'zpětná_smyčka_síť.주소읽기',
        'jnet_peer': 'zpětná_smyčka_síť.odesílatel_účastník', 'jnet_close': 'zpětná_smyčka_síť.Zavřené'})
    exportovat_tabulka.update({'jstream_create': 'tok_síť.Create_položka', 'jstream_bind': 'tok_síť.vázat_účastník', 'jstream_listen': 'tok_síť.naslouchat_účastník', 'jstream_connect': 'tok_síť.Připojit', 'jstream_accept': 'tok_síť.přijmout_kontakt', 'jstream_read': 'tok_síť.Čtení', 'jstream_write': 'tok_síť.Zápis', 'jstream_port': 'tok_síť.창구읽기', 'jstream_peer': 'tok_síť.상대창구읽기', 'jstream_close': 'tok_síť.Zavřené'})
    for symbol_HODNOTA in list(exportovat_tabulka):
        if symbol_HODNOTA.startswith('jstream_') or symbol_HODNOTA.startswith('jnet_') and symbol_HODNOTA not in ('jnet_put', 'jnet_get'):
            exportovat_tabulka[symbol_HODNOTA.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = exportovat_tabulka.pop(symbol_HODNOTA)
    예제들 = ['public final class sada { public static void Připravit() {']
    for cesta_2 in sorted((akce_kořen / '예제').iterdir()):
        if cesta_2.is_file():
            예제들.append('příkaz_interpret.statický_Soubor(%s, %s);' %
                (json.dumps(cesta_2.name), json.dumps(cesta_2.read_text(encoding='utf-8'), ensure_ascii=True)))
    (BLD_cesta / 'sada.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(akce_kořen, úložiště_kořen, Provést_příkaz)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(BLD_cesta)) as 작업경로:
        Třída_cesta = Path(작업경로)
        Provést_příkaz(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Třída_cesta, '-sourcepath', Třída_cesta, '-d', Třída_cesta] + sorted((akce_kořen / 'zdrojový_soubor').glob('*.java')) + [BLD_cesta / 'sada.java', BLD_cesta / '예제꾸러미.java'])
        # název_souboru·prostředí·Okno 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argument_pole = ['sh', úložiště_kořen / 'compiler/미리번역.sh', '--entry', 'jádro.Spustit_2', '--heap-words', '1048576', '-o', BLD_cesta / 'kernel-java.c']
        for symbol_HODNOTA, metoda_položka in sorted(exportovat_tabulka.items()):
            argument_pole += ['--export', symbol_HODNOTA + '=' + metoda_položka]
        Provést_příkaz(argument_pole + sorted(Třída_cesta.glob('*.class')))
    (BLD_cesta / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfigurace_BITS = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = úložiště_kořen / 'posix-kor/arm64-native'
    Create_uživatel_Space(akce_kořen, úložiště_kořen, C_kompilátor, 시플플번역기, linker_nástroj, Archiv_nástroj, konfigurace_BITS, Provést_příkaz)
    síť = Create_síť(akce_kořen, C_kompilátor, Archiv_nástroj, konfigurace_BITS, Provést_příkaz)
    vzdálený_použít = Create_vzdálený(akce_kořen, C_kompilátor, Archiv_nástroj, konfigurace_BITS, Provést_příkaz)
    포함인수 = ['-I', 포직스경로 / 'deklarace', '-I', BLD_cesta]
    빌드작업 = [(C_kompilátor, [], BLD_cesta / 'terminal-font.S', 'font.o'),
            (C_kompilátor, ['-std=c11', '-Wall', '-Wextra', '-Werror'], akce_kořen / 'počítač/interpret_příkazů.c', 'terminal.o'),
            (C_kompilátor, ['-std=c11', '-Wall', '-Wextra', '-Werror'], akce_kořen / 'počítač/prvek_obrazovky.c', 'widgets.o'),
            (C_kompilátor, ['-std=c11'], BLD_cesta / 'kernel-java.c', 'java.o'),
            (C_kompilátor, ['-std=c11', '-Wall', '-Wextra', '-Werror'], akce_kořen / 'počítač/Panel.c', 'board.o'),
            (C_kompilátor, ['-std=c11', '-Wall', '-Wextra', '-Werror'], akce_kořen / 'počítač/화면그림.c', 'drawing.o'),
            (C_kompilátor, ['-std=c11', '-Wall', '-Wextra', '-Werror'], akce_kořen / 'počítač/uživatelský_prostor.c', 'user.o'),
            (C_kompilátor, [], akce_kořen / 'spuštění_stroje/vstupní_bod_HODNOTA.S', 'entry.o'),
            (C_kompilátor, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Připojit.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], akce_kořen / 'zkoušky/Soubor_Hovory.cpp', 'cpp.o')]
    for kompilátor_nástroj, 추가영역, 원본자료, výstup in 빌드작업:
        원본설정 = [Soubor_položka for Soubor_položka in konfigurace_BITS if Soubor_položka != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else konfigurace_BITS
        Provést_příkaz([kompilátor_nástroj] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', BLD_cesta / výstup])
    Provést_příkaz([Archiv_nástroj, 'rcs', BLD_cesta / 'libposix-kor-arm64.a', BLD_cesta / 'posix.o'])
    Provést_příkaz([linker_nástroj, '--gc-sections', '-T', akce_kořen / 'spuštění_stroje/rozvržení_spojování.ld', '-Map', BLD_cesta / 'kernel.map', '-o', BLD_cesta / 'kernel.elf'] +
        [BLD_cesta / Název for Název in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', BLD_cesta / 'libposix-kor-arm64.a', síť, vzdálený_použít, BLD_cesta / 'remote/libassh.a', BLD_cesta / 'remote/libbearssl.a', '--end-group'])
    Provést_příkaz([objekt_Soubor_převaděč, '-O', 'binary', BLD_cesta / 'kernel.elf', BLD_cesta / 'kernel8.img'])
    sada_manifest = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'čeština.vlastní', 'korean_exceptions': 20,
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
    for Název in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        sada_manifest['sha256'][Název] = hashlib.sha256((BLD_cesta / Název).read_bytes()).hexdigest()
    (BLD_cesta / 'build.json').write_text(json.dumps(sada_manifest, indent=2) + '\n')
    print('완료:', BLD_cesta / 'kernel8.img')


if __name__ == '__main__':
    Spustit_2()
