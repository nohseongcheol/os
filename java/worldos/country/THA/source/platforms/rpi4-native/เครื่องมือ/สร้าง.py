#!/usr/bin/env python3
"""โฮสต์ javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from รุ่น_ผู้ใช้_สเปซ import เปิด_ผู้ใช้_สเปซ
from รุ่น_เครือข่าย import เปิด_เครือข่าย_48d29d6d
from 예제빌드 import 예제만들기
from รุ่น_ระยะไกล import เปิด_ระยะไกล

แสดง_ราก = Path(__file__).resolve().parents[1]
ที่เก็บ_ราก = แสดง_ราก.parents[1]
รุ่น_พาธ = แสดง_ราก / 'build'


def ดําเนินการ_คําสั่ง(อาร์กิวเมนต์_อาร์เรย์):
    subprocess.check_call([str(첫째값) for 첫째값 in อาร์กิวเมนต์_อาร์เรย์], cwd=str(แสดง_ราก))


def เรียกใช้งาน():
    รุ่น_พาธ.mkdir(exist_ok=True)
    시언어번역기 = os.environ.get('ARM64_CC', 'clang')
    시플플번역기 = os.environ.get('ARM64_CXX', 'clang++')
    ตัวเชื่อมโยง_เครื่องมือ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    วัตถุ_แฟ้ม_ตัวแปลง = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    เก็บถาวร_เครื่องมือ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for เครื่องมือ in ('javac', 시언어번역기, 시플플번역기, ตัวเชื่อมโยง_เครื่องมือ, วัตถุ_แฟ้ม_ตัวแปลง, เก็บถาวร_เครื่องมือ):
        if not shutil.which(เครื่องมือ):
            raise SystemExit('필요한 สร้าง เครื่องมือ 없음: ' + เครื่องมือ)
    ฟอนต์_ข้อมูล_c16c0f1c = json.loads((แสดง_ราก / 'vendor/terminal-font.json').read_text())
    ฟอนต์_ข้อมูล = (แสดง_ราก / 'vendor/terminal-font.bin').read_bytes()
    if len(ฟอนต์_ข้อมูล) != 65616 * 32 or hashlib.sha256(ฟอนต์_ข้อมูล).hexdigest() != ฟอนต์_ข้อมูล_c16c0f1c['sha256']:
        raise SystemExit('เทอร์มินัล ฟอนต์_ค่า ขนาด/SHA256 불일치')
    ส่งออก_ตาราง = {'jshell_interactive': '셸입출력.대화가능', 'jshell_output': '셸입출력.ข้อความออก', 'jshell_input': '셸입출력.입력', 'java_task': 'แก่นระบบ.작업', 'jfs_path_start': 'แฟ้มในหน่วยความจํา.พาธ_เริ่ม',
               'jfs_path_byte': 'แฟ้มในหน่วยความจํา.พาธ_ไบต์', 'jfs_open': 'แฟ้มในหน่วยความจํา.เปิด',
               'jfs_read': 'แฟ้มในหน่วยความจํา.อ่าน', 'jfs_write': 'แฟ้มในหน่วยความจํา.เขียน',
               'jfs_seek': 'แฟ้มในหน่วยความจํา.กรอ_ตําแหน่ง', 'jfs_close': 'แฟ้มในหน่วยความจํา.ปิด',
               'jfs_size': 'แฟ้มในหน่วยความจํา.ขนาด', 'jfs_unlink': 'แฟ้มในหน่วยความจํา.ลบ_รายการ',
               'jfs_truncate': 'แฟ้มในหน่วยความจํา.길이정하기'}
    ส่งออก_ตาราง.update({'jfs_entry_count': 'แฟ้มในหน่วยความจํา.파일한도', 'jfs_entry_length': 'แฟ้มในหน่วยความจํา.공개이름길이', 'jfs_entry_byte': 'แฟ้มในหน่วยความจํา.공개이름바이트', 'jfs_entry_size': 'แฟ้มในหน่วยความจํา.공개파일크기'})
    ส่งออก_ตาราง.update({'jdraw_prepare': '화면합성.จัดเตรียม', 'jdraw_width': '화면합성.너비얻기',
        'jdraw_height': '화면합성.높이얻기', 'jdraw_count_low': '화면합성.기록아래얻기',
        'jdraw_count_high': '화면합성.기록위얻기', 'jdraw_clip': '화면합성.คลิป',
        'jdraw_clip_value': '화면합성.คลิป_ค่า', 'jdraw_begin': '화면합성.เรียกใช้งาน',
        'jdraw_end': '화면합성.เสร็จสิ้น', 'jdraw_pixel': '화면합성.พิกเซล',
        'jdraw_rectangle': '화면합성.สี่เหลี่ยมผืนผ้า_เติม', 'jdraw_pointer': '화면합성.ตัวชี้'})
    ส่งออก_ตาราง.update({'jfs_mkdir': 'แฟ้มในหน่วยความจํา.เปิด_ไดเรกทอรี', 'jfs_rmdir': 'แฟ้มในหน่วยความจํา.นําออก_ไดเรกทอรี', 'jfs_kind': 'แฟ้มในหน่วยความจํา.항목종류'})
    ส่งออก_ตาราง.update({'jnet_socket': 'วนกลับ_เครือข่าย.เปิด_รายการ', 'jnet_bind': 'วนกลับ_เครือข่าย.ผูก_ปลายทาง',
        'jnet_put': 'วนกลับ_เครือข่าย.자료넣기', 'jnet_get': 'วนกลับ_เครือข่าย.자료읽기', 'jnet_send': 'วนกลับ_เครือข่าย.ส่ง',
        'jnet_recv': 'วนกลับ_เครือข่าย.รับ', 'jnet_port': 'วนกลับ_เครือข่าย.창구읽기', 'jnet_address': 'วนกลับ_เครือข่าย.주소읽기',
        'jnet_peer': 'วนกลับ_เครือข่าย.ผู้ส่ง_ปลายทาง', 'jnet_close': 'วนกลับ_เครือข่าย.ปิด'})
    ส่งออก_ตาราง.update({'jstream_create': 'สตรีม_เครือข่าย.เปิด_รายการ', 'jstream_bind': 'สตรีม_เครือข่าย.ผูก_ปลายทาง', 'jstream_listen': 'สตรีม_เครือข่าย.รอการติดต่อ_ปลายทาง', 'jstream_connect': 'สตรีม_เครือข่าย.เชื่อมต่อ', 'jstream_accept': 'สตรีม_เครือข่าย.ยอมรับ_เพื่อน', 'jstream_read': 'สตรีม_เครือข่าย.อ่าน', 'jstream_write': 'สตรีม_เครือข่าย.เขียน', 'jstream_port': 'สตรีม_เครือข่าย.창구읽기', 'jstream_peer': 'สตรีม_เครือข่าย.상대창구읽기', 'jstream_close': 'สตรีม_เครือข่าย.ปิด'})
    for สัญลักษณ์_ค่า in list(ส่งออก_ตาราง):
        if สัญลักษณ์_ค่า.startswith('jstream_') or สัญลักษณ์_ค่า.startswith('jnet_') and สัญลักษณ์_ค่า not in ('jnet_put', 'jnet_get'):
            ส่งออก_ตาราง[สัญลักษณ์_ค่า.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = ส่งออก_ตาราง.pop(สัญลักษณ์_ค่า)
    예제들 = ['public final class รวม { public static void จัดเตรียม() {']
    for เส้นทาง in sorted((แสดง_ราก / '예제').iterdir()):
        if เส้นทาง.is_file():
            예제들.append('ตัวแปลคําสั่ง.คงที่_แฟ้ม(%s, %s);' %
                (json.dumps(เส้นทาง.name), json.dumps(เส้นทาง.read_text(encoding='utf-8'), ensure_ascii=True)))
    (รุ่น_พาธ / 'รวม.java').write_text('\n'.join(예제들 + ['}}']), encoding='utf-8')
    예제만들기(แสดง_ราก, ที่เก็บ_ราก, ดําเนินการ_คําสั่ง)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(รุ่น_พาธ)) as 작업경로:
        คลาส_พาธ = Path(작업경로)
        ดําเนินการ_คําสั่ง(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', คลาส_พาธ, '-sourcepath', คลาส_พาธ, '-d', คลาส_พาธ] + sorted((แสดง_ราก / 'รหัสต้นฉบับ').glob('*.java')) + [รุ่น_พาธ / 'รวม.java', รุ่น_พาธ / '예제꾸러미.java'])
        # แฟ้ม·เชลล์·หน้าต่าง 세션·통신과 Java 화면 합성 배열을 모두 수용한다.
        อาร์กิวเมนต์_อาร์เรย์ = ['sh', ที่เก็บ_ราก / 'compiler/미리번역.sh', '--entry', 'แก่นระบบ.เรียกใช้งาน', '--heap-words', '1048576', '-o', รุ่น_พาธ / 'kernel-java.c']
        for สัญลักษณ์_ค่า, เมธอด_รายการ in sorted(ส่งออก_ตาราง.items()):
            อาร์กิวเมนต์_อาร์เรย์ += ['--export', สัญลักษณ์_ค่า + '=' + เมธอด_รายการ]
        ดําเนินการ_คําสั่ง(อาร์กิวเมนต์_อาร์เรย์ + sorted(คลาส_พาธ.glob('*.class')))
    (รุ่น_พาธ / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    설정비트 = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    포직스경로 = ที่เก็บ_ราก / 'posix-kor/arm64-native'
    เปิด_ผู้ใช้_สเปซ(แสดง_ราก, ที่เก็บ_ราก, 시언어번역기, 시플플번역기, ตัวเชื่อมโยง_เครื่องมือ, เก็บถาวร_เครื่องมือ, 설정비트, ดําเนินการ_คําสั่ง)
    เครือข่าย_9b2e3222 = เปิด_เครือข่าย_48d29d6d(แสดง_ราก, 시언어번역기, เก็บถาวร_เครื่องมือ, 설정비트, ดําเนินการ_คําสั่ง)
    ระยะไกล_ใช้ = เปิด_ระยะไกล(แสดง_ราก, 시언어번역기, เก็บถาวร_เครื่องมือ, 설정비트, ดําเนินการ_คําสั่ง)
    포함인수 = ['-I', 포직스경로 / '포함', '-I', รุ่น_พาธ]
    빌드작업 = [(시언어번역기, [], รุ่น_พาธ / 'terminal-font.S', 'font.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], แสดง_ราก / 'เครื่อง/เทอร์มินัล.c', 'terminal.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], แสดง_ราก / 'เครื่อง/วิดเจ็ต.c', 'widgets.o'),
            (시언어번역기, ['-std=c11'], รุ่น_พาธ / 'kernel-java.c', 'java.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], แสดง_ราก / 'เครื่อง/บอร์ด.c', 'board.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], แสดง_ราก / 'เครื่อง/화면그림.c', 'drawing.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], แสดง_ราก / 'เครื่อง/ผู้ใช้.c', 'user.o'),
            (시언어번역기, [], แสดง_ราก / '부팅/จุดเข้าใช้งาน_ค่า.S', 'entry.o'),
            (시언어번역기, ['-std=c11', '-Wall', '-Wextra', '-Werror'], 포직스경로 / 'เชื่อมต่อ.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], แสดง_ราก / '시험/แฟ้ม_การโทร.cpp', 'cpp.o')]
    for คอมไพเลอร์_เครื่องมือ, 추가영역, 원본자료, ผลผลิต in 빌드작업:
        원본설정 = [แฟ้ม_รายการ_3d0c1245 for แฟ้ม_รายการ_3d0c1245 in 설정비트 if แฟ้ม_รายการ_3d0c1245 != '-mgeneral-regs-only'] if 원본자료.suffix == '.S' else 설정비트
        ดําเนินการ_คําสั่ง([คอมไพเลอร์_เครื่องมือ] + 원본설정 + 추가영역 + 포함인수 + ['-c', 원본자료, '-o', รุ่น_พาธ / ผลผลิต])
    ดําเนินการ_คําสั่ง([เก็บถาวร_เครื่องมือ, 'rcs', รุ่น_พาธ / 'libposix-kor-arm64.a', รุ่น_พาธ / 'posix.o'])
    ดําเนินการ_คําสั่ง([ตัวเชื่อมโยง_เครื่องมือ, '--gc-sections', '-T', แสดง_ราก / '부팅/ลิงก์_การนําทาง.ld', '-Map', รุ่น_พาธ / 'kernel.map', '-o', รุ่น_พาธ / 'kernel.elf'] +
        [รุ่น_พาธ / ชื่อ for ชื่อ in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', รุ่น_พาธ / 'libposix-kor-arm64.a', เครือข่าย_9b2e3222, ระยะไกล_ใช้, รุ่น_พาธ / 'remote/libassh.a', รุ่น_พาธ / 'remote/libbearssl.a', '--end-group'])
    ดําเนินการ_คําสั่ง([วัตถุ_แฟ้ม_ตัวแปลง, '-O', 'binary', รุ่น_พาธ / 'kernel.elf', รุ่น_พาธ / 'kernel8.img'])
    รวม_ไฟล์กํากับ = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'ไทย.เอง', 'korean_exceptions': 20,
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
    for ชื่อ in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        รวม_ไฟล์กํากับ['sha256'][ชื่อ] = hashlib.sha256((รุ่น_พาธ / ชื่อ).read_bytes()).hexdigest()
    (รุ่น_พาธ / 'build.json').write_text(json.dumps(รวม_ไฟล์กํากับ, indent=2) + '\n')
    print('완료:', รุ่น_พาธ / 'kernel8.img')


if __name__ == '__main__':
    เรียกใช้งาน()
