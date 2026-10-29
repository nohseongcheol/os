#!/usr/bin/env python3
"""óstach javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from tóg_úsáideoir_spás import Create_úsáideoir_spás
from tóg_Líonra import Create_Líonra
from 예제빌드 import 예제만들기
from tóg_cianda import Create_cianda

teilgean_fréamh = Path(__file__).resolve().parents[1]
저장소 = teilgean_fréamh.parents[1]
tóg_cosán = teilgean_fréamh / 'build'


def Rith_ordú(argóint_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in argóint_ARRAY], cwd=str(teilgean_fréamh))


def Rith_2():
    tóg_cosán.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    oibiacht_comhad_tiontaire = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Cartlann_uirlis = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Uirlisí in ('javac', 시언어번역기, 시플플번역기, 연결편집기, oibiacht_comhad_tiontaire, Cartlann_uirlis):
        if not shutil.which(Uirlisí):
            raise SystemExit('필요한 tóg_córas Uirlisí 없음: ' + Uirlisí)
    clófhoireann_faisnéis = json.loads((teilgean_fréamh / 'vendor/terminal-font.json').read_text())
    clófhoireann_sonraí = (teilgean_fréamh / 'vendor/terminal-font.bin').read_bytes()
    if len(clófhoireann_sonraí) != 65616 * 32 or hashlib.sha256(clófhoireann_sonraí).hexdigest() != clófhoireann_faisnéis['sha256']:
        raise SystemExit('Teirminéal clófhoireann_VALUE Méid/SHA256 불일치')
    easportáil_tábla = {'jshell_interactive': '셸입출력.teicneolaíocht_faisnéise_idirghníomhach', 'jshell_output': '셸입출력.Aschur', 'jshell_input': '셸입출력.입력', 'java_task': 'eithne.작업', 'jfs_path_start': 'Cuimhne_Comhaid.cosán_Start',
               'jfs_path_byte': 'Cuimhne_Comhaid.cosán_beart', 'jfs_open': 'Cuimhne_Comhaid.Oscail',
               'jfs_read': 'Cuimhne_Comhaid.Léigh', 'jfs_write': 'Cuimhne_Comhaid.Scríobh',
               'jfs_seek': 'Cuimhne_Comhaid.lorg_suíomh', 'jfs_close': 'Cuimhne_Comhaid.Dún',
               'jfs_size': 'Cuimhne_Comhaid.Méid', 'jfs_unlink': 'Cuimhne_Comhaid.지우기',
               'jfs_truncate': 'Cuimhne_Comhaid.tacar_fad'}
    easportáil_tábla.update({'jfs_entry_count': 'Cuimhne_Comhaid.파일한도', 'jfs_entry_length': 'Cuimhne_Comhaid.공개이름길이', 'jfs_entry_byte': 'Cuimhne_Comhaid.공개이름바이트', 'jfs_entry_size': 'Cuimhne_Comhaid.공개파일크기'})
    easportáil_tábla.update({'jdraw_prepare': '화면합성.Ullmhaigh', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.gearrthóg',
        'jdraw_clip_value': '화면합성.gearrthóg_VALUE', 'jdraw_begin': '화면합성.Rith_2',
        'jdraw_end': '화면합성.Críochnaigh', 'jdraw_pixel': '화면합성.picteilín',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.pointeoir'})
    easportáil_tábla.update({'jfs_mkdir': 'Cuimhne_Comhaid.Create_eolaire', 'jfs_rmdir': 'Cuimhne_Comhaid.bain_eolaire', 'jfs_kind': 'Cuimhne_Comhaid.항목종류'})
    easportáil_tábla.update({'jnet_socket': '되돌림망.Create_iontráil', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.seol',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Dún'})
    easportáil_tábla.update({'jstream_create': 'sruth_Líonra.Create_iontráil', 'jstream_bind': 'sruth_Líonra.묶기', 'jstream_listen': 'sruth_Líonra.듣기', 'jstream_connect': 'sruth_Líonra.Nasc', 'jstream_accept': 'sruth_Líonra.glac_le_nasc', 'jstream_read': 'sruth_Líonra.Léigh', 'jstream_write': 'sruth_Líonra.Scríobh', 'jstream_port': 'sruth_Líonra.창구읽기', 'jstream_peer': 'sruth_Líonra.상대창구읽기', 'jstream_close': 'sruth_Líonra.Dún'})
    for siombail_VALUE in list(easportáil_tábla):
        if siombail_VALUE.startswith('jstream_') or siombail_VALUE.startswith('jnet_') and siombail_VALUE not in ('jnet_put', 'jnet_get'):
            easportáil_tábla[siombail_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = easportáil_tábla.pop(siombail_VALUE)
    예제들 = ['public final class beart { public static void Ullmhaigh() {']
    for CONAIR in sorted((teilgean_fréamh / '예제').iterdir()):
        if CONAIR.is_file():
            예제들.append('명령해석기.statach_comhad(%s, %s);' %
                (json.dumps(CONAIR.name), json.dumps(CONAIR.read_text(encoding='utf-8'), ensure_ascii=True)))
    (tóg_cosán / 'beart.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(teilgean_fréamh, 저장소, Rith_ordú)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(tóg_cosán)) as 작업경로:
        aicme_cosán = Path(작업경로)
        Rith_ordú(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', aicme_cosán, '-sourcepath', aicme_cosán, '-d', aicme_cosán] + sorted((teilgean_fréamh / 'FOINSE').glob('*.java')) + [tóg_cosán / 'beart.java', tóg_cosán / '예제꾸러미.java'])
        # Comhad·blaosc·fuinneog 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        argóint_ARRAY = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'eithne.Rith_2', '--heap-words', '1048576', '-o', tóg_cosán / 'kernel-java.c']
        for siombail_VALUE, modh_iontráil in sorted(easportáil_tábla.items()):
            argóint_ARRAY += ['--export', siombail_VALUE + '=' + modh_iontráil]
        Rith_ordú(argóint_ARRAY + sorted(aicme_cosán.glob('*.class')))
    (tóg_cosán / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    Create_úsáideoir_spás(teilgean_fréamh, 저장소, 시언어번역기, 시플플번역기, 연결편집기, Cartlann_uirlis, 설정비트, Rith_ordú)
    Líonra = Create_Líonra(teilgean_fréamh, 시언어번역기, Cartlann_uirlis, 설정비트, Rith_ordú)
    원격사용 = Create_cianda(teilgean_fréamh, 시언어번역기, Cartlann_uirlis, 설정비트, Rith_ordú)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', tóg_cosán]
    빌드작업 = [(시언어번역기, [], tóg_cosán / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], teilgean_fréamh / 'meaisín/Teirminéal.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], teilgean_fréamh / 'meaisín/giuirléid.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], tóg_cosán / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], teilgean_fréamh / 'meaisín/clár.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], teilgean_fréamh / 'meaisín/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], teilgean_fréamh / 'meaisín/úsáideoir.c', 'user.o'),
            (시언어번역기, [], teilgean_fréamh / '부팅/iontráil_pointe_VALUE.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Nasc.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], teilgean_fréamh / '시험/comhad_Glaonna.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [comhad_iontráil for comhad_iontráil in 설정비트 if comhad_iontráil != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        Rith_ordú([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', tóg_cosán / 출력결과])
    Rith_ordú([Cartlann_uirlis, 'rcs', tóg_cosán / 'libposix-kor-arm64.a', tóg_cosán / 'posix.o'])
    Rith_ordú([연결편집기, '--gc-sections', '-T', teilgean_fréamh / '부팅/Nasc_dáileadh.ld', '-Map', tóg_cosán / 'kernel.map', '-o', tóg_cosán / 'kernel.elf'] +
        [tóg_cosán / Ainm for Ainm in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', tóg_cosán / 'libposix-kor-arm64.a', Líonra, 원격사용, tóg_cosán / 'remote/libassh.a', tóg_cosán / 'remote/libbearssl.a', '--end-group'])
    Rith_ordú([oibiacht_comhad_tiontaire, '-O', 'binary', tóg_cosán / 'kernel.elf', tóg_cosán / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Gaeilge.자체', 'korean_exceptions': 20,
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
    for Ainm in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Ainm] = hashlib.sha256((tóg_cosán / Ainm).read_bytes()).hexdigest()
    (tóg_cosán / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', tóg_cosán / 'kernel8.img')


if __name__ == '__main__':
    Rith_2()
