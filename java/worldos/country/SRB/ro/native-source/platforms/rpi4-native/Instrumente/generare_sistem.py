#!/usr/bin/env python3
"""gazdă javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from generare_utilizator_SPAȚIU import crea_utilizator_SPAȚIU
from generare_rețea import crea_rețea_48d29d6d
from 예제빌드 import 예제만들기
from generare_la_distanță import crea_la_distanță

Project_rădăcină = Path(__file__).resolve().parents[1]
depozit_rădăcină = Project_rădăcină.parents[1]
generare_cale = Project_rădăcină / 'build'


def executa_comandă(argument_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in argument_ARRAY], cwd=str(Project_rădăcină))


def Pornește():
    generare_cale.mkdir(exist_ok=True)
    C_compilator = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    obiect_Fișier_convertor = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arhivă_instrument = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Instrumente in ('javac', C_compilator, 시플플번역기, 연결편집기, obiect_Fișier_convertor, Arhivă_instrument):
        if not shutil.which(Instrumente):
            raise SystemExit('필요한 generare_sistem Instrumente 없음: ' + Instrumente)
    font_info = json.loads((Project_rădăcină / 'vendor/terminal-font.json').read_text())
    font_date = (Project_rădăcină / 'vendor/terminal-font.bin').read_bytes()
    if len(font_date) != 65616 * 32 or hashlib.sha256(font_date).hexdigest() != font_info['sha256']:
        raise SystemExit('Terminal font_VALUE Mărime/SHA256 불일치')
    exporta_tabel = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.Rezultat', 'jshell_input': '셸입출력.입력', 'java_task': 'nucleu.작업', 'jfs_path_start': 'Memorie_Fișiere.cale_buta',
               'jfs_path_byte': 'Memorie_Fișiere.cale_byte', 'jfs_open': 'Memorie_Fișiere.Deschide',
               'jfs_read': 'Memorie_Fișiere.Citire', 'jfs_write': 'Memorie_Fișiere.Scriere',
               'jfs_seek': 'Memorie_Fișiere.căuta_poziție', 'jfs_close': 'Memorie_Fișiere.Închide',
               'jfs_size': 'Memorie_Fișiere.Mărime', 'jfs_unlink': 'Memorie_Fișiere.șterge_intrare',
               'jfs_truncate': 'Memorie_Fișiere.set_lungime'}
    exporta_tabel.update({'jfs_entry_count': 'Memorie_Fișiere.파일한도', 'jfs_entry_length': 'Memorie_Fișiere.공개이름길이', 'jfs_entry_byte': 'Memorie_Fișiere.공개이름바이트', 'jfs_entry_size': 'Memorie_Fișiere.공개파일크기'})
    exporta_tabel.update({'jdraw_prepare': '화면합성.Pregătiți', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.clip',
        'jdraw_clip_value': '화면합성.clip_VALUE', 'jdraw_begin': '화면합성.Pornește',
        'jdraw_end': '화면합성.sfârșit', 'jdraw_pixel': '화면합성.element_imagine',
        'jdraw_rectangle': '화면합성.dreptunghi_umple', 'jdraw_pointer': '화면합성.cursor'})
    exporta_tabel.update({'jfs_mkdir': 'Memorie_Fișiere.crea_Director', 'jfs_rmdir': 'Memorie_Fișiere.elimina_Director', 'jfs_kind': 'Memorie_Fișiere.항목종류'})
    exporta_tabel.update({'jnet_socket': 'cu_reacție_în_buclă_rețea.crea_intrare', 'jnet_bind': 'cu_reacție_în_buclă_rețea.BIND_participant',
        'jnet_put': 'cu_reacție_în_buclă_rețea.자료넣기', 'jnet_get': 'cu_reacție_în_buclă_rețea.자료읽기', 'jnet_send': 'cu_reacție_în_buclă_rețea.trimite',
        'jnet_recv': 'cu_reacție_în_buclă_rețea.primi', 'jnet_port': 'cu_reacție_în_buclă_rețea.창구읽기', 'jnet_address': 'cu_reacție_în_buclă_rețea.주소읽기',
        'jnet_peer': 'cu_reacție_în_buclă_rețea.expeditor_participant', 'jnet_close': 'cu_reacție_în_buclă_rețea.Închide'})
    exporta_tabel.update({'jstream_create': 'flux_rețea.crea_intrare', 'jstream_bind': 'flux_rețea.BIND_participant', 'jstream_listen': 'flux_rețea.asculta_participant', 'jstream_connect': 'flux_rețea.Conectează', 'jstream_accept': 'flux_rețea.accepta_conexiune', 'jstream_read': 'flux_rețea.Citire', 'jstream_write': 'flux_rețea.Scriere', 'jstream_port': 'flux_rețea.창구읽기', 'jstream_peer': 'flux_rețea.상대창구읽기', 'jstream_close': 'flux_rețea.Închide'})
    for simbol_VALUE in list(exporta_tabel):
        if simbol_VALUE.startswith('jstream_') or simbol_VALUE.startswith('jnet_') and simbol_VALUE not in ('jnet_put', 'jnet_get'):
            exporta_tabel[simbol_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = exporta_tabel.pop(simbol_VALUE)
    예제들 = ['public final class set { public static void Pregătiți() {']
    for Cale in sorted((Project_rădăcină / '예제').iterdir()):
        if Cale.is_file():
            예제들.append('명령해석기.정적파일(%s, %s);' %
                (json.dumps(Cale.name), json.dumps(Cale.read_text(encoding='utf-8'), ensure_ascii=True)))
    (generare_cale / 'set.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Project_rădăcină, depozit_rădăcină, executa_comandă)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(generare_cale)) as 작업경로:
        Clasă_cale = Path(작업경로)
        executa_comandă(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Clasă_cale, '-sourcepath', Clasă_cale, '-d', Clasă_cale] + sorted((Project_rădăcină / 'SURSĂ').glob('*.java')) + [generare_cale / 'set.java', generare_cale / '예제꾸러미.java'])
        # Fișier·shell·Fereastră 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argument_ARRAY = ['sh', depozit_rădăcină / 'compiler/미리번역.sh', '--entry', 'nucleu.Pornește', '--heap-words', '1048576', '-o', generare_cale / 'kernel-java.c']
        for simbol_VALUE, metodă_intrare in sorted(exporta_tabel.items()):
            argument_ARRAY += ['--export', simbol_VALUE + '=' + metodă_intrare]
        executa_comandă(argument_ARRAY + sorted(Clasă_cale.glob('*.class')))
    (generare_cale / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    configurație_Serviciu_de_transfer_inteligent_în_fundal = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = depozit_rădăcină / 'posix-kor/arm64-native'
    crea_utilizator_SPAȚIU(Project_rădăcină, depozit_rădăcină, C_compilator, 시플플번역기, 연결편집기, Arhivă_instrument, configurație_Serviciu_de_transfer_inteligent_în_fundal, executa_comandă)
    rețea = crea_rețea_48d29d6d(Project_rădăcină, C_compilator, Arhivă_instrument, configurație_Serviciu_de_transfer_inteligent_în_fundal, executa_comandă)
    la_distanță_utiliza = crea_la_distanță(Project_rădăcină, C_compilator, Arhivă_instrument, configurație_Serviciu_de_transfer_inteligent_în_fundal, executa_comandă)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', generare_cale]
    빌드작업 = [(C_compilator, [], generare_cale / 'terminal-font.S', 'font.o'),
            (C_compilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_rădăcină / 'mașină/Terminal.c', 'terminal.o'),
            (C_compilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_rădăcină / 'mașină/widget.c', 'widgets.o'),
            (C_compilator, ['-std=c11'], generare_cale / 'kernel-java.c', 'java.o'),
            (C_compilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_rădăcină / 'mașină/Avizier.c', 'board.o'),
            (C_compilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_rădăcină / 'mașină/화면그림.c', 'drawing.o'),
            (C_compilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_rădăcină / 'mașină/utilizator.c', 'user.o'),
            (C_compilator, [], Project_rădăcină / '부팅/intrare_p_VALUE.S', 'entry.o'),
            (C_compilator, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Conectează.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Project_rădăcină / '시험/Fișier_Apeluri.cpp', 'cpp.o')]
    for compilator_instrument, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [Fișier_intrare for Fișier_intrare in configurație_Serviciu_de_transfer_inteligent_în_fundal if Fișier_intrare != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else configurație_Serviciu_de_transfer_inteligent_în_fundal
        executa_comandă([compilator_instrument] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', generare_cale / 출력결과])
    executa_comandă([Arhivă_instrument, 'rcs', generare_cale / 'libposix-kor-arm64.a', generare_cale / 'posix.o'])
    executa_comandă([연결편집기, '--gc-sections', '-T', Project_rădăcină / '부팅/Link_Aspect.ld', '-Map', generare_cale / 'kernel.map', '-o', generare_cale / 'kernel.elf'] +
        [generare_cale / Nume for Nume in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', generare_cale / 'libposix-kor-arm64.a', rețea, la_distanță_utiliza, generare_cale / 'remote/libassh.a', generare_cale / 'remote/libbearssl.a', '--end-group'])
    executa_comandă([obiect_Fișier_convertor, '-O', 'binary', generare_cale / 'kernel.elf', generare_cale / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Română.propriu', 'korean_exceptions': 20,
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
    for Nume in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Nume] = hashlib.sha256((generare_cale / Nume).read_bytes()).hexdigest()
    (generare_cale / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', generare_cale / 'kernel8.img')


if __name__ == '__main__':
    Pornește()
