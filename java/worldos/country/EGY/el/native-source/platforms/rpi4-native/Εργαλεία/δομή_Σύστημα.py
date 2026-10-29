#!/usr/bin/env python3
"""φιλοξενώ javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from δομή_χρήστης_χώρος import ανοίγω_χρήστης_χώρος
from δομή_δίκτυο import ανοίγω_δίκτυο_48d29d6d
from 예제빌드 import 예제만들기
from δομή_απομακρυσμένος import ανοίγω_απομακρυσμένος

έργο_ρίζα = Path(__file__).resolve().parents[1]
αποθετήριο_ρίζα = έργο_ρίζα.parents[1]
δομή_διαδρομή = έργο_ρίζα / 'build'


def εκτελώ_εντολή(όρισμα_πίνακας):
    subprocess.check_call([str(첫째값) for 첫째값 in όρισμα_πίνακας], cwd=str(έργο_ρίζα))


def Εκτέλεση_2():
    δομή_διαδρομή.mkdir(exist_ok=True)
    Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    πρόγραμμα_σύνδεσης_εργαλείο = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    αντικείμενο_Αρχείο_μετατροπέας = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    Αρχειοθήκη_εργαλείο = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for Εργαλεία in ('javac', Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης, 시플플번역기, πρόγραμμα_σύνδεσης_εργαλείο, αντικείμενο_Αρχείο_μετατροπέας, Αρχειοθήκη_εργαλείο):
        if not shutil.which(Εργαλεία):
            raise SystemExit('필요한 δομή_Σύστημα Εργαλεία 없음: ' + Εργαλεία)
    γραμματοσειρά_πληροφορία = json.loads((έργο_ρίζα / 'vendor/terminal-font.json').read_text())
    γραμματοσειρά_δεδομένα = (έργο_ρίζα / 'vendor/terminal-font.bin').read_bytes()
    if len(γραμματοσειρά_δεδομένα) != 65616 * 32 or hashlib.sha256(γραμματοσειρά_δεδομένα).hexdigest() != γραμματοσειρά_πληροφορία['sha256']:
        raise SystemExit('Τερματικό γραμματοσειρά_τιμή Μέγεθος/SHA256 불일치')
    εξάγω_πίνακας = {'jshell_interactive': '셸입출력.πληροφοριακά_συστήματα_αλληλεπιδραστικός', 'jshell_output': '셸입출력.Έξοδος', 'jshell_input': '셸입출력.είσοδος_τιμή', 'java_task': 'πυρήνας.작업', 'jfs_path_start': 'Μνήμη_Αρχεία.διαδρομή_αρχή',
               'jfs_path_byte': 'Μνήμη_Αρχεία.경로바이트', 'jfs_open': 'Μνήμη_Αρχεία.Άνοιγμα',
               'jfs_read': 'Μνήμη_Αρχεία.Ανάγνωση', 'jfs_write': 'Μνήμη_Αρχεία.Εγγραφή',
               'jfs_seek': 'Μνήμη_Αρχεία.αναζητώ_θέση', 'jfs_close': 'Μνήμη_Αρχεία.Κλείσιμο',
               'jfs_size': 'Μνήμη_Αρχεία.Μέγεθος', 'jfs_unlink': 'Μνήμη_Αρχεία.διαγράφω_καταχώρηση',
               'jfs_truncate': 'Μνήμη_Αρχεία.σύνολο_διάρκεια'}
    εξάγω_πίνακας.update({'jfs_entry_count': 'Μνήμη_Αρχεία.파일한도', 'jfs_entry_length': 'Μνήμη_Αρχεία.공개이름길이', 'jfs_entry_byte': 'Μνήμη_Αρχεία.공개이름바이트', 'jfs_entry_size': 'Μνήμη_Αρχεία.공개파일크기'})
    εξάγω_πίνακας.update({'jdraw_prepare': '화면합성.Προετοίμασε', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.λαμβάνω_ύψος', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.απόσπασμα',
        'jdraw_clip_value': '화면합성.απόσπασμα_τιμή', 'jdraw_begin': '화면합성.Εκτέλεση_2',
        'jdraw_end': '화면합성.Τέλος', 'jdraw_pixel': '화면합성.화소',
        'jdraw_rectangle': '화면합성.ορθογώνιο_γεμίζω', 'jdraw_pointer': '화면합성.δείκτης'})
    εξάγω_πίνακας.update({'jfs_mkdir': 'Μνήμη_Αρχεία.ανοίγω_Κατάλογος', 'jfs_rmdir': 'Μνήμη_Αρχεία.καταργώ_Κατάλογος', 'jfs_kind': 'Μνήμη_Αρχεία.항목종류'})
    εξάγω_πίνακας.update({'jnet_socket': 'βρόχος_επιστροφής_δίκτυο.ανοίγω_καταχώρηση', 'jnet_bind': 'βρόχος_επιστροφής_δίκτυο.συνδέω_τελικό_σημείο_bbe6b410',
        'jnet_put': 'βρόχος_επιστροφής_δίκτυο.자료넣기', 'jnet_get': 'βρόχος_επιστροφής_δίκτυο.자료읽기', 'jnet_send': 'βρόχος_επιστροφής_δίκτυο.στέλνω',
        'jnet_recv': 'βρόχος_επιστροφής_δίκτυο.λαμβάνω', 'jnet_port': 'βρόχος_επιστροφής_δίκτυο.창구읽기', 'jnet_address': 'βρόχος_επιστροφής_δίκτυο.주소읽기',
        'jnet_peer': 'βρόχος_επιστροφής_δίκτυο.αποστολέας_τελικό_σημείο', 'jnet_close': 'βρόχος_επιστροφής_δίκτυο.Κλείσιμο'})
    εξάγω_πίνακας.update({'jstream_create': 'ροή_δίκτυο.ανοίγω_καταχώρηση', 'jstream_bind': 'ροή_δίκτυο.συνδέω_τελικό_σημείο_bbe6b410', 'jstream_listen': 'ροή_δίκτυο.ακρόαση_τελικό_σημείο', 'jstream_connect': 'ροή_δίκτυο.Σύνδεση', 'jstream_accept': 'ροή_δίκτυο.αποδέχομαι_σύνδεση', 'jstream_read': 'ροή_δίκτυο.Ανάγνωση', 'jstream_write': 'ροή_δίκτυο.Εγγραφή', 'jstream_port': 'ροή_δίκτυο.창구읽기', 'jstream_peer': 'ροή_δίκτυο.상대창구읽기', 'jstream_close': 'ροή_δίκτυο.Κλείσιμο'})
    for σύμβολο_τιμή in list(εξάγω_πίνακας):
        if σύμβολο_τιμή.startswith('jstream_') or σύμβολο_τιμή.startswith('jnet_') and σύμβολο_τιμή not in ('jnet_put', 'jnet_get'):
            εξάγω_πίνακας[σύμβολο_τιμή.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = εξάγω_πίνακας.pop(σύμβολο_τιμή)
    예제들 = ['public final class πακέτο { public static void Προετοίμασε() {']
    for ΔΙΑΔΡΟΜΗ in sorted((έργο_ρίζα / '예제').iterdir()):
        if ΔΙΑΔΡΟΜΗ.is_file():
            예제들.append('명령해석기.στατικός_Αρχείο(%s, %s);' %
                (json.dumps(ΔΙΑΔΡΟΜΗ.name), json.dumps(ΔΙΑΔΡΟΜΗ.read_text(encoding='utf-8'), ensure_ascii=True)))
    (δομή_διαδρομή / 'πακέτο.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(έργο_ρίζα, αποθετήριο_ρίζα, εκτελώ_εντολή)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(δομή_διαδρομή)) as 작업경로:
        Τάξη_διαδρομή = Path(작업경로)
        εκτελώ_εντολή(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Τάξη_διαδρομή, '-sourcepath', Τάξη_διαδρομή, '-d', Τάξη_διαδρομή] + sorted((έργο_ρίζα / 'ΠΗΓΗ').glob('*.java')) + [δομή_διαδρομή / 'πακέτο.java', δομή_διαδρομή / '예제꾸러미.java'])
        # Αρχείο·κέλυφος·Παράθυρο 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        όρισμα_πίνακας = ['sh', αποθετήριο_ρίζα / 'compiler/미리번역.sh', '--entry', 'πυρήνας.Εκτέλεση_2', '--heap-words', '1048576', '-o', δομή_διαδρομή / 'kernel-java.c']
        for σύμβολο_τιμή, μέθοδος_καταχώρηση in sorted(εξάγω_πίνακας.items()):
            όρισμα_πίνακας += ['--export', σύμβολο_τιμή + '=' + μέθοδος_καταχώρηση]
        εκτελώ_εντολή(όρισμα_πίνακας + sorted(Τάξη_διαδρομή.glob('*.class')))
    (δομή_διαδρομή / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    ρυθμίσεις_Υπηρεσία_έξυπνης_μεταφοράς_στο_παρασκήνιο = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = αποθετήριο_ρίζα / 'posix-kor/arm64-native'
    ανοίγω_χρήστης_χώρος(έργο_ρίζα, αποθετήριο_ρίζα, Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης, 시플플번역기, πρόγραμμα_σύνδεσης_εργαλείο, Αρχειοθήκη_εργαλείο, ρυθμίσεις_Υπηρεσία_έξυπνης_μεταφοράς_στο_παρασκήνιο, εκτελώ_εντολή)
    δίκτυο = ανοίγω_δίκτυο_48d29d6d(έργο_ρίζα, Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης, Αρχειοθήκη_εργαλείο, ρυθμίσεις_Υπηρεσία_έξυπνης_μεταφοράς_στο_παρασκήνιο, εκτελώ_εντολή)
    απομακρυσμένος_χρήση = ανοίγω_απομακρυσμένος(έργο_ρίζα, Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης, Αρχειοθήκη_εργαλείο, ρυθμίσεις_Υπηρεσία_έξυπνης_μεταφοράς_στο_παρασκήνιο, εκτελώ_εντολή)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', δομή_διαδρομή]
    빌드작업 = [(Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης, [], δομή_διαδρομή / 'terminal-font.S', 'font.o'),
            (Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης, ['-std=c11', '-Wall', '-Wextra', '-Werror'], έργο_ρίζα / 'υπολογιστής_5eb260fa/Τερματικό.c', 'terminal.o'),
            (Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης, ['-std=c11', '-Wall', '-Wextra', '-Werror'], έργο_ρίζα / 'υπολογιστής_5eb260fa/γραφικό_στοιχείο.c', 'widgets.o'),
            (Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης, ['-std=c11'], δομή_διαδρομή / 'kernel-java.c', 'java.o'),
            (Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης, ['-std=c11', '-Wall', '-Wextra', '-Werror'], έργο_ρίζα / 'υπολογιστής_5eb260fa/Πίνακας.c', 'board.o'),
            (Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης, ['-std=c11', '-Wall', '-Wextra', '-Werror'], έργο_ρίζα / 'υπολογιστής_5eb260fa/화면그림.c', 'drawing.o'),
            (Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης, ['-std=c11', '-Wall', '-Wextra', '-Werror'], έργο_ρίζα / 'υπολογιστής_5eb260fa/χρήστης.c', 'user.o'),
            (Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης, [], έργο_ρίζα / '부팅/σημείο_εισόδου_τιμή.S', 'entry.o'),
            (Ταχυδρομικός_κώδικας_πρόγραμμα_μεταγλώττισης, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'Σύνδεση.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], έργο_ρίζα / '시험/Αρχείο_Κλήσεις.cpp', 'cpp.o')]
    for πρόγραμμα_μεταγλώττισης_εργαλείο, 추가영역, 원본자료, 출력결과 in 빌드작업:
        원본설정 = [Αρχείο_καταχώρηση for Αρχείο_καταχώρηση in ρυθμίσεις_Υπηρεσία_έξυπνης_μεταφοράς_στο_παρασκήνιο if Αρχείο_καταχώρηση != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else ρυθμίσεις_Υπηρεσία_έξυπνης_μεταφοράς_στο_παρασκήνιο
        εκτελώ_εντολή([πρόγραμμα_μεταγλώττισης_εργαλείο] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', δομή_διαδρομή / 출력결과])
    εκτελώ_εντολή([Αρχειοθήκη_εργαλείο, 'rcs', δομή_διαδρομή / 'libposix-kor-arm64.a', δομή_διαδρομή / 'posix.o'])
    εκτελώ_εντολή([πρόγραμμα_σύνδεσης_εργαλείο, '--gc-sections', '-T', έργο_ρίζα / '부팅/συνδέω_Διάταξη.ld', '-Map', δομή_διαδρομή / 'kernel.map', '-o', δομή_διαδρομή / 'kernel.elf'] +
        [δομή_διαδρομή / Όνομα for Όνομα in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', δομή_διαδρομή / 'libposix-kor-arm64.a', δίκτυο, απομακρυσμένος_χρήση, δομή_διαδρομή / 'remote/libassh.a', δομή_διαδρομή / 'remote/libbearssl.a', '--end-group'])
    εκτελώ_εντολή([αντικείμενο_Αρχείο_μετατροπέας, '-O', 'binary', δομή_διαδρομή / 'kernel.elf', δομή_διαδρομή / 'kernel8.img'])
    πακέτο_διακήρυξη = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'ελληνικά.ίδιο', 'korean_exceptions': 20,
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
    for Όνομα in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        πακέτο_διακήρυξη['sha256'][Όνομα] = hashlib.sha256((δομή_διαδρομή / Όνομα).read_bytes()).hexdigest()
    (δομή_διαδρομή / 'build.json').write_text(json.dumps(πακέτο_διακήρυξη, indent=2) + '\n')
    print('완료:', δομή_διαδρομή / 'kernel8.img')


if __name__ == '__main__':
    Εκτέλεση_2()
