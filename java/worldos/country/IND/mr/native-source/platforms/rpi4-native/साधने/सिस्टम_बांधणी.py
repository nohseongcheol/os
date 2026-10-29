#!/usr/bin/env python3
"""होस्ट javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from प्रयोक्ता_जागा_बांधणी import प्रयोक्ता_जागा_तयार_करा
from संचारजाळे_बांधणी import संचारजाळे_तयार_करा
from उदाहरणे_बांधणी import उदाहरणे_तयार_करा
from दूरस्_थ_बांधणी import दूरस्_थ_तयार_करा

प्रोजेक्ट_मूळ = Path(__file__).resolve().parents[1]
भांडार_मूळ = प्रोजेक्ट_मूळ.parents[1]
पथ_बांधणी = प्रोजेक्ट_मूळ / 'build'


def आज्ञा_कार्यवाही_करा(वितर्क_ऍरे):
    subprocess.check_call([str(पहिले_मूल्य) for पहिले_मूल्य in वितर्क_ऍरे], cwd=str(प्रोजेक्ट_मूळ))


def सुरू_करा():
    पथ_बांधणी.mkdir(exist_ok=True)
    सी_संकलक = os.environ.get('ARM64_CC', 'clang')
    सीप्लसप्लस_संकलक = os.environ.get('ARM64_CXX', 'clang++')
    जोडणीकार_साधन = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ऑब्जेक्ट_संचिका_कन्व्हर्टर = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    संग्रह_साधन = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for साधने in ('javac', सी_संकलक, सीप्लसप्लस_संकलक, जोडणीकार_साधन, ऑब्जेक्ट_संचिका_कन्व्हर्टर, संग्रह_साधन):
        if not shutil.which(साधने):
            raise SystemExit('필요한 सिस्टम_बांधणी साधने अनुपस्थित_पद्धत: ' + साधने)
    फॉन्ट_माहिती = json.loads((प्रोजेक्ट_मूळ / 'vendor/terminal-font.json').read_text())
    फॉन्ट_डेटा = (प्रोजेक्ट_मूळ / 'vendor/terminal-font.bin').read_bytes()
    if len(फॉन्ट_डेटा) != 65616 * 32 or hashlib.sha256(फॉन्ट_डेटा).hexdigest() != फॉन्ट_माहिती['sha256']:
        raise SystemExit('टर्मिनल फॉन्ट_मूल्य आकार/SHA256 불일치')
    निर्यात_करा_सारणी = {'jshell_interactive': 'शेल_आदानप्रदान.आहे_परस्परसंवादी', 'jshell_output': 'शेल_आदानप्रदान.आउटपुट', 'jshell_input': 'शेल_आदानप्रदान.आदान_मूल्य', 'java_task': 'गाभा.पारपाडा_कार्य', 'jfs_path_start': 'स्मृती_संचिका.पथ_प्रारंभ',
               'jfs_path_byte': 'स्मृती_संचिका.पथ_बाइट', 'jfs_open': 'स्मृती_संचिका.उघडा',
               'jfs_read': 'स्मृती_संचिका.वाचन', 'jfs_write': 'स्मृती_संचिका.लेखन',
               'jfs_seek': 'स्मृती_संचिका.शोधा_स्थान', 'jfs_close': 'स्मृती_संचिका.बंद_करा',
               'jfs_size': 'स्मृती_संचिका.आकार', 'jfs_unlink': 'स्मृती_संचिका.पुसा_प्रविष्टी',
               'jfs_truncate': 'स्मृती_संचिका.लांबी_संच'}
    निर्यात_करा_सारणी.update({'jfs_entry_count': 'स्मृती_संचिका.संचिका_मर्यादा', 'jfs_entry_length': 'स्मृती_संचिका.निर्यातकेलेले_नाव_लांबी', 'jfs_entry_byte': 'स्मृती_संचिका.निर्यातकेलेले_नाव_बाइट', 'jfs_entry_size': 'स्मृती_संचिका.निर्यातकेलेले_संचिका_आकारा'})
    निर्यात_करा_सारणी.update({'jdraw_prepare': 'प्रतिमास्मृती_संयोजक.तयार_करणे', 'jdraw_width': 'प्रतिमास्मृती_संयोजक.रुंदी_मिळवा',
        'jdraw_height': 'प्रतिमास्मृती_संयोजक.उंची_मिळवा', 'jdraw_count_low': 'प्रतिमास्मृती_संयोजक.काउंटर_कमी_मिळवा',
        'jdraw_count_high': 'प्रतिमास्मृती_संयोजक.काउंटर_उच्च_मिळवा', 'jdraw_clip': 'प्रतिमास्मृती_संयोजक.क्लिप',
        'jdraw_clip_value': 'प्रतिमास्मृती_संयोजक.क्लिप_मूल्य', 'jdraw_begin': 'प्रतिमास्मृती_संयोजक.सुरू_करा',
        'jdraw_end': 'प्रतिमास्मृती_संयोजक.समाप्त', 'jdraw_pixel': 'प्रतिमास्मृती_संयोजक.पिक्सेल',
        'jdraw_rectangle': 'प्रतिमास्मृती_संयोजक.आयत_भरणे', 'jdraw_pointer': 'प्रतिमास्मृती_संयोजक.निर्देशक'})
    निर्यात_करा_सारणी.update({'jfs_mkdir': 'स्मृती_संचिका.निर्देशिका_तयार_करा', 'jfs_rmdir': 'स्मृती_संचिका.निर्देशिका_काढणे', 'jfs_kind': 'स्मृती_संचिका.प्रविष्टी_प्रकार'})
    निर्यात_करा_सारणी.update({'jnet_socket': 'स्वपरतावा_संचारजाळे.प्रविष्टी_तयार_करा', 'jnet_bind': 'स्वपरतावा_संचारजाळे.बाइंड_करा_संचारटोक',
        'jnet_put': 'स्वपरतावा_संचारजाळे.ठेवा_डेटा', 'jnet_get': 'स्वपरतावा_संचारजाळे.डेटा_वाचा', 'jnet_send': 'स्वपरतावा_संचारजाळे.पाठवा',
        'jnet_recv': 'स्वपरतावा_संचारजाळे.स्वीकारा', 'jnet_port': 'स्वपरतावा_संचारजाळे.संचारटोक_पॉर्ट_वाचा', 'jnet_address': 'स्वपरतावा_संचारजाळे.पत्ता_वाचा',
        'jnet_peer': 'स्वपरतावा_संचारजाळे.प्रेषक_संचारटोक', 'jnet_close': 'स्वपरतावा_संचारजाळे.बंद_करा'})
    निर्यात_करा_सारणी.update({'jstream_create': 'प्रवाह_संचारजाळे.प्रविष्टी_तयार_करा', 'jstream_bind': 'प्रवाह_संचारजाळे.बाइंड_करा_संचारटोक', 'jstream_listen': 'प्रवाह_संचारजाळे.ऐका_संचारटोक', 'jstream_connect': 'प्रवाह_संचारजाळे.जोडा', 'jstream_accept': 'प्रवाह_संचारजाळे.स्वीकारा_कनेक्शन', 'jstream_read': 'प्रवाह_संचारजाळे.वाचन', 'jstream_write': 'प्रवाह_संचारजाळे.लेखन', 'jstream_port': 'प्रवाह_संचारजाळे.संचारटोक_पॉर्ट_वाचा', 'jstream_peer': 'प्रवाह_संचारजाळे.समकक्ष_पॉर्ट_वाचा', 'jstream_close': 'प्रवाह_संचारजाळे.बंद_करा'})
    for चिन्ह_मूल्य in list(निर्यात_करा_सारणी):
        if चिन्ह_मूल्य.startswith('jstream_') or चिन्ह_मूल्य.startswith('jnet_') and चिन्ह_मूल्य not in ('jnet_put', 'jnet_get'):
            निर्यात_करा_सारणी[चिन्ह_मूल्य.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = निर्यात_करा_सारणी.pop(चिन्ह_मूल्य)
    उदाहरण_नोंदी = ['public final class बंडल { public static void तयार_करणे() {']
    for मार्ग in sorted((प्रोजेक्ट_मूळ / 'उदाहरणे').iterdir()):
        if मार्ग.is_file():
            उदाहरण_नोंदी.append('आज्ञा_अर्थविश्लेषक.स्थिर_संचिका(%s, %s);' %
                (json.dumps(मार्ग.name), json.dumps(मार्ग.read_text(encoding='utf-8'), ensure_ascii=True)))
    (पथ_बांधणी / 'बंडल.java').write_text('\n'.join(उदाहरण_नोंदी + ['}}']), encoding='utf-8')
    उदाहरणे_तयार_करा(प्रोजेक्ट_मूळ, भांडार_मूळ, आज्ञा_कार्यवाही_करा)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(पथ_बांधणी)) as कार्यरत_पथ:
        वर्ग_पथ = Path(कार्यरत_पथ)
        आज्ञा_कार्यवाही_करा(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', वर्ग_पथ, '-sourcepath', वर्ग_पथ, '-d', वर्ग_पथ] + sorted((प्रोजेक्ट_मूळ / 'स्रोत').glob('*.java')) + [पथ_बांधणी / 'बंडल.java', पथ_बांधणी / 'उदाहरण_बंडल.java'])
        # फाइल·शेल·विंडो 세션·통신과 Java पडदा 합성 배열을 सर्व_बांधणी 수용한다.
        वितर्क_ऍरे = ['sh', भांडार_मूळ / 'compiler/आगाऊ_संबंधित_वेळ.sh', '--entry', 'गाभा.सुरू_करा', '--heap-words', '1048576', '-o', पथ_बांधणी / 'kernel-java.c']
        for चिन्ह_मूल्य, पद्धत_प्रविष्टी in sorted(निर्यात_करा_सारणी.items()):
            वितर्क_ऍरे += ['--export', चिन्ह_मूल्य + '=' + पद्धत_प्रविष्टी]
        आज्ञा_कार्यवाही_करा(वितर्क_ऍरे + sorted(वर्ग_पथ.glob('*.class')))
    (पथ_बांधणी / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    कॉन्फिगरेशन_द्व्यंक = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    पॉझिक्स = भांडार_मूळ / 'posix-kor/arm64-native'
    प्रयोक्ता_जागा_तयार_करा(प्रोजेक्ट_मूळ, भांडार_मूळ, सी_संकलक, सीप्लसप्लस_संकलक, जोडणीकार_साधन, संग्रह_साधन, कॉन्फिगरेशन_द्व्यंक, आज्ञा_कार्यवाही_करा)
    संचारजाळे = संचारजाळे_तयार_करा(प्रोजेक्ट_मूळ, सी_संकलक, संग्रह_साधन, कॉन्फिगरेशन_द्व्यंक, आज्ञा_कार्यवाही_करा)
    दूरस्_थ_वापर = दूरस्_थ_तयार_करा(प्रोजेक्ट_मूळ, सी_संकलक, संग्रह_साधन, कॉन्फिगरेशन_द्व्यंक, आज्ञा_कार्यवाही_करा)
    समावेश = ['-I', पॉझिक्स / 'घोषणाशीर्षे', '-I', पथ_बांधणी]
    कामे_बांधणी = [(सी_संकलक, [], पथ_बांधणी / 'terminal-font.S', 'font.o'),
            (सी_संकलक, ['-std=c11', '-Wall', '-Wextra', '-Werror'], प्रोजेक्ट_मूळ / 'मशीन/टर्मिनल.c', 'terminal.o'),
            (सी_संकलक, ['-std=c11', '-Wall', '-Wextra', '-Werror'], प्रोजेक्ट_मूळ / 'मशीन/विजेट.c', 'widgets.o'),
            (सी_संकलक, ['-std=c11'], पथ_बांधणी / 'kernel-java.c', 'java.o'),
            (सी_संकलक, ['-std=c11', '-Wall', '-Wextra', '-Werror'], प्रोजेक्ट_मूळ / 'मशीन/बोर्ड.c', 'board.o'),
            (सी_संकलक, ['-std=c11', '-Wall', '-Wextra', '-Werror'], प्रोजेक्ट_मूळ / 'मशीन/पडदा_रेखांकन.c', 'drawing.o'),
            (सी_संकलक, ['-std=c11', '-Wall', '-Wextra', '-Werror'], प्रोजेक्ट_मूळ / 'मशीन/प्रयोक्ता.c', 'user.o'),
            (सी_संकलक, [], प्रोजेक्ट_मूळ / 'प्रणालीप्रारंभ/प्रविष्टी_गुण_मूल्य.S', 'entry.o'),
            (सी_संकलक, ['-std=c11', '-Wall', '-Wextra', '-Werror'], पॉझिक्स / 'जोडा.c', 'posix.o'),
            (सीप्लसप्लस_संकलक, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], प्रोजेक्ट_मूळ / 'चाचण्या/संचिका_कॉल्स.cpp', 'cpp.o')]
    for संकलक_साधन, अतिरिक्त_प्रदेश, मूळ_डेटा, प्रदान in कामे_बांधणी:
        मूळ_कॉन्फिगरेशन = [संचिका_प्रविष्टी for संचिका_प्रविष्टी in कॉन्फिगरेशन_द्व्यंक if संचिका_प्रविष्टी != '-mgeneral-regs-only'] if मूळ_डेटा.suffix == '.S' else कॉन्फिगरेशन_द्व्यंक
        आज्ञा_कार्यवाही_करा([संकलक_साधन] + मूळ_कॉन्फिगरेशन + अतिरिक्त_प्रदेश + समावेश + ['-c', मूळ_डेटा, '-o', पथ_बांधणी / प्रदान])
    आज्ञा_कार्यवाही_करा([संग्रह_साधन, 'rcs', पथ_बांधणी / 'libposix-kor-arm64.a', पथ_बांधणी / 'posix.o'])
    आज्ञा_कार्यवाही_करा([जोडणीकार_साधन, '--gc-sections', '-T', प्रोजेक्ट_मूळ / 'प्रणालीप्रारंभ/लिंक_लेआउट.ld', '-Map', पथ_बांधणी / 'kernel.map', '-o', पथ_बांधणी / 'kernel.elf'] +
        [पथ_बांधणी / नाव for नाव in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', पथ_बांधणी / 'libposix-kor-arm64.a', संचारजाळे, दूरस्_थ_वापर, पथ_बांधणी / 'remote/libassh.a', पथ_बांधणी / 'remote/libbearssl.a', '--end-group'])
    आज्ञा_कार्यवाही_करा([ऑब्जेक्ट_संचिका_कन्व्हर्टर, '-O', 'binary', पथ_बांधणी / 'kernel.elf', पथ_बांधणी / 'kernel8.img'])
    बंडल_सूचीलेख = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'मराठी.स्वकीय', 'korean_exceptions': 20,
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
    for नाव in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        बंडल_सूचीलेख['sha256'][नाव] = hashlib.sha256((पथ_बांधणी / नाव).read_bytes()).hexdigest()
    (पथ_बांधणी / 'build.json').write_text(json.dumps(बंडल_सूचीलेख, indent=2) + '\n')
    print('आहे_पूर्ण:', पथ_बांधणी / 'kernel8.img')


if __name__ == '__main__':
    सुरू_करा()
