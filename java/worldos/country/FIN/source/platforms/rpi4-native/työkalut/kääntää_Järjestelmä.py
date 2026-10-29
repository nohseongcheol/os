#!/usr/bin/env python3
"""isäntä javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from kääntää_käyttäjä_tila import Luo_käyttäjä_tila
from kääntää_verkko import Luo_verkko
from 예제빌드 import 예제만들기
from kääntää_etä import Luo_etä

aloite_juuri = Path(__file__).resolve().parents[1]
säilö_juuri = aloite_juuri.parents[1]
kääntää_polku = aloite_juuri / 'build'


def Suorita_komento(argumentti_MATRIISI):
    subprocess.check_call([str(첫째값) for 첫째값 in argumentti_MATRIISI], cwd=str(aloite_juuri))


def Suorita_2():
    kääntää_polku.mkdir(exist_ok=True)
    C_kääntäjä = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    linkitin_työkalu = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objekti_Tiedosto_muunnin = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arkisto_työkalu = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for työkalut in ('javac', C_kääntäjä, 시플플번역기, linkitin_työkalu, objekti_Tiedosto_muunnin, Arkisto_työkalu):
        if not shutil.which(työkalut):
            raise SystemExit('필요한 kääntää_Järjestelmä työkalut 없음: ' + työkalut)
    fontti_info = json.loads((aloite_juuri / 'vendor/terminal-font.json').read_text())
    fontti_data = (aloite_juuri / 'vendor/terminal-font.bin').read_bytes()
    if len(fontti_data) != 65616 * 32 or hashlib.sha256(fontti_data).hexdigest() != fontti_info['sha256']:
        raise SystemExit('komentotulkki fontti_ARVO Koko/SHA256 불일치')
    viedä_taulukko = {'jshell_interactive': '셸입출력.tietojärjestelmät_vuorovaikutteinen', 'jshell_output': '셸입출력.tulostuspaikka', 'jshell_input': '셸입출력.syöte_ARVO', 'java_task': 'ydin.작업', 'jfs_path_start': 'Muisti_Files.polku_alku',
               'jfs_path_byte': 'Muisti_Files.polku_tavu', 'jfs_open': 'Muisti_Files.Avaa',
               'jfs_read': 'Muisti_Files.Luku', 'jfs_write': 'Muisti_Files.Kirjoitus',
               'jfs_seek': 'Muisti_Files.hae_toimi', 'jfs_close': 'Muisti_Files.Sulje',
               'jfs_size': 'Muisti_Files.Koko', 'jfs_unlink': 'Muisti_Files.poistaa_merkintä_c8dbc399',
               'jfs_truncate': 'Muisti_Files.ryhmä_kesto'}
    viedä_taulukko.update({'jfs_entry_count': 'Muisti_Files.파일한도', 'jfs_entry_length': 'Muisti_Files.공개이름길이', 'jfs_entry_byte': 'Muisti_Files.공개이름바이트', 'jfs_entry_size': 'Muisti_Files.공개파일크기'})
    viedä_taulukko.update({'jdraw_prepare': '화면합성.Valmistele', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.leikata',
        'jdraw_clip_value': '화면합성.leikata_ARVO', 'jdraw_begin': '화면합성.Suorita_2',
        'jdraw_end': '화면합성.loppu', 'jdraw_pixel': '화면합성.kuvapiste',
        'jdraw_rectangle': '화면합성.suorakulmio_täyttö', 'jdraw_pointer': '화면합성.osoitin'})
    viedä_taulukko.update({'jfs_mkdir': 'Muisti_Files.Luo_Directory', 'jfs_rmdir': 'Muisti_Files.poistaa_Directory', 'jfs_kind': 'Muisti_Files.항목종류'})
    viedä_taulukko.update({'jnet_socket': 'silmukka_verkko.Luo_merkintä', 'jnet_bind': 'silmukka_verkko.BIND_päätepiste',
        'jnet_put': 'silmukka_verkko.자료넣기', 'jnet_get': 'silmukka_verkko.lukea_data', 'jnet_send': 'silmukka_verkko.lähettää',
        'jnet_recv': 'silmukka_verkko.saada', 'jnet_port': 'silmukka_verkko.lukea_päätepiste_portti', 'jnet_address': 'silmukka_verkko.lukea_OSOITE',
        'jnet_peer': 'silmukka_verkko.lähettäjä_päätepiste', 'jnet_close': 'silmukka_verkko.Sulje'})
    viedä_taulukko.update({'jstream_create': 'virta_verkko.Luo_merkintä', 'jstream_bind': 'virta_verkko.BIND_päätepiste', 'jstream_listen': 'virta_verkko.kuunnella_päätepiste', 'jstream_connect': 'virta_verkko.Yhdistä', 'jstream_accept': 'virta_verkko.hyväksyä_yhteys', 'jstream_read': 'virta_verkko.Luku', 'jstream_write': 'virta_verkko.Kirjoitus', 'jstream_port': 'virta_verkko.lukea_päätepiste_portti', 'jstream_peer': 'virta_verkko.lukea_vertaissolmu_portti', 'jstream_close': 'virta_verkko.Sulje'})
    for symboli_ARVO in list(viedä_taulukko):
        if symboli_ARVO.startswith('jstream_') or symboli_ARVO.startswith('jnet_') and symboli_ARVO not in ('jnet_put', 'jnet_get'):
            viedä_taulukko[symboli_ARVO.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = viedä_taulukko.pop(symboli_ARVO)
    예제들 = ['public final class nippu { public static void Valmistele() {']
    for polku_2 in sorted((aloite_juuri / '예제').iterdir()):
        if polku_2.is_file():
            예제들.append('명령해석기.staattinen_Tiedosto(%s, %s);' %
                (json.dumps(polku_2.name), json.dumps(polku_2.read_text(encoding='utf-8'), ensure_ascii=True)))
    (kääntää_polku / 'nippu.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(aloite_juuri, säilö_juuri, Suorita_komento)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(kääntää_polku)) as 작업경로:
        Luokka_polku = Path(작업경로)
        Suorita_komento(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Luokka_polku, '-sourcepath', Luokka_polku, '-d', Luokka_polku] + sorted((aloite_juuri / 'lähdetiedosto').glob('*.java')) + [kääntää_polku / 'nippu.java', kääntää_polku / '예제꾸러미.java'])
        # tiedoston_nimi·liittymä·Ikkuna 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argumentti_MATRIISI = ['sh', säilö_juuri / 'compiler/미리번역.sh', '--entry', 'ydin.Suorita_2', '--heap-words', '1048576', '-o', kääntää_polku / 'kernel-java.c']
        for symboli_ARVO, menetelmä_merkintä in sorted(viedä_taulukko.items()):
            argumentti_MATRIISI += ['--export', symboli_ARVO + '=' + menetelmä_merkintä]
        Suorita_komento(argumentti_MATRIISI + sorted(Luokka_polku.glob('*.class')))
    (kääntää_polku / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    määritys_Background_Intelligent_Transfer_Service = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = säilö_juuri / 'posix-kor/arm64-native'
    Luo_käyttäjä_tila(aloite_juuri, säilö_juuri, C_kääntäjä, 시플플번역기, linkitin_työkalu, Arkisto_työkalu, määritys_Background_Intelligent_Transfer_Service, Suorita_komento)
    verkko = Luo_verkko(aloite_juuri, C_kääntäjä, Arkisto_työkalu, määritys_Background_Intelligent_Transfer_Service, Suorita_komento)
    etä_käyttö = Luo_etä(aloite_juuri, C_kääntäjä, Arkisto_työkalu, määritys_Background_Intelligent_Transfer_Service, Suorita_komento)
    포함인수 = ['-I', 포직스경로 / 'esittelyt', '-I', kääntää_polku]
    빌드작업 = [(C_kääntäjä, [], kääntää_polku / 'terminal-font.S', 'font.o'),
            (C_kääntäjä, ['-std=c11', '-Wall', '-Wextra', '-Werror'], aloite_juuri / 'kone/komentotulkki.c', 'terminal.o'),
            (C_kääntäjä, ['-std=c11', '-Wall', '-Wextra', '-Werror'], aloite_juuri / 'kone/näyttöelementti.c', 'widgets.o'),
            (C_kääntäjä, ['-std=c11'], kääntää_polku / 'kernel-java.c', 'java.o'),
            (C_kääntäjä, ['-std=c11', '-Wall', '-Wextra', '-Werror'], aloite_juuri / 'kone/Taulu.c', 'board.o'),
            (C_kääntäjä, ['-std=c11', '-Wall', '-Wextra', '-Werror'], aloite_juuri / 'kone/화면그림.c', 'drawing.o'),
            (C_kääntäjä, ['-std=c11', '-Wall', '-Wextra', '-Werror'], aloite_juuri / 'kone/käyttäjätila.c', 'user.o'),
            (C_kääntäjä, [], aloite_juuri / 'koneen_käynnistys/aloituskohta_ARVO.S', 'entry.o'),
            (C_kääntäjä, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Yhdistä.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], aloite_juuri / 'testit/Tiedosto_Puhelut.cpp', 'cpp.o')]
    for kääntäjä_työkalu, 추가영역, 원본자료, tulos in 빌드작업:
        원본설정 = [Tiedosto_merkintä for Tiedosto_merkintä in määritys_Background_Intelligent_Transfer_Service if Tiedosto_merkintä != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else määritys_Background_Intelligent_Transfer_Service
        Suorita_komento([kääntäjä_työkalu] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', kääntää_polku / tulos])
    Suorita_komento([Arkisto_työkalu, 'rcs', kääntää_polku / 'libposix-kor-arm64.a', kääntää_polku / 'posix.o'])
    Suorita_komento([linkitin_työkalu, '--gc-sections', '-T', aloite_juuri / 'koneen_käynnistys/linkitysasettelu.ld', '-Map', kääntää_polku / 'kernel.map', '-o', kääntää_polku / 'kernel.elf'] +
        [kääntää_polku / Nimi for Nimi in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', kääntää_polku / 'libposix-kor-arm64.a', verkko, etä_käyttö, kääntää_polku / 'remote/libassh.a', kääntää_polku / 'remote/libbearssl.a', '--end-group'])
    Suorita_komento([objekti_Tiedosto_muunnin, '-O', 'binary', kääntää_polku / 'kernel.elf', kääntää_polku / 'kernel8.img'])
    nippu_kokoonpanotiedot = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'suomi.oma', 'korean_exceptions': 20,
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
    for Nimi in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        nippu_kokoonpanotiedot['sha256'][Nimi] = hashlib.sha256((kääntää_polku / Nimi).read_bytes()).hexdigest()
    (kääntää_polku / 'build.json').write_text(json.dumps(nippu_kokoonpanotiedot, indent=2) + '\n')
    print('완료:', kääntää_polku / 'kernel8.img')


if __name__ == '__main__':
    Suorita_2()
