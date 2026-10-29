#!/usr/bin/env python3
"""হোস্ট javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from গঠন_ব্যবহারকারী_স্পেস import ক্রিয়েট_ব্যবহারকারী_স্পেস
from গঠন_নেটওয়ার্ক import ক্রিয়েট_নেটওয়ার্ক
from 예제빌드 import 예제만들기
from গঠন_দূরবর্তী import ক্রিয়েট_দূরবর্তী

প্রকল্প_মূল = Path(__file__).resolve().parents[1]
সংগ্রহস্থলের_মূল = প্রকল্প_মূল.parents[1]
গঠন_পথ = প্রকল্প_মূল / 'build'


def কার্যকর_করুন_আদেশ(যুক্তি_অ্যারে):
    subprocess.check_call([str(첫째값) for 첫째값 in যুক্তি_অ্যারে], cwd=str(প্রকল্প_মূল))


def চালনা():
    গঠন_পথ.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    বস্তু_ফাইল_পরিবর্তক = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    সংগ্রহ_করা_টুল = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for সরঞ্জামগুলি in ('javac', 시언어번역기, 시플플번역기, 연결편집기, বস্তু_ফাইল_পরিবর্তক, সংগ্রহ_করা_টুল):
        if not shutil.which(সরঞ্জামগুলি):
            raise SystemExit('필요한 গঠন_সিস্টেম সরঞ্জামগুলি 없음: ' + সরঞ্জামগুলি)
    হরফ_তথ্য = json.loads((প্রকল্প_মূল / 'vendor/terminal-font.json').read_text())
    হরফ_ডাটা = (প্রকল্প_মূল / 'vendor/terminal-font.bin').read_bytes()
    if len(হরফ_ডাটা) != 65616 * 32 or hashlib.sha256(হরফ_ডাটা).hexdigest() != হরফ_তথ্য['sha256']:
        raise SystemExit('আদেশ_ব্যাখ্যাকারী হরফ_মান আকার/SHA256 불일치')
    রপ্তানি_সারণি = {'jshell_interactive': '셸입출력.তথ্য_প্রযুক্তি_মিথস্ক্রিয়', 'jshell_output': '셸입출력.নির্গম', 'jshell_input': '셸입출력.입력', 'java_task': 'কারনেল.작업', 'jfs_path_start': 'মেমরি_ফাইলগুলি.পথ_শুরু',
               'jfs_path_byte': 'মেমরি_ফাইলগুলি.পথ_বাইট', 'jfs_open': 'মেমরি_ফাইলগুলি.খুলুন',
               'jfs_read': 'মেমরি_ফাইলগুলি.পড়া', 'jfs_write': 'মেমরি_ফাইলগুলি.লেখা',
               'jfs_seek': 'মেমরি_ফাইলগুলি.সিক_পদ', 'jfs_close': 'মেমরি_ফাইলগুলি.বন্ধ_করুন',
               'jfs_size': 'মেমরি_ফাইলগুলি.আকার', 'jfs_unlink': 'মেমরি_ফাইলগুলি.মুছুন_ভুক্তি',
               'jfs_truncate': 'মেমরি_ফাইলগুলি.সেট_দৈর্ঘ্য'}
    রপ্তানি_সারণি.update({'jfs_entry_count': 'মেমরি_ফাইলগুলি.파일한도', 'jfs_entry_length': 'মেমরি_ফাইলগুলি.공개이름길이', 'jfs_entry_byte': 'মেমরি_ফাইলগুলি.공개이름바이트', 'jfs_entry_size': 'মেমরি_ফাইলগুলি.공개파일크기'})
    রপ্তানি_সারণি.update({'jdraw_prepare': '화면합성.প্রস্তুত_করুন', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.ক্লিপ',
        'jdraw_clip_value': '화면합성.ক্লিপ_মান', 'jdraw_begin': '화면합성.চালনা',
        'jdraw_end': '화면합성.শেষ', 'jdraw_pixel': '화면합성.পেল্',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.নির্দেশক'})
    রপ্তানি_সারণি.update({'jfs_mkdir': 'মেমরি_ফাইলগুলি.ক্রিয়েট_ডিরেক্টরি', 'jfs_rmdir': 'মেমরি_ফাইলগুলি.সরানো_ডিরেক্টরি', 'jfs_kind': 'মেমরি_ফাইলগুলি.항목종류'})
    রপ্তানি_সারণি.update({'jnet_socket': '되돌림망.ক্রিয়েট_ভুক্তি', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.পাঠান',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.বন্ধ_করুন'})
    রপ্তানি_সারণি.update({'jstream_create': 'প্রবাহ_নেটওয়ার্ক.ক্রিয়েট_ভুক্তি', 'jstream_bind': 'প্রবাহ_নেটওয়ার্ক.묶기', 'jstream_listen': 'প্রবাহ_নেটওয়ার্ক.듣기', 'jstream_connect': 'প্রবাহ_নেটওয়ার্ক.সংযোগ_স্থাপনা', 'jstream_accept': 'প্রবাহ_নেটওয়ার্ক.স্বীকার_করুন_সংযোগ', 'jstream_read': 'প্রবাহ_নেটওয়ার্ক.পড়া', 'jstream_write': 'প্রবাহ_নেটওয়ার্ক.লেখা', 'jstream_port': 'প্রবাহ_নেটওয়ার্ক.창구읽기', 'jstream_peer': 'প্রবাহ_নেটওয়ার্ক.상대창구읽기', 'jstream_close': 'প্রবাহ_নেটওয়ার্ক.বন্ধ_করুন'})
    for প্রতীক_মান in list(রপ্তানি_সারণি):
        if প্রতীক_মান.startswith('jstream_') or প্রতীক_মান.startswith('jnet_') and প্রতীক_মান not in ('jnet_put', 'jnet_get'):
            রপ্তানি_সারণি[প্রতীক_মান.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = রপ্তানি_সারণি.pop(প্রতীক_মান)
    예제들 = ['public final class পাঁজা { public static void প্রস্তুত_করুন() {']
    for পথ_2 in sorted((প্রকল্প_মূল / '예제').iterdir()):
        if পথ_2.is_file():
            예제들.append('명령해석기.স্থির_ফাইল(%s, %s);' %
                (json.dumps(পথ_2.name), json.dumps(পথ_2.read_text(encoding='utf-8'), ensure_ascii=True)))
    (গঠন_পথ / 'পাঁজা.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(প্রকল্প_মূল, সংগ্রহস্থলের_মূল, কার্যকর_করুন_আদেশ)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(গঠন_পথ)) as 작업경로:
        শ্রেণী_পথ = Path(작업경로)
        কার্যকর_করুন_আদেশ(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', শ্রেণী_পথ, '-sourcepath', শ্রেণী_পথ, '-d', শ্রেণী_পথ] + sorted((প্রকল্প_মূল / 'উৎস_নথি').glob('*.java')) + [গঠন_পথ / 'পাঁজা.java', গঠন_পথ / '예제꾸러미.java'])
        # নথির_নাম·শেল·উইন্ডো 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        যুক্তি_অ্যারে = ['sh', সংগ্রহস্থলের_মূল / 'compiler/미리번역.sh', '--entry', 'কারনেল.চালনা', '--heap-words', '1048576', '-o', গঠন_পথ / 'kernel-java.c']
        for প্রতীক_মান, পদ্ধতি_ভুক্তি in sorted(রপ্তানি_সারণি.items()):
            যুক্তি_অ্যারে += ['--export', প্রতীক_মান + '=' + পদ্ধতি_ভুক্তি]
        কার্যকর_করুন_আদেশ(যুক্তি_অ্যারে + sorted(শ্রেণী_পথ.glob('*.class')))
    (গঠন_পথ / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = সংগ্রহস্থলের_মূল / 'posix-kor/arm64-native'
    ক্রিয়েট_ব্যবহারকারী_স্পেস(প্রকল্প_মূল, সংগ্রহস্থলের_মূল, 시언어번역기, 시플플번역기, 연결편집기, সংগ্রহ_করা_টুল, বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস, কার্যকর_করুন_আদেশ)
    নেটওয়ার্ক_9b2e3222 = ক্রিয়েট_নেটওয়ার্ক(প্রকল্প_মূল, 시언어번역기, সংগ্রহ_করা_টুল, বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস, কার্যকর_করুন_আদেশ)
    원격사용 = ক্রিয়েট_দূরবর্তী(প্রকল্প_মূল, 시언어번역기, সংগ্রহ_করা_টুল, বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস, কার্যকর_করুন_আদেশ)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', গঠন_পথ]
    빌드작업 = [(시언어번역기, [], গঠন_পথ / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], প্রকল্প_মূল / 'মেশিন/আদেশ_ব্যাখ্যাকারী.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], প্রকল্প_মূল / 'মেশিন/উইজেট.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], গঠন_পথ / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], প্রকল্প_মূল / 'মেশিন/বোর্ড.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], প্রকল্প_মূল / 'মেশিন/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], প্রকল্প_মূল / 'মেশিন/ব্যবহারকারী.c', 'user.o'),
            (시언어번역기, [], প্রকল্প_মূল / '부팅/ভুক্তি_বিন্দু_মান.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'সংযোগ_স্থাপনা.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], প্রকল্প_মূল / '시험/ফাইল_কলগুলি.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [ফাইল_ভুক্তি for ফাইল_ভুক্তি in বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস if ফাইল_ভুক্তি != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস
        কার্যকর_করুন_আদেশ([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', গঠন_পথ / 출력결과])
    কার্যকর_করুন_আদেশ([সংগ্রহ_করা_টুল, 'rcs', গঠন_পথ / 'libposix-kor-arm64.a', গঠন_পথ / 'posix.o'])
    কার্যকর_করুন_আদেশ([연결편집기, '--gc-sections', '-T', প্রকল্প_মূল / '부팅/লিংক_লেআউট.ld', '-Map', গঠন_পথ / 'kernel.map', '-o', গঠন_পথ / 'kernel.elf'] +
        [গঠন_পথ / নাম for নাম in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', গঠন_পথ / 'libposix-kor-arm64.a', নেটওয়ার্ক_9b2e3222, 원격사용, গঠন_পথ / 'remote/libassh.a', গঠন_পথ / 'remote/libbearssl.a', '--end-group'])
    কার্যকর_করুন_আদেশ([বস্তু_ফাইল_পরিবর্তক, '-O', 'binary', গঠন_পথ / 'kernel.elf', গঠন_পথ / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'বাংলা.নিজ', 'korean_exceptions': 20,
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
        꾸러미명세['sha256'][নাম] = hashlib.sha256((গঠন_পথ / নাম).read_bytes()).hexdigest()
    (গঠন_পথ / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', গঠন_পথ / 'kernel8.img')


if __name__ == '__main__':
    চালনা()
