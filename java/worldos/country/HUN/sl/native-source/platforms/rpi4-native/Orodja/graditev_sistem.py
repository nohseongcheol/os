#!/usr/bin/env python3
"""gostiti javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from graditev_uporabnik_Space import Ustvari_uporabnik_Space
from graditev_mreža import Ustvari_mreža
from 예제빌드 import 예제만들기
from graditev_oddaljen import Ustvari_oddaljen

pobuda_koren = Path(__file__).resolve().parents[1]
shramba_koren = pobuda_koren.parents[1]
graditev_pot = pobuda_koren / 'build'


def Izvedi_ukaz(argument_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in argument_ARRAY], cwd=str(pobuda_koren))


def Zaženi():
    graditev_pot.mkdir(exist_ok=True)
    C_prevajalnik = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    predmet_Datoteka_pretvornik = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arhiv_orodje = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Orodja in ('javac', C_prevajalnik, 시플플번역기, 연결편집기, predmet_Datoteka_pretvornik, Arhiv_orodje):
        if not shutil.which(Orodja):
            raise SystemExit('필요한 graditev_sistem Orodja 없음: ' + Orodja)
    pisava_informacije = json.loads((pobuda_koren / 'vendor/terminal-font.json').read_text())
    pisava_podatki = (pobuda_koren / 'vendor/terminal-font.bin').read_bytes()
    if len(pisava_podatki) != 65616 * 32 or hashlib.sha256(pisava_podatki).hexdigest() != pisava_informacije['sha256']:
        raise SystemExit('Terminal pisava_VALUE Velikost/SHA256 불일치')
    izvoziti_tabela = {'jshell_interactive': '셸입출력.informacijska_tehnologija_interaktiven', 'jshell_output': '셸입출력.Izpis', 'jshell_input': '셸입출력.입력', 'java_task': 'jedro.작업', 'jfs_path_start': 'pomnilnik_Datoteke.pot_Start',
               'jfs_path_byte': 'pomnilnik_Datoteke.pot_bajt', 'jfs_open': 'pomnilnik_Datoteke.Odpri',
               'jfs_read': 'pomnilnik_Datoteke.Branje', 'jfs_write': 'pomnilnik_Datoteke.Pisanje',
               'jfs_seek': 'pomnilnik_Datoteke.iskati_položaj', 'jfs_close': 'pomnilnik_Datoteke.Zapri',
               'jfs_size': 'pomnilnik_Datoteke.Velikost', 'jfs_unlink': 'pomnilnik_Datoteke.izbrisati_vnos',
               'jfs_truncate': 'pomnilnik_Datoteke.길이정하기'}
    izvoziti_tabela.update({'jfs_entry_count': 'pomnilnik_Datoteke.파일한도', 'jfs_entry_length': 'pomnilnik_Datoteke.공개이름길이', 'jfs_entry_byte': 'pomnilnik_Datoteke.공개이름바이트', 'jfs_entry_size': 'pomnilnik_Datoteke.공개파일크기'})
    izvoziti_tabela.update({'jdraw_prepare': '화면합성.Pripravi', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.dobiti_višina', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.izrezek',
        'jdraw_clip_value': '화면합성.izrezek_VALUE', 'jdraw_begin': '화면합성.Zaženi',
        'jdraw_end': '화면합성.konec', 'jdraw_pixel': '화면합성.slikovna_pika',
        'jdraw_rectangle': '화면합성.pravokotnik_polnilo', 'jdraw_pointer': '화면합성.kazalec'})
    izvoziti_tabela.update({'jfs_mkdir': 'pomnilnik_Datoteke.Ustvari_Imenik', 'jfs_rmdir': 'pomnilnik_Datoteke.odstraniti_Imenik', 'jfs_kind': 'pomnilnik_Datoteke.항목종류'})
    izvoziti_tabela.update({'jnet_socket': 'povratna_zanka_mreža.Ustvari_vnos', 'jnet_bind': 'povratna_zanka_mreža.BIND_končna_točka',
        'jnet_put': 'povratna_zanka_mreža.자료넣기', 'jnet_get': 'povratna_zanka_mreža.자료읽기', 'jnet_send': 'povratna_zanka_mreža.poslati',
        'jnet_recv': 'povratna_zanka_mreža.sprejeti_sprejemati_prejeti_prejemati', 'jnet_port': 'povratna_zanka_mreža.창구읽기', 'jnet_address': 'povratna_zanka_mreža.주소읽기',
        'jnet_peer': 'povratna_zanka_mreža.pošiljatelj_končna_točka', 'jnet_close': 'povratna_zanka_mreža.Zapri'})
    izvoziti_tabela.update({'jstream_create': 'tok_mreža.Ustvari_vnos', 'jstream_bind': 'tok_mreža.BIND_končna_točka', 'jstream_listen': 'tok_mreža.poslušati_končna_točka', 'jstream_connect': 'tok_mreža.Poveži', 'jstream_accept': 'tok_mreža.sprejeti_povezava', 'jstream_read': 'tok_mreža.Branje', 'jstream_write': 'tok_mreža.Pisanje', 'jstream_port': 'tok_mreža.창구읽기', 'jstream_peer': 'tok_mreža.상대창구읽기', 'jstream_close': 'tok_mreža.Zapri'})
    for simbol_VALUE in list(izvoziti_tabela):
        if simbol_VALUE.startswith('jstream_') or simbol_VALUE.startswith('jnet_') and simbol_VALUE not in ('jnet_put', 'jnet_get'):
            izvoziti_tabela[simbol_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = izvoziti_tabela.pop(simbol_VALUE)
    예제들 = ['public final class sveženj { public static void Pripravi() {']
    for POT in sorted((pobuda_koren / '예제').iterdir()):
        if POT.is_file():
            예제들.append('명령해석기.statičen_Datoteka(%s, %s);' %
                (json.dumps(POT.name), json.dumps(POT.read_text(encoding='utf-8'), ensure_ascii=True)))
    (graditev_pot / 'sveženj.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(pobuda_koren, shramba_koren, Izvedi_ukaz)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(graditev_pot)) as 작업경로:
        Razred_pot = Path(작업경로)
        Izvedi_ukaz(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Razred_pot, '-sourcepath', Razred_pot, '-d', Razred_pot] + sorted((pobuda_koren / 'VIR').glob('*.java')) + [graditev_pot / 'sveženj.java', graditev_pot / '예제꾸러미.java'])
        # Datoteka·lupina·okno 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argument_ARRAY = ['sh', shramba_koren / 'compiler/미리번역.sh', '--entry', 'jedro.Zaženi', '--heap-words', '1048576', '-o', graditev_pot / 'kernel-java.c']
        for simbol_VALUE, metoda_vnos in sorted(izvoziti_tabela.items()):
            argument_ARRAY += ['--export', simbol_VALUE + '=' + metoda_vnos]
        Izvedi_ukaz(argument_ARRAY + sorted(Razred_pot.glob('*.class')))
    (graditev_pot / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfiguracija_storitev_Background_Intelligent_Transfer_Service = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = shramba_koren / 'posix-kor/arm64-native'
    Ustvari_uporabnik_Space(pobuda_koren, shramba_koren, C_prevajalnik, 시플플번역기, 연결편집기, Arhiv_orodje, konfiguracija_storitev_Background_Intelligent_Transfer_Service, Izvedi_ukaz)
    mreža = Ustvari_mreža(pobuda_koren, C_prevajalnik, Arhiv_orodje, konfiguracija_storitev_Background_Intelligent_Transfer_Service, Izvedi_ukaz)
    oddaljen_uporaba = Ustvari_oddaljen(pobuda_koren, C_prevajalnik, Arhiv_orodje, konfiguracija_storitev_Background_Intelligent_Transfer_Service, Izvedi_ukaz)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', graditev_pot]
    빌드작업 = [(C_prevajalnik, [], graditev_pot / 'terminal-font.S', 'font.o'),
            (C_prevajalnik, ['-std=c11', '-Wall', '-Wextra', '-Werror'], pobuda_koren / 'računalnik/Terminal.c', 'terminal.o'),
            (C_prevajalnik, ['-std=c11', '-Wall', '-Wextra', '-Werror'], pobuda_koren / 'računalnik/pripomoček.c', 'widgets.o'),
            (C_prevajalnik, ['-std=c11'], graditev_pot / 'kernel-java.c', 'java.o'),
            (C_prevajalnik, ['-std=c11', '-Wall', '-Wextra', '-Werror'], pobuda_koren / 'računalnik/Tabla.c', 'board.o'),
            (C_prevajalnik, ['-std=c11', '-Wall', '-Wextra', '-Werror'], pobuda_koren / 'računalnik/화면그림.c', 'drawing.o'),
            (C_prevajalnik, ['-std=c11', '-Wall', '-Wextra', '-Werror'], pobuda_koren / 'računalnik/uporabnik.c', 'user.o'),
            (C_prevajalnik, [], pobuda_koren / '부팅/vnos_p_VALUE.S', 'entry.o'),
            (C_prevajalnik, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Poveži.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], pobuda_koren / '시험/Datoteka_Klici.cpp', 'cpp.o')]
    for prevajalnik_orodje, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [Datoteka_vnos for Datoteka_vnos in konfiguracija_storitev_Background_Intelligent_Transfer_Service if Datoteka_vnos != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else konfiguracija_storitev_Background_Intelligent_Transfer_Service
        Izvedi_ukaz([prevajalnik_orodje] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', graditev_pot / 출력결과])
    Izvedi_ukaz([Arhiv_orodje, 'rcs', graditev_pot / 'libposix-kor-arm64.a', graditev_pot / 'posix.o'])
    Izvedi_ukaz([연결편집기, '--gc-sections', '-T', pobuda_koren / '부팅/Povezava_Krmarjenje.ld', '-Map', graditev_pot / 'kernel.map', '-o', graditev_pot / 'kernel.elf'] +
        [graditev_pot / Ime for Ime in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', graditev_pot / 'libposix-kor-arm64.a', mreža, oddaljen_uporaba, graditev_pot / 'remote/libassh.a', graditev_pot / 'remote/libbearssl.a', '--end-group'])
    Izvedi_ukaz([predmet_Datoteka_pretvornik, '-O', 'binary', graditev_pot / 'kernel.elf', graditev_pot / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'slovenščina.lastno', 'korean_exceptions': 20,
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
        꾸러미명세['sha256'][Ime] = hashlib.sha256((graditev_pot / Ime).read_bytes()).hexdigest()
    (graditev_pot / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', graditev_pot / 'kernel8.img')


if __name__ == '__main__':
    Zaženi()
