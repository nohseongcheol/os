#!/usr/bin/env python3
"""येजमान javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from दाळचे_उपेगकर्तो_SPACE import निर्माण_करचें_उपेगकर्तो_SPACE
from दाळचे_नॅटवर्क import निर्माण_करचें_नॅटवर्क
from 예제빌드 import 예제만들기
from दाळचे_दुर्मीळ import निर्माण_करचें_दुर्मीळ

प्रॉजॅक्ट_रूट = Path(__file__).resolve().parents[1]
저장소 = प्रॉजॅक्ट_रूट.parents[1]
दाळचे_पाथ = प्रॉजॅक्ट_रूट / 'build'


def पाळो_दिवचो_आदेश(युक्तीवाद_क्रम):
    subprocess.check_call([str(첫째값) for 첫째값 in युक्तीवाद_क्रम], cwd=str(प्रॉजॅक्ट_रूट))


def चलोवप():
    दाळचे_पाथ.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ऑब्जॅक्ट_फायल_रूपांतर_करपी = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    संग्रह_साधन = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for साधनां in ('javac', 시언어번역기, 시플플번역기, 연결편집기, ऑब्जॅक्ट_फायल_रूपांतर_करपी, संग्रह_साधन):
        if not shutil.which(साधनां):
            raise SystemExit('필요한 दाळचे_प्रणाली साधनां 없음: ' + साधनां)
    फाँट_म्हायती = json.loads((प्रॉजॅक्ट_रूट / 'vendor/terminal-font.json').read_text())
    फाँट_डेटा = (प्रॉजॅक्ट_रूट / 'vendor/terminal-font.bin').read_bytes()
    if len(फाँट_डेटा) != 65616 * 32 or hashlib.sha256(फाँट_डेटा).hexdigest() != फाँट_म्हायती['sha256']:
        raise SystemExit('टर्मिनल फाँट_मोल आवाठ/SHA256 불일치')
    निर्यात_तकटो = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.출력', 'jshell_input': '셸입출력.입력', 'java_task': 'कर्नेल.작업', 'jfs_path_start': 'मेमरी_फायली.पाथ_Start',
               'jfs_path_byte': 'मेमरी_फायली.पाथ_बायट', 'jfs_open': 'मेमरी_फायली.उगडचें',
               'jfs_read': 'मेमरी_फायली.읽기', 'jfs_write': 'मेमरी_फायली.बरोवचें',
               'jfs_seek': 'मेमरी_फायली.सोद_स्थिती', 'jfs_close': 'मेमरी_फायली.शेवट',
               'jfs_size': 'मेमरी_फायली.आवाठ', 'jfs_unlink': 'मेमरी_फायली.지우기',
               'jfs_truncate': 'मेमरी_फायली.संच_लांबाय'}
    निर्यात_तकटो.update({'jfs_entry_count': 'मेमरी_फायली.파일한도', 'jfs_entry_length': 'मेमरी_फायली.공개이름길이', 'jfs_entry_byte': 'मेमरी_फायली.공개이름바이트', 'jfs_entry_size': 'मेमरी_फायली.공개파일크기'})
    निर्यात_तकटो.update({'jdraw_prepare': '화면합성.तयार_करचें_9ce364fc', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.क्लिप',
        'jdraw_clip_value': '화면합성.क्लिप_मोल', 'jdraw_begin': '화면합성.चलोवप',
        'jdraw_end': '화면합성.समाप्त', 'jdraw_pixel': '화면합성.पिक्सॅल',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.पॉयंटर'})
    निर्यात_तकटो.update({'jfs_mkdir': 'मेमरी_फायली.निर्माण_करचें_नामावळ', 'jfs_rmdir': 'मेमरी_फायली.काडचें_नामावळ', 'jfs_kind': 'मेमरी_फायली.항목종류'})
    निर्यात_तकटो.update({'jnet_socket': '되돌림망.निर्माण_करचें_प्रवेश', 'jnet_bind': '되돌림망.묶기',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.धाडचें',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.보낸곳', 'jnet_close': '되돌림망.शेवट'})
    निर्यात_तकटो.update({'jstream_create': 'Stream_नॅटवर्क.निर्माण_करचें_प्रवेश', 'jstream_bind': 'Stream_नॅटवर्क.묶기', 'jstream_listen': 'Stream_नॅटवर्क.듣기', 'jstream_connect': 'Stream_नॅटवर्क.कनॅक्ट', 'jstream_accept': 'Stream_नॅटवर्क.स्विकारचें_कनॅक्शन', 'jstream_read': 'Stream_नॅटवर्क.읽기', 'jstream_write': 'Stream_नॅटवर्क.बरोवचें', 'jstream_port': 'Stream_नॅटवर्क.창구읽기', 'jstream_peer': 'Stream_नॅटवर्क.상대창구읽기', 'jstream_close': 'Stream_नॅटवर्क.शेवट'})
    for चिन्न_मोल in list(निर्यात_तकटो):
        if चिन्न_मोल.startswith('jstream_') or चिन्न_मोल.startswith('jnet_') and चिन्न_मोल not in ('jnet_put', 'jnet_get'):
            निर्यात_तकटो[चिन्न_मोल.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = निर्यात_तकटो.pop(चिन्न_मोल)
    예제들 = ['public final class रास { public static void तयार_करचें_9ce364fc() {']
    for पाथ in sorted((प्रॉजॅक्ट_रूट / '예제').iterdir()):
        if पाथ.is_file():
            예제들.append('명령해석기.थीर_फायल(%s, %s);' %
                (json.dumps(पाथ.name), json.dumps(पाथ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (दाळचे_पाथ / 'रास.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(प्रॉजॅक्ट_रूट, 저장소, पाळो_दिवचो_आदेश)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(दाळचे_पाथ)) as 작업경로:
        वर्ग_पाथ = Path(작업경로)
        पाळो_दिवचो_आदेश(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', वर्ग_पाथ, '-sourcepath', वर्ग_पाथ, '-d', वर्ग_पाथ] + sorted((प्रॉजॅक्ट_रूट / 'स्त्रोत').glob('*.java')) + [दाळचे_पाथ / 'रास.java', दाळचे_पाथ / '예제꾸러미.java'])
        # फायल·शॅल·विंडो 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        युक्तीवाद_क्रम = ['sh', 저장소 / 'compiler/미리번역.sh', '--entry', 'कर्नेल.चलोवप', '--heap-words', '1048576', '-o', दाळचे_पाथ / 'kernel-java.c']
        for चिन्न_मोल, पद्दत_प्रवेश in sorted(निर्यात_तकटो.items()):
            युक्तीवाद_क्रम += ['--export', चिन्न_मोल + '=' + पद्दत_प्रवेश]
        पाळो_दिवचो_आदेश(युक्तीवाद_क्रम + sorted(वर्ग_पाथ.glob('*.class')))
    (दाळचे_पाथ / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = 저장소 / 'posix-kor/arm64-native'
    निर्माण_करचें_उपेगकर्तो_SPACE(प्रॉजॅक्ट_रूट, 저장소, 시언어번역기, 시플플번역기, 연결편집기, संग्रह_साधन, 설정비트, पाळो_दिवचो_आदेश)
    नॅटवर्क = निर्माण_करचें_नॅटवर्क(प्रॉजॅक्ट_रूट, 시언어번역기, संग्रह_साधन, 설정비트, पाळो_दिवचो_आदेश)
    원격사용 = निर्माण_करचें_दुर्मीळ(प्रॉजॅक्ट_रूट, 시언어번역기, संग्रह_साधन, 설정비트, पाळो_दिवचो_आदेश)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', दाळचे_पाथ]
    빌드작업 = [(시언어번역기, [], दाळचे_पाथ / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], प्रॉजॅक्ट_रूट / 'यंत्र/टर्मिनल.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], प्रॉजॅक्ट_रूट / 'यंत्र/विजीट.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], दाळचे_पाथ / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], प्रॉजॅक्ट_रूट / 'यंत्र/बोर्ड.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], प्रॉजॅक्ट_रूट / 'यंत्र/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], प्रॉजॅक्ट_रूट / 'यंत्र/उपेगकर्तो.c', 'user.o'),
            (시언어번역기, [], प्रॉजॅक्ट_रूट / '부팅/प्रवेश_पॉयंट_मोल.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'कनॅक्ट.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], प्रॉजॅक्ट_रूट / '시험/फायल_कॉलां.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [फायल_प्रवेश for फायल_प्रवेश in 설정비트 if फायल_प्रवेश != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        पाळो_दिवचो_आदेश([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', दाळचे_पाथ / 출력결과])
    पाळो_दिवचो_आदेश([संग्रह_साधन, 'rcs', दाळचे_पाथ / 'libposix-kor-arm64.a', दाळचे_पाथ / 'posix.o'])
    पाळो_दिवचो_आदेश([연결편집기, '--gc-sections', '-T', प्रॉजॅक्ट_रूट / '부팅/लिंक_रचणाय.ld', '-Map', दाळचे_पाथ / 'kernel.map', '-o', दाळचे_पाथ / 'kernel.elf'] +
        [दाळचे_पाथ / नांव for नांव in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', दाळचे_पाथ / 'libposix-kor-arm64.a', नॅटवर्क, 원격사용, दाळचे_पाथ / 'remote/libassh.a', दाळचे_पाथ / 'remote/libbearssl.a', '--end-group'])
    पाळो_दिवचो_आदेश([ऑब्जॅक्ट_फायल_रूपांतर_करपी, '-O', 'binary', दाळचे_पाथ / 'kernel.elf', दाळचे_पाथ / 'kernel8.img'])
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
    for नांव in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        꾸러미명세['sha256'][नांव] = hashlib.sha256((दाळचे_पाथ / नांव).read_bytes()).hexdigest()
    (दाळचे_पाथ / 'build.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
    print('완료:', दाळचे_पाथ / 'kernel8.img')


if __name__ == '__main__':
    चलोवप()
