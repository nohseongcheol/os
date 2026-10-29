#!/usr/bin/env python3
"""होस्ट javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from बनाउनुहोस्_प्रयोगकर्ता_स्थान import सिर्जना_प्रयोगकर्ता_स्थान
from बनाउनुहोस्_सञ्जाल import सिर्जना_सञ्जाल_48d29d6d
from 예제빌드 import 예제만들기
from बनाउनुहोस्_दूर import सिर्जना_दूर

परियोजना_रूट = Path(__file__).resolve().parents[1]
저장소 = परियोजना_रूट.parents[1]
बनाउनुहोस्_बाटो = परियोजना_रूट / 'build'


def कार्यान्वयन_गर्नुहोस्_आदेश(तर्क_विन्यास):
    subprocess.check_call([str(첫째값) for 첫째값 in तर्क_विन्यास], cwd=str(परियोजना_रूट))


def चलाउनुहोस्():
    बनाउनुहोस्_बाटो.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    वस्तु_फाइल_रुपान्तरणकर्ता = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    सङ्ग्रह_उपकरण = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for उपकरणहरू in ('javac', 시언어번역기, 시플플번역기, 연결편집기, वस्तु_फाइल_रुपान्तरणकर्ता, सङ्ग्रह_उपकरण):
        if not shutil.which(उपकरणहरू):
            raise SystemExit('필요한 बनाउनुहोस्_प्रणाली उपकरणहरू 없음: ' + उपकरणहरू)
    फन्ट_जानकारी = json.loads((परियोजना_रूट / 'vendor/terminal-font.json').read_text())
    फन्ट_लगत = (परियोजना_रूट / 'vendor/terminal-font.bin').read_bytes()
    if len(फन्ट_लगत) != 65616 * 32 or hashlib.sha256(फन्ट_लगत).hexdigest() != फन्ट_जानकारी['sha256']:
        raise SystemExit('टर्मिनल फन्ट_मान आकार/SHA256 불일치')
    निर्यात_गर्नुहोस्_तालिका = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'कर्णेल.작업', 'jfs_path_start': 'मेमोरी_फाइलहरू.बाटो_सुरु',
               'jfs_path_byte': 'मेमोरी_फाइलहरू.बाटो_बाइट', 'jfs_open': 'मेमोरी_फाइलहरू.खोल्नुहोस्',
               'jfs_read': 'मेमोरी_फाइलहरू.पढनुहोस्', 'jfs_write': 'मेमोरी_फाइलहरू.लेख्नुहोस्',
               'jfs_seek': 'मेमोरी_फाइलहरू.खोज्नुहोस्_राख्नुहोस्', 'jfs_close': 'मेमोरी_फाइलहरू.बन्दगर्नुहोस्',
               'jfs_size': 'मेमोरी_फाइलहरू.आकार', 'jfs_unlink': 'मेमोरी_फाइलहरू.지우기',
               'jfs_truncate': 'मेमोरी_फाइलहरू.सेट_लम्बाइ'}
    निर्यात_गर्नुहोस्_तालिका.update({'jfs_entry_count': 'मेमोरी_फाइलहरू.파일한도', 'jfs_entry_length': 'मेमोरी_फाइलहरू.공개이름길이', 'jfs_entry_byte': 'मेमोरी_फाइलहरू.공개이름바이트', 'jfs_entry_size': 'मेमोरी_फाइलहरू.공개파일크기'})
    निर्यात_गर्नुहोस्_तालिका.update({'jdraw_prepare': '화면합성.तयार_गर्नुहोस्', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.क्लिप',
        'jdraw_clip_value': '화면합성.क्लिप_मान', 'jdraw_begin': '화면합성.चलाउनुहोस्',
        'jdraw_end': '화면합성.समाप्त', 'jdraw_pixel': '화면합성.पेल',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.पोइन्टर'})
    निर्यात_गर्नुहोस्_तालिका.update({'jfs_mkdir': 'मेमोरी_फाइलहरू.सिर्जना_डाइरेक्टरी', 'jfs_rmdir': 'मेमोरी_फाइलहरू.हटाउनुहोस्_डाइरेक्टरी', 'jfs_kind': 'मेमोरी_फाइलहरू.항목종류'})
    निर्यात_गर्नुहोस्_तालिका.update({'jnet_socket': '되돌림망.सिर्जना_प्रविष्टि', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.पठाउनुहोस्',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.बन्दगर्नुहोस्'})
    निर्यात_गर्नुहोस्_तालिका.update({'jstream_create': 'प्रवाह_सञ्जाल.सिर्जना_प्रविष्टि', 'jstream_bind': 'प्रवाह_सञ्जाल.묶기', 'jstream_listen': 'प्रवाह_सञ्जाल.듣기', 'jstream_connect': 'प्रवाह_सञ्जाल.जडान', 'jstream_accept': 'प्रवाह_सञ्जाल.स्वीकार्नुहोस्_जडान', 'jstream_read': 'प्रवाह_सञ्जाल.पढनुहोस्', 'jstream_write': 'प्रवाह_सञ्जाल.लेख्नुहोस्', 'jstream_port': 'प्रवाह_सञ्जाल.창구읽기', 'jstream_peer': 'प्रवाह_सञ्जाल.상대창구읽기', 'jstream_close': 'प्रवाह_सञ्जाल.बन्दगर्नुहोस्'})
    for चिन्ह_मान in list(निर्यात_गर्नुहोस्_तालिका):
        if चिन्ह_मान.startswith('jstream_') or चिन्ह_मान.startswith('jnet_') and चिन्ह_मान not in ('jnet_put', 'jnet_get'):
            निर्यात_गर्नुहोस्_तालिका[चिन्ह_मान.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = निर्यात_गर्नुहोस्_तालिका.pop(चिन्ह_मान)
    예제들 = ['public final class पोको { public static void तयार_गर्नुहोस्() {']
    for मार्ग in sorted((परियोजना_रूट / '예제').iterdir()):
        if मार्ग.is_file():
            예제들.append('명령해석기.तथ्याङ्कित_फाइल(%s, %s);' %
                (json.dumps(मार्ग.name), json.dumps(मार्ग.read_text(encoding='utf-8'), ensure_ascii=True)))
    (बनाउनुहोस्_बाटो / 'पोको.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(परियोजना_रूट, 저장소, कार्यान्वयन_गर्नुहोस्_आदेश)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(बनाउनुहोस्_बाटो)) as 작업경로:
        वर्ग_बाटो = Path(작업경로)
        कार्यान्वयन_गर्नुहोस्_आदेश(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', वर्ग_बाटो, '-sourcepath', वर्ग_बाटो, '-d', वर्ग_बाटो] + sorted((परियोजना_रूट / 'स्रोत').glob('*.java')) + [बनाउनुहोस्_बाटो / 'पोको.java', बनाउनुहोस्_बाटो / '예제꾸러미.java'])
        # फाइल·शेल·सन्झ्याल 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        तर्क_विन्यास = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'कर्णेल.चलाउनुहोस्', '--heap-words', '1048576', '-o', बनाउनुहोस्_बाटो / 'kernel-java.c']
        for चिन्ह_मान, तरिका_प्रविष्टि in sorted(निर्यात_गर्नुहोस्_तालिका.items()):
            तर्क_विन्यास += ['--export', चिन्ह_मान + '=' + तरिका_प्रविष्टि]
        कार्यान्वयन_गर्नुहोस्_आदेश(तर्क_विन्यास + sorted(वर्ग_बाटो.glob('*.class')))
    (बनाउनुहोस्_बाटो / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    सिर्जना_प्रयोगकर्ता_स्थान(परियोजना_रूट, 저장소, 시언어번역기, 시플플번역기, 연결편집기, सङ्ग्रह_उपकरण, 설정비트, कार्यान्वयन_गर्नुहोस्_आदेश)
    सञ्जाल = सिर्जना_सञ्जाल_48d29d6d(परियोजना_रूट, 시언어번역기, सङ्ग्रह_उपकरण, 설정비트, कार्यान्वयन_गर्नुहोस्_आदेश)
    원격사용 = सिर्जना_दूर(परियोजना_रूट, 시언어번역기, सङ्ग्रह_उपकरण, 설정비트, कार्यान्वयन_गर्नुहोस्_आदेश)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', बनाउनुहोस्_बाटो]
    빌드작업 = [(시언어번역기, [], बनाउनुहोस्_बाटो / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], परियोजना_रूट / 'मेशिन/टर्मिनल.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], परियोजना_रूट / 'मेशिन/विजेट.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], बनाउनुहोस्_बाटो / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], परियोजना_रूट / 'मेशिन/बोर्ड.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], परियोजना_रूट / 'मेशिन/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], परियोजना_रूट / 'मेशिन/प्रयोगकर्ता.c', 'user.o'),
            (시언어번역기, [], परियोजना_रूट / '부팅/प्रविष्टि_अंक_मान.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'जडान.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], परियोजना_रूट / '시험/फाइल_कलहरू.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [फाइल_प्रविष्टि for फाइल_प्रविष्टि in 설정비트 if फाइल_प्रविष्टि != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        कार्यान्वयन_गर्नुहोस्_आदेश([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', बनाउनुहोस्_बाटो / 출력결과])
    कार्यान्वयन_गर्नुहोस्_आदेश([सङ्ग्रह_उपकरण, 'rcs', बनाउनुहोस्_बाटो / 'libposix-kor-arm64.a', बनाउनुहोस्_बाटो / 'posix.o'])
    कार्यान्वयन_गर्नुहोस्_आदेश([연결편집기, '--gc-sections', '-T', परियोजना_रूट / '부팅/लिङ्क_लेआउट.ld', '-Map', बनाउनुहोस्_बाटो / 'kernel.map', '-o', बनाउनुहोस्_बाटो / 'kernel.elf'] +
        [बनाउनुहोस्_बाटो / नाम for नाम in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', बनाउनुहोस्_बाटो / 'libposix-kor-arm64.a', सञ्जाल, 원격사용, बनाउनुहोस्_बाटो / 'remote/libassh.a', बनाउनुहोस्_बाटो / 'remote/libbearssl.a', '--end-group'])
    कार्यान्वयन_गर्नुहोस्_आदेश([वस्तु_फाइल_रुपान्तरणकर्ता, '-O', 'binary', बनाउनुहोस्_बाटो / 'kernel.elf', बनाउनुहोस्_बाटो / 'kernel8.img'])
    꾸러미명세 = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'नेपाली.निज', 'korean_exceptions': 20,
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
        꾸러미명세['sha256'][नाम] = hashlib.sha256((बनाउनुहोस्_बाटो / नाम).read_bytes()).hexdigest()
    (बनाउनुहोस्_बाटो / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', बनाउनुहोस्_बाटो / 'kernel8.img')


if __name__ == '__main__':
    चलाउनुहोस्()
