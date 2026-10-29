#!/usr/bin/env python3
"""organizator javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from verzija_korisnik_prostor import Create_korisnik_prostor
from verzija_Mreža import Create_Mreža
from 예제빌드 import 예제만들기
from verzija_udaljeno import Create_udaljeno

projicirati_koijen = Path(__file__).resolve().parents[1]
저장소 = projicirati_koijen.parents[1]
verzija_put = projicirati_koijen / 'build'


def Izvrši_komanda(argument_niz):
    subprocess.check_call([str(첫째값) for 첫째값 in argument_niz], cwd=str(projicirati_koijen))


def Pokreni():
    verzija_put.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objekt_fajl_pretvarač = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arhiva_alatka = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Alati in ('javac', 시언어번역기, 시플플번역기, 연결편집기, objekt_fajl_pretvarač, Arhiva_alatka):
        if not shutil.which(Alati):
            raise SystemExit('필요한 verzija_sistem Alati 없음: ' + Alati)
    font_informacija = json.loads((projicirati_koijen / 'vendor/terminal-font.json').read_text())
    font_podaci = (projicirati_koijen / 'vendor/terminal-font.bin').read_bytes()
    if len(font_podaci) != 65616 * 32 or hashlib.sha256(font_podaci).hexdigest() != font_informacija['sha256']:
        raise SystemExit('Terminal font_VALUE Veličina/SHA256 불일치')
    izvesti_tabela = {'jshell_interactive': '셸입출력.odjel_za_informacijske_tehnologije_interaktivno', 'jshell_output': '셸입출력.Ispis', 'jshell_input': '셸입출력.입력', 'java_task': 'jezgro.작업', 'jfs_path_start': 'Memorija_Fajlovi.put_START',
               'jfs_path_byte': 'Memorija_Fajlovi.put_bajt', 'jfs_open': 'Memorija_Fajlovi.Otvori',
               'jfs_read': 'Memorija_Fajlovi.Čitaj', 'jfs_write': 'Memorija_Fajlovi.Piši',
               'jfs_seek': 'Memorija_Fajlovi.tražiti_položaj', 'jfs_close': 'Memorija_Fajlovi.Zatvori',
               'jfs_size': 'Memorija_Fajlovi.Veličina', 'jfs_unlink': 'Memorija_Fajlovi.지우기',
               'jfs_truncate': 'Memorija_Fajlovi.skup_dužina'}
    izvesti_tabela.update({'jfs_entry_count': 'Memorija_Fajlovi.파일한도', 'jfs_entry_length': 'Memorija_Fajlovi.공개이름길이', 'jfs_entry_byte': 'Memorija_Fajlovi.공개이름바이트', 'jfs_entry_size': 'Memorija_Fajlovi.공개파일크기'})
    izvesti_tabela.update({'jdraw_prepare': '화면합성.Pripremiti', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.isječak',
        'jdraw_clip_value': '화면합성.isječak_VALUE', 'jdraw_begin': '화면합성.Pokreni',
        'jdraw_end': '화면합성.Kraj', 'jdraw_pixel': '화면합성.pel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.pokazivač'})
    izvesti_tabela.update({'jfs_mkdir': 'Memorija_Fajlovi.Create_Direktorij', 'jfs_rmdir': 'Memorija_Fajlovi.ukloniti_Direktorij', 'jfs_kind': 'Memorija_Fajlovi.항목종류'})
    izvesti_tabela.update({'jnet_socket': '되돌림망.Create_unos', 'jnet_bind': '되돌림망.BIND_završna_tačka',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.poslati',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.pošiljalac_završna_tačka', 'jnet_close': '되돌림망.Zatvori'})
    izvesti_tabela.update({'jstream_create': 'tok_Mreža.Create_unos', 'jstream_bind': 'tok_Mreža.BIND_završna_tačka', 'jstream_listen': 'tok_Mreža.slušati_završna_tačka', 'jstream_connect': 'tok_Mreža.Spoji_se', 'jstream_accept': 'tok_Mreža.prihvatiti_veza', 'jstream_read': 'tok_Mreža.Čitaj', 'jstream_write': 'tok_Mreža.Piši', 'jstream_port': 'tok_Mreža.창구읽기', 'jstream_peer': 'tok_Mreža.상대창구읽기', 'jstream_close': 'tok_Mreža.Zatvori'})
    for simbol_VALUE in list(izvesti_tabela):
        if simbol_VALUE.startswith('jstream_') or simbol_VALUE.startswith('jnet_') and simbol_VALUE not in ('jnet_put', 'jnet_get'):
            izvesti_tabela[simbol_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = izvesti_tabela.pop(simbol_VALUE)
    예제들 = ['public final class paket { public static void Pripremiti() {']
    for Putanja in sorted((projicirati_koijen / '예제').iterdir()):
        if Putanja.is_file():
            예제들.append('명령해석기.statični_fajl(%s, %s);' %
                (json.dumps(Putanja.name), json.dumps(Putanja.read_text(encoding='utf-8'), ensure_ascii=True)))
    (verzija_put / 'paket.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(projicirati_koijen, 저장소, Izvrši_komanda)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(verzija_put)) as 작업경로:
        klasa_put = Path(작업경로)
        Izvrši_komanda(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klasa_put, '-sourcepath', klasa_put, '-d', klasa_put] + sorted((projicirati_koijen / 'IZVOR').glob('*.java')) + [verzija_put / 'paket.java', verzija_put / '예제꾸러미.java'])
        # Fajl·ljuska·prozor 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argument_niz = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'jezgro.Pokreni', '--heap-words', '1048576', '-o', verzija_put / 'kernel-java.c']
        for simbol_VALUE, metoda_unos in sorted(izvesti_tabela.items()):
            argument_niz += ['--export', simbol_VALUE + '=' + metoda_unos]
        Izvrši_komanda(argument_niz + sorted(klasa_put.glob('*.class')))
    (verzija_put / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    Create_korisnik_prostor(projicirati_koijen, 저장소, 시언어번역기, 시플플번역기, 연결편집기, Arhiva_alatka, 설정비트, Izvrši_komanda)
    Mreža = Create_Mreža(projicirati_koijen, 시언어번역기, Arhiva_alatka, 설정비트, Izvrši_komanda)
    원격사용 = Create_udaljeno(projicirati_koijen, 시언어번역기, Arhiva_alatka, 설정비트, Izvrši_komanda)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', verzija_put]
    빌드작업 = [(시언어번역기, [], verzija_put / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projicirati_koijen / 'mašina/Terminal.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projicirati_koijen / 'mašina/vidžet.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], verzija_put / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projicirati_koijen / 'mašina/ploča.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projicirati_koijen / 'mašina/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projicirati_koijen / 'mašina/korisnik.c', 'user.o'),
            (시언어번역기, [], projicirati_koijen / '부팅/unos_p_VALUE.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Spoji_se.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], projicirati_koijen / '시험/fajl_Pozivi.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [fajl_unos for fajl_unos in 설정비트 if fajl_unos != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        Izvrši_komanda([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', verzija_put / 출력결과])
    Izvrši_komanda([Arhiva_alatka, 'rcs', verzija_put / 'libposix-kor-arm64.a', verzija_put / 'posix.o'])
    Izvrši_komanda([연결편집기, '--gc-sections', '-T', projicirati_koijen / '부팅/Veza_izgled.ld', '-Map', verzija_put / 'kernel.map', '-o', verzija_put / 'kernel.elf'] +
        [verzija_put / Naziv for Naziv in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', verzija_put / 'libposix-kor-arm64.a', Mreža, 원격사용, verzija_put / 'remote/libassh.a', verzija_put / 'remote/libbearssl.a', '--end-group'])
    Izvrši_komanda([objekt_fajl_pretvarač, '-O', 'binary', verzija_put / 'kernel.elf', verzija_put / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': '한국어.자체', 'korean_exceptions': 20,
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
    for Naziv in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Naziv] = hashlib.sha256((verzija_put / Naziv).read_bytes()).hexdigest()
    (verzija_put / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', verzija_put / 'kernel8.img')


if __name__ == '__main__':
    Pokreni()
