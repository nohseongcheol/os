#!/usr/bin/env python3
"""hýsa javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from smíð_notandi_svæði import stofna_notandi_svæði
from smíð_Net import stofna_Net
from 예제빌드 import 예제만들기
from smíð_fjartengdur import stofna_fjartengdur

verk_rót = Path(__file__).resolve().parents[1]
gagnageymsla_rót = verk_rót.parents[1]
smíð_slóð = verk_rót / 'build'


def keyra_skipun(frumbreyta_ARRAY):
    subprocess.check_call([str(첫째값) for 첫째값 in frumbreyta_ARRAY], cwd=str(verk_rót))


def Keyra_2():
    smíð_slóð.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    hlutur_skrá_umbreytir = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Safn_verkfæri = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Verkfæri in ('javac', 시언어번역기, 시플플번역기, 연결편집기, hlutur_skrá_umbreytir, Safn_verkfæri):
        if not shutil.which(Verkfæri):
            raise SystemExit('필요한 smíð_kerfi Verkfæri 없음: ' + Verkfæri)
    leturgerð_uppl = json.loads((verk_rót / 'vendor/terminal-font.json').read_text())
    leturgerð_gögn = (verk_rót / 'vendor/terminal-font.bin').read_bytes()
    if len(leturgerð_gögn) != 65616 * 32 or hashlib.sha256(leturgerð_gögn).hexdigest() != leturgerð_uppl['sha256']:
        raise SystemExit('Skjáhermir leturgerð_VALUE Stærð/SHA256 불일치')
    flytja_út_tafla = {'jshell_interactive': '셸입출력.upplýsingatækni_gagnvirkur', 'jshell_output': '셸입출력.úttak', 'jshell_input': '셸입출력.입력', 'java_task': 'kjarni.작업', 'jfs_path_start': 'Minni_Skrár.slóð_Opna',
               'jfs_path_byte': 'Minni_Skrár.slóð_bæti', 'jfs_open': 'Minni_Skrár.Opna',
               'jfs_read': 'Minni_Skrár.Lestur', 'jfs_write': 'Minni_Skrár.Skrift',
               'jfs_seek': 'Minni_Skrár.leita_staða', 'jfs_close': 'Minni_Skrár.Loka',
               'jfs_size': 'Minni_Skrár.Stærð', 'jfs_unlink': 'Minni_Skrár.eyða_færsla',
               'jfs_truncate': 'Minni_Skrár.sett_lengd'}
    flytja_út_tafla.update({'jfs_entry_count': 'Minni_Skrár.파일한도', 'jfs_entry_length': 'Minni_Skrár.공개이름길이', 'jfs_entry_byte': 'Minni_Skrár.공개이름바이트', 'jfs_entry_size': 'Minni_Skrár.공개파일크기'})
    flytja_út_tafla.update({'jdraw_prepare': '화면합성.Undirbúa', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.miðlaskrá',
        'jdraw_clip_value': '화면합성.miðlaskrá_VALUE', 'jdraw_begin': '화면합성.Keyra_2',
        'jdraw_end': '화면합성.Ljúka', 'jdraw_pixel': '화면합성.díll',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.bendill'})
    flytja_út_tafla.update({'jfs_mkdir': 'Minni_Skrár.stofna_skráasafn', 'jfs_rmdir': 'Minni_Skrár.fjarlægja_skráasafn', 'jfs_kind': 'Minni_Skrár.항목종류'})
    flytja_út_tafla.update({'jnet_socket': '되돌림망.stofna_færsla', 'jnet_bind': '되돌림망.BIND_endastöð',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.senda',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.sendandi_endastöð', 'jnet_close': '되돌림망.Loka'})
    flytja_út_tafla.update({'jstream_create': 'Stream_Net.stofna_færsla', 'jstream_bind': 'Stream_Net.BIND_endastöð', 'jstream_listen': 'Stream_Net.hlusta_endastöð', 'jstream_connect': 'Stream_Net.Tengjast', 'jstream_accept': 'Stream_Net.samþykkja_tenging', 'jstream_read': 'Stream_Net.Lestur', 'jstream_write': 'Stream_Net.Skrift', 'jstream_port': 'Stream_Net.창구읽기', 'jstream_peer': 'Stream_Net.상대창구읽기', 'jstream_close': 'Stream_Net.Loka'})
    for tákn_VALUE in list(flytja_út_tafla):
        if tákn_VALUE.startswith('jstream_') or tákn_VALUE.startswith('jnet_') and tákn_VALUE not in ('jnet_put', 'jnet_get'):
            flytja_út_tafla[tákn_VALUE.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = flytja_út_tafla.pop(tákn_VALUE)
    예제들 = ['public final class búnt { public static void Undirbúa() {']
    for SLÓÐ in sorted((verk_rót / '예제').iterdir()):
        if SLÓÐ.is_file():
            예제들.append('명령해석기.fast_skrá(%s, %s);' %
                (json.dumps(SLÓÐ.name), json.dumps(SLÓÐ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (smíð_slóð / 'búnt.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(verk_rót, gagnageymsla_rót, keyra_skipun)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(smíð_slóð)) as 작업경로:
        klasi_slóð = Path(작업경로)
        keyra_skipun(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klasi_slóð, '-sourcepath', klasi_slóð, '-d', klasi_slóð] + sorted((verk_rót / 'Uppruni').glob('*.java')) + [smíð_slóð / 'búnt.java', smíð_slóð / '예제꾸러미.java'])
        # Skrá·skel·Gluggi 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        frumbreyta_ARRAY = ['sh', gagnageymsla_rót / 'compiler/미리번역.sh', '--entry', 'kjarni.Keyra_2', '--heap-words', '1048576', '-o', smíð_slóð / 'kernel-java.c']
        for tákn_VALUE, aðferð_færsla in sorted(flytja_út_tafla.items()):
            frumbreyta_ARRAY += ['--export', tákn_VALUE + '=' + aðferð_færsla]
        keyra_skipun(frumbreyta_ARRAY + sorted(klasi_slóð.glob('*.class')))
    (smíð_slóð / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    afbrigði_Background_Intelligent_Transfer_Service = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = gagnageymsla_rót / 'posix-kor/arm64-native'
    stofna_notandi_svæði(verk_rót, gagnageymsla_rót, 시언어번역기, 시플플번역기, 연결편집기, Safn_verkfæri, afbrigði_Background_Intelligent_Transfer_Service, keyra_skipun)
    Net = stofna_Net(verk_rót, 시언어번역기, Safn_verkfæri, afbrigði_Background_Intelligent_Transfer_Service, keyra_skipun)
    원격사용 = stofna_fjartengdur(verk_rót, 시언어번역기, Safn_verkfæri, afbrigði_Background_Intelligent_Transfer_Service, keyra_skipun)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', smíð_slóð]
    빌드작업 = [(시언어번역기, [], smíð_slóð / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], verk_rót / 'vél/Skjáhermir.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], verk_rót / 'vél/græja.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], smíð_slóð / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], verk_rót / 'vél/bretti.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], verk_rót / 'vél/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], verk_rót / 'vél/notandi.c', 'user.o'),
            (시언어번역기, [], verk_rót / '부팅/færsla_P_VALUE.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Tengjast.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], verk_rót / '시험/skrá_Símtöl.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, úttak_54cd5e1d in 빌드작업:
        원본설정 = [skrá_færsla_3d0c1245 for skrá_færsla_3d0c1245 in afbrigði_Background_Intelligent_Transfer_Service if skrá_færsla_3d0c1245 != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else afbrigði_Background_Intelligent_Transfer_Service
        keyra_skipun([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', smíð_slóð / úttak_54cd5e1d])
    keyra_skipun([Safn_verkfæri, 'rcs', smíð_slóð / 'libposix-kor-arm64.a', smíð_slóð / 'posix.o'])
    keyra_skipun([연결편집기, '--gc-sections', '-T', verk_rót / '부팅/tengja_útlit.ld', '-Map', smíð_slóð / 'kernel.map', '-o', smíð_slóð / 'kernel.elf'] +
        [smíð_slóð / Heiti for Heiti in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', smíð_slóð / 'libposix-kor-arm64.a', Net, 원격사용, smíð_slóð / 'remote/libassh.a', smíð_slóð / 'remote/libbearssl.a', '--end-group'])
    keyra_skipun([hlutur_skrá_umbreytir, '-O', 'binary', smíð_slóð / 'kernel.elf', smíð_slóð / 'kernel8.img'])
    búnt_skrá = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Íslenska.eigin', 'korean_exceptions': 20,
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
    for Heiti in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        búnt_skrá['sha256'][Heiti] = hashlib.sha256((smíð_slóð / Heiti).read_bytes()).hexdigest()
    (smíð_slóð / 'build.json').write_text(json.dumps(búnt_skrá, indent=2) + '\n')
    print('완료:', smíð_slóð / 'kernel8.img')


if __name__ == '__main__':
    Keyra_2()
