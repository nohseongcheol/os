#!/usr/bin/env python3
"""hostiteľ javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from zostava_používateľ_priestor import Create_používateľ_priestor
from zostava_sieť import Create_sieť
from 예제빌드 import 예제만들기
from zostava_vzdialený import Create_vzdialený

akcia_koreň = Path(__file__).resolve().parents[1]
odkladací_priestor_koreň = akcia_koreň.parents[1]
zostava_cesta = akcia_koreň / 'build'


def Vykonať_príkaz(argument_pole):
    subprocess.check_call([str(첫째값) for 첫째값 in argument_pole], cwd=str(akcia_koreň))


def Spustiť_2():
    zostava_cesta.mkdir(exist_ok=True)
    C_kompilátor = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objekt_Súbor_konvertor = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Archív_nástroj = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Nástroje in ('javac', C_kompilátor, 시플플번역기, 연결편집기, objekt_Súbor_konvertor, Archív_nástroj):
        if not shutil.which(Nástroje):
            raise SystemExit('필요한 zostava_systém Nástroje 없음: ' + Nástroje)
    písmo_informácia = json.loads((akcia_koreň / 'vendor/terminal-font.json').read_text())
    písmo_údaje = (akcia_koreň / 'vendor/terminal-font.bin').read_bytes()
    if len(písmo_údaje) != 65616 * 32 or hashlib.sha256(písmo_údaje).hexdigest() != písmo_informácia['sha256']:
        raise SystemExit('Terminál písmo_VALUE Veľkosť/SHA256 불일치')
    exportovať_tabuľka = {'jshell_interactive': '셸입출력.Informačné_systémy_interaktívny', 'jshell_output': '셸입출력.Výstup', 'jshell_input': '셸입출력.vstup_VALUE', 'java_task': 'jadro.작업', 'jfs_path_start': 'Pamäť_Súbory.cesta_START',
               'jfs_path_byte': 'Pamäť_Súbory.cesta_Byte', 'jfs_open': 'Pamäť_Súbory.Otvoriť',
               'jfs_read': 'Pamäť_Súbory.Čítanie', 'jfs_write': 'Pamäť_Súbory.Zápis',
               'jfs_seek': 'Pamäť_Súbory.hľadať_pozícia', 'jfs_close': 'Pamäť_Súbory.Zatvoriť',
               'jfs_size': 'Pamäť_Súbory.Veľkosť', 'jfs_unlink': 'Pamäť_Súbory.vymazať_položka',
               'jfs_truncate': 'Pamäť_Súbory.množina_dĺžka'}
    exportovať_tabuľka.update({'jfs_entry_count': 'Pamäť_Súbory.파일한도', 'jfs_entry_length': 'Pamäť_Súbory.공개이름길이', 'jfs_entry_byte': 'Pamäť_Súbory.공개이름바이트', 'jfs_entry_size': 'Pamäť_Súbory.공개파일크기'})
    exportovať_tabuľka.update({'jdraw_prepare': '화면합성.Pripraviť', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.načítať_výška', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.klip',
        'jdraw_clip_value': '화면합성.klip_VALUE', 'jdraw_begin': '화면합성.Spustiť_2',
        'jdraw_end': '화면합성.Dokončiť', 'jdraw_pixel': '화면합성.pixel',
        'jdraw_rectangle': '화면합성.obdĺžnik_výplň', 'jdraw_pointer': '화면합성.ukazovateľ'})
    exportovať_tabuľka.update({'jfs_mkdir': 'Pamäť_Súbory.Create_Adresár', 'jfs_rmdir': 'Pamäť_Súbory.odobrať_Adresár', 'jfs_kind': 'Pamäť_Súbory.항목종류'})
    exportovať_tabuľka.update({'jnet_socket': 'spätná_slučka_sieť.Create_položka', 'jnet_bind': 'spätná_slučka_sieť.BIND_účastník',
        'jnet_put': 'spätná_slučka_sieť.자료넣기', 'jnet_get': 'spätná_slučka_sieť.자료읽기', 'jnet_send': 'spätná_slučka_sieť.odoslať',
        'jnet_recv': 'spätná_slučka_sieť.dostať', 'jnet_port': 'spätná_slučka_sieť.창구읽기', 'jnet_address': 'spätná_slučka_sieť.주소읽기',
        'jnet_peer': 'spätná_slučka_sieť.odosielateľ_účastník', 'jnet_close': 'spätná_slučka_sieť.Zatvoriť'})
    exportovať_tabuľka.update({'jstream_create': 'Stream_sieť.Create_položka', 'jstream_bind': 'Stream_sieť.BIND_účastník', 'jstream_listen': 'Stream_sieť.načúvať_účastník', 'jstream_connect': 'Stream_sieť.Pripojiť', 'jstream_accept': 'Stream_sieť.prijať_kontakt', 'jstream_read': 'Stream_sieť.Čítanie', 'jstream_write': 'Stream_sieť.Zápis', 'jstream_port': 'Stream_sieť.창구읽기', 'jstream_peer': 'Stream_sieť.상대창구읽기', 'jstream_close': 'Stream_sieť.Zatvoriť'})
    for symbol_VALUE in list(exportovať_tabuľka):
        if symbol_VALUE.startswith('jstream_') or symbol_VALUE.startswith('jnet_') and symbol_VALUE not in ('jnet_put', 'jnet_get'):
            exportovať_tabuľka[symbol_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = exportovať_tabuľka.pop(symbol_VALUE)
    예제들 = ['public final class zväzok { public static void Pripraviť() {']
    for Cesta in sorted((akcia_koreň / '예제').iterdir()):
        if Cesta.is_file():
            예제들.append('명령해석기.정적파일(%s, %s);' %
                (json.dumps(Cesta.name), json.dumps(Cesta.read_text(encoding='utf-8'), ensure_ascii=True)))
    (zostava_cesta / 'zväzok.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(akcia_koreň, odkladací_priestor_koreň, Vykonať_príkaz)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(zostava_cesta)) as 작업경로:
        lekcia_cesta = Path(작업경로)
        Vykonať_príkaz(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', lekcia_cesta, '-sourcepath', lekcia_cesta, '-d', lekcia_cesta] + sorted((akcia_koreň / 'ZDROJ').glob('*.java')) + [zostava_cesta / 'zväzok.java', zostava_cesta / '예제꾸러미.java'])
        # Súbor·셸·Okno 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argument_pole = ['sh', odkladací_priestor_koreň / 'compiler/미리번역.sh', '--entry', 'jadro.Spustiť_2', '--heap-words', '1048576', '-o', zostava_cesta / 'kernel-java.c']
        for symbol_VALUE, metóda_položka in sorted(exportovať_tabuľka.items()):
            argument_pole += ['--export', symbol_VALUE + '=' + metóda_položka]
        Vykonať_príkaz(argument_pole + sorted(lekcia_cesta.glob('*.class')))
    (zostava_cesta / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfigurácia_Background_Intelligent_Transfer_Service = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = odkladací_priestor_koreň / 'posix-kor/arm64-native'
    Create_používateľ_priestor(akcia_koreň, odkladací_priestor_koreň, C_kompilátor, 시플플번역기, 연결편집기, Archív_nástroj, konfigurácia_Background_Intelligent_Transfer_Service, Vykonať_príkaz)
    sieť = Create_sieť(akcia_koreň, C_kompilátor, Archív_nástroj, konfigurácia_Background_Intelligent_Transfer_Service, Vykonať_príkaz)
    vzdialený_používať = Create_vzdialený(akcia_koreň, C_kompilátor, Archív_nástroj, konfigurácia_Background_Intelligent_Transfer_Service, Vykonať_príkaz)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', zostava_cesta]
    빌드작업 = [(C_kompilátor, [], zostava_cesta / 'terminal-font.S', 'font.o'),
            (C_kompilátor, ['-std=c11', '-Wall', '-Wextra', '-Werror'], akcia_koreň / 'počítač_5eb260fa/Terminál.c', 'terminal.o'),
            (C_kompilátor, ['-std=c11', '-Wall', '-Wextra', '-Werror'], akcia_koreň / 'počítač_5eb260fa/widget.c', 'widgets.o'),
            (C_kompilátor, ['-std=c11'], zostava_cesta / 'kernel-java.c', 'java.o'),
            (C_kompilátor, ['-std=c11', '-Wall', '-Wextra', '-Werror'], akcia_koreň / 'počítač_5eb260fa/Panel.c', 'board.o'),
            (C_kompilátor, ['-std=c11', '-Wall', '-Wextra', '-Werror'], akcia_koreň / 'počítač_5eb260fa/화면그림.c', 'drawing.o'),
            (C_kompilátor, ['-std=c11', '-Wall', '-Wextra', '-Werror'], akcia_koreň / 'počítač_5eb260fa/používateľ.c', 'user.o'),
            (C_kompilátor, [], akcia_koreň / '부팅/položka_bod_VALUE.S', 'entry.o'),
            (C_kompilátor, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Pripojiť.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], akcia_koreň / '시험/Súbor_Hovory.cpp', 'cpp.o')]
    for kompilátor_nástroj, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [Súbor_položka for Súbor_položka in konfigurácia_Background_Intelligent_Transfer_Service if Súbor_položka != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else konfigurácia_Background_Intelligent_Transfer_Service
        Vykonať_príkaz([kompilátor_nástroj] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', zostava_cesta / 출력결과])
    Vykonať_príkaz([Archív_nástroj, 'rcs', zostava_cesta / 'libposix-kor-arm64.a', zostava_cesta / 'posix.o'])
    Vykonať_príkaz([연결편집기, '--gc-sections', '-T', akcia_koreň / '부팅/odkaz_Navigácia.ld', '-Map', zostava_cesta / 'kernel.map', '-o', zostava_cesta / 'kernel.elf'] +
        [zostava_cesta / Názov for Názov in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', zostava_cesta / 'libposix-kor-arm64.a', sieť, vzdialený_používať, zostava_cesta / 'remote/libassh.a', zostava_cesta / 'remote/libbearssl.a', '--end-group'])
    Vykonať_príkaz([objekt_Súbor_konvertor, '-O', 'binary', zostava_cesta / 'kernel.elf', zostava_cesta / 'kernel8.img'])
    zväzok_manifest_zostáv = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Slovenský.vlastné', 'korean_exceptions': 20,
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
    for Názov in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        zväzok_manifest_zostáv['sha256'][Názov] = hashlib.sha256((zostava_cesta / Názov).read_bytes()).hexdigest()
    (zostava_cesta / 'build.json').write_text(json.dumps(zväzok_manifest_zostáv, indent=2) + '\n')
    print('완료:', zostava_cesta / 'kernel8.img')


if __name__ == '__main__':
    Spustiť_2()
