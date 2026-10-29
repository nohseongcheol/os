#!/usr/bin/env python3
"""Host javac/Clang으로 Linux 없이 실행되는 Pi4 커널을 만든다."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from buildUserSpace import createUserSpace
from buildNetwork import createNetwork
from buildExamples import createExamples
from buildRemote import createRemote

projectRoot = Path(__file__).resolve().parents[1]
repositoryRoot = projectRoot.parents[1]
buildPath = projectRoot / 'build'


def executeCommand(argumentArray):
    subprocess.check_call([str(firstValue) for firstValue in argumentArray], cwd=str(projectRoot))


def run():
    buildPath.mkdir(exist_ok=True)
    CCompiler = os.environ.get('ARM64_CC', 'clang')
    cppCompiler = os.environ.get('ARM64_CXX', 'clang++')
    linkerTool = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    objectFileConverter = os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy')
    archiveTool = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    for tools in ('javac', CCompiler, cppCompiler, linkerTool, objectFileConverter, archiveTool):
        if not shutil.which(tools):
            raise SystemExit('필요한 buildSystem tools missingMethod: ' + tools)
    fontInformation = json.loads((projectRoot / 'vendor/terminal-font.json').read_text())
    fontData = (projectRoot / 'vendor/terminal-font.bin').read_bytes()
    if len(fontData) != 65616 * 32 or hashlib.sha256(fontData).hexdigest() != fontInformation['sha256']:
        raise SystemExit('terminal fontValue size/SHA256 불일치')
    exportTable = {'jshell_interactive': 'ShellIO.isInteractive', 'jshell_output': 'ShellIO.Output', 'jshell_input': 'ShellIO.inputValue', 'java_task': 'Kernel.performTask', 'jfs_path_start': 'MemoryFiles.pathStart',
               'jfs_path_byte': 'MemoryFiles.pathByte', 'jfs_open': 'MemoryFiles.open',
               'jfs_read': 'MemoryFiles.read', 'jfs_write': 'MemoryFiles.write',
               'jfs_seek': 'MemoryFiles.seekPosition', 'jfs_close': 'MemoryFiles.close',
               'jfs_size': 'MemoryFiles.size', 'jfs_unlink': 'MemoryFiles.eraseEntry',
               'jfs_truncate': 'MemoryFiles.setLength'}
    exportTable.update({'jfs_entry_count': 'MemoryFiles.fileLimit', 'jfs_entry_length': 'MemoryFiles.exportedNameLength', 'jfs_entry_byte': 'MemoryFiles.exportedNameByte', 'jfs_entry_size': 'MemoryFiles.exportedFileSize'})
    exportTable.update({'jdraw_prepare': 'FramebufferComposer.prepare', 'jdraw_width': 'FramebufferComposer.getWidth',
        'jdraw_height': 'FramebufferComposer.getHeight', 'jdraw_count_low': 'FramebufferComposer.getCounterLow',
        'jdraw_count_high': 'FramebufferComposer.getCounterHigh', 'jdraw_clip': 'FramebufferComposer.clip',
        'jdraw_clip_value': 'FramebufferComposer.clipValue', 'jdraw_begin': 'FramebufferComposer.run',
        'jdraw_end': 'FramebufferComposer.finish', 'jdraw_pixel': 'FramebufferComposer.pixel',
        'jdraw_rectangle': 'FramebufferComposer.rectangleFill', 'jdraw_pointer': 'FramebufferComposer.pointer'})
    exportTable.update({'jfs_mkdir': 'MemoryFiles.createDirectory', 'jfs_rmdir': 'MemoryFiles.removeDirectory', 'jfs_kind': 'MemoryFiles.entryKind'})
    exportTable.update({'jnet_socket': 'LoopbackNetwork.createEntry', 'jnet_bind': 'LoopbackNetwork.bindEndpoint',
        'jnet_put': 'LoopbackNetwork.putData', 'jnet_get': 'LoopbackNetwork.readData', 'jnet_send': 'LoopbackNetwork.send',
        'jnet_recv': 'LoopbackNetwork.receive', 'jnet_port': 'LoopbackNetwork.readEndpointPort', 'jnet_address': 'LoopbackNetwork.readAddress',
        'jnet_peer': 'LoopbackNetwork.senderEndpoint', 'jnet_close': 'LoopbackNetwork.close'})
    exportTable.update({'jstream_create': 'StreamNetwork.createEntry', 'jstream_bind': 'StreamNetwork.bindEndpoint', 'jstream_listen': 'StreamNetwork.listenEndpoint', 'jstream_connect': 'StreamNetwork.connect', 'jstream_accept': 'StreamNetwork.acceptConnection', 'jstream_read': 'StreamNetwork.read', 'jstream_write': 'StreamNetwork.write', 'jstream_port': 'StreamNetwork.readEndpointPort', 'jstream_peer': 'StreamNetwork.readPeerPort', 'jstream_close': 'StreamNetwork.close'})
    for symbolValue in list(exportTable):
        if symbolValue.startswith('jstream_') or symbolValue.startswith('jnet_') and symbolValue not in ('jnet_put', 'jnet_get'):
            exportTable[symbolValue.replace('jstream_', 'jloopstream_').replace('jnet_', 'jloopnet_')] = exportTable.pop(symbolValue)
    exampleEntries = ['public final class Bundle { public static void prepare() {']
    for path in sorted((projectRoot / 'examples').iterdir()):
        if path.is_file():
            exampleEntries.append('CommandInterpreter.staticFile(%s, %s);' %
                (json.dumps(path.name), json.dumps(path.read_text(encoding='utf-8'), ensure_ascii=True)))
    (buildPath / 'Bundle.java').write_text('\n'.join(exampleEntries + ['}}']), encoding='utf-8')
    createExamples(projectRoot, repositoryRoot, executeCommand)
    with tempfile.TemporaryDirectory(prefix='classes-', dir=str(buildPath)) as workingPath:
        classPath = Path(workingPath)
        executeCommand(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', classPath, '-sourcepath', classPath, '-d', classPath] + sorted((projectRoot / 'source').glob('*.java')) + [buildPath / 'Bundle.java', buildPath / 'ExampleBundle.java'])
        # file·shell·window 세션·통신과 Java Screen 합성 배열을 buildAll 수용한다.
        argumentArray = ['sh', repositoryRoot / 'compiler/aheadOfTime.sh', '--entry', 'Kernel.run', '--heap-words', '1048576', '-o', buildPath / 'kernel-java.c']
        for symbolValue, methodEntry in sorted(exportTable.items()):
            argumentArray += ['--export', symbolValue + '=' + methodEntry]
        executeCommand(argumentArray + sorted(classPath.glob('*.class')))
    (buildPath / 'terminal-font.S').write_text('.section .rodata.font,"a"\n.balign 16\n.global terminal_font\nterminal_font:\n.incbin "vendor/terminal-font.bin"\n.section .note.GNU-stack,"",%progbits\n')
    configurationBits = ['--target=aarch64-none-elf', '-mcpu=cortex-a72', '-mgeneral-regs-only',
             '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
             '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2']
    posix = repositoryRoot / 'posix-kor/arm64-native'
    createUserSpace(projectRoot, repositoryRoot, CCompiler, cppCompiler, linkerTool, archiveTool, configurationBits, executeCommand)
    network = createNetwork(projectRoot, CCompiler, archiveTool, configurationBits, executeCommand)
    remoteUse = createRemote(projectRoot, CCompiler, archiveTool, configurationBits, executeCommand)
    includes = ['-I', posix / 'headers', '-I', buildPath]
    buildJobs = [(CCompiler, [], buildPath / 'terminal-font.S', 'font.o'),
            (CCompiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projectRoot / 'machine/terminal.c', 'terminal.o'),
            (CCompiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projectRoot / 'machine/Widget.c', 'widgets.o'),
            (CCompiler, ['-std=c11'], buildPath / 'kernel-java.c', 'java.o'),
            (CCompiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projectRoot / 'machine/Board.c', 'board.o'),
            (CCompiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projectRoot / 'machine/screenDrawing.c', 'drawing.o'),
            (CCompiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], projectRoot / 'machine/User.c', 'user.o'),
            (CCompiler, [], projectRoot / 'machine_boot/entryPointValue.S', 'entry.o'),
            (CCompiler, ['-std=c11', '-Wall', '-Wextra', '-Werror'], posix / 'connect.c', 'posix.o'),
            (cppCompiler, ['-std=c++11', '-fno-exceptions', '-fno-rtti', '-Wall', '-Wextra', '-Werror'], projectRoot / 'tests/FileCalls.cpp', 'cpp.o')]
    for compilerTool, additionalRegion, originalData, output in buildJobs:
        originalConfiguration = [fileEntry for fileEntry in configurationBits if fileEntry != '-mgeneral-regs-only'] if originalData.suffix == '.S' else configurationBits
        executeCommand([compilerTool] + originalConfiguration + additionalRegion + includes + ['-c', originalData, '-o', buildPath / output])
    executeCommand([archiveTool, 'rcs', buildPath / 'libposix-kor-arm64.a', buildPath / 'posix.o'])
    executeCommand([linkerTool, '--gc-sections', '-T', projectRoot / 'machine_boot/link_layout.ld', '-Map', buildPath / 'kernel.map', '-o', buildPath / 'kernel.elf'] +
        [buildPath / name for name in ('entry.o', 'java.o', 'board.o', 'drawing.o', 'terminal.o', 'widgets.o', 'font.o', 'user.o', 'programs.o', 'cpp.o')] + ['--start-group', buildPath / 'libposix-kor-arm64.a', network, remoteUse, buildPath / 'remote/libassh.a', buildPath / 'remote/libbearssl.a', '--end-group'])
    executeCommand([objectFileConverter, '-O', 'binary', buildPath / 'kernel.elf', buildPath / 'kernel8.img'])
    bundleManifest = {'target': 'raspberry-pi-4-bare-metal-aarch64', 'linux': False,
                'java': 'static subset AOT through freestanding C',
                'openjdk': False, 'guest_java': 'jkoros JVM 0.4, class 45..52 and JAR subset; subset source compiler',
                'guest_c_compiler': 'TinyCC ARM64, native ABI, freestanding C / Korean POSIX',
                'guest_aot': 'jaot: static Java 8 int/reference subset -> TinyCC -> native ARM64 ELF',
                'all_class_or_jar_compatible': False,
                'java_runtime': {'classes': 16, 'threads': 4, 'heap_slots': 32768,
                                 'objects': True, 'exceptions': 'subset', 'gc': 'mark-sweep',
                                 'network': 'java.net datagram and stream IPv4 subset; lwIP/SLIP plus Java loopback', 'korean_package': 'English.Native', 'korean_exceptions': 20,
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
    for name in ('kernel8.img', 'kernel.elf', 'libposix-kor-arm64.a', 'libposix-kor-user.a', 'user/demo.elf', 'user/fault.elf', 'user/network.elf', 'user/java-tools.elf', 'user/python.elf', 'user/vi.elf', 'user/cc.elf'):
        bundleManifest['sha256'][name] = hashlib.sha256((buildPath / name).read_bytes()).hexdigest()
    (buildPath / 'build.json').write_text(json.dumps(bundleManifest, indent=2) + '\n')
    print('isComplete:', buildPath / 'kernel8.img')


if __name__ == '__main__':
    run()
