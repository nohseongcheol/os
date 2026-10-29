#!/usr/bin/env python3
"""host javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from BLD_użytkownik_SPACJA import Twórca_użytkownik_SPACJA
from BLD_sieć import Twórca_sieć
from 예제빌드 import 예제만들기
from BLD_zdalny import Twórca_zdalny

Project_korzeń = Path(__file__).resolve().parents[1]
repozytorium_korzeń = Project_korzeń.parents[1]
BLD_ścieżka = Project_korzeń / 'build'


def Wykonaj_polecenie(argument_TABLICA):
    subprocess.check_call([str(첫째값) for 첫째값 in argument_TABLICA], cwd=str(Project_korzeń))


def Uruchom_2():
    BLD_ścieżka.mkdir(exist_ok=True)
    C_kompilator = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    konsolidator_narzędzie = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    plik_obiektu_konwerter = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Archiwum_narzędzie = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for narzędzia in ('javac', C_kompilator, 시플플번역기, konsolidator_narzędzie, plik_obiektu_konwerter, Archiwum_narzędzie):
        if not shutil.which(narzędzia):
            raise SystemExit('필요한 BLD_System narzędzia 없음: ' + narzędzia)
    czcionka_informacje = json.loads((Project_korzeń / 'vendor/terminal-font.json').read_text())
    czcionka_dane = (Project_korzeń / 'vendor/terminal-font.bin').read_bytes()
    if len(czcionka_dane) != 65616 * 32 or hashlib.sha256(czcionka_dane).hexdigest() != czcionka_informacje['sha256']:
        raise SystemExit('interpretator_poleceń czcionka_WARTOŚĆ Rozmiar/SHA256 불일치')
    eksportować_tabela = {'jshell_interactive': '셸입출력.systemy_informacyjne_interakcyjny', 'jshell_output': '셸입출력.pozycja_wyjścia', 'jshell_input': '셸입출력.wejście_WARTOŚĆ', 'java_task': 'jądro.작업', 'jfs_path_start': 'Pamięć_Files.ścieżka_START',
               'jfs_path_byte': 'Pamięć_Files.ścieżka_bajt', 'jfs_open': 'Pamięć_Files.Otwórz',
               'jfs_read': 'Pamięć_Files.Odczyt', 'jfs_write': 'Pamięć_Files.Zapis',
               'jfs_seek': 'Pamięć_Files.szukać_stanowisko', 'jfs_close': 'Pamięć_Files.Zamknięte',
               'jfs_size': 'Pamięć_Files.Rozmiar', 'jfs_unlink': 'Pamięć_Files.usunąć_wpis',
               'jfs_truncate': 'Pamięć_Files.set_długość'}
    eksportować_tabela.update({'jfs_entry_count': 'Pamięć_Files.파일한도', 'jfs_entry_length': 'Pamięć_Files.공개이름길이', 'jfs_entry_byte': 'Pamięć_Files.공개이름바이트', 'jfs_entry_size': 'Pamięć_Files.공개파일크기'})
    eksportować_tabela.update({'jdraw_prepare': '화면합성.Przygotuj', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.pobrać_wysokość', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.obcinać',
        'jdraw_clip_value': '화면합성.obcinać_WARTOŚĆ', 'jdraw_begin': '화면합성.Uruchom_2',
        'jdraw_end': '화면합성.Zakończ', 'jdraw_pixel': '화면합성.piksel',
        'jdraw_rectangle': '화면합성.prostokąt_Wypełnij', 'jdraw_pointer': '화면합성.wskaźnik'})
    eksportować_tabela.update({'jfs_mkdir': 'Pamięć_Files.Twórca_Katalog', 'jfs_rmdir': 'Pamięć_Files.usuń_Katalog', 'jfs_kind': 'Pamięć_Files.wpis_Rodzaj'})
    eksportować_tabela.update({'jnet_socket': 'sprzężenie_zwrotne_sieć.Twórca_wpis', 'jnet_bind': 'sprzężenie_zwrotne_sieć.BIND_uczestnik',
        'jnet_put': 'sprzężenie_zwrotne_sieć.자료넣기', 'jnet_get': 'sprzężenie_zwrotne_sieć.자료읽기', 'jnet_send': 'sprzężenie_zwrotne_sieć.wysłać',
        'jnet_recv': 'sprzężenie_zwrotne_sieć.odbierać', 'jnet_port': 'sprzężenie_zwrotne_sieć.창구읽기', 'jnet_address': 'sprzężenie_zwrotne_sieć.주소읽기',
        'jnet_peer': 'sprzężenie_zwrotne_sieć.nadawca_uczestnik', 'jnet_close': 'sprzężenie_zwrotne_sieć.Zamknięte'})
    eksportować_tabela.update({'jstream_create': 'Stream_sieć.Twórca_wpis', 'jstream_bind': 'Stream_sieć.BIND_uczestnik', 'jstream_listen': 'Stream_sieć.nasłuchiwać_uczestnik', 'jstream_connect': 'Stream_sieć.Połącz', 'jstream_accept': 'Stream_sieć.akceptować_połączenie', 'jstream_read': 'Stream_sieć.Odczyt', 'jstream_write': 'Stream_sieć.Zapis', 'jstream_port': 'Stream_sieć.창구읽기', 'jstream_peer': 'Stream_sieć.상대창구읽기', 'jstream_close': 'Stream_sieć.Zamknięte'})
    for symbol_WARTOŚĆ in list(eksportować_tabela):
        if symbol_WARTOŚĆ.startswith('jstream_') or symbol_WARTOŚĆ.startswith('jnet_') and symbol_WARTOŚĆ not in ('jnet_put', 'jnet_get'):
            eksportować_tabela[symbol_WARTOŚĆ.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = eksportować_tabela.pop(symbol_WARTOŚĆ)
    예제들 = ['public final class pakiet { public static void Przygotuj() {']
    for ścieżka_2 in sorted((Project_korzeń / '예제').iterdir()):
        if ścieżka_2.is_file():
            예제들.append('polecenie_interpreter.statyczny_Plik(%s, %s);' %
                (json.dumps(ścieżka_2.name), json.dumps(ścieżka_2.read_text(encoding='utf-8'), ensure_ascii=True)))
    (BLD_ścieżka / 'pakiet.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Project_korzeń, repozytorium_korzeń, Wykonaj_polecenie)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(BLD_ścieżka)) as 작업경로:
        Klasa_ścieżka = Path(작업경로)
        Wykonaj_polecenie(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Klasa_ścieżka, '-sourcepath', Klasa_ścieżka, '-d', Klasa_ścieżka] + sorted((Project_korzeń / 'plik_źródłowy').glob('*.java')) + [BLD_ścieżka / 'pakiet.java', BLD_ścieżka / '예제꾸러미.java'])
        # nazwa_pliku·powłoka·Okno 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argument_TABLICA = ['sh', repozytorium_korzeń / 'compiler/미리번역.sh', '--entry', 'jądro.Uruchom_2', '--heap-words', '1048576', '-o', BLD_ścieżka / 'kernel-java.c']
        for symbol_WARTOŚĆ, metoda_wpis in sorted(eksportować_tabela.items()):
            argument_TABLICA += ['--export', symbol_WARTOŚĆ + '=' + metoda_wpis]
        Wykonaj_polecenie(argument_TABLICA + sorted(Klasa_ścieżka.glob('*.class')))
    (BLD_ścieżka / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfiguracja_BITS = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = repozytorium_korzeń / 'posix-kor/arm64-native'
    Twórca_użytkownik_SPACJA(Project_korzeń, repozytorium_korzeń, C_kompilator, 시플플번역기, konsolidator_narzędzie, Archiwum_narzędzie, konfiguracja_BITS, Wykonaj_polecenie)
    sieć = Twórca_sieć(Project_korzeń, C_kompilator, Archiwum_narzędzie, konfiguracja_BITS, Wykonaj_polecenie)
    zdalny_używać = Twórca_zdalny(Project_korzeń, C_kompilator, Archiwum_narzędzie, konfiguracja_BITS, Wykonaj_polecenie)
    포함인수 = ['-I', 포직스경로 / 'deklaracje', '-I', BLD_ścieżka]
    빌드작업 = [(C_kompilator, [], BLD_ścieżka / 'terminal-font.S', 'font.o'),
            (C_kompilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_korzeń / 'maszyna/interpretator_poleceń.c', 'terminal.o'),
            (C_kompilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_korzeń / 'maszyna/element_ekranu.c', 'widgets.o'),
            (C_kompilator, ['-std=c11'], BLD_ścieżka / 'kernel-java.c', 'java.o'),
            (C_kompilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_korzeń / 'maszyna/Tablica.c', 'board.o'),
            (C_kompilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_korzeń / 'maszyna/화면그림.c', 'drawing.o'),
            (C_kompilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_korzeń / 'maszyna/przestrzeń_użytkownika.c', 'user.o'),
            (C_kompilator, [], Project_korzeń / 'rozruch_maszyny/punkt_wejścia_WARTOŚĆ.S', 'entry.o'),
            (C_kompilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Połącz.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Project_korzeń / 'testy/Plik_Połączenia.cpp', 'cpp.o')]
    for kompilator_narzędzie, 추가영역, 원본자료, produkt_wyjściowy in 빌드작업:
        원본설정 = [Plik_wpis for Plik_wpis in konfiguracja_BITS if Plik_wpis != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else konfiguracja_BITS
        Wykonaj_polecenie([kompilator_narzędzie] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', BLD_ścieżka / produkt_wyjściowy])
    Wykonaj_polecenie([Archiwum_narzędzie, 'rcs', BLD_ścieżka / 'libposix-kor-arm64.a', BLD_ścieżka / 'posix.o'])
    Wykonaj_polecenie([konsolidator_narzędzie, '--gc-sections', '-T', Project_korzeń / 'rozruch_maszyny/układ_konsolidacji.ld', '-Map', BLD_ścieżka / 'kernel.map', '-o', BLD_ścieżka / 'kernel.elf'] +
        [BLD_ścieżka / Nazwa for Nazwa in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', BLD_ścieżka / 'libposix-kor-arm64.a', sieć, zdalny_używać, BLD_ścieżka / 'remote/libassh.a', BLD_ścieżka / 'remote/libbearssl.a', '--end-group'])
    Wykonaj_polecenie([plik_obiektu_konwerter, '-O', 'binary', BLD_ścieżka / 'kernel.elf', BLD_ścieżka / 'kernel8.img'])
    pakiet_manifest = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'polski.własny', 'korean_exceptions': 20,
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
    for Nazwa in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        pakiet_manifest['sha256'][Nazwa] = hashlib.sha256((BLD_ścieżka / Nazwa).read_bytes()).hexdigest()
    (BLD_ścieżka / 'build.json').write_text(json.dumps(pakiet_manifest, indent=2) + '\n')
    print('완료:', BLD_ścieżka / 'kernel8.img')


if __name__ == '__main__':
    Uruchom_2()
