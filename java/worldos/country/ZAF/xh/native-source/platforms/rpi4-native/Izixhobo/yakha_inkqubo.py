#!/usr/bin/env python3
"""umsingathi javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from yakha_umsebenzisi_isithuba import yila_umsebenzisi_isithuba
from yakha_Inethiwekhi import yila_Inethiwekhi
from 예제빌드 import 예제만들기
from yakha_kude import yila_kude

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
yakha_indlela = 기준 / 'build'


def ukwenza_umyalelo(isiniki_myalelo_ULUHLU):
    subprocess.check_call([str(첫째값) for 첫째값 in isiniki_myalelo_ULUHLU], cwd=str(기준))


def Phumeza():
    yakha_indlela.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    into_ifayile_isiguquli = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Uvimba_isixhobo_sokutayipha = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Izixhobo in ('javac', 시언어번역기, 시플플번역기, 연결편집기, into_ifayile_isiguquli, Uvimba_isixhobo_sokutayipha):
        if not shutil.which(Izixhobo):
            raise SystemExit('필요한 yakha_inkqubo Izixhobo 없음: ' + Izixhobo)
    ifonti_ingcaciso = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    ifonti_iingcombolo = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(ifonti_iingcombolo) != 65616 * 32 or hashlib.sha256(ifonti_iingcombolo).hexdigest() != ifonti_ingcaciso['sha256']:
        raise SystemExit('i_Terminal ifonti_ixabiso Ubukhulu/SHA256 불일치')
    thumela_ngaphandle_itheyibhile = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'ikheneli.작업', 'jfs_path_start': 'imemori_Iifayile.indlela_qala',
               'jfs_path_byte': 'imemori_Iifayile.indlela_ibhayithi', 'jfs_open': 'imemori_Iifayile.Vula',
               'jfs_read': 'imemori_Iifayile.Funda', 'jfs_write': 'imemori_Iifayile.Bhala',
               'jfs_seek': 'imemori_Iifayile.옮기기', 'jfs_close': 'imemori_Iifayile.Vala',
               'jfs_size': 'imemori_Iifayile.Ubukhulu', 'jfs_unlink': 'imemori_Iifayile.지우기',
               'jfs_truncate': 'imemori_Iifayile.isethi_ubude'}
    thumela_ngaphandle_itheyibhile.update({'jfs_entry_count': 'imemori_Iifayile.파일한도', 'jfs_entry_length': 'imemori_Iifayile.공개이름길이', 'jfs_entry_byte': 'imemori_Iifayile.공개이름바이트', 'jfs_entry_size': 'imemori_Iifayile.공개파일크기'})
    thumela_ngaphandle_itheyibhile.update({'jdraw_prepare': '화면합성.lungisa', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.ikliphu',
        'jdraw_clip_value': '화면합성.ikliphu_ixabiso', 'jdraw_begin': '화면합성.Phumeza',
        'jdraw_end': '화면합성.Gqiba', 'jdraw_pixel': '화면합성.i_pel',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.isalathisi'})
    thumela_ngaphandle_itheyibhile.update({'jfs_mkdir': 'imemori_Iifayile.yila_isalathisi', 'jfs_rmdir': 'imemori_Iifayile.shenxisa_isalathisi', 'jfs_kind': 'imemori_Iifayile.항목종류'})
    thumela_ngaphandle_itheyibhile.update({'jnet_socket': '되돌림망.yila_ufako_nkcukacha', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.thumela',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Vala'})
    thumela_ngaphandle_itheyibhile.update({'jstream_create': 'Stream_Inethiwekhi.yila_ufako_nkcukacha', 'jstream_bind': 'Stream_Inethiwekhi.묶기', 'jstream_listen': 'Stream_Inethiwekhi.듣기', 'jstream_connect': 'Stream_Inethiwekhi.Nxulumanisa', 'jstream_accept': 'Stream_Inethiwekhi.yamkela_uqhagamshelo', 'jstream_read': 'Stream_Inethiwekhi.Funda', 'jstream_write': 'Stream_Inethiwekhi.Bhala', 'jstream_port': 'Stream_Inethiwekhi.창구읽기', 'jstream_peer': 'Stream_Inethiwekhi.상대창구읽기', 'jstream_close': 'Stream_Inethiwekhi.Vala'})
    for isimboli_ixabiso in list(thumela_ngaphandle_itheyibhile):
        if isimboli_ixabiso.startswith('jstream_') or isimboli_ixabiso.startswith('jnet_') and isimboli_ixabiso not in ('jnet_put', 'jnet_get'):
            thumela_ngaphandle_itheyibhile[isimboli_ixabiso.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = thumela_ngaphandle_itheyibhile.pop(isimboli_ixabiso)
    예제들 = ['public final class umqulu { public static void lungisa() {']
    for INDLELA in sorted((기준 / '예제').iterdir()):
        if INDLELA.is_file():
            예제들.append('명령해석기.imi_ndawonye_ifayile(%s, %s);' %
                (json.dumps(INDLELA.name), json.dumps(INDLELA.read_text(encoding='utf-8'), ensure_ascii=True)))
    (yakha_indlela / 'umqulu.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, ukwenza_umyalelo)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(yakha_indlela)) as 작업경로:
        iklasi_indlela = Path(작업경로)
        ukwenza_umyalelo(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', iklasi_indlela, '-sourcepath', iklasi_indlela, '-d', iklasi_indlela] + sorted((기준 / 'UMTHOMBO').glob('*.java')) + [yakha_indlela / 'umqulu.java', yakha_indlela / '예제꾸러미.java'])
        # iFayili·isiniki_myalelo·i_window 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        isiniki_myalelo_ULUHLU = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'ikheneli.Phumeza', '--heap-words', '1048576', '-o', yakha_indlela / 'kernel-java.c']
        for isimboli_ixabiso, imethodi_ufako_nkcukacha in sorted(thumela_ngaphandle_itheyibhile.items()):
            isiniki_myalelo_ULUHLU += ['--export', isimboli_ixabiso + '=' + imethodi_ufako_nkcukacha]
        ukwenza_umyalelo(isiniki_myalelo_ULUHLU + sorted(iklasi_indlela.glob('*.class')))
    (yakha_indlela / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    yila_umsebenzisi_isithuba(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, Uvimba_isixhobo_sokutayipha, 설정비트, ukwenza_umyalelo)
    Inethiwekhi = yila_Inethiwekhi(기준, 시언어번역기, Uvimba_isixhobo_sokutayipha, 설정비트, ukwenza_umyalelo)
    원격사용 = yila_kude(기준, 시언어번역기, Uvimba_isixhobo_sokutayipha, 설정비트, ukwenza_umyalelo)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', yakha_indlela]
    빌드작업 = [(시언어번역기, [], yakha_indlela / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'umatshini/i_Terminal.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'umatshini/iwijethi.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], yakha_indlela / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'umatshini/보드.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'umatshini/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'umatshini/umsebenzisi.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/ufako_nkcukacha_inqaku_ixabiso.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Nxulumanisa.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/파일호출.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ifayile_ufako_nkcukacha for ifayile_ufako_nkcukacha in 설정비트 if ifayile_ufako_nkcukacha != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        ukwenza_umyalelo([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', yakha_indlela / 출력결과])
    ukwenza_umyalelo([Uvimba_isixhobo_sokutayipha, 'rcs', yakha_indlela / 'libposix-kor-arm64.a', yakha_indlela / 'posix.o'])
    ukwenza_umyalelo([연결편집기, '--gc-sections', '-T', 기준 / '부팅/Ilinki_ubume.ld', '-Map', yakha_indlela / 'kernel.map', '-o', yakha_indlela / 'kernel.elf'] +
        [yakha_indlela / Igama for Igama in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', yakha_indlela / 'libposix-kor-arm64.a', Inethiwekhi, 원격사용, yakha_indlela / 'remote/libassh.a', yakha_indlela / 'remote/libbearssl.a', '--end-group'])
    ukwenza_umyalelo([into_ifayile_isiguquli, '-O', 'binary', yakha_indlela / 'kernel.elf', yakha_indlela / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'isiXhosa.자체', 'korean_exceptions': 20,
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
    for Igama in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Igama] = hashlib.sha256((yakha_indlela / Igama).read_bytes()).hexdigest()
    (yakha_indlela / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', yakha_indlela / 'kernel8.img')


if __name__ == '__main__':
    Phumeza()
