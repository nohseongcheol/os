#!/usr/bin/env python3
"""Real host TCP client -> SLIP -> bare-metal lwIP -> FTP -> Java VFS."""
import ftplib
import hashlib
import io
import json
import selectors
import socket
import subprocess
import time
import zipfile
from 网络桥接 import 网络桥接
from 执行命令 import 项目根, 命令
from 回显测试夹具 import 回显测试夹具
from 测试ELF import Linux示例


def 运行():
    结果数据 = 项目根 / 'build/verification/ftp'; 结果数据.mkdir(parents=True, exist_ok=True)
    有效性验证报告 = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((项目根 / 'build/kernel8.img').read_bytes()).hexdigest()}
    执行记录 = bytearray()
    Java源代码 = 结果数据 / '测试捆绑.java'
    Java源代码.write_text('public class 测试捆绑 { public static void main(String[] 实参) throws Exception { 中文.内置.输出.写入行("JAR 执行命令: " + 实参[0]); 中文.内置.文件.写入("jar.txt", "内置 内核值 文件"); 中文.内置.输出.写入行(中文.内置.文件.读取("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(项目根/'build/java-library/classes'), '-d', str(结果数据), str(Java源代码)])
    存档 = io.BytesIO()
    with zipfile.ZipFile(存档, 'w', zipfile.ZIP_DEFLATED) as Java捆绑:
        Java捆绑.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 测试捆绑\r\n\r\n')
        Java捆绑.write(str(结果数据/'测试捆绑.class'), '测试捆绑.class')
    with socket.socket() as 临时:
        临时.bind(('127.0.0.1', 0)); 端口编号 = 临时.getsockname()[1]
    with socket.socket() as 临时:
        临时.bind(('127.0.0.1', 0)); 服务器流端口 = 临时.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 临时:
        临时.bind(('127.0.0.1', 0)); 服务器数据报端口 = 临时.getsockname()[1]
    with 网络桥接(端口编号, ['tcp:{}:9300'.format(服务器流端口), 'udp:{}:9301'.format(服务器数据报端口)], 捕获=True) as 桥接:
        进程 = subprocess.Popen(命令() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 桥接.已转发参数(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        就绪选择器 = selectors.DefaultSelector(); 就绪选择器.register(进程.stdout, selectors.EVENT_READ)
        def 接收消息(标记=b'jkoros-native> ', 执行状态超时=60):
            数据 = bytearray(); 结束偏移 = time.monotonic() + 执行状态超时
            while 标记 not in 数据:
                if time.monotonic() > 结束偏移 or 进程.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + 数据.decode('utf-8', 'replace'))
                for 已按下值, _ in 就绪选择器.select(.1):
                    片段值 = 已按下值.fileobj.read(4096)
                    if 片段值: 数据.extend(片段值); 执行记录.extend(片段值)
                if b'PANIC:' in 数据 or b'FAIL ' in 数据: raise AssertionError(数据)
            return 数据.decode('utf-8', 'replace').replace('\r\n', '\n')
        def 命令壳(行):
            进程.stdin.write(行.encode() + b'\n'); 进程.stdin.flush(); return 接收消息()
        try:
            接收消息(); assert 'FTP listening' in 命令壳('ftpd start')
            文件传送连接状态 = ftplib.FTP(); 文件传送连接状态.encoding = 'utf-8'; 文件传送连接状态.connect('127.0.0.1', 端口编号, timeout=20); 文件传送连接状态.login()
            载荷数据数据 = bytes(range(256)) * 32
            文件传送连接状态.storbinary('STOR binary.dat', io.BytesIO(载荷数据数据))
            结果 = bytearray(); 文件传送连接状态.retrbinary('RETR binary.dat', 结果.extend)
            assert 结果 == 载荷数据数据; assert 文件传送连接状态.size('binary.dat') == len(载荷数据数据)
            有效性验证报告['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            文件传送连接状态.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in 命令壳('cat 한글.txt')
            assert '한글.txt' in 文件传送连接状态.nlst()
            assert dict(文件传送连接状态.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            有效性验证报告['checks'].append('UTF-8 filename and content visible in guest shell')
            try: 文件传送连接状态.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 辅助条目: assert str(辅助条目).startswith('552'), str(辅助条目)
            else: raise AssertionError('oversized upload accepted')
            结果 = bytearray(); 文件传送连接状态.retrbinary('RETR binary.dat', 结果.extend); assert 结果 == 载荷数据数据
            有效性验证报告['checks'].append('oversized replacement rejected; previous file preserved')
            with 文件传送连接状态.transfercmd('STOR pending.txt') as 上传文件集:
                # A control command must not change the active upload's destination.
                assert 文件传送连接状态.size('binary.dat') == len(载荷数据数据)
                上传文件集.sendall(b'UPLOAD TARGET PRESERVED')
            assert 文件传送连接状态.voidresp().startswith('226')
            结果 = bytearray(); 文件传送连接状态.retrbinary('RETR pending.txt', 结果.extend)
            assert 结果 == b'UPLOAD TARGET PRESERVED'
            结果 = bytearray(); 文件传送连接状态.retrbinary('RETR binary.dat', 结果.extend)
            assert 结果 == 载荷数据数据
            文件传送连接状态.delete('pending.txt')
            有效性验证报告['checks'].append('interleaved SIZE cannot change the active STOR destination')
            文件传送连接状态.storbinary('STOR 问候例.jar', io.BytesIO(存档.getvalue()))
            文本 = 命令壳('java -jar 问候例.jar 누리')
            assert 'JAR 执行命令: 누리' in 文本 and '内置 内核值 文件' in 文本 and 'exit 0' in 文本, 文本
            文本 = 命令壳('./问候例.jar 세상')
            assert 'JAR 执行命令: 세상' in 文本 and 'exit 0' in 文本, 文本
            有效性验证报告['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            原始数据 = '#include <文件ABI.h>\nstruct 数据 { int 数; double 비율; };\nint 总和值(int n) { return n ? n + 总和值(n-1) : 0; }\nint main(void) { struct 数据 值 = {总和值(10), 1.25}; if (值.数 != 55 || 值.비율 * 2 != 2.5) return 3; const char 问候例[] = "CC NATIVE PASS\\n"; int 文档集 = 打开文件("cc.txt", 读取写入 | 创建条件缺失 | 截断内容, 0600); if (文档集 < 0) return 1; 写入文件数据(文档集, 问候例, sizeof(问候例)-1); 关闭文件(文档集); 写入文件数据(1, 问候例, sizeof(问候例)-1); return 0; }\n'
            文件传送连接状态.storbinary('STOR 韩文文本.c', io.BytesIO(原始数据.encode()))
            文本 = 命令壳('cc 韩文文本.c -o 韩文文本.elf'); assert 'Compiled native ARM64 ELF:' in 文本 and 'exit 0' in 文本, 文本
            文本 = 命令壳('run 韩文文本.elf'); assert 'CC NATIVE PASS' in 文本 and 'exit 0' in 文本, 文本
            assert 'CC NATIVE PASS' in 命令壳('cat cc.txt')
            可执行文件文件 = bytearray(); 文件传送连接状态.retrbinary('RETR 韩文文本.elf', 可执行文件文件.extend)
            assert 可执行文件文件[:4] == b'\x7fELF' and 可执行文件文件[18:20] == b'\xb7\x00'
            文件传送连接状态.storbinary('STOR 复制值.elf', io.BytesIO(可执行文件文件)); 文本 = 命令壳('run 复制值.elf'); assert 'CC NATIVE PASS' in 文本 and 'exit 0' in 文本, 文本
            文件传送连接状态.storbinary('STOR 执行命令', io.BytesIO(可执行文件文件)); 文本=命令壳('./执行命令');assert 'CC NATIVE PASS' in 文本 and 'exit 0' in 文本,文本
            文件传送连接状态.storbinary('STOR 名称.txt', io.BytesIO(可执行文件文件)); 文本=命令壳('./名称.txt');assert 'CC NATIVE PASS' in 文本 and 'exit 0' in 文本,文本
            命令壳('rm 执行命令 名称.txt')
            有效性验证报告['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            命令壳('rm binary.dat 韩文文本.txt 韩文文本.c 韩文文本.elf 复制值.elf cc.txt jar.txt')
            Linux文件,预期=Linux示例(结果数据/'linux-reference')
            文件传送连接状态.storbinary('STOR 리눅스인사',io.BytesIO(Linux文件.read_bytes()))
            文本=命令壳('./리눅스인사');assert 'exit -8' in 文本,文本
            文本=命令壳('run --linux 리눅스인사 한글인수');assert 预期+'exit 0' in 文本,文本
            assert 'LINUX ELF FILE IO' in 命令壳('cat linux.txt')
            文件传送连接状态.delete('리눅스인사');文件传送连接状态.delete('linux.txt')
            文件传送连接状态.storbinary('STOR 假值.elf',io.BytesIO(b'plain text'))
            assert '실행할 数 없습니다:' in 命令壳('./假值.elf');文件传送连接状态.delete('假值.elf')
            有效性验证报告['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 回显测试夹具() as 回显服务器条目:
                网络层源代码 = 结果数据/'外部通信.java'
                网络层源代码.write_text('''import java.net.*; import java.io.*;
public class 外部通信 { public static void main(String[] args) throws Exception {
 Socket 连接 = 中文.内置.连接状态传输.连接("10.0.2.2", Integer.parseInt(args[0]));
 连接.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] 源代码 = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<源代码.length;i++) if (连接.getInputStream().read() != (源代码[i]&255)) throw new RuntimeException("TCP mismatch");
 连接.close();
 DatagramSocket 端点 = 中文.内置.通信.打开(0); 中文.内置.通信.超时(端点, 500);
 中文.内置.通信.发送(端点, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!中文.内置.通信.接收(端点).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 端点.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(项目根/'build/java-library/classes'),'-d',str(结果数据),str(网络层源代码)])
                文件传送连接状态.storbinary('STOR 外部通信.class', io.BytesIO((结果数据/'外部通信.class').read_bytes()))
                文本 = 命令壳('java 外部通信 {} {}'.format(回显服务器条目.TCP端口, 回显服务器条目.UDP端口))
                assert 'EXTERNAL TCP UDP PASS' in 文本 and '10.0.2.2' in 文本 and 'exit 0' in 文本, 文本
                assert 回显服务器条目.拥有已接收 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 回显服务器条目.拥有已接收
                assert not 回显服务器条目.错误列, 回显服务器条目.错误列
            有效性验证报告['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            文件传送连接状态.delete('外部通信.class')
            服务器源代码=结果数据/'服务器测试.java'
            服务器源代码.write_text('''import java.net.*; public class 服务器测试 {
 public static void main(String[] args) throws Exception {
  ServerSocket 服务器值 = new ServerSocket(9300); DatagramSocket 端点 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket 客户机值 = 服务器值.accept();
  客户机值.getOutputStream().write(客户机值.getInputStream().read()+1); 客户机值.close(); 服务器值.close();
  byte[] 内容值 = new byte[8]; DatagramPacket 数据报 = new DatagramPacket(内容值, 内容值.length); 端点.receive(数据报);
  端点.send(数据报); 端点.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(结果数据),str(服务器源代码)])
            文件传送连接状态.storbinary('STOR 服务器测试.class',io.BytesIO((结果数据/'服务器测试.class').read_bytes()))
            进程.stdin.write('java 服务器测试\n'.encode());进程.stdin.flush();接收消息(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',服务器流端口),timeout=5) as 对端值:
                对端值.sendall(b'A');assert 对端值.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as 对端值:
                对端值.settimeout(5);对端值.sendto(b'UDP-IN',('127.0.0.1',服务器数据报端口));assert 对端值.recvfrom(512)[0]==b'UDP-IN'
            文本=接收消息();assert 'INBOUND TCP UDP PASS' in 文本 and 'exit 0' in 文本,文本
            有效性验证报告['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            文件传送连接状态.delete('服务器测试.class')
            指令序列 = 'public class 颜色 { public static void main(String[] 实参) throws Exception { int 总和值 = 0; int 数 = 1; while (数 <= 10) { 总和值 = 总和值 + 数; 数 = 数 + 1; } 中文.内置.输出.写入编号(总和值); 中文.内置.文件.写入("aot.txt", "한글 AOT 文件 😀"); 中文.内置.输出.写入行(中文.内置.文件.读取("aot.txt")); } }'
            文件传送连接状态.storbinary('STOR 颜色.java', io.BytesIO(指令序列.encode()))
            文本 = 命令壳('javac 颜色.java'); assert 'exit 0' in 文本 and 'Compiled:' in 文本, 文本
            文本 = 命令壳('jaot 颜色.class -o 颜色.elf'); assert 'AOT compiled native ARM64 ELF:' in 文本 and 'exit 0' in 文本, 文本
            文本 = 命令壳('run 颜色.elf'); assert '\n55\n' in 文本 and '한글 AOT 文件 😀' in 文本 and 'exit 0' in 文本, 文本
            原生 = bytearray(); 文件传送连接状态.retrbinary('RETR 颜色.elf', 原生.extend)
            文本 = 命令壳('jaot 问候例.jar -o 颜色.elf'); assert 'exit 1' in 文本 and 'unsupported' in 文本, 文本
            已保留数据 = bytearray(); 文件传送连接状态.retrbinary('RETR 颜色.elf', 已保留数据.extend); assert 原生 == 已保留数据
            字节码 = bytearray(); 文件传送连接状态.retrbinary('RETR 颜色.class', 字节码.extend)
            已打包 = io.BytesIO()
            with zipfile.ZipFile(已打包, 'w', zipfile.ZIP_DEFLATED) as Java捆绑:
                Java捆绑.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 颜色\r\n\r\n')
                Java捆绑.writestr('颜色.class', 字节码)
            文件传送连接状态.storbinary('STOR 颜色.jar', io.BytesIO(已打包.getvalue()))
            文本 = 命令壳('jaot 颜色.jar -o 颜色.elf'); assert 'AOT compiled native ARM64 ELF:' in 文本 and 'exit 0' in 文本, 文本
            文本 = 命令壳('run 颜色.elf'); assert '\n55\n' in 文本 and '한글 AOT 文件 😀' in 文本 and 'exit 0' in 文本, 文本
            有效性验证报告['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            有效性验证报告['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            静态源代码=结果数据/'静态测试.java'
            静态源代码.write_text('''public class 静态测试 {
 static int 项目根 = 3;
 static int 总和值(int n) { return n == 0 ? 0 : n + 总和值(n-1); }
 public static void main(String[] 实参) {
  int[] 值 = new int[] {项目根, 总和值(10)};
  System.out.println(值[0] + 值[1]); System.out.println(实参[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(结果数据),str(静态源代码)])
            文件传送连接状态.storbinary('STOR 静态测试.class',io.BytesIO((结果数据/'静态测试.class').read_bytes()))
            文本=命令壳('jaot 静态测试.class -o 静态测试.elf');assert 'exit 0' in 文本,文本
            文本=命令壳('run 静态测试.elf 한글인수');assert '\n58\n한글인수\nexit 0' in 文本,文本
            文件传送连接状态.delete('静态测试.class');文件传送连接状态.delete('静态测试.elf')
            有效性验证报告['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            已损坏=bytearray(存档.getvalue());已损坏[14]^=1
            文件传送连接状态.storbinary('STOR 问候例.jar',io.BytesIO(已损坏))
            文本=命令壳('java -jar 问候例.jar');assert 'Main-Class\nexit 1' in 文本,文本
            有效性验证报告['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            文件传送连接状态.quit(); assert 'FTP stopped' in 命令壳('ftpd stop')
            assert not 桥接.错误, 桥接.错误
            有效性验证报告.update(passed=True, frames_to_guest=桥接.帧列目标侧客户机, frames_from_guest=桥接.帧列起点客户机)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 已按下值,_ in 就绪选择器.select(0):
                片段值=已按下值.fileobj.read(65536)
                if 片段值: 执行记录.extend(片段值)
            桥接.暂停事件.set()
            进程.terminate()
            try: 进程.wait(timeout=5)
            except subprocess.TimeoutExpired: 进程.kill(); 进程.wait()
            就绪选择器.close(); 进程.stdin.close(); 进程.stdout.close()
            有效性验证报告['bridge_error'] = 桥接.错误
            有效性验证报告['frames_to_guest'] = 桥接.帧列目标侧客户机; 有效性验证报告['frames_from_guest'] = 桥接.帧列起点客户机
            (结果数据/'packets.json').write_text(json.dumps(桥接.追踪日志,indent=2)+'\n')
            (结果数据 / 'serial.log').write_bytes(执行记录)
            (结果数据 / 'report.json').write_text(json.dumps(有效性验证报告, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': 运行()
