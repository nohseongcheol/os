#!/usr/bin/env python3
"""ஓம்பு javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from தொகு_பயனர்_தளம் import உருவாக்கு_பயனர்_தளம்
from தொகு_பிணையம் import உருவாக்கு_பிணையம்
from 예제빌드 import 예제만들기
from தொகு_தொலைநிலை import உருவாக்கு_தொலைநிலை

திட்டப்பணி_மூலம் = Path(__file__).resolve().parents[1]
தொகுபதிவகம்_மூலம் = திட்டப்பணி_மூலம்.parents[1]
தொகு_பாதை = திட்டப்பணி_மூலம் / 'build'


def இயக்கு_கட்டளை(மதிப்புரு_கோவை):
    subprocess.check_call([str(첫째값) for 첫째값 in மதிப்புரு_கோவை], cwd=str(திட்டப்பணி_மூலம்))


def செயல்படுத்துக():
    தொகு_பாதை.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    பொருள்_கோப்பு_மாற்றி = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    காப்பகம்_கருவி = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for கருவிகள் in ('javac', 시언어번역기, 시플플번역기, 연결편집기, பொருள்_கோப்பு_மாற்றி, காப்பகம்_கருவி):
        if not shutil.which(கருவிகள்):
            raise SystemExit('필요한 தொகு_முறைமை கருவிகள் 없음: ' + கருவிகள்)
    எழுத்துரு_தகவல் = json.loads((திட்டப்பணி_மூலம் / 'vendor/terminal-font.json').read_text())
    எழுத்துரு_தரவு = (திட்டப்பணி_மூலம் / 'vendor/terminal-font.bin').read_bytes()
    if len(எழுத்துரு_தரவு) != 65616 * 32 or hashlib.sha256(எழுத்துரு_தரவு).hexdigest() != எழுத்துரு_தகவல்['sha256']:
        raise SystemExit('கட்டளை_விளக்கி எழுத்துரு_மதிப்பு அளவு/SHA256 불일치')
    ஏற்றுமதிசெய்_அட்டவணை = {'jshell_interactive': '셸입출력.தகவல்_தொழில்நுட்பம்_ஊடாடு', 'jshell_output': '셸입출력.வெளியீட்டு_இடம்', 'jshell_input': '셸입출력.입력', 'java_task': 'கரு.작업', 'jfs_path_start': 'நினைவகம்_கோப்புகள்.பாதை_தொடங்கு',
               'jfs_path_byte': 'நினைவகம்_கோப்புகள்.பாதை_பைட்', 'jfs_open': 'நினைவகம்_கோப்புகள்.திற',
               'jfs_read': 'நினைவகம்_கோப்புகள்.படி', 'jfs_write': 'நினைவகம்_கோப்புகள்.எழுது',
               'jfs_seek': 'நினைவகம்_கோப்புகள்.தேடு_நிலை', 'jfs_close': 'நினைவகம்_கோப்புகள்.மூடு',
               'jfs_size': 'நினைவகம்_கோப்புகள்.அளவு', 'jfs_unlink': 'நினைவகம்_கோப்புகள்.அழி_உள்ளீடு',
               'jfs_truncate': 'நினைவகம்_கோப்புகள்.அமை_நீளம்'}
    ஏற்றுமதிசெய்_அட்டவணை.update({'jfs_entry_count': 'நினைவகம்_கோப்புகள்.파일한도', 'jfs_entry_length': 'நினைவகம்_கோப்புகள்.공개이름길이', 'jfs_entry_byte': 'நினைவகம்_கோப்புகள்.공개이름바이트', 'jfs_entry_size': 'நினைவகம்_கோப்புகள்.공개파일크기'})
    ஏற்றுமதிசெய்_அட்டவணை.update({'jdraw_prepare': '화면합성.தயார்படுத்த', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.கிளிப்',
        'jdraw_clip_value': '화면합성.கிளிப்_மதிப்பு', 'jdraw_begin': '화면합성.செயல்படுத்துக',
        'jdraw_end': '화면합성.முடிப்பு', 'jdraw_pixel': '화면합성.படக்_கூறு',
        'jdraw_rectangle': '화면합성.사각그림', 'jdraw_pointer': '화면합성.குறிப்பான்'})
    ஏற்றுமதிசெய்_அட்டவணை.update({'jfs_mkdir': 'நினைவகம்_கோப்புகள்.உருவாக்கு_கோப்பகம்', 'jfs_rmdir': 'நினைவகம்_கோப்புகள்.அகற்று_கோப்பகம்', 'jfs_kind': 'நினைவகம்_கோப்புகள்.항목종류'})
    ஏற்றுமதிசெய்_அட்டவணை.update({'jnet_socket': '되돌림망.உருவாக்கு_உள்ளீடு', 'jnet_bind': '되돌림망.கட்டு_முடிவுப்_புள்ளி',
        'jnet_put': '되돌림망.자료넣기', 'jnet_get': '되돌림망.자료읽기', 'jnet_send': '되돌림망.அனுப்பு',
        'jnet_recv': '되돌림망.받기', 'jnet_port': '되돌림망.창구읽기', 'jnet_address': '되돌림망.주소읽기',
        'jnet_peer': '되돌림망.அனுப்புநர்_முடிவுப்_புள்ளி', 'jnet_close': '되돌림망.மூடு'})
    ஏற்றுமதிசெய்_அட்டவணை.update({'jstream_create': 'தொடரோடி_பிணையம்.உருவாக்கு_உள்ளீடு', 'jstream_bind': 'தொடரோடி_பிணையம்.கட்டு_முடிவுப்_புள்ளி', 'jstream_listen': 'தொடரோடி_பிணையம்.கவனி_முடிவுப்_புள்ளி', 'jstream_connect': 'தொடரோடி_பிணையம்.இணைக்க', 'jstream_accept': 'தொடரோடி_பிணையம்.ஏற்றுக்கொள்_இணைப்பு', 'jstream_read': 'தொடரோடி_பிணையம்.படி', 'jstream_write': 'தொடரோடி_பிணையம்.எழுது', 'jstream_port': 'தொடரோடி_பிணையம்.창구읽기', 'jstream_peer': 'தொடரோடி_பிணையம்.상대창구읽기', 'jstream_close': 'தொடரோடி_பிணையம்.மூடு'})
    for சின்னம்_மதிப்பு in list(ஏற்றுமதிசெய்_அட்டவணை):
        if சின்னம்_மதிப்பு.startswith('jstream_') or சின்னம்_மதிப்பு.startswith('jnet_') and சின்னம்_மதிப்பு not in ('jnet_put', 'jnet_get'):
            ஏற்றுமதிசெய்_அட்டவணை[சின்னம்_மதிப்பு.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = ஏற்றுமதிசெய்_அட்டவணை.pop(சின்னம்_மதிப்பு)
    예제들 = ['public final class மூட்டை { public static void தயார்படுத்த() {']
    for பாதை_2 in sorted((திட்டப்பணி_மூலம் / '예제').iterdir()):
        if பாதை_2.is_file():
            예제들.append('명령해석기.மாறா_கோப்பு(%s, %s);' %
                (json.dumps(பாதை_2.name), json.dumps(பாதை_2.read_text(encoding='utf-8'), ensure_ascii=True)))
    (தொகு_பாதை / 'மூட்டை.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(திட்டப்பணி_மூலம், தொகுபதிவகம்_மூலம், இயக்கு_கட்டளை)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(தொகு_பாதை)) as 작업경로:
        பிரிவு_பாதை = Path(작업경로)
        இயக்கு_கட்டளை(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', பிரிவு_பாதை, '-sourcepath', பிரிவு_பாதை, '-d', பிரிவு_பாதை] + sorted((திட்டப்பணி_மூலம் / 'மூலக்_கோப்பு').glob('*.java')) + [தொகு_பாதை / 'மூட்டை.java', தொகு_பாதை / '예제꾸러미.java'])
        # கோப்பின்_பெயர்·கூடு·சாளரம் 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        மதிப்புரு_கோவை = ['sh', தொகுபதிவகம்_மூலம் / 'compiler/미리번역.sh', '--entry', 'கரு.செயல்படுத்துக', '--heap-words', '1048576', '-o', தொகு_பாதை / 'kernel-java.c']
        for சின்னம்_மதிப்பு, முறை_உள்ளீடு in sorted(ஏற்றுமதிசெய்_அட்டவணை.items()):
            மதிப்புரு_கோவை += ['--export', சின்னம்_மதிப்பு + '=' + முறை_உள்ளீடு]
        இயக்கு_கட்டளை(மதிப்புரு_கோவை + sorted(பிரிவு_பாதை.glob('*.class')))
    (தொகு_பாதை / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = தொகுபதிவகம்_மூலம் / 'posix-kor/arm64-native'
    உருவாக்கு_பயனர்_தளம்(திட்டப்பணி_மூலம், தொகுபதிவகம்_மூலம், 시언어번역기, 시플플번역기, 연결편집기, காப்பகம்_கருவி, உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை, இயக்கு_கட்டளை)
    பிணையம் = உருவாக்கு_பிணையம்(திட்டப்பணி_மூலம், 시언어번역기, காப்பகம்_கருவி, உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை, இயக்கு_கட்டளை)
    원격사용 = உருவாக்கு_தொலைநிலை(திட்டப்பணி_மூலம், 시언어번역기, காப்பகம்_கருவி, உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை, இயக்கு_கட்டளை)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', தொகு_பாதை]
    빌드작업 = [(시언어번역기, [], தொகு_பாதை / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], திட்டப்பணி_மூலம் / 'இயந்திரம்/கட்டளை_விளக்கி.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], திட்டப்பணி_மூலம் / 'இயந்திரம்/விட்ஜெட்.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], தொகு_பாதை / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], திட்டப்பணி_மூலம் / 'இயந்திரம்/போர்டு.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], திட்டப்பணி_மூலம் / 'இயந்திரம்/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], திட்டப்பணி_மூலம் / 'இயந்திரம்/பயனர்.c', 'user.o'),
            (시언어번역기, [], திட்டப்பணி_மூலம் / '부팅/நுழைவுப்_புள்ளி_மதிப்பு.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'இணைக்க.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], திட்டப்பணி_மூலம் / '시험/கோப்பு_அழைப்புகள்.cpp', 'cpp.o')]
    for 번역기, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [கோப்பு_உள்ளீடு for கோப்பு_உள்ளீடு in உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை if கோப்பு_உள்ளீடு != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை
        இயக்கு_கட்டளை([번역기] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', தொகு_பாதை / 출력결과])
    இயக்கு_கட்டளை([காப்பகம்_கருவி, 'rcs', தொகு_பாதை / 'libposix-kor-arm64.a', தொகு_பாதை / 'posix.o'])
    இயக்கு_கட்டளை([연결편집기, '--gc-sections', '-T', திட்டப்பணி_மூலம் / '부팅/இணை_லேஅவுட்.ld', '-Map', தொகு_பாதை / 'kernel.map', '-o', தொகு_பாதை / 'kernel.elf'] +
        [தொகு_பாதை / பெயர் for பெயர் in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', தொகு_பாதை / 'libposix-kor-arm64.a', பிணையம், 원격사용, தொகு_பாதை / 'remote/libassh.a', தொகு_பாதை / 'remote/libbearssl.a', '--end-group'])
    இயக்கு_கட்டளை([பொருள்_கோப்பு_மாற்றி, '-O', 'binary', தொகு_பாதை / 'kernel.elf', தொகு_பாதை / 'kernel8.img'])
    மூட்டை_தொற்றம் = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'தமிழ்.자체', 'korean_exceptions': 20,
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
    for பெயர் in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        மூட்டை_தொற்றம்['sha256'][பெயர்] = hashlib.sha256((தொகு_பாதை / பெயர்).read_bytes()).hexdigest()
    (தொகு_பாதை / 'build.json').write_text(json.dumps(மூட்டை_தொற்றம், indent=2) + '\n')
    print('완료:', தொகு_பாதை / 'kernel8.img')


if __name__ == '__main__':
    செயல்படுத்துக()
