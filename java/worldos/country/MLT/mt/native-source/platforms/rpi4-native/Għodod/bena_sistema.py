#!/usr/bin/env python3
"""host javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from bena_utent_SPACE import ħalaq_utent_SPACE
from bena_netwerk import ħalaq_netwerk
from 예제빌드 import 예제만들기
from bena_mill_bogħod import ħalaq_mill_bogħod

pprojetta_għerq = Path(__file__).resolve().parents[1]
저장소 = pprojetta_għerq.parents[1]
bena_mogħdija = pprojetta_għerq / 'build'


def eżegwixxa_kmand(argument_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in argument_ARRAY], cwd=str(pprojetta_għerq))


def serje():
    bena_mogħdija.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    oġġett_fajl_konverter = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Arkivju_għodda = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Għodod in ('javac', 시언어번역기, 시플플번역기, 연결편집기, oġġett_fajl_konverter, Arkivju_għodda):
        if not shutil.which(Għodod):
            raise SystemExit('필요한 bena_sistema Għodod 없음: ' + Għodod)
    font_informazzjoni = json.loads((pprojetta_għerq / 'vendor/terminal-font.json').read_text())
    font_data = (pprojetta_għerq / 'vendor/terminal-font.bin').read_bytes()
    if len(font_data) != 65616 * 32 or hashlib.sha256(font_data).hexdigest() != font_informazzjoni['sha256']:
        raise SystemExit('Terminal font_VALUE daqqas/SHA256 불일치')
    esporta_tabella = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'kernel.작업', 'jfs_path_start': 'Memorja_Fajls.mogħdija_Bidu',
               'jfs_path_byte': 'Memorja_Fajls.mogħdija_byte', 'jfs_open': 'Memorja_Fajls.fetaħ',
               'jfs_read': 'Memorja_Fajls.읽기', 'jfs_write': 'Memorja_Fajls.kiteb',
               'jfs_seek': 'Memorja_Fajls.fittex_pożizzjoni', 'jfs_close': 'Memorja_Fajls.agħlaq',
               'jfs_size': 'Memorja_Fajls.daqqas', 'jfs_unlink': 'Memorja_Fajls.지우기',
               'jfs_truncate': 'Memorja_Fajls.sett_tul'}
    esporta_tabella.update({'jfs_entry_count': 'Memorja_Fajls.파일한도', 'jfs_entry_length': 'Memorja_Fajls.공개이름길이', 'jfs_entry_byte': 'Memorja_Fajls.공개이름바이트', 'jfs_entry_size': 'Memorja_Fajls.공개파일크기'})
    esporta_tabella.update({'jdraw_prepare': '화면합성.Ħejji', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.klipp',
        'jdraw_clip_value': '화면합성.klipp_VALUE', 'jdraw_begin': '화면합성.serje',
        'jdraw_end': '화면합성.Tmiem', 'jdraw_pixel': '화면합성.pel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.pointer'})
    esporta_tabella.update({'jfs_mkdir': 'Memorja_Fajls.ħalaq_direttorju', 'jfs_rmdir': 'Memorja_Fajls.neħħa_direttorju', 'jfs_kind': 'Memorja_Fajls.항목종류'})
    esporta_tabella.update({'jnet_socket': '되돌림망.ħalaq_entrata', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.bagħat',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.agħlaq'})
    esporta_tabella.update({'jstream_create': 'Stream_netwerk.ħalaq_entrata', 'jstream_bind': 'Stream_netwerk.묶기', 'jstream_listen': 'Stream_netwerk.듣기', 'jstream_connect': 'Stream_netwerk.AQBAD', 'jstream_accept': 'Stream_netwerk.aċċetta_konnessjoni', 'jstream_read': 'Stream_netwerk.읽기', 'jstream_write': 'Stream_netwerk.kiteb', 'jstream_port': 'Stream_netwerk.창구읽기', 'jstream_peer': 'Stream_netwerk.상대창구읽기', 'jstream_close': 'Stream_netwerk.agħlaq'})
    for simbolu_VALUE in list(esporta_tabella):
        if simbolu_VALUE.startswith('jstream_') or simbolu_VALUE.startswith('jnet_') and simbolu_VALUE not in ('jnet_put', 'jnet_get'):
            esporta_tabella[simbolu_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = esporta_tabella.pop(simbolu_VALUE)
    예제들 = ['public final class lott { public static void Ħejji() {']
    for mogħdija in sorted((pprojetta_għerq / '예제').iterdir()):
        if mogħdija.is_file():
            예제들.append('명령해석기.statiku_fajl(%s, %s);' %
                (json.dumps(mogħdija.name), json.dumps(mogħdija.read_text(encoding='utf-8'), ensure_ascii=True)))
    (bena_mogħdija / 'lott.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(pprojetta_għerq, 저장소, eżegwixxa_kmand)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(bena_mogħdija)) as 작업경로:
        klassi_mogħdija = Path(작업경로)
        eżegwixxa_kmand(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klassi_mogħdija, '-sourcepath', klassi_mogħdija, '-d', klassi_mogħdija] + sorted((pprojetta_għerq / 'sors').glob('*.java')) + [bena_mogħdija / 'lott.java', bena_mogħdija / '예제꾸러미.java'])
        # fajl·shell·tieqa 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argument_ARRAY = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'kernel.serje', '--heap-words', '1048576', '-o', bena_mogħdija / 'kernel-java.c']
        for simbolu_VALUE, metodu_entrata in sorted(esporta_tabella.items()):
            argument_ARRAY += ['--export', simbolu_VALUE + '=' + metodu_entrata]
        eżegwixxa_kmand(argument_ARRAY + sorted(klassi_mogħdija.glob('*.class')))
    (bena_mogħdija / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    ħalaq_utent_SPACE(pprojetta_għerq, 저장소, 시언어번역기, 시플플번역기, 연결편집기, Arkivju_għodda, 설정비트, eżegwixxa_kmand)
    netwerk = ħalaq_netwerk(pprojetta_għerq, 시언어번역기, Arkivju_għodda, 설정비트, eżegwixxa_kmand)
    원격사용 = ħalaq_mill_bogħod(pprojetta_għerq, 시언어번역기, Arkivju_għodda, 설정비트, eżegwixxa_kmand)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', bena_mogħdija]
    빌드작업 = [(시언어번역기, [], bena_mogħdija / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], pprojetta_għerq / 'kompjuter/Terminal.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], pprojetta_għerq / 'kompjuter/widget.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], bena_mogħdija / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], pprojetta_għerq / 'kompjuter/bord.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], pprojetta_għerq / 'kompjuter/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], pprojetta_għerq / 'kompjuter/utent.c', 'user.o'),
            (시언어번역기, [], pprojetta_għerq / '부팅/entrata_punt_VALUE.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'AQBAD.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], pprojetta_għerq / '시험/fajl_Telefonati.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [fajl_entrata for fajl_entrata in 설정비트 if fajl_entrata != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        eżegwixxa_kmand([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', bena_mogħdija / 출력결과])
    eżegwixxa_kmand([Arkivju_għodda, 'rcs', bena_mogħdija / 'libposix-kor-arm64.a', bena_mogħdija / 'posix.o'])
    eżegwixxa_kmand([연결편집기, '--gc-sections', '-T', pprojetta_għerq / '부팅/Link_Tqassim.ld', '-Map', bena_mogħdija / 'kernel.map', '-o', bena_mogħdija / 'kernel.elf'] +
        [bena_mogħdija / isem for isem in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', bena_mogħdija / 'libposix-kor-arm64.a', netwerk, 원격사용, bena_mogħdija / 'remote/libassh.a', bena_mogħdija / 'remote/libbearssl.a', '--end-group'])
    eżegwixxa_kmand([oġġett_fajl_konverter, '-O', 'binary', bena_mogħdija / 'kernel.elf', bena_mogħdija / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Malti.자체', 'korean_exceptions': 20,
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
    for isem in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][isem] = hashlib.sha256((bena_mogħdija / isem).read_bytes()).hexdigest()
    (bena_mogħdija / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', bena_mogħdija / 'kernel8.img')


if __name__ == '__main__':
    serje()
