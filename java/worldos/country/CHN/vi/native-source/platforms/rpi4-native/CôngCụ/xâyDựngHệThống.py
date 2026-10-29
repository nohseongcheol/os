#!/usr/bin/env python3
"""Chủ javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from xâyDựngKhôngGianNgườiDùng import tạoKhôngGianNgườiDùng
from xâyDựngMạng import tạoMạng
from xâyDựngCácVíDụ import tạoCácVíDụ
from xâyDựngTừXa import tạoTừXa

gốcCâyDựÁn = Path(__file__).resolve().parents[1]
gốcCâyKhoNguồn = gốcCâyDựÁn.parents[1]
xâyDựngĐườngDẫn = gốcCâyDựÁn / 'build'


def thựcThiLệnh(mảngĐốiSố):
    subprocess.check_call([str(giáTrịĐầuTiên) for giáTrịĐầuTiên in mảngĐốiSố], cwd=str(gốcCâyDựÁn))


def chạy():
    xâyDựngĐườngDẫn.mkdir(exist_ok=True)
    TrìnhBiênDịchC = os.environ.get('ARM64_CC', 'clang')
    trìnhBiênDịchCộngCộng = os.environ.get('ARM64_CXX', 'clang++')
    côngCụTrìnhLiênKết = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    bộChuyểnĐổiTệpĐốiTượng = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    côngCụKhoLưuTrữ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for CôngCụ in ('javac', TrìnhBiênDịchC, trìnhBiênDịchCộngCộng, côngCụTrìnhLiênKết, bộChuyểnĐổiTệpĐốiTượng, côngCụKhoLưuTrữ):
        if not shutil.which(CôngCụ):
            raise SystemExit('필요한 xâyDựngHệThống CôngCụ phươngThứcThiếu: ' + CôngCụ)
    thôngTinPhôngChữ = json.loads((gốcCâyDựÁn / 'vendor/terminal-font.json').read_text())
    dữLiệuPhôngChữ = (gốcCâyDựÁn / 'vendor/terminal-font.bin').read_bytes()
    if len(dữLiệuPhôngChữ) != 65616 * 32 or hashlib.sha256(dữLiệuPhôngChữ).hexdigest() != thôngTinPhôngChữ['sha256']:
        raise SystemExit('thiếtBịCuối giáTrịPhôngChữ cỡ/SHA256 불일치')
    bảngTraXuất = {'jshell_interactive': 'VàoRaVỏLệnh.làTươngTác', 'jshell_output': 'VàoRaVỏLệnh.ĐầuRa', 'jshell_input': 'VàoRaVỏLệnh.giáTrịVào', 'java_task': 'Nhân.TácVụ', 'jfs_path_start': 'CácTệpBộNhớ.bắtChạyĐườngDẫn',
               'jfs_path_byte': 'CácTệpBộNhớ.byteĐườngDẫn', 'jfs_open': 'CácTệpBộNhớ.mở',
               'jfs_read': 'CácTệpBộNhớ.đọc', 'jfs_write': 'CácTệpBộNhớ.ghi',
               'jfs_seek': 'CácTệpBộNhớ.dịchVịVịTrí', 'jfs_close': 'CácTệpBộNhớ.đóng',
               'jfs_size': 'CácTệpBộNhớ.cỡ', 'jfs_unlink': 'CácTệpBộNhớ.xóaMục',
               'jfs_truncate': 'CácTệpBộNhớ.đặtGiáTrịĐộDài'}
    bảngTraXuất.update({'jfs_entry_count': 'CácTệpBộNhớ.giớiHạnTệp', 'jfs_entry_length': 'CácTệpBộNhớ.độDàiTênĐãXuất', 'jfs_entry_byte': 'CácTệpBộNhớ.byteTênĐãXuất', 'jfs_entry_size': 'CácTệpBộNhớ.cỡTệpĐãXuất'})
    bảngTraXuất.update({'jdraw_prepare': 'BộGhépBộĐệmKhung.chuẩnBị', 'jdraw_width': 'BộGhépBộĐệmKhung.lấyRộng',
        'jdraw_height': 'BộGhépBộĐệmKhung.lấyCao', 'jdraw_count_low': 'BộGhépBộĐệmKhung.lấyThấpBộĐếm',
        'jdraw_count_high': 'BộGhépBộĐệmKhung.lấyCaoTrênBộĐếm', 'jdraw_clip': 'BộGhépBộĐệmKhung.cắtXén',
        'jdraw_clip_value': 'BộGhépBộĐệmKhung.giáTrịCắtXén', 'jdraw_begin': 'BộGhépBộĐệmKhung.chạy',
        'jdraw_end': 'BộGhépBộĐệmKhung.hoànThành', 'jdraw_pixel': 'BộGhépBộĐệmKhung.điểmẢnh',
        'jdraw_rectangle': 'BộGhépBộĐệmKhung.lấpHìnhChữNhật', 'jdraw_pointer': 'BộGhépBộĐệmKhung.conTrỏ'})
    bảngTraXuất.update({'jfs_mkdir': 'CácTệpBộNhớ.tạoThưMục', 'jfs_rmdir': 'CácTệpBộNhớ.gỡThưMục', 'jfs_kind': 'CácTệpBộNhớ.loạiMục'})
    bảngTraXuất.update({'jnet_socket': 'MạngVòngVề.tạoMục', 'jnet_bind': 'MạngVòngVề.GóiTệpThựcThi',
        'jnet_put': 'MạngVòngVề.đặtDữLiệu', 'jnet_get': 'MạngVòngVề.đọcDữLiệu', 'jnet_send': 'MạngVòngVề.gửi',
        'jnet_recv': 'MạngVòngVề.nhận', 'jnet_port': 'MạngVòngVề.đọcCổngĐiểmCuối', 'jnet_address': 'MạngVòngVề.đọcĐịaChỉ',
        'jnet_peer': 'MạngVòngVề.điểmCuốiBộGửi', 'jnet_close': 'MạngVòngVề.đóng'})
    bảngTraXuất.update({'jstream_create': 'MạngLuồng.tạoMục', 'jstream_bind': 'MạngLuồng.GóiTệpThựcThi', 'jstream_listen': 'MạngLuồng.lắngNgheĐiểmCuối', 'jstream_connect': 'MạngLuồng.nốiKết', 'jstream_accept': 'MạngLuồng.chấpNhậnKếtNối', 'jstream_read': 'MạngLuồng.đọc', 'jstream_write': 'MạngLuồng.ghi', 'jstream_port': 'MạngLuồng.đọcCổngĐiểmCuối', 'jstream_peer': 'MạngLuồng.đọcCổngĐốiTác', 'jstream_close': 'MạngLuồng.đóng'})
    for giáTrịKýHiệu in list(bảngTraXuất):
        if giáTrịKýHiệu.startswith('jstream_') or giáTrịKýHiệu.startswith('jnet_') and giáTrịKýHiệu not in ('jnet_put', 'jnet_get'):
            bảngTraXuất[giáTrịKýHiệu.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = bảngTraXuất.pop(giáTrịKýHiệu)
    cácMụcVíDụ = ['public final class GóiGộp { public static void chuẩnBị() {']
    for đườngDẫn in sorted((gốcCâyDựÁn / 'VíDụ').iterdir()):
        if đườngDẫn.is_file():
            cácMụcVíDụ.append('TrìnhThôngDịchLệnh.tệpTĩnh(%s, %s);' %
                (json.dumps(đườngDẫn.name), json.dumps(đườngDẫn.read_text(encoding='utf-8'), ensure_ascii=True)))
    (xâyDựngĐườngDẫn / 'GóiGộp.java').write_text('\n'.join(cácMụcVíDụ + ['}}']), encoding='utf-8')
    tạoCácVíDụ(gốcCâyDựÁn, gốcCâyKhoNguồn, thựcThiLệnh)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(xâyDựngĐườngDẫn)) as đườngDẫnĐangLàmViệc:
        đườngDẫnLớp = Path(đườngDẫnĐangLàmViệc)
        thựcThiLệnh(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', đườngDẫnLớp, '-sourcepath', đườngDẫnLớp, '-d', đườngDẫnLớp] + sorted((gốcCâyDựÁn / 'mãNguồn').glob('*.java')) + [xâyDựngĐườngDẫn / 'GóiGộp.java', xâyDựngĐườngDẫn / 'GóiGộpVíDụ.java'])
        # Tệp·vỏLệnh·cửaSổ 세션·통신과 Java MànHình 합성 배열을 xâyDựngTấtCả 수용한다.
        mảngĐốiSố = ['sh', gốcCâyKhoNguồn / 'compiler/thờiGianCủaTrước.sh', '--entry', 'Nhân.chạy', '--heap-words', '1048576', '-o', xâyDựngĐườngDẫn / 'kernel-java.c']
        for giáTrịKýHiệu, mụcPhươngThức in sorted(bảngTraXuất.items()):
            mảngĐốiSố += ['--export', giáTrịKýHiệu + '=' + mụcPhươngThức]
        thựcThiLệnh(mảngĐốiSố + sorted(đườngDẫnLớp.glob('*.class')))
    (xâyDựngĐườngDẫn / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    cácBitCấuHình = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    pOSIX = gốcCâyKhoNguồn / 'posix-kor/arm64-native'
    tạoKhôngGianNgườiDùng(gốcCâyDựÁn, gốcCâyKhoNguồn, TrìnhBiênDịchC, trìnhBiênDịchCộngCộng, côngCụTrìnhLiênKết, côngCụKhoLưuTrữ, cácBitCấuHình, thựcThiLệnh)
    mạng = tạoMạng(gốcCâyDựÁn, TrìnhBiênDịchC, côngCụKhoLưuTrữ, cácBitCấuHình, thựcThiLệnh)
    dùngTừXa = tạoTừXa(gốcCâyDựÁn, TrìnhBiênDịchC, côngCụKhoLưuTrữ, cácBitCấuHình, thựcThiLệnh)
    cóBaoGồm = ['-I', pOSIX / 'TệpĐầuMục', '-I', xâyDựngĐườngDẫn]
    xâyDựngCácCôngViệc = [(TrìnhBiênDịchC, [], xâyDựngĐườngDẫn / 'terminal-font.S', 'font.o'),
            (TrìnhBiênDịchC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], gốcCâyDựÁn / 'máy/thiếtBịCuối.c', 'terminal.o'),
            (TrìnhBiênDịchC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], gốcCâyDựÁn / 'máy/ThànhTốGiaoDiện.c', 'widgets.o'),
            (TrìnhBiênDịchC, ['-std=c11'], xâyDựngĐườngDẫn / 'kernel-java.c', 'java.o'),
            (TrìnhBiênDịchC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], gốcCâyDựÁn / 'máy/BoMạch.c', 'board.o'),
            (TrìnhBiênDịchC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], gốcCâyDựÁn / 'máy/bảnVẽMànHình.c', 'drawing.o'),
            (TrìnhBiênDịchC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], gốcCâyDựÁn / 'máy/NgườiDùng.c', 'user.o'),
            (TrìnhBiênDịchC, [], gốcCâyDựÁn / 'KhởiĐộng/giáTrịĐiểmMục.S', 'entry.o'),
            (TrìnhBiênDịchC, ['-std=c11', '-Wall', '-Wextra', '-Werror'], pOSIX / 'nốiKết.c', 'posix.o'),
            (trìnhBiênDịchCộngCộng, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], gốcCâyDựÁn / 'KiểmThử/CácLờiGọiTệp.cpp', 'cpp.o')]
    for côngCụTrìnhBiênDịch, miềnBổSung, dữLiệuNguyênBản, đầuRa in xâyDựngCácCôngViệc:
        cấuHìnhNguyênBản = [mụcTệp for mụcTệp in cácBitCấuHình if mụcTệp != '-mgeneral-regs-only'] if dữLiệuNguyênBản.suffix == '.S' else cácBitCấuHình
        thựcThiLệnh([côngCụTrìnhBiênDịch] + cấuHìnhNguyênBản + miềnBổSung + cóBaoGồm + ['-c', dữLiệuNguyênBản, '-o', xâyDựngĐườngDẫn / đầuRa])
    thựcThiLệnh([côngCụKhoLưuTrữ, 'rcs', xâyDựngĐườngDẫn / 'libposix-kor-arm64.a', xâyDựngĐườngDẫn / 'posix.o'])
    thựcThiLệnh([côngCụTrìnhLiênKết, '--gc-sections', '-T', gốcCâyDựÁn / 'KhởiĐộng/BốTríLiênKết.ld', '-Map', xâyDựngĐườngDẫn / 'kernel.map', '-o', xâyDựngĐườngDẫn / 'kernel.elf'] +
        [xâyDựngĐườngDẫn / tên for tên in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', xâyDựngĐườngDẫn / 'libposix-kor-arm64.a', mạng, dùngTừXa, xâyDựngĐườngDẫn / 'remote/libassh.a', xâyDựngĐườngDẫn / 'remote/libbearssl.a', '--end-group'])
    thựcThiLệnh([bộChuyểnĐổiTệpĐốiTượng, '-O', 'binary', xâyDựngĐườngDẫn / 'kernel.elf', xâyDựngĐườngDẫn / 'kernel8.img'])
    bảnKêGóiGộp = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'tiếngViệt.tựThân', 'korean_exceptions': 20,
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
    for tên in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        bảnKêGóiGộp['sha256'][tên] = hashlib.sha256((xâyDựngĐườngDẫn / tên).read_bytes()).hexdigest()
    (xâyDựngĐườngDẫn / 'build.json').write_text(json.dumps(bảnKêGóiGộp, indent=2) + '\n')
    print('làĐầyĐủ:', xâyDựngĐườngDẫn / 'kernel8.img')


if __name__ == '__main__':
    chạy()
