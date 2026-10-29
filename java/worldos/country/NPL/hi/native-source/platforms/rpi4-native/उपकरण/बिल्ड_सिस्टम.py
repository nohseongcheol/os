#!/usr/bin/env python3
"""आयोजक javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from बिल्ड_उपयोगकर्ता_स्थान import बनाएँ_उपयोगकर्ता_स्थान
from बिल्ड_नेटवर्क import बनाएँ_नेटवर्क
from 예제빌드 import 예제만들기
from बिल्ड_दूरस्थ import बनाएँ_दूरस्थ

प्रोजेक्ट_करें_मूल = Path(__file__).resolve().parents[1]
संग्रह_मूल = प्रोजेक्ट_करें_मूल.parents[1]
बिल्ड_पथ = प्रोजेक्ट_करें_मूल / 'build'


def निष्पादित_करें_आदेश(तर्क_सरणी):
    subprocess.check_call([str(첫째값) for 첫째값 in तर्क_सरणी], cwd=str(प्रोजेक्ट_करें_मूल))


def चलाएँ():
    बिल्ड_पथ.mkdir(exist_ok=True)
    सी_कंपाइलर = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ऑब्जेक्ट_फ़ाइल_परिर्वतक = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    संग्रह_उपकरण = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for उपकरण in ('javac', सी_कंपाइलर, 시플플번역기, 연결편집기, ऑब्जेक्ट_फ़ाइल_परिर्वतक, संग्रह_उपकरण):
        if not shutil.which(उपकरण):
            raise SystemExit('필요한 बिल्ड_सिस्टम उपकरण 없음: ' + उपकरण)
    फ़ॉन्ट_जानकारी = json.loads((प्रोजेक्ट_करें_मूल / 'vendor/terminal-font.json').read_text())
    फ़ॉन्ट_डेटा = (प्रोजेक्ट_करें_मूल / 'vendor/terminal-font.bin').read_bytes()
    if len(फ़ॉन्ट_डेटा) != 65616 * 32 or hashlib.sha256(फ़ॉन्ट_डेटा).hexdigest() != फ़ॉन्ट_जानकारी['sha256']:
        raise SystemExit('आदेशपटल फ़ॉन्ट_मान आकार/SHA256 불일치')
    निर्यात_करें_तालिका = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.निर्गम', 'jshell_input': '셸입출력.입력', 'java_task': 'कर्नेल.작업', 'jfs_path_start': 'मेमोरी_फ़ाइलें.पथ_प्रारंभ',
               'jfs_path_byte': 'मेमोरी_फ़ाइलें.पथ_बाइट', 'jfs_open': 'मेमोरी_फ़ाइलें.खोलें',
               'jfs_read': 'मेमोरी_फ़ाइलें.पढ़ें', 'jfs_write': 'मेमोरी_फ़ाइलें.लिखें',
               'jfs_seek': 'मेमोरी_फ़ाइलें.खोजें_पद', 'jfs_close': 'मेमोरी_फ़ाइलें.बंदकरें',
               'jfs_size': 'मेमोरी_फ़ाइलें.आकार', 'jfs_unlink': 'मेमोरी_फ़ाइलें.मिटाएँ_एन्ट्री',
               'jfs_truncate': 'मेमोरी_फ़ाइलें.길이정하기'}
    निर्यात_करें_तालिका.update({'jfs_entry_count': 'मेमोरी_फ़ाइलें.파일한도', 'jfs_entry_length': 'मेमोरी_फ़ाइलें.공개이름길이', 'jfs_entry_byte': 'मेमोरी_फ़ाइलें.공개이름바이트', 'jfs_entry_size': 'मेमोरी_फ़ाइलें.공개파일크기'})
    निर्यात_करें_तालिका.update({'jdraw_prepare': 'पटलसंयोजन.준비', 'jdraw_width': 'पटलसंयोजन.너비얻기',
        'jdraw_height': 'पटलसंयोजन.높이얻기', 'jdraw_count_low': 'पटलसंयोजन.기록아래얻기',
        'jdraw_count_high': 'पटलसंयोजन.기록위얻기', 'jdraw_clip': 'पटलसंयोजन.क्लिप',
        'jdraw_clip_value': 'पटलसंयोजन.क्लिप_मान', 'jdraw_begin': 'पटलसंयोजन.चलाएँ',
        'jdraw_end': 'पटलसंयोजन.पूर्ण', 'jdraw_pixel': 'पटलसंयोजन.पिक्सेल',
        'jdraw_rectangle': 'पटलसंयोजन.रेक्_टेंगल_भरण', 'jdraw_pointer': 'पटलसंयोजन.सूचक'})
    निर्यात_करें_तालिका.update({'jfs_mkdir': 'मेमोरी_फ़ाइलें.बनाएँ_डायरेक्टरी', 'jfs_rmdir': 'मेमोरी_फ़ाइलें.निकालें_डायरेक्टरी', 'jfs_kind': 'मेमोरी_फ़ाइलें.항목종류'})
    निर्यात_करें_तालिका.update({'jnet_socket': 'लूपबैक_नेटवर्क.बनाएँ_एन्ट्री', 'jnet_bind': 'लूपबैक_नेटवर्क.बाइंड_करें_एंडपॉइंट',
        'jnet_put': 'लूपबैक_नेटवर्क.자료넣기', 'jnet_get': 'लूपबैक_नेटवर्क.पढें_डेटा', 'jnet_send': 'लूपबैक_नेटवर्क.भेजें',
        'jnet_recv': 'लूपबैक_नेटवर्क.받기', 'jnet_port': 'लूपबैक_नेटवर्क.पढें_एंडपॉइंट_पोर्ट', 'jnet_address': 'लूपबैक_नेटवर्क.पढें_पता',
        'jnet_peer': 'लूपबैक_नेटवर्क.प्रेषक_एंडपॉइंट', 'jnet_close': 'लूपबैक_नेटवर्क.बंदकरें'})
    निर्यात_करें_तालिका.update({'jstream_create': 'स्ट्रीम_नेटवर्क.बनाएँ_एन्ट्री', 'jstream_bind': 'स्ट्रीम_नेटवर्क.बाइंड_करें_एंडपॉइंट', 'jstream_listen': 'स्ट्रीम_नेटवर्क.सुनिए_एंडपॉइंट', 'jstream_connect': 'स्ट्रीम_नेटवर्क.जोड़ना', 'jstream_accept': 'स्ट्रीम_नेटवर्क.स्वीकार_करें_कनेक्शन', 'jstream_read': 'स्ट्रीम_नेटवर्क.पढ़ें', 'jstream_write': 'स्ट्रीम_नेटवर्क.लिखें', 'jstream_port': 'स्ट्रीम_नेटवर्क.पढें_एंडपॉइंट_पोर्ट', 'jstream_peer': 'स्ट्रीम_नेटवर्क.पढें_पीअर_पोर्ट', 'jstream_close': 'स्ट्रीम_नेटवर्क.बंदकरें'})
    for प्रतीक_मान in list(निर्यात_करें_तालिका):
        if प्रतीक_मान.startswith('jstream_') or प्रतीक_मान.startswith('jnet_') and प्रतीक_मान not in ('jnet_put', 'jnet_get'):
            निर्यात_करें_तालिका[प्रतीक_मान.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = निर्यात_करें_तालिका.pop(प्रतीक_मान)
    예제들 = ['public final class बंडल { public static void 준비() {']
    for पथ in sorted((प्रोजेक्ट_करें_मूल / '예제').iterdir()):
        if पथ.is_file():
            예제들.append('आदेश_व्याख्याकार.정적파일(%s, %s);' %
                (json.dumps(पथ.name), json.dumps(पथ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (बिल्ड_पथ / 'बंडल.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(प्रोजेक्ट_करें_मूल, संग्रह_मूल, निष्पादित_करें_आदेश)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(बिल्ड_पथ)) as 작업경로:
        कक्षा_पथ = Path(작업경로)
        निष्पादित_करें_आदेश(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', कक्षा_पथ, '-sourcepath', कक्षा_पथ, '-d', कक्षा_पथ] + sorted((प्रोजेक्ट_करें_मूल / 'स्रोत').glob('*.java')) + [बिल्ड_पथ / 'बंडल.java', बिल्ड_पथ / '예제꾸러미.java'])
        # संचिका·शेल·खिड़की 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        तर्क_सरणी = ['sh', संग्रह_मूल / 'compiler/미리번역.sh', '--entry', 'कर्नेल.चलाएँ', '--heap-words', '1048576', '-o', बिल्ड_पथ / 'kernel-java.c']
        for प्रतीक_मान, विधि_एन्ट्री in sorted(निर्यात_करें_तालिका.items()):
            तर्क_सरणी += ['--export', प्रतीक_मान + '=' + विधि_एन्ट्री]
        निष्पादित_करें_आदेश(तर्क_सरणी + sorted(कक्षा_पथ.glob('*.class')))
    (बिल्ड_पथ / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = संग्रह_मूल / 'posix-kor/arm64-native'
    बनाएँ_उपयोगकर्ता_स्थान(प्रोजेक्ट_करें_मूल, संग्रह_मूल, सी_कंपाइलर, 시플플번역기, 연결편집기, संग्रह_उपकरण, कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस, निष्पादित_करें_आदेश)
    नेटवर्क = बनाएँ_नेटवर्क(प्रोजेक्ट_करें_मूल, सी_कंपाइलर, संग्रह_उपकरण, कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस, निष्पादित_करें_आदेश)
    원격사용 = बनाएँ_दूरस्थ(प्रोजेक्ट_करें_मूल, सी_कंपाइलर, संग्रह_उपकरण, कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस, निष्पादित_करें_आदेश)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', बिल्ड_पथ]
    빌드작업 = [(सी_कंपाइलर, [], बिल्ड_पथ / 'terminal-font.S', 'font.o'),
            (सी_कंपाइलर, ['-std=c11', '-Wall', '-Wextra', '-Werror'], प्रोजेक्ट_करें_मूल / 'यंत्र/आदेशपटल.c', 'terminal.o'),
            (सी_कंपाइलर, ['-std=c11', '-Wall', '-Wextra', '-Werror'], प्रोजेक्ट_करें_मूल / 'यंत्र/विजेट.c', 'widgets.o'),
            (सी_कंपाइलर, ['-std=c11'], बिल्ड_पथ / 'kernel-java.c', 'java.o'),
            (सी_कंपाइलर, ['-std=c11', '-Wall', '-Wextra', '-Werror'], प्रोजेक्ट_करें_मूल / 'यंत्र/बोर्ड.c', 'board.o'),
            (सी_कंपाइलर, ['-std=c11', '-Wall', '-Wextra', '-Werror'], प्रोजेक्ट_करें_मूल / 'यंत्र/화면그림.c', 'drawing.o'),
            (सी_कंपाइलर, ['-std=c11', '-Wall', '-Wextra', '-Werror'], प्रोजेक्ट_करें_मूल / 'यंत्र/उपयोगकर्ता.c', 'user.o'),
            (सी_कंपाइलर, [], प्रोजेक्ट_करें_मूल / '부팅/प्रवेश_बिदुं_मान.S', 'entry.o'),
            (सी_कंपाइलर, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'जोड़ना.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], प्रोजेक्ट_करें_मूल / '시험/फ़ाइल_कॉल्स.cpp', 'cpp.o')]
    for कंपाइलर_उपकरण, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [फ़ाइल_एन्ट्री for फ़ाइल_एन्ट्री in कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस if फ़ाइल_एन्ट्री != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else कॉन्फ़िगरेशन_बैकग्राउंड_इंटेलिजेंट_ट्रांसफ़र_सर्विस
        निष्पादित_करें_आदेश([कंपाइलर_उपकरण] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', बिल्ड_पथ / 출력결과])
    निष्पादित_करें_आदेश([संग्रह_उपकरण, 'rcs', बिल्ड_पथ / 'libposix-kor-arm64.a', बिल्ड_पथ / 'posix.o'])
    निष्पादित_करें_आदेश([연결편집기, '--gc-sections', '-T', प्रोजेक्ट_करें_मूल / '부팅/लिंक_लेआउट.ld', '-Map', बिल्ड_पथ / 'kernel.map', '-o', बिल्ड_पथ / 'kernel.elf'] +
        [बिल्ड_पथ / नाम for नाम in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', बिल्ड_पथ / 'libposix-kor-arm64.a', नेटवर्क, 원격사용, बिल्ड_पथ / 'remote/libassh.a', बिल्ड_पथ / 'remote/libbearssl.a', '--end-group'])
    निष्पादित_करें_आदेश([ऑब्जेक्ट_फ़ाइल_परिर्वतक, '-O', 'binary', बिल्ड_पथ / 'kernel.elf', बिल्ड_पथ / 'kernel8.img'])
    बंडल_सूची = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'हिंदी.निज', 'korean_exceptions': 20,
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
    for नाम in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        बंडल_सूची['sha256'][नाम] = hashlib.sha256((बिल्ड_पथ / नाम).read_bytes()).hexdigest()
    (बिल्ड_पथ / 'build.json').write_text(json.dumps(बंडल_सूची, indent=2) + '\n')
    print('완료:', बिल्ड_पथ / 'kernel8.img')


if __name__ == '__main__':
    चलाएँ()
