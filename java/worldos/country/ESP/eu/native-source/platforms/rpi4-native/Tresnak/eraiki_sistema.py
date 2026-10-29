#!/usr/bin/env python3
"""Ostalari javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from eraiki_erabiltzaile_gune import sortu_erabiltzaile_gune
from eraiki_sare import sortu_sare
from 예제빌드 import 예제만들기
from eraiki_urruneko import sortu_urruneko

Project_erro = Path(__file__).resolve().parents[1]
biltegi_erro = Project_erro.parents[1]
eraiki_bide_izen = Project_erro / 'build'


def exekutatu_komando(arg_matrize):
    subprocess.check_call([str(첫째값) for 첫째값 in arg_matrize], cwd=str(Project_erro))


def Exekutatu_2():
    eraiki_bide_izen.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objektu_fitxategi_bihurgailu = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    artxibo_tresna = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Tresnak in ('javac', 시언어번역기, 시플플번역기, 연결편집기, objektu_fitxategi_bihurgailu, artxibo_tresna):
        if not shutil.which(Tresnak):
            raise SystemExit('필요한 eraiki_sistema Tresnak 없음: ' + Tresnak)
    letra_tipo_info = json.loads((Project_erro / 'vendor/terminal-font.json').read_text())
    letra_tipo_datuak = (Project_erro / 'vendor/terminal-font.bin').read_bytes()
    if len(letra_tipo_datuak) != 65616 * 32 or hashlib.sha256(letra_tipo_datuak).hexdigest() != letra_tipo_info['sha256']:
        raise SystemExit('Terminala letra_tipo_balio Tamaina/SHA256 불일치')
    esportatu_taula = {'jshell_interactive': '셸입출력.informatika_interaktibo', 'jshell_output': '셸입출력.Irteera', 'jshell_input': '셸입출력.입력', 'java_task': 'nukleo.작업', 'jfs_path_start': 'Memoria_Fitxategiak.bide_izen_HASI',
               'jfs_path_byte': 'Memoria_Fitxategiak.bide_izen_byte', 'jfs_open': 'Memoria_Fitxategiak.Ireki',
               'jfs_read': 'Memoria_Fitxategiak.Irakurri', 'jfs_write': 'Memoria_Fitxategiak.Idatzi',
               'jfs_seek': 'Memoria_Fitxategiak.bilatu_kargu', 'jfs_close': 'Memoria_Fitxategiak.Itxi',
               'jfs_size': 'Memoria_Fitxategiak.Tamaina', 'jfs_unlink': 'Memoria_Fitxategiak.ezabatu_sarrera',
               'jfs_truncate': 'Memoria_Fitxategiak.sorta_luzera'}
    esportatu_taula.update({'jfs_entry_count': 'Memoria_Fitxategiak.파일한도', 'jfs_entry_length': 'Memoria_Fitxategiak.공개이름길이', 'jfs_entry_byte': 'Memoria_Fitxategiak.공개이름바이트', 'jfs_entry_size': 'Memoria_Fitxategiak.공개파일크기'})
    esportatu_taula.update({'jdraw_prepare': '화면합성.준비', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.klip',
        'jdraw_clip_value': '화면합성.klip_balio', 'jdraw_begin': '화면합성.Exekutatu_2',
        'jdraw_end': '화면합성.Amaitu', 'jdraw_pixel': '화면합성.pixel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.erakusle'})
    esportatu_taula.update({'jfs_mkdir': 'Memoria_Fitxategiak.sortu_direktorio', 'jfs_rmdir': 'Memoria_Fitxategiak.kendu_direktorio', 'jfs_kind': 'Memoria_Fitxategiak.항목종류'})
    esportatu_taula.update({'jnet_socket': '되돌림망.sortu_sarrera', 'jnet_bind': '되돌림망.lotu_amaiera_puntu',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.bidali',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.bidaltzaile_amaiera_puntu', 'jnet_close': '되돌림망.Itxi'})
    esportatu_taula.update({'jstream_create': 'Stream_sare.sortu_sarrera', 'jstream_bind': 'Stream_sare.lotu_amaiera_puntu', 'jstream_listen': 'Stream_sare.entzun_amaiera_puntu', 'jstream_connect': 'Stream_sare.Konektatu', 'jstream_accept': 'Stream_sare.onartu_konexio', 'jstream_read': 'Stream_sare.Irakurri', 'jstream_write': 'Stream_sare.Idatzi', 'jstream_port': 'Stream_sare.창구읽기', 'jstream_peer': 'Stream_sare.상대창구읽기', 'jstream_close': 'Stream_sare.Itxi'})
    for ikur_balio in list(esportatu_taula):
        if ikur_balio.startswith('jstream_') or ikur_balio.startswith('jnet_') and ikur_balio not in ('jnet_put', 'jnet_get'):
            esportatu_taula[ikur_balio.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = esportatu_taula.pop(ikur_balio)
    예제들 = ['public final class multzo { public static void 준비() {']
    for Bide_izena in sorted((Project_erro / '예제').iterdir()):
        if Bide_izena.is_file():
            예제들.append('명령해석기.estatiko_fitxategi(%s, %s);' %
                (json.dumps(Bide_izena.name), json.dumps(Bide_izena.read_text(encoding='utf-8'), ensure_ascii=True)))
    (eraiki_bide_izen / 'multzo.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(Project_erro, biltegi_erro, exekutatu_komando)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(eraiki_bide_izen)) as 작업경로:
        Gela_bide_izen = Path(작업경로)
        exekutatu_komando(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Gela_bide_izen, '-sourcepath', Gela_bide_izen, '-d', Gela_bide_izen] + sorted((Project_erro / 'ITURBURUA').glob('*.java')) + [eraiki_bide_izen / 'multzo.java', eraiki_bide_izen / '예제꾸러미.java'])
        # Fitxategia·shell·Leihoa 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        arg_matrize = ['sh', biltegi_erro / 'compiler/미리번역.sh', '--entry', 'nukleo.Exekutatu_2', '--heap-words', '1048576', '-o', eraiki_bide_izen / 'kernel-java.c']
        for ikur_balio, 메소드 in sorted(esportatu_taula.items()):
            arg_matrize += ['--export', ikur_balio + '=' + 메소드]
        exekutatu_komando(arg_matrize + sorted(Gela_bide_izen.glob('*.class')))
    (eraiki_bide_izen / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = biltegi_erro / 'posix-kor/arm64-native'
    sortu_erabiltzaile_gune(Project_erro, biltegi_erro, 시언어번역기, 시플플번역기, 연결편집기, artxibo_tresna, konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna, exekutatu_komando)
    sare = sortu_sare(Project_erro, 시언어번역기, artxibo_tresna, konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna, exekutatu_komando)
    원격사용 = sortu_urruneko(Project_erro, 시언어번역기, artxibo_tresna, konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna, exekutatu_komando)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', eraiki_bide_izen]
    빌드작업 = [(시언어번역기, [], eraiki_bide_izen / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_erro / 'gailu/Terminala.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_erro / 'gailu/widget.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], eraiki_bide_izen / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_erro / 'gailu/arbel.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_erro / 'gailu/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], Project_erro / 'gailu/erabiltzaile.c', 'user.o'),
            (시언어번역기, [], Project_erro / '부팅/sarrera_p_balio.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Konektatu.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], Project_erro / '시험/fitxategi_Deiak.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [fitxategi_sarrera for fitxategi_sarrera in konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna if fitxategi_sarrera != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna
        exekutatu_komando([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', eraiki_bide_izen / 출력결과])
    exekutatu_komando([artxibo_tresna, 'rcs', eraiki_bide_izen / 'libposix-kor-arm64.a', eraiki_bide_izen / 'posix.o'])
    exekutatu_komando([연결편집기, '--gc-sections', '-T', Project_erro / '부팅/lotu_diseinu.ld', '-Map', eraiki_bide_izen / 'kernel.map', '-o', eraiki_bide_izen / 'kernel.elf'] +
        [eraiki_bide_izen / Izena for Izena in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', eraiki_bide_izen / 'libposix-kor-arm64.a', sare, 원격사용, eraiki_bide_izen / 'remote/libassh.a', eraiki_bide_izen / 'remote/libbearssl.a', '--end-group'])
    exekutatu_komando([objektu_fitxategi_bihurgailu, '-O', 'binary', eraiki_bide_izen / 'kernel.elf', eraiki_bide_izen / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Euskara.자체', 'korean_exceptions': 20,
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
    for Izena in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Izena] = hashlib.sha256((eraiki_bide_izen / Izena).read_bytes()).hexdigest()
    (eraiki_bide_izen / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', eraiki_bide_izen / 'kernel8.img')


if __name__ == '__main__':
    Exekutatu_2()
