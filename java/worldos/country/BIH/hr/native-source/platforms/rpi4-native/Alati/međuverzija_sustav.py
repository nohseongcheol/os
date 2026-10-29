#!/usr/bin/env python3
"""domaćin javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from međuverzija_korisnik_Space import Create_korisnik_Space
from međuverzija_mreža import Create_mreža
from 예제빌드 import 예제만들기
from međuverzija_udaljeno import Create_udaljeno

akcija_korijen = Path(__file__).resolve().parents[1]
spremište_korijen = akcija_korijen.parents[1]
međuverzija_put = akcija_korijen / 'build'


def Izvrši_naredba(argument_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in argument_ARRAY], cwd=str(akcija_korijen))


def Pokreni():
    međuverzija_put.mkdir(exist_ok=True)
    C_kompilator = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objekt_Datoteka_pretvornik = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arhiva_alat = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Alati in ('javac', C_kompilator, 시플플번역기, 연결편집기, objekt_Datoteka_pretvornik, Arhiva_alat):
        if not shutil.which(Alati):
            raise SystemExit('필요한 međuverzija_sustav Alati 없음: ' + Alati)
    font_informacija = json.loads((akcija_korijen / 'vendor/terminal-font.json').read_text())
    font_podaci = (akcija_korijen / 'vendor/terminal-font.bin').read_bytes()
    if len(font_podaci) != 65616 * 32 or hashlib.sha256(font_podaci).hexdigest() != font_informacija['sha256']:
        raise SystemExit('Terminal font_VALUE Veličina/SHA256 불일치')
    izvezi_tablica = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.Izlaz', 'jshell_input': '셸입출력.입력', 'java_task': 'jezgra_sustava.작업', 'jfs_path_start': 'Memorija_Datoteke.put_START',
               'jfs_path_byte': 'Memorija_Datoteke.put_bajt', 'jfs_open': 'Memorija_Datoteke.Otvori',
               'jfs_read': 'Memorija_Datoteke.Čitaj', 'jfs_write': 'Memorija_Datoteke.Zapisuj',
               'jfs_seek': 'Memorija_Datoteke.tražiti_položaj', 'jfs_close': 'Memorija_Datoteke.Zatvori',
               'jfs_size': 'Memorija_Datoteke.Veličina', 'jfs_unlink': 'Memorija_Datoteke.izbrisati_unos',
               'jfs_truncate': 'Memorija_Datoteke.길이정하기'}
    izvezi_tablica.update({'jfs_entry_count': 'Memorija_Datoteke.파일한도', 'jfs_entry_length': 'Memorija_Datoteke.공개이름길이', 'jfs_entry_byte': 'Memorija_Datoteke.공개이름바이트', 'jfs_entry_size': 'Memorija_Datoteke.공개파일크기'})
    izvezi_tablica.update({'jdraw_prepare': '화면합성.Pripremi', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.isječak',
        'jdraw_clip_value': '화면합성.isječak_VALUE', 'jdraw_begin': '화면합성.Pokreni',
        'jdraw_end': '화면합성.Završi', 'jdraw_pixel': '화면합성.slikovni_element',
        'jdraw_rectangle': '화면합성.pravokutnik_ispuna', 'jdraw_pointer': '화면합성.pokazivač'})
    izvezi_tablica.update({'jfs_mkdir': 'Memorija_Datoteke.Create_imenik', 'jfs_rmdir': 'Memorija_Datoteke.ukloniti_imenik', 'jfs_kind': 'Memorija_Datoteke.항목종류'})
    izvezi_tablica.update({'jnet_socket': 'povratna_obrada_mreža.Create_unos', 'jnet_bind': 'povratna_obrada_mreža.BIND_sudionik',
        'jnet_put': 'povratna_obrada_mreža.자료넣기', 'jnet_get': 'povratna_obrada_mreža.자료읽기', 'jnet_send': 'povratna_obrada_mreža.slati',
        'jnet_recv': 'povratna_obrada_mreža.primiti', 'jnet_port': 'povratna_obrada_mreža.창구읽기', 'jnet_address': 'povratna_obrada_mreža.주소읽기',
        'jnet_peer': 'povratna_obrada_mreža.pošiljatelj_sudionik', 'jnet_close': 'povratna_obrada_mreža.Zatvori'})
    izvezi_tablica.update({'jstream_create': 'tok_mreža.Create_unos', 'jstream_bind': 'tok_mreža.BIND_sudionik', 'jstream_listen': 'tok_mreža.osluškivati_sudionik', 'jstream_connect': 'tok_mreža.Spoji_se', 'jstream_accept': 'tok_mreža.prihvatiti_veza', 'jstream_read': 'tok_mreža.Čitaj', 'jstream_write': 'tok_mreža.Zapisuj', 'jstream_port': 'tok_mreža.창구읽기', 'jstream_peer': 'tok_mreža.상대창구읽기', 'jstream_close': 'tok_mreža.Zatvori'})
    for simbol_VALUE in list(izvezi_tablica):
        if simbol_VALUE.startswith('jstream_') or simbol_VALUE.startswith('jnet_') and simbol_VALUE not in ('jnet_put', 'jnet_get'):
            izvezi_tablica[simbol_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = izvezi_tablica.pop(simbol_VALUE)
    예제들 = ['public final class komplet { public static void Pripremi() {']
    for PUTANJA in sorted((akcija_korijen / '예제').iterdir()):
        if PUTANJA.is_file():
            예제들.append('명령해석기.정적파일(%s, %s);' %
                (json.dumps(PUTANJA.name), json.dumps(PUTANJA.read_text(encoding='utf-8'), ensure_ascii=True)))
    (međuverzija_put / 'komplet.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(akcija_korijen, spremište_korijen, Izvrši_naredba)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(međuverzija_put)) as 작업경로:
        poduka_put = Path(작업경로)
        Izvrši_naredba(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', poduka_put, '-sourcepath', poduka_put, '-d', poduka_put] + sorted((akcija_korijen / 'IZVOR').glob('*.java')) + [međuverzija_put / 'komplet.java', međuverzija_put / '예제꾸러미.java'])
        # Datoteka·ljuska·Prozor 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argument_ARRAY = ['sh', spremište_korijen / 'compiler/미리번역.sh', '--entry', 'jezgra_sustava.Pokreni', '--heap-words', '1048576', '-o', međuverzija_put / 'kernel-java.c']
        for simbol_VALUE, postupak_unos in sorted(izvezi_tablica.items()):
            argument_ARRAY += ['--export', simbol_VALUE + '=' + postupak_unos]
        Izvrši_naredba(argument_ARRAY + sorted(poduka_put.glob('*.class')))
    (međuverzija_put / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfiguracija_Pozadinski_pametni_servis_za_transfer = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = spremište_korijen / 'posix-kor/arm64-native'
    Create_korisnik_Space(akcija_korijen, spremište_korijen, C_kompilator, 시플플번역기, 연결편집기, Arhiva_alat, konfiguracija_Pozadinski_pametni_servis_za_transfer, Izvrši_naredba)
    mreža = Create_mreža(akcija_korijen, C_kompilator, Arhiva_alat, konfiguracija_Pozadinski_pametni_servis_za_transfer, Izvrši_naredba)
    udaljeno_uporaba = Create_udaljeno(akcija_korijen, C_kompilator, Arhiva_alat, konfiguracija_Pozadinski_pametni_servis_za_transfer, Izvrši_naredba)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', međuverzija_put]
    빌드작업 = [(C_kompilator, [], međuverzija_put / 'terminal-font.S', 'font.o'),
            (C_kompilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], akcija_korijen / 'stroj/Terminal.c', 'terminal.o'),
            (C_kompilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], akcija_korijen / 'stroj/widget.c', 'widgets.o'),
            (C_kompilator, ['-std=c11'], međuverzija_put / 'kernel-java.c', 'java.o'),
            (C_kompilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], akcija_korijen / 'stroj/pano.c', 'board.o'),
            (C_kompilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], akcija_korijen / 'stroj/화면그림.c', 'drawing.o'),
            (C_kompilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], akcija_korijen / 'stroj/korisnik.c', 'user.o'),
            (C_kompilator, [], akcija_korijen / '부팅/unos_p_VALUE.S', 'entry.o'),
            (C_kompilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Spoji_se.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], akcija_korijen / '시험/Datoteka_Pozivi.cpp', 'cpp.o')]
    for kompilator_alat, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [Datoteka_unos for Datoteka_unos in konfiguracija_Pozadinski_pametni_servis_za_transfer if Datoteka_unos != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else konfiguracija_Pozadinski_pametni_servis_za_transfer
        Izvrši_naredba([kompilator_alat] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', međuverzija_put / 출력결과])
    Izvrši_naredba([Arhiva_alat, 'rcs', međuverzija_put / 'libposix-kor-arm64.a', međuverzija_put / 'posix.o'])
    Izvrši_naredba([연결편집기, '--gc-sections', '-T', akcija_korijen / '부팅/veza_Raspored.ld', '-Map', međuverzija_put / 'kernel.map', '-o', međuverzija_put / 'kernel.elf'] +
        [međuverzija_put / Ime for Ime in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', međuverzija_put / 'libposix-kor-arm64.a', mreža, udaljeno_uporaba, međuverzija_put / 'remote/libassh.a', međuverzija_put / 'remote/libbearssl.a', '--end-group'])
    Izvrši_naredba([objekt_Datoteka_pretvornik, '-O', 'binary', međuverzija_put / 'kernel.elf', međuverzija_put / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'hrvatski.vlastiti', 'korean_exceptions': 20,
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
    for Ime in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Ime] = hashlib.sha256((međuverzija_put / Ime).read_bytes()).hexdigest()
    (međuverzija_put / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', međuverzija_put / 'kernel8.img')


if __name__ == '__main__':
    Pokreni()
