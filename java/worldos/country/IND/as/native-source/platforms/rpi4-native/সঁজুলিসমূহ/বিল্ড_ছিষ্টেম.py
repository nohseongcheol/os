#!/usr/bin/env python3
"""হ_ষ্ট javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from বিল্ড_ব্যৱহাৰকৰ্তা_স্থান import ক্ৰিয়েট_ব্যৱহাৰকৰ্তা_স্থান
from বিল্ড_নেটৱৰ্ক import ক্ৰিয়েট_নেটৱৰ্ক
from 예제빌드 import 예제만들기
from বিল্ড_দূৰবৰ্তী import ক্ৰিয়েট_দূৰবৰ্তী

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
বিল্ড_পথ = 기준 / 'build'


def নিষ্পাদন_আদেশ(যুক্তি_শৃঙ্খলা):
    subprocess.check_call([str(첫째값) for 첫째값 in যুক্তি_শৃঙ্খলা], cwd=str(기준))


def সঞ্চালন():
    বিল্ড_পথ.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    অবজেক্ট_ফাইল_কনভাৰ্টাৰ = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    অভিলেখাগাৰ_সঁজুলি = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for সঁজুলিসমূহ in ('javac', 시언어번역기, 시플플번역기, 연결편집기, অবজেক্ট_ফাইল_কনভাৰ্টাৰ, অভিলেখাগাৰ_সঁজুলি):
        if not shutil.which(সঁজুলিসমূহ):
            raise SystemExit('필요한 বিল্ড_ছিষ্টেম সঁজুলিসমূহ 없음: ' + সঁজুলিসমূহ)
    ফ_ন্ট_তথ্য = json.loads((기준 / 'vendor/terminal-font.json').read_text())
    ফ_ন্ট_ডাটা = (기준 / 'vendor/terminal-font.bin').read_bytes()
    if len(ফ_ন্ট_ডাটা) != 65616 * 32 or hashlib.sha256(ফ_ন্ট_ডাটা).hexdigest() != ফ_ন্ট_তথ্য['sha256']:
        raise SystemExit('টাৰ্মিনেল ফ_ন্ট_মান মাপ/SHA256 불일치')
    ৰপ্তানি_কৰক_তালিকা = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.নিৰ্গম', 'jshell_input': '셸입출력.입력', 'java_task': 'কাৰ্ণেল.작업', 'jfs_path_start': 'মেম_ৰি_ফাইলসমূহ.পথ_আৰম্ভ',
               'jfs_path_byte': 'মেম_ৰি_ফাইলসমূহ.পথ_বাইট', 'jfs_open': 'মেম_ৰি_ফাইলসমূহ.খোলো',
               'jfs_read': 'মেম_ৰি_ফাইলসমূহ.পড়া', 'jfs_write': 'মেম_ৰি_ফাইলসমূহ.লিখা',
               'jfs_seek': 'মেম_ৰি_ফাইলসমূহ.ছীক_স্থান_সলনি_কৰক', 'jfs_close': 'মেম_ৰি_ফাইলসমূহ.বন্ধ_কৰক',
               'jfs_size': 'মেম_ৰি_ফাইলসমূহ.মাপ', 'jfs_unlink': 'মেম_ৰি_ফাইলসমূহ.지우기',
               'jfs_truncate': 'মেম_ৰি_ফাইলসমূহ.ছেট_দৈর্ঘ্য'}
    ৰপ্তানি_কৰক_তালিকা.update({'jfs_entry_count': 'মেম_ৰি_ফাইলসমূহ.파일한도', 'jfs_entry_length': 'মেম_ৰি_ফাইলসমূহ.공개이름길이', 'jfs_entry_byte': 'মেম_ৰি_ফাইলসমূহ.공개이름바이트', 'jfs_entry_size': 'মেম_ৰি_ফাইলসমূহ.공개파일크기'})
    ৰপ্তানি_কৰক_তালিকা.update({'jdraw_prepare': '화면합성.প্ৰস্তুত_কৰক', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.ক্লিপ',
        'jdraw_clip_value': '화면합성.ক্লিপ_মান', 'jdraw_begin': '화면합성.সঞ্চালন',
        'jdraw_end': '화면합성.সমাপ্ত_কৰক', 'jdraw_pixel': '화면합성.পিক্সেল',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.পইণ্টাৰ'})
    ৰপ্তানি_কৰক_তালিকা.update({'jfs_mkdir': 'মেম_ৰি_ফাইলসমূহ.ক্ৰিয়েট_ডাইৰেক্টৰী', 'jfs_rmdir': 'মেম_ৰি_ফাইলসমূহ.আঁতৰাওক_ডাইৰেক্টৰী', 'jfs_kind': 'মেম_ৰি_ফাইলসমূহ.항목종류'})
    ৰপ্তানি_কৰক_তালিকা.update({'jnet_socket': '되돌림망.ক্ৰিয়েট_প্রবিষ্ট', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.ই_মেইল_কৰক',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.বন্ধ_কৰক'})
    ৰপ্তানি_কৰক_তালিকা.update({'jstream_create': 'ষ্ট্ৰিম_নেটৱৰ্ক.ক্ৰিয়েট_প্রবিষ্ট', 'jstream_bind': 'ষ্ট্ৰিম_নেটৱৰ্ক.묶기', 'jstream_listen': 'ষ্ট্ৰিম_নেটৱৰ্ক.듣기', 'jstream_connect': 'ষ্ট্ৰিম_নেটৱৰ্ক.সংযোগ_স্থাপনা', 'jstream_accept': 'ষ্ট্ৰিম_নেটৱৰ্ক.গ্ৰহণ_সংযোগ', 'jstream_read': 'ষ্ট্ৰিম_নেটৱৰ্ক.পড়া', 'jstream_write': 'ষ্ট্ৰিম_নেটৱৰ্ক.লিখা', 'jstream_port': 'ষ্ট্ৰিম_নেটৱৰ্ক.창구읽기', 'jstream_peer': 'ষ্ট্ৰিম_নেটৱৰ্ক.상대창구읽기', 'jstream_close': 'ষ্ট্ৰিম_নেটৱৰ্ক.বন্ধ_কৰক'})
    for প্ৰতীক_মান in list(ৰপ্তানি_কৰক_তালিকা):
        if প্ৰতীক_মান.startswith('jstream_') or প্ৰতীক_মান.startswith('jnet_') and প্ৰতীক_মান not in ('jnet_put', 'jnet_get'):
            ৰপ্তানি_কৰক_তালিকা[প্ৰতীক_মান.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = ৰপ্তানি_কৰক_তালিকা.pop(প্ৰতীক_মান)
    예제들 = ['public final class বাণ্ডল { public static void প্ৰস্তুত_কৰক() {']
    for পথ in sorted((기준 / '예제').iterdir()):
        if পথ.is_file():
            예제들.append('명령해석기.স্থিৰ_ফাইল(%s, %s);' %
                (json.dumps(পথ.name), json.dumps(পথ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (বিল্ড_পথ / 'বাণ্ডল.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(기준, 저장소, নিষ্পাদন_আদেশ)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(বিল্ড_পথ)) as 작업경로:
        শ্ৰেণী_পথ = Path(작업경로)
        নিষ্পাদন_আদেশ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', শ্ৰেণী_পথ, '-sourcepath', শ্ৰেণী_পথ, '-d', শ্ৰেণী_পথ] + sorted((기준 / 'উৎস').glob('*.java')) + [বিল্ড_পথ / 'বাণ্ডল.java', বিল্ড_পথ / '예제꾸러미.java'])
        # নথিপত্ৰ·শ্বেল·উইণ্ড 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        যুক্তি_শৃঙ্খলা = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'কাৰ্ণেল.সঞ্চালন', '--heap-words', '1048576', '-o', বিল্ড_পথ / 'kernel-java.c']
        for প্ৰতীক_মান, পদ্ধতি_প্রবিষ্ট in sorted(ৰপ্তানি_কৰক_তালিকা.items()):
            যুক্তি_শৃঙ্খলা += ['--export', প্ৰতীক_মান + '=' + পদ্ধতি_প্রবিষ্ট]
        নিষ্পাদন_আদেশ(যুক্তি_শৃঙ্খলা + sorted(শ্ৰেণী_পথ.glob('*.class')))
    (বিল্ড_পথ / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    ক্ৰিয়েট_ব্যৱহাৰকৰ্তা_স্থান(기준, 저장소, 시언어번역기, 시플플번역기, 연결편집기, অভিলেখাগাৰ_সঁজুলি, 설정비트, নিষ্পাদন_আদেশ)
    নেটৱৰ্ক = ক্ৰিয়েট_নেটৱৰ্ক(기준, 시언어번역기, অভিলেখাগাৰ_সঁজুলি, 설정비트, নিষ্পাদন_আদেশ)
    원격사용 = ক্ৰিয়েট_দূৰবৰ্তী(기준, 시언어번역기, অভিলেখাগাৰ_সঁজুলি, 설정비트, নিষ্পাদন_আদেশ)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', বিল্ড_পথ]
    빌드작업 = [(시언어번역기, [], বিল্ড_পথ / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'মেচিন/টাৰ্মিনেল.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'মেচিন/ৱিজেট.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], বিল্ড_পথ / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'মেচিন/ব_ৰ্ড.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'মেচিন/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 기준 / 'মেচিন/ব্যৱহাৰকৰ্তা.c', 'user.o'),
            (시언어번역기, [], 기준 / '부팅/প্রবিষ্ট_পইণ্ট_মান.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'সংযোগ_স্থাপনা.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], 기준 / '시험/ফাইল_কলসমূহ.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ফাইল_প্রবিষ্ট for ফাইল_প্রবিষ্ট in 설정비트 if ফাইল_প্রবিষ্ট != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        নিষ্পাদন_আদেশ([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', বিল্ড_পথ / 출력결과])
    নিষ্পাদন_আদেশ([অভিলেখাগাৰ_সঁজুলি, 'rcs', বিল্ড_পথ / 'libposix-kor-arm64.a', বিল্ড_পথ / 'posix.o'])
    নিষ্পাদন_আদেশ([연결편집기, '--gc-sections', '-T', 기준 / '부팅/লিংক_লেআউট.ld', '-Map', বিল্ড_পথ / 'kernel.map', '-o', বিল্ড_পথ / 'kernel.elf'] +
        [বিল্ড_পথ / নাম for নাম in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', বিল্ড_পথ / 'libposix-kor-arm64.a', নেটৱৰ্ক, 원격사용, বিল্ড_পথ / 'remote/libassh.a', বিল্ড_পথ / 'remote/libbearssl.a', '--end-group'])
    নিষ্পাদন_আদেশ([অবজেক্ট_ফাইল_কনভাৰ্টাৰ, '-O', 'binary', বিল্ড_পথ / 'kernel.elf', বিল্ড_পথ / 'kernel8.img'])
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
    for নাম in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][নাম] = hashlib.sha256((বিল্ড_পথ / নাম).read_bytes()).hexdigest()
    (বিল্ড_পথ / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', বিল্ড_পথ / 'kernel8.img')


if __name__ == '__main__':
    সঞ্চালন()
