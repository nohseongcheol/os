#!/usr/bin/env python3
"""میزبان javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from بلڈ_صارف_اسپیس import بنائیں_صارف_اسپیس
from بلڈ_نیٹ_ورک import بنائیں_نیٹ_ورک_48d29d6d
from 예제빌드 import 예제만들기
from بلڈ_بعید import بنائیں_بعید

عکس_ڈالنا_روٹ = Path(__file__).resolve().parents[1]
저장소 = عکس_ڈالنا_روٹ.parents[1]
بلڈ_راہ = عکس_ڈالنا_روٹ / 'build'


def نفاذ_کریں_حکم(دلائل_لڑی):
    subprocess.check_call([str(첫째값) for 첫째값 in دلائل_لڑی], cwd=str(عکس_ڈالنا_روٹ))


def چلائیں():
    بلڈ_راہ.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    آبجیکٹ_فائل_تبدیل_کار = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    محفوظ_ٹول = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for ٹولز in ('javac', 시언어번역기, 시플플번역기, 연결편집기, آبجیکٹ_فائل_تبدیل_کار, محفوظ_ٹول):
        if not shutil.which(ٹولز):
            raise SystemExit('필요한 بلڈ_نظام ٹولز 없음: ' + ٹولز)
    فانٹ_معلومات = json.loads((عکس_ڈالنا_روٹ / 'vendor/terminal-font.json').read_text())
    فانٹ_کوائف = (عکس_ڈالنا_روٹ / 'vendor/terminal-font.bin').read_bytes()
    if len(فانٹ_کوائف) != 65616 * 32 or hashlib.sha256(فانٹ_کوائف).hexdigest() != فانٹ_معلومات['sha256']:
        raise SystemExit('حکم_کی_تشریح_کرنے_والا فانٹ_قدر حجم/SHA256 불일치')
    برآمد_کریں_جدول = {'jshell_interactive': '셸입출력.معلومات_ٹیکنالوجی_متعامل', 'jshell_output': '셸입출력.اخراج_کا_مقام', 'jshell_input': '셸입출력.입력', 'java_task': 'کرنیل.작업', 'jfs_path_start': 'میموری_فائلیں.راہ_ابتدا',
               'jfs_path_byte': 'میموری_فائلیں.راہ_بائٹ', 'jfs_open': 'میموری_فائلیں.کھولیں',
               'jfs_read': 'میموری_فائلیں.پڑھیں', 'jfs_write': 'میموری_فائلیں.لکھیں',
               'jfs_seek': 'میموری_فائلیں.تلاش_کرنا_پوزیشن_ٹھیک_کریں', 'jfs_close': 'میموری_فائلیں.بند_کریں',
               'jfs_size': 'میموری_فائلیں.حجم', 'jfs_unlink': 'میموری_فائلیں.지우기',
               'jfs_truncate': 'میموری_فائلیں.سیٹ_لمبا_ئی'}
    برآمد_کریں_جدول.update({'jfs_entry_count': 'میموری_فائلیں.파일한도', 'jfs_entry_length': 'میموری_فائلیں.공개이름길이', 'jfs_entry_byte': 'میموری_فائلیں.공개이름바이트', 'jfs_entry_size': 'میموری_فائلیں.공개파일크기'})
    برآمد_کریں_جدول.update({'jdraw_prepare': '화면합성.تیار_کریں', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.تراشہ',
        'jdraw_clip_value': '화면합성.تراشہ_قدر', 'jdraw_begin': '화면합성.چلائیں',
        'jdraw_end': '화면합성.تکمیل', 'jdraw_pixel': '화면합성.پکسل',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.پوائنٹر'})
    برآمد_کریں_جدول.update({'jfs_mkdir': 'میموری_فائلیں.بنائیں_ڈائریکٹری', 'jfs_rmdir': 'میموری_فائلیں.ہٹائیں_ڈائریکٹری', 'jfs_kind': 'میموری_فائلیں.항목종류'})
    برآمد_کریں_جدول.update({'jnet_socket': '되돌림망.بنائیں_اندراج', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.بھیجیں',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.بند_کریں'})
    برآمد_کریں_جدول.update({'jstream_create': 'بہاؤ_نیٹ_ورک.بنائیں_اندراج', 'jstream_bind': 'بہاؤ_نیٹ_ورک.묶기', 'jstream_listen': 'بہاؤ_نیٹ_ورک.듣기', 'jstream_connect': 'بہاؤ_نیٹ_ورک.متصل_ہوں', 'jstream_accept': 'بہاؤ_نیٹ_ورک.قبول_کریں_رابطہ', 'jstream_read': 'بہاؤ_نیٹ_ورک.پڑھیں', 'jstream_write': 'بہاؤ_نیٹ_ورک.لکھیں', 'jstream_port': 'بہاؤ_نیٹ_ورک.창구읽기', 'jstream_peer': 'بہاؤ_نیٹ_ورک.상대창구읽기', 'jstream_close': 'بہاؤ_نیٹ_ورک.بند_کریں'})
    for علامت_قدر in list(برآمد_کریں_جدول):
        if علامت_قدر.startswith('jstream_') or علامت_قدر.startswith('jnet_') and علامت_قدر not in ('jnet_put', 'jnet_get'):
            برآمد_کریں_جدول[علامت_قدر.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = برآمد_کریں_جدول.pop(علامت_قدر)
    예제들 = ['public final class بنڈل { public static void تیار_کریں() {']
    for راستہ_2 in sorted((عکس_ڈالنا_روٹ / '예제').iterdir()):
        if راستہ_2.is_file():
            예제들.append('명령해석기.جامد_فائل(%s, %s);' %
                (json.dumps(راستہ_2.name), json.dumps(راستہ_2.read_text(encoding='utf-8'), ensure_ascii=True)))
    (بلڈ_راہ / 'بنڈل.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(عکس_ڈالنا_روٹ, 저장소, نفاذ_کریں_حکم)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(بلڈ_راہ)) as 작업경로:
        صنف_راہ = Path(작업경로)
        نفاذ_کریں_حکم(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', صنف_راہ, '-sourcepath', صنف_راہ, '-d', صنف_راہ] + sorted((عکس_ڈالنا_روٹ / 'ماخذ_فائل').glob('*.java')) + [بلڈ_راہ / 'بنڈل.java', بلڈ_راہ / '예제꾸러미.java'])
        # فائل_کا_نام·شیل·ونڈو 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        دلائل_لڑی = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'کرنیل.چلائیں', '--heap-words', '1048576', '-o', بلڈ_راہ / 'kernel-java.c']
        for علامت_قدر, طریقہ_اندراج in sorted(برآمد_کریں_جدول.items()):
            دلائل_لڑی += ['--export', علامت_قدر + '=' + طریقہ_اندراج]
        نفاذ_کریں_حکم(دلائل_لڑی + sorted(صنف_راہ.glob('*.class')))
    (بلڈ_راہ / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    بنائیں_صارف_اسپیس(عکس_ڈالنا_روٹ, 저장소, 시언어번역기, 시플플번역기, 연결편집기, محفوظ_ٹول, 설정비트, نفاذ_کریں_حکم)
    نیٹ_ورک = بنائیں_نیٹ_ورک_48d29d6d(عکس_ڈالنا_روٹ, 시언어번역기, محفوظ_ٹول, 설정비트, نفاذ_کریں_حکم)
    원격사용 = بنائیں_بعید(عکس_ڈالنا_روٹ, 시언어번역기, محفوظ_ٹول, 설정비트, نفاذ_کریں_حکم)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', بلڈ_راہ]
    빌드작업 = [(시언어번역기, [], بلڈ_راہ / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], عکس_ڈالنا_روٹ / 'مشین/حکم_کی_تشریح_کرنے_والا.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], عکس_ڈالنا_روٹ / 'مشین/ویجٹ.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], بلڈ_راہ / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], عکس_ڈالنا_روٹ / 'مشین/بورڈ.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], عکس_ڈالنا_روٹ / 'مشین/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], عکس_ڈالنا_روٹ / 'مشین/صارف.c', 'user.o'),
            (시언어번역기, [], عکس_ڈالنا_روٹ / '부팅/اندراج_نقطہ_قدر.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'متصل_ہوں.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], عکس_ڈالنا_روٹ / '시험/فائل_کالز.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [فائل_اندراج for فائل_اندراج in 설정비트 if فائل_اندراج != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        نفاذ_کریں_حکم([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', بلڈ_راہ / 출력결과])
    نفاذ_کریں_حکم([محفوظ_ٹول, 'rcs', بلڈ_راہ / 'libposix-kor-arm64.a', بلڈ_راہ / 'posix.o'])
    نفاذ_کریں_حکم([연결편집기, '--gc-sections', '-T', عکس_ڈالنا_روٹ / '부팅/ربط_ترتیب.ld', '-Map', بلڈ_راہ / 'kernel.map', '-o', بلڈ_راہ / 'kernel.elf'] +
        [بلڈ_راہ / نام for نام in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', بلڈ_راہ / 'libposix-kor-arm64.a', نیٹ_ورک, 원격사용, بلڈ_راہ / 'remote/libassh.a', بلڈ_راہ / 'remote/libbearssl.a', '--end-group'])
    نفاذ_کریں_حکم([آبجیکٹ_فائل_تبدیل_کار, '-O', 'binary', بلڈ_راہ / 'kernel.elf', بلڈ_راہ / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'اردو.اپنا', 'korean_exceptions': 20,
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
    for نام in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][نام] = hashlib.sha256((بلڈ_راہ / نام).read_bytes()).hexdigest()
    (بلڈ_راہ / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', بلڈ_راہ / 'kernel8.img')


if __name__ == '__main__':
    چلائیں()
