#!/usr/bin/env python3
"""مضيف javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from بنية_مستخدم_مساحة import فتح_مستخدم_مساحة
from بنية_شبكة import فتح_شبكة_48d29d6d
from 예제빌드 import 예제만들기
from بنية_بعيد import فتح_بعيد

يعرض_جذر = Path(__file__).resolve().parents[1]
مستودع_جذر = يعرض_جذر.parents[1]
بنية_مسار = يعرض_جذر / 'build'


def ينفذ_أمر(وسيطة_صفيف):
    subprocess.check_call([str(첫째값) for 첫째값 in وسيطة_صفيف], cwd=str(يعرض_جذر))


def تشغيل():
    بنية_مسار.mkdir(exist_ok=True)
    الرمز_البريدي_محول_برمجي = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    برنامج_ربط_أداة = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    عنصر_ملف_محوّل = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    أرشيف_أداة = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for أدوات in ('javac', الرمز_البريدي_محول_برمجي, 시플플번역기, برنامج_ربط_أداة, عنصر_ملف_محوّل, أرشيف_أداة):
        if not shutil.which(أدوات):
            raise SystemExit('필요한 بنية_نظام أدوات 없음: ' + أدوات)
    خط_معلومات = json.loads((يعرض_جذر / 'vendor/terminal-font.json').read_text())
    خط_بيانات = (يعرض_جذر / 'vendor/terminal-font.bin').read_bytes()
    if len(خط_بيانات) != 65616 * 32 or hashlib.sha256(خط_بيانات).hexdigest() != خط_معلومات['sha256']:
        raise SystemExit('طرفية خط_قيمة حجم/SHA256 불일치')
    تصدير_جدول = {'jshell_interactive': '셸입출력.أنظمة_المعلومات_تفاعلي', 'jshell_output': '셸입출력.مخرجات', 'jshell_input': '셸입출력.إدخال_قيمة', 'java_task': 'نواة.작업', 'jfs_path_start': 'ذاكرة_الملفات.مسار_بدء',
               'jfs_path_byte': 'ذاكرة_الملفات.مسار_بايت', 'jfs_open': 'ذاكرة_الملفات.فتح',
               'jfs_read': 'ذاكرة_الملفات.قراءة', 'jfs_write': 'ذاكرة_الملفات.كتابة',
               'jfs_seek': 'ذاكرة_الملفات.يبحث_منصب', 'jfs_close': 'ذاكرة_الملفات.إغلاق',
               'jfs_size': 'ذاكرة_الملفات.حجم', 'jfs_unlink': 'ذاكرة_الملفات.مسح_إدخال',
               'jfs_truncate': 'ذاكرة_الملفات.길이정하기'}
    تصدير_جدول.update({'jfs_entry_count': 'ذاكرة_الملفات.파일한도', 'jfs_entry_length': 'ذاكرة_الملفات.공개이름길이', 'jfs_entry_byte': 'ذاكرة_الملفات.공개이름바이트', 'jfs_entry_size': 'ذاكرة_الملفات.공개파일크기'})
    تصدير_جدول.update({'jdraw_prepare': 'تركيبالشاشة.إعداد', 'jdraw_width': 'تركيبالشاشة.너비얻기',
        'jdraw_height': 'تركيبالشاشة.الحصول_على_ارتفاع', 'jdraw_count_low': 'تركيبالشاشة.기록아래얻기',
        'jdraw_count_high': 'تركيبالشاشة.기록위얻기', 'jdraw_clip': 'تركيبالشاشة.يقص',
        'jdraw_clip_value': 'تركيبالشاشة.يقص_قيمة', 'jdraw_begin': 'تركيبالشاشة.تشغيل',
        'jdraw_end': 'تركيبالشاشة.إنهاء', 'jdraw_pixel': 'تركيبالشاشة.عنصر_صورة',
        'jdraw_rectangle': 'تركيبالشاشة.مستطيل_يملأ', 'jdraw_pointer': 'تركيبالشاشة.مؤشر'})
    تصدير_جدول.update({'jfs_mkdir': 'ذاكرة_الملفات.فتح_دليل', 'jfs_rmdir': 'ذاكرة_الملفات.يزيل_دليل', 'jfs_kind': 'ذاكرة_الملفات.항목종류'})
    تصدير_جدول.update({'jnet_socket': 'استرجاع_شبكة.فتح_إدخال', 'jnet_bind': 'استرجاع_شبكة.يربط_المشارك',
        'jnet_put': 'استرجاع_شبكة.자료넣기', 'jnet_get': 'استرجاع_شبكة.يقرأ_بيانات', 'jnet_send': 'استرجاع_شبكة.يرسل',
        'jnet_recv': 'استرجاع_شبكة.يستلم', 'jnet_port': 'استرجاع_شبكة.يقرأ_المشارك_منفذ', 'jnet_address': 'استرجاع_شبكة.يقرأ_عنوان',
        'jnet_peer': 'استرجاع_شبكة.مرسل_المشارك', 'jnet_close': 'استرجاع_شبكة.إغلاق'})
    تصدير_جدول.update({'jstream_create': 'بث_شبكة.فتح_إدخال', 'jstream_bind': 'بث_شبكة.يربط_المشارك', 'jstream_listen': 'بث_شبكة.انصات_المشارك', 'jstream_connect': 'بث_شبكة.اتصال', 'jstream_accept': 'بث_شبكة.قبول_صديق', 'jstream_read': 'بث_شبكة.قراءة', 'jstream_write': 'بث_شبكة.كتابة', 'jstream_port': 'بث_شبكة.يقرأ_المشارك_منفذ', 'jstream_peer': 'بث_شبكة.يقرأ_نظير_منفذ', 'jstream_close': 'بث_شبكة.إغلاق'})
    for رمز_قيمة in list(تصدير_جدول):
        if رمز_قيمة.startswith('jstream_') or رمز_قيمة.startswith('jnet_') and رمز_قيمة not in ('jnet_put', 'jnet_get'):
            تصدير_جدول[رمز_قيمة.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = تصدير_جدول.pop(رمز_قيمة)
    예제들 = ['public final class يُجمع { public static void إعداد() {']
    for مسار in sorted((يعرض_جذر / '예제').iterdir()):
        if مسار.is_file():
            예제들.append('مفسر_الأوامر.ثابت_ملف(%s, %s);' %
                (json.dumps(مسار.name), json.dumps(مسار.read_text(encoding='utf-8'), ensure_ascii=True)))
    (بنية_مسار / 'يُجمع.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(يعرض_جذر, مستودع_جذر, ينفذ_أمر)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(بنية_مسار)) as 작업경로:
        فئة_مسار = Path(작업경로)
        ينفذ_أمر(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', فئة_مسار, '-sourcepath', فئة_مسار, '-d', فئة_مسار] + sorted((يعرض_جذر / 'مصدر').glob('*.java')) + [بنية_مسار / 'يُجمع.java', بنية_مسار / '예제꾸러미.java'])
        # ملف·셸·نافذة 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        وسيطة_صفيف = ['sh', مستودع_جذر / 'compiler/미리번역.sh', '--entry', 'نواة.تشغيل', '--heap-words', '1048576', '-o', بنية_مسار / 'kernel-java.c']
        for رمز_قيمة, أسلوب_إدخال in sorted(تصدير_جدول.items()):
            وسيطة_صفيف += ['--export', رمز_قيمة + '=' + أسلوب_إدخال]
        ينفذ_أمر(وسيطة_صفيف + sorted(فئة_مسار.glob('*.class')))
    (بنية_مسار / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    تكوين_خدمة_النقل_الذكي_في_الخلفية = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = مستودع_جذر / 'posix-kor/arm64-native'
    فتح_مستخدم_مساحة(يعرض_جذر, مستودع_جذر, الرمز_البريدي_محول_برمجي, 시플플번역기, برنامج_ربط_أداة, أرشيف_أداة, تكوين_خدمة_النقل_الذكي_في_الخلفية, ينفذ_أمر)
    شبكة = فتح_شبكة_48d29d6d(يعرض_جذر, الرمز_البريدي_محول_برمجي, أرشيف_أداة, تكوين_خدمة_النقل_الذكي_في_الخلفية, ينفذ_أمر)
    بعيد_يستخدم = فتح_بعيد(يعرض_جذر, الرمز_البريدي_محول_برمجي, أرشيف_أداة, تكوين_خدمة_النقل_الذكي_في_الخلفية, ينفذ_أمر)
    포함인수 = ['-I', 포직스경로 / 'تصريحات', '-I', بنية_مسار]
    빌드작업 = [(الرمز_البريدي_محول_برمجي, [], بنية_مسار / 'terminal-font.S', 'font.o'),
            (الرمز_البريدي_محول_برمجي, ['-std=c11', '-Wall', '-Wextra', '-Werror'], يعرض_جذر / 'جهاز/طرفية.c', 'terminal.o'),
            (الرمز_البريدي_محول_برمجي, ['-std=c11', '-Wall', '-Wextra', '-Werror'], يعرض_جذر / 'جهاز/عنصر_شاشة.c', 'widgets.o'),
            (الرمز_البريدي_محول_برمجي, ['-std=c11'], بنية_مسار / 'kernel-java.c', 'java.o'),
            (الرمز_البريدي_محول_برمجي, ['-std=c11', '-Wall', '-Wextra', '-Werror'], يعرض_جذر / 'جهاز/لوحة.c', 'board.o'),
            (الرمز_البريدي_محول_برمجي, ['-std=c11', '-Wall', '-Wextra', '-Werror'], يعرض_جذر / 'جهاز/화면그림.c', 'drawing.o'),
            (الرمز_البريدي_محول_برمجي, ['-std=c11', '-Wall', '-Wextra', '-Werror'], يعرض_جذر / 'جهاز/فضاء_المستخدم.c', 'user.o'),
            (الرمز_البريدي_محول_برمجي, [], يعرض_جذر / 'إقلاع_الآلة/نقطة_الإدخال_قيمة.S', 'entry.o'),
            (الرمز_البريدي_محول_برمجي, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'اتصال.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], يعرض_جذر / 'اختبارات/ملف_المكالمات.cpp', 'cpp.o')]
    for محول_برمجي_أداة, 추가영역, 원본자료, الناتج in 빌드작업:
        원본설정 = [ملف_إدخال_3d0c1245 for ملف_إدخال_3d0c1245 in تكوين_خدمة_النقل_الذكي_في_الخلفية if ملف_إدخال_3d0c1245 != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else تكوين_خدمة_النقل_الذكي_في_الخلفية
        ينفذ_أمر([محول_برمجي_أداة] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', بنية_مسار / الناتج])
    ينفذ_أمر([أرشيف_أداة, 'rcs', بنية_مسار / 'libposix-kor-arm64.a', بنية_مسار / 'posix.o'])
    ينفذ_أمر([برنامج_ربط_أداة, '--gc-sections', '-T', يعرض_جذر / 'إقلاع_الآلة/تخطيط_الربط.ld', '-Map', بنية_مسار / 'kernel.map', '-o', بنية_مسار / 'kernel.elf'] +
        [بنية_مسار / اسم for اسم in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', بنية_مسار / 'libposix-kor-arm64.a', شبكة, بعيد_يستخدم, بنية_مسار / 'remote/libassh.a', بنية_مسار / 'remote/libbearssl.a', '--end-group'])
    ينفذ_أمر([عنصر_ملف_محوّل, '-O', 'binary', بنية_مسار / 'kernel.elf', بنية_مسار / 'kernel8.img'])
    يُجمع_بيان = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'العربية.ذاتي', 'korean_exceptions': 20,
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
    for اسم in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        يُجمع_بيان['sha256'][اسم] = hashlib.sha256((بنية_مسار / اسم).read_bytes()).hexdigest()
    (بنية_مسار / 'build.json').write_text(json.dumps(يُجمع_بيان, indent=2) + '\n')
    print('완료:', بنية_مسار / 'kernel8.img')


if __name__ == '__main__':
    تشغيل()
