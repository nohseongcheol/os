#!/usr/bin/env python3
"""taurima javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from hanga_kaiwhakamahi_wāhi import Waihanga_kaiwhakamahi_wāhi
from hanga_whatunga import Waihanga_whatunga
from 예제빌드 import 예제만들기
from hanga_mamao import Waihanga_mamao

whakaatu_pūtake = Path(__file__).resolve().parents[1]
저장소 = whakaatu_pūtake.parents[1]
hanga_ara = whakaatu_pūtake / 'build'


def kawe_tono(tohenga_HUĀNGA):
    subprocess.check_call([str(첫째값) for 첫째값 in tohenga_HUĀNGA], cwd=str(whakaatu_pūtake))


def whakahaere():
    hanga_ara.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ahanoa_kōnae_pūtahuri = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Pūranga_utauta = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Ngā_Utauta in ('javac', 시언어번역기, 시플플번역기, 연결편집기, ahanoa_kōnae_pūtahuri, Pūranga_utauta):
        if not shutil.which(Ngā_Utauta):
            raise SystemExit('필요한 hanga_pūnaha Ngā_Utauta 없음: ' + Ngā_Utauta)
    momotuhi_mōhiohio = json.loads((whakaatu_pūtake / 'vendor/terminal-font.json').read_text())
    momotuhi_raraunga = (whakaatu_pūtake / 'vendor/terminal-font.bin').read_bytes()
    if len(momotuhi_raraunga) != 65616 * 32 or hashlib.sha256(momotuhi_raraunga).hexdigest() != momotuhi_mōhiohio['sha256']:
        raise SystemExit('Tauranga momotuhi_uara rahi/SHA256 불일치')
    kaweake_ripanga = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'kākano.작업', 'jfs_path_start': 'Pūmahara_Ngā_Kōnae.ara_Start',
               'jfs_path_byte': 'Pūmahara_Ngā_Kōnae.ara_paita', 'jfs_open': 'Pūmahara_Ngā_Kōnae.Huaki',
               'jfs_read': 'Pūmahara_Ngā_Kōnae.Pānuitia', 'jfs_write': 'Pūmahara_Ngā_Kōnae.Tuhia',
               'jfs_seek': 'Pūmahara_Ngā_Kōnae.kimi_tūranga', 'jfs_close': 'Pūmahara_Ngā_Kōnae.Kati',
               'jfs_size': 'Pūmahara_Ngā_Kōnae.rahi', 'jfs_unlink': 'Pūmahara_Ngā_Kōnae.지우기',
               'jfs_truncate': 'Pūmahara_Ngā_Kōnae.huinga_roa'}
    kaweake_ripanga.update({'jfs_entry_count': 'Pūmahara_Ngā_Kōnae.파일한도', 'jfs_entry_length': 'Pūmahara_Ngā_Kōnae.공개이름길이', 'jfs_entry_byte': 'Pūmahara_Ngā_Kōnae.공개이름바이트', 'jfs_entry_size': 'Pūmahara_Ngā_Kōnae.공개파일크기'})
    kaweake_ripanga.update({'jdraw_prepare': '화면합성.Whakarite', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.topenga',
        'jdraw_clip_value': '화면합성.topenga_uara', 'jdraw_begin': '화면합성.whakahaere',
        'jdraw_end': '화면합성.Mutu', 'jdraw_pixel': '화면합성.pika',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.atatohu'})
    kaweake_ripanga.update({'jfs_mkdir': 'Pūmahara_Ngā_Kōnae.Waihanga_whaiaronga', 'jfs_rmdir': 'Pūmahara_Ngā_Kōnae.tango_whaiaronga', 'jfs_kind': 'Pūmahara_Ngā_Kōnae.항목종류'})
    kaweake_ripanga.update({'jnet_socket': '되돌림망.Waihanga_tāurunga', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.tuku',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.Kati'})
    kaweake_ripanga.update({'jstream_create': 'roma_whatunga.Waihanga_tāurunga', 'jstream_bind': 'roma_whatunga.묶기', 'jstream_listen': 'roma_whatunga.듣기', 'jstream_connect': 'roma_whatunga.TŪHONO', 'jstream_accept': 'roma_whatunga.whakaae_hononga', 'jstream_read': 'roma_whatunga.Pānuitia', 'jstream_write': 'roma_whatunga.Tuhia', 'jstream_port': 'roma_whatunga.창구읽기', 'jstream_peer': 'roma_whatunga.상대창구읽기', 'jstream_close': 'roma_whatunga.Kati'})
    for tohu_uara in list(kaweake_ripanga):
        if tohu_uara.startswith('jstream_') or tohu_uara.startswith('jnet_') and tohu_uara not in ('jnet_put', 'jnet_get'):
            kaweake_ripanga[tohu_uara.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = kaweake_ripanga.pop(tohu_uara)
    예제들 = ['public final class pūpū { public static void Whakarite() {']
    for ara in sorted((whakaatu_pūtake / '예제').iterdir()):
        if ara.is_file():
            예제들.append('명령해석기.pateko_kōnae(%s, %s);' %
                (json.dumps(ara.name), json.dumps(ara.read_text(encoding='utf-8'), ensure_ascii=True)))
    (hanga_ara / 'pūpū.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(whakaatu_pūtake, 저장소, kawe_tono)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(hanga_ara)) as 작업경로:
        tauaha_ara = Path(작업경로)
        kawe_tono(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', tauaha_ara, '-sourcepath', tauaha_ara, '-d', tauaha_ara] + sorted((whakaatu_pūtake / 'pūtake').glob('*.java')) + [hanga_ara / 'pūpū.java', hanga_ara / '예제꾸러미.java'])
        # Kōnae·anga·matapihi 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        tohenga_HUĀNGA = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'kākano.whakahaere', '--heap-words', '1048576', '-o', hanga_ara / 'kernel-java.c']
        for tohu_uara, aratuka_tāurunga in sorted(kaweake_ripanga.items()):
            tohenga_HUĀNGA += ['--export', tohu_uara + '=' + aratuka_tāurunga]
        kawe_tono(tohenga_HUĀNGA + sorted(tauaha_ara.glob('*.class')))
    (hanga_ara / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    Waihanga_kaiwhakamahi_wāhi(whakaatu_pūtake, 저장소, 시언어번역기, 시플플번역기, 연결편집기, Pūranga_utauta, 설정비트, kawe_tono)
    whatunga = Waihanga_whatunga(whakaatu_pūtake, 시언어번역기, Pūranga_utauta, 설정비트, kawe_tono)
    원격사용 = Waihanga_mamao(whakaatu_pūtake, 시언어번역기, Pūranga_utauta, 설정비트, kawe_tono)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', hanga_ara]
    빌드작업 = [(시언어번역기, [], hanga_ara / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], whakaatu_pūtake / 'mīhini/Tauranga.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], whakaatu_pūtake / 'mīhini/taputapu.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], hanga_ara / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], whakaatu_pūtake / 'mīhini/papa.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], whakaatu_pūtake / 'mīhini/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], whakaatu_pūtake / 'mīhini/kaiwhakamahi.c', 'user.o'),
            (시언어번역기, [], whakaatu_pūtake / '부팅/tāurunga_ira_uara.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'TŪHONO.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], whakaatu_pūtake / '시험/kōnae_Ngā_Waeatanga.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [kōnae_tāurunga for kōnae_tāurunga in 설정비트 if kōnae_tāurunga != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        kawe_tono([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', hanga_ara / 출력결과])
    kawe_tono([Pūranga_utauta, 'rcs', hanga_ara / 'libposix-kor-arm64.a', hanga_ara / 'posix.o'])
    kawe_tono([연결편집기, '--gc-sections', '-T', whakaatu_pūtake / '부팅/Hono_Tahora.ld', '-Map', hanga_ara / 'kernel.map', '-o', hanga_ara / 'kernel.elf'] +
        [hanga_ara / Ingoa for Ingoa in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', hanga_ara / 'libposix-kor-arm64.a', whatunga, 원격사용, hanga_ara / 'remote/libassh.a', hanga_ara / 'remote/libbearssl.a', '--end-group'])
    kawe_tono([ahanoa_kōnae_pūtahuri, '-O', 'binary', hanga_ara / 'kernel.elf', hanga_ara / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'Reo_Māori.자체', 'korean_exceptions': 20,
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
    for Ingoa in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][Ingoa] = hashlib.sha256((hanga_ara / Ingoa).read_bytes()).hexdigest()
    (hanga_ara / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', hanga_ara / 'kernel8.img')


if __name__ == '__main__':
    whakahaere()
