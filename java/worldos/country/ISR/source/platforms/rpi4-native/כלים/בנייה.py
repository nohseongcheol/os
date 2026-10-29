#!/usr/bin/env python3
"""ארח javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from בנה_משתמש_חלל import ליצור_משתמש_חלל
from בנה_רשת import ליצור_רשת
from 예제빌드 import 예제만들기
from בנה_מרוחק import ליצור_מרוחק

לשקף_בסיס = Path(__file__).resolve().parents[1]
מאגר_בסיס = לשקף_בסיס.parents[1]
בנה_נתיב = לשקף_בסיס / 'build'


def לבצע_פקודה(ארגומנט_מערך):
    subprocess.check_call([str(첫째값) for 첫째값 in ארגומנט_מערך], cwd=str(לשקף_בסיס))


def הפעלה():
    בנה_נתיב.mkdir(exist_ok=True)
    מ_מהדר = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    연결편집기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    אובייקט_קובץ_ממיר = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    ארכיון_כלי = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for כלים in ('javac', מ_מהדר, 시플플번역기, 연결편집기, אובייקט_קובץ_ממיר, ארכיון_כלי):
        if not shutil.which(כלים):
            raise SystemExit('필요한 בנייה כלים 없음: ' + כלים)
    גופן_מידע = json.loads((לשקף_בסיס / 'vendor/terminal-font.json').read_text())
    גופן_נתונים = (לשקף_בסיס / 'vendor/terminal-font.bin').read_bytes()
    if len(גופן_נתונים) != 65616 * 32 or hashlib.sha256(גופן_נתונים).hexdigest() != גופן_מידע['sha256']:
        raise SystemExit('מסוף גופן_ערך גודל/SHA256 불일치')
    ייצא_טבלה = {'jshell_interactive': '셸입출력.מערכות_מידע_אינטראקטיבי', 'jshell_output': '셸입출력.פלטטקסט', 'jshell_input': '셸입출력.קלט_ערך', 'java_task': 'ליבה.작업', 'jfs_path_start': 'קבציםבזיכרון.נתיב_התחל',
               'jfs_path_byte': 'קבציםבזיכרון.נתיב_בית', 'jfs_open': 'קבציםבזיכרון.פתח',
               'jfs_read': 'קבציםבזיכרון.קרא', 'jfs_write': 'קבציםבזיכרון.כתוב',
               'jfs_seek': 'קבציםבזיכרון.חפש_עמדה', 'jfs_close': 'קבציםבזיכרון.סגירה',
               'jfs_size': 'קבציםבזיכרון.גודל', 'jfs_unlink': 'קבציםבזיכרון.מחק_ערך',
               'jfs_truncate': 'קבציםבזיכרון.길이정하기'}
    ייצא_טבלה.update({'jfs_entry_count': 'קבציםבזיכרון.파일한도', 'jfs_entry_length': 'קבציםבזיכרון.공개이름길이', 'jfs_entry_byte': 'קבציםבזיכרון.공개이름바이트', 'jfs_entry_size': 'קבציםבזיכרון.공개파일크기'})
    ייצא_טבלה.update({'jdraw_prepare': '화면합성.להכין', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.לקבל_גובה', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.לגזור',
        'jdraw_clip_value': '화면합성.לגזור_ערך', 'jdraw_begin': '화면합성.הפעלה',
        'jdraw_end': '화면합성.סיום', 'jdraw_pixel': '화면합성.פיקסל',
        'jdraw_rectangle': '화면합성.מלבן_למלא', 'jdraw_pointer': '화면합성.מצביע'})
    ייצא_טבלה.update({'jfs_mkdir': 'קבציםבזיכרון.ליצור_מדריך', 'jfs_rmdir': 'קבציםבזיכרון.הסר_מדריך', 'jfs_kind': 'קבציםבזיכרון.항목종류'})
    ייצא_טבלה.update({'jnet_socket': 'לולאה_חוזרת_Loopback_רשת.ליצור_ערך', 'jnet_bind': 'לולאה_חוזרת_Loopback_רשת.לאגד_משתתף',
        'jnet_put': 'לולאה_חוזרת_Loopback_רשת.자료넣기', 'jnet_get': 'לולאה_חוזרת_Loopback_רשת.자료읽기', 'jnet_send': 'לולאה_חוזרת_Loopback_רשת.שלח',
        'jnet_recv': 'לולאה_חוזרת_Loopback_רשת.לקבל', 'jnet_port': 'לולאה_חוזרת_Loopback_רשת.창구읽기', 'jnet_address': 'לולאה_חוזרת_Loopback_רשת.주소읽기',
        'jnet_peer': 'לולאה_חוזרת_Loopback_רשת.שולח_משתתף', 'jnet_close': 'לולאה_חוזרת_Loopback_רשת.סגירה'})
    ייצא_טבלה.update({'jstream_create': 'זרם_רשת.ליצור_ערך', 'jstream_bind': 'זרם_רשת.לאגד_משתתף', 'jstream_listen': 'זרם_רשת.להאזין_משתתף', 'jstream_connect': 'זרם_רשת.חיבור', 'jstream_accept': 'זרם_רשת.לקבל_קשר', 'jstream_read': 'זרם_רשת.קרא', 'jstream_write': 'זרם_רשת.כתוב', 'jstream_port': 'זרם_רשת.창구읽기', 'jstream_peer': 'זרם_רשת.상대창구읽기', 'jstream_close': 'זרם_רשת.סגירה'})
    for סימן_ערך in list(ייצא_טבלה):
        if סימן_ערך.startswith('jstream_') or סימן_ערך.startswith('jnet_') and סימן_ערך not in ('jnet_put', 'jnet_get'):
            ייצא_טבלה[סימן_ערך.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = ייצא_טבלה.pop(סימן_ערך)
    예제들 = ['public final class חבילה { public static void להכין() {']
    for נתיב in sorted((לשקף_בסיס / '예제').iterdir()):
        if נתיב.is_file():
            예제들.append('מפרשפקודות.סטטי_קובץ(%s, %s);' %
                (json.dumps(נתיב.name), json.dumps(נתיב.read_text(encoding='utf-8'), ensure_ascii=True)))
    (בנה_נתיב / 'חבילה.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(לשקף_בסיס, מאגר_בסיס, לבצע_פקודה)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(בנה_נתיב)) as 작업경로:
        כיתה_נתיב = Path(작업경로)
        לבצע_פקודה(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', כיתה_נתיב, '-sourcepath', כיתה_נתיב, '-d', כיתה_נתיב] + sorted((לשקף_בסיס / 'קודמקור').glob('*.java')) + [בנה_נתיב / 'חבילה.java', בנה_נתיב / '예제꾸러미.java'])
        # קובץ·מעטפת·חלון 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        ארגומנט_מערך = ['sh', מאגר_בסיס / 'compiler/미리번역.sh', '--entry', 'ליבה.הפעלה', '--heap-words', '1048576', '-o', בנה_נתיב / 'kernel-java.c']
        for סימן_ערך, פעולת_שירות_ערך_5c76dce4 in sorted(ייצא_טבלה.items()):
            ארגומנט_מערך += ['--export', סימן_ערך + '=' + פעולת_שירות_ערך_5c76dce4]
        לבצע_פקודה(ארגומנט_מערך + sorted(כיתה_נתיב.glob('*.class')))
    (בנה_נתיב / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = מאגר_בסיס / 'posix-kor/arm64-native'
    ליצור_משתמש_חלל(לשקף_בסיס, מאגר_בסיס, מ_מהדר, 시플플번역기, 연결편집기, ארכיון_כלי, 설정비트, לבצע_פקודה)
    רשת = ליצור_רשת(לשקף_בסיס, מ_מהדר, ארכיון_כלי, 설정비트, לבצע_פקודה)
    מרוחק_שימוש = ליצור_מרוחק(לשקף_בסיס, מ_מהדר, ארכיון_כלי, 설정비트, לבצע_פקודה)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', בנה_נתיב]
    빌드작업 = [(מ_מהדר, [], בנה_נתיב / 'terminal-font.S', 'font.o'),
            (מ_מהדר, ['-std=c11', '-Wall', '-Wextra', '-Werror'], לשקף_בסיס / 'מחשב/מסוף.c', 'terminal.o'),
            (מ_מהדר, ['-std=c11', '-Wall', '-Wextra', '-Werror'], לשקף_בסיס / 'מחשב/רכיב_גרפי.c', 'widgets.o'),
            (מ_מהדר, ['-std=c11'], בנה_נתיב / 'kernel-java.c', 'java.o'),
            (מ_מהדר, ['-std=c11', '-Wall', '-Wextra', '-Werror'], לשקף_בסיס / 'מחשב/לוח.c', 'board.o'),
            (מ_מהדר, ['-std=c11', '-Wall', '-Wextra', '-Werror'], לשקף_בסיס / 'מחשב/화면그림.c', 'drawing.o'),
            (מ_מהדר, ['-std=c11', '-Wall', '-Wextra', '-Werror'], לשקף_בסיס / 'מחשב/משתמש.c', 'user.o'),
            (מ_מהדר, [], לשקף_בסיס / '부팅/נקודת_כניסה_ערך.S', 'entry.o'),
            (מ_מהדר, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'חיבור.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], לשקף_בסיס / '시험/קובץ_שיחות_טלפון.cpp', 'cpp.o')]
    for מהדר_כלי, 추가영역, 원본자료, פלט in 빌드작업:
        원본설정 = [קובץ_ערך for קובץ_ערך in 설정비트 if קובץ_ערך != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        לבצע_פקודה([מהדר_כלי] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', בנה_נתיב / פלט])
    לבצע_פקודה([ארכיון_כלי, 'rcs', בנה_נתיב / 'libposix-kor-arm64.a', בנה_נתיב / 'posix.o'])
    לבצע_פקודה([연결편집기, '--gc-sections', '-T', לשקף_בסיס / '부팅/לקשר_ניווט.ld', '-Map', בנה_נתיב / 'kernel.map', '-o', בנה_נתיב / 'kernel.elf'] +
        [בנה_נתיב / שם for שם in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', בנה_נתיב / 'libposix-kor-arm64.a', רשת, מרוחק_שימוש, בנה_נתיב / 'remote/libassh.a', בנה_נתיב / 'remote/libbearssl.a', '--end-group'])
    לבצע_פקודה([אובייקט_קובץ_ממיר, '-O', 'binary', בנה_נתיב / 'kernel.elf', בנה_נתיב / 'kernel8.img'])
    חבילה_מניפסט = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'עברית.עצמי', 'korean_exceptions': 20,
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
    for שם in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        חבילה_מניפסט['sha256'][שם] = hashlib.sha256((בנה_נתיב / שם).read_bytes()).hexdigest()
    (בנה_נתיב / 'build.json').write_text(json.dumps(חבילה_מניפסט, indent=2) + '\n')
    print('완료:', בנה_נתיב / 'kernel8.img')


if __name__ == '__main__':
    הפעלה()
