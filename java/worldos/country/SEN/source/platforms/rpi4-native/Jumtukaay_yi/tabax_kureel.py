#!/usr/bin/env python3
"""dalal javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from tabax_kiy_jariñoo_internet_Espace import sos_kiy_jariñoo_internet_Espace
from tabax_mbaal import sos_mbaal_48d29d6d
from 예제빌드 import 예제만들기
from tabax_lu_soree import sos_lu_soree

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
tabax_Yoonu_jëmale = 기준 / 'build'


def def_ndigel(Tegtal_TABLO):
    subprocess.check_call([str(첫째값) for 첫째값 in Tegtal_TABLO], cwd=str(기준))


def daw():
    tabax_Yoonu_jëmale.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    yëf_bara_denc_soppikaay = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    denc_jumtukaay = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Jumtukaay_yi in ('javac', 시언어번역기, 시플플번역기, 연결편집기, yëf_bara_denc_soppikaay, denc_jumtukaay):
        if not shutil.which(Jumtukaay_yi):
            raise SystemExit('필요한 tabax_kureel Jumtukaay_yi 없음: ' + Jumtukaay_yi)
    mbindin_yëglë = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    mbindin_mbir = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(mbindin_mbir) != 65616 * 32 or hashlib.sha256(mbindin_mbir).hexdigest() != mbindin_yëglë['sha256']:
        raise SystemExit('터미널 mbindin_xëyma tolluwaay/SHA256 불일치')
    toxal_àlluwa = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'xoox.작업', 'jfs_path_start': 'fatlekookaay_Fisiye_yi.Yoonu_jëmale_Door',
               'jfs_path_byte': 'fatlekookaay_Fisiye_yi.Yoonu_jëmale_okte', 'jfs_open': 'fatlekookaay_Fisiye_yi.sos',
               'jfs_read': 'fatlekookaay_Fisiye_yi.읽기', 'jfs_write': 'fatlekookaay_Fisiye_yi.biir',
               'jfs_seek': 'fatlekookaay_Fisiye_yi.옮기기', 'jfs_close': 'fatlekookaay_Fisiye_yi.Tej',
               'jfs_size': 'fatlekookaay_Fisiye_yi.tolluwaay', 'jfs_unlink': 'fatlekookaay_Fisiye_yi.지우기',
               'jfs_truncate': 'fatlekookaay_Fisiye_yi.Boole_gi_diir'}
    toxal_àlluwa.update({'jfs_entry_count': 'fatlekookaay_Fisiye_yi.파일한도', 'jfs_entry_length': 'fatlekookaay_Fisiye_yi.공개이름길이', 'jfs_entry_byte': 'fatlekookaay_Fisiye_yi.공개이름바이트', 'jfs_entry_size': 'fatlekookaay_Fisiye_yi.공개파일크기'})
    toxal_àlluwa.update({'jdraw_prepare': '화면합성.jël_matuwaay', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.kilip',
        'jdraw_clip_value': '화면합성.kilip_xëyma', 'jdraw_begin': '화면합성.daw',
        'jdraw_end': '화면합성.Sottal', 'jdraw_pixel': '화면합성.piksel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.joxañukaay'})
    toxal_àlluwa.update({'jfs_mkdir': 'fatlekookaay_Fisiye_yi.sos_dàmb', 'jfs_rmdir': 'fatlekookaay_Fisiye_yi.dandal_dàmb', 'jfs_kind': 'fatlekookaay_Fisiye_yi.항목종류'})
    toxal_àlluwa.update({'jnet_socket': '되돌림망.sos_dugal_xabaar', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.Yónnee',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Tej'})
    toxal_àlluwa.update({'jstream_create': 'dawal_mbaal.sos_dugal_xabaar', 'jstream_bind': 'dawal_mbaal.묶기', 'jstream_listen': 'dawal_mbaal.듣기', 'jstream_connect': 'dawal_mbaal.JOKKOO', 'jstream_accept': 'dawal_mbaal.nangu_jokkalóo', 'jstream_read': 'dawal_mbaal.읽기', 'jstream_write': 'dawal_mbaal.biir', 'jstream_port': 'dawal_mbaal.창구읽기', 'jstream_peer': 'dawal_mbaal.상대창구읽기', 'jstream_close': 'dawal_mbaal.Tej'})
    for sembóol_xëyma in list(toxal_àlluwa):
        if sembóol_xëyma.startswith('jstream_') or sembóol_xëyma.startswith('jnet_') and sembóol_xëyma not in ('jnet_put', 'jnet_get'):
            toxal_àlluwa[sembóol_xëyma.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = toxal_àlluwa.pop(sembóol_xëyma)
    예제들 = ['public final class takku_xéewël { public static void jël_matuwaay() {']
    for Yoonu_jëmale in sorted((기준 / '예제').iterdir()):
        if Yoonu_jëmale.is_file():
            예제들.append('명령해석기.Soppeekoodi_bara_denc(%s, %s);' %
                (json.dumps(Yoonu_jëmale.name), json.dumps(Yoonu_jëmale.read_text(encoding='utf-8'), ensure_ascii=True)))
    (tabax_Yoonu_jëmale / 'takku_xéewël.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, def_ndigel)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(tabax_Yoonu_jëmale)) as 작업경로:
        maas_Yoonu_jëmale = Path(작업경로)
        def_ndigel(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', maas_Yoonu_jëmale, '-sourcepath', maas_Yoonu_jëmale, '-d', maas_Yoonu_jëmale] + sorted((기준 / 'Cosaan').glob('*.java')) + [tabax_Yoonu_jëmale / 'takku_xéewël.java', tabax_Yoonu_jëmale / '예제꾸러미.java'])
        # bara_denc·Wëreef·palanteer 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        Tegtal_TABLO = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'xoox.daw', '--heap-words', '1048576', '-o', tabax_Yoonu_jëmale / 'kernel-java.c']
        for sembóol_xëyma, doxalin_dugal_xabaar in sorted(toxal_àlluwa.items()):
            Tegtal_TABLO += ['--export', sembóol_xëyma + '=' + doxalin_dugal_xabaar]
        def_ndigel(Tegtal_TABLO + sorted(maas_Yoonu_jëmale.glob('*.class')))
    (tabax_Yoonu_jëmale / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    sos_kiy_jariñoo_internet_Espace(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, denc_jumtukaay, 설정비트, def_ndigel)
    mbaal = sos_mbaal_48d29d6d(기준, 시언어번역기, denc_jumtukaay, 설정비트, def_ndigel)
    원격사용 = sos_lu_soree(기준, 시언어번역기, denc_jumtukaay, 설정비트, def_ndigel)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', tabax_Yoonu_jëmale]
    빌드작업 = [(시언어번역기, [], tabax_Yoonu_jëmale / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'masin/터미널.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'masin/kifin.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], tabax_Yoonu_jëmale / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'masin/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'masin/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'masin/kiy_jariñoo_internet.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/dugal_xabaar_Tomb_xëyma.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'JOKKOO.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [bara_denc_dugal_xabaar for bara_denc_dugal_xabaar in 설정비트 if bara_denc_dugal_xabaar != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        def_ndigel([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', tabax_Yoonu_jëmale / 출력결과])
    def_ndigel([denc_jumtukaay, 'rcs', tabax_Yoonu_jëmale / 'libposix-kor-arm64.a', tabax_Yoonu_jëmale / 'posix.o'])
    def_ndigel([연결편집기, '--gc-sections', '-T', 기준 / '부팅/lëkkale_Tëralin.ld', '-Map', tabax_Yoonu_jëmale / 'kernel.map', '-o', tabax_Yoonu_jëmale / 'kernel.elf'] +
        [tabax_Yoonu_jëmale / tur_253d1510 for tur_253d1510 in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', tabax_Yoonu_jëmale / 'libposix-kor-arm64.a', mbaal, 원격사용, tabax_Yoonu_jëmale / 'remote/libassh.a', tabax_Yoonu_jëmale / 'remote/libbearssl.a', '--end-group'])
    def_ndigel([yëf_bara_denc_soppikaay, '-O', 'binary', tabax_Yoonu_jëmale / 'kernel.elf', tabax_Yoonu_jëmale / 'kernel8.img'])
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
    for tur_253d1510 in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][tur_253d1510] = hashlib.sha256((tabax_Yoonu_jëmale / tur_253d1510).read_bytes()).hexdigest()
    (tabax_Yoonu_jëmale / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', tabax_Yoonu_jëmale / 'kernel8.img')


if __name__ == '__main__':
    daw()
