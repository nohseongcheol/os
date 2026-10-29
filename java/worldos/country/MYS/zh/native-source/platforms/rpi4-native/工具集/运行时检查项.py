#!/usr/bin/env python3
"""QEMU의 实际数据 CPU 权限值, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
import ftplib
import hashlib
import io
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time

from 执行命令 import 项目根, 命令
from 网络桥接 import 网络桥接
from 回显测试夹具 import 回显测试夹具


def 运行():
    输出 = 项目根 / 'build/verification/execution-network-review'
    输出.mkdir(parents=True, exist_ok=True)
    报告值 = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((项目根 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    源代码文件集 = {
        '特权检查': '''public class 特权检查 {
 public static void main(String[] 实参) {
  System.out.println("EL0_PROBE_READY");
  int 数 = 0; while (true) { 数++; }
 }
}''',
        '网络检查': '''import java.net.*;
public class 网络检查 {
 public static void main(String[] 实参) throws Exception {
  Socket 连接 = new Socket("10.0.2.2", Integer.parseInt(实参[0]));
  连接.setSoTimeout(3000);
  byte[] 文本 = "TCP 한글\\n".getBytes("UTF-8");
  连接.getOutputStream().write(文本);
  for (int 位置索引 = 0; 位置索引 < 文本.length; 位置索引++)
   if (连接.getInputStream().read() != (文本[位置索引] & 255)) throw new RuntimeException("TCP mismatch");
  连接.close();
  DatagramSocket 端点 = new DatagramSocket(); 端点.setSoTimeout(3000);
  文本 = "UDP 한글".getBytes("UTF-8");
  端点.send(new DatagramPacket(文本, 文本.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(实参[1])));
  byte[] 回复 = new byte[64]; DatagramPacket 数据报 = new DatagramPacket(回复, 回复.length);
  端点.receive(数据报);
  if (数据报.getLength() != 文本.length) throw new RuntimeException("UDP length");
  for (int 位置索引 = 0; 位置索引 < 文本.length; 位置索引++)
   if (回复[位置索引] != 文本[位置索引]) throw new RuntimeException("UDP mismatch");
  端点.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '接收检查': '''import java.net.*;
public class 接收检查 {
 public static void main(String[] 实参) throws Exception {
  ServerSocket 服务器值 = new ServerSocket(9300); 服务器值.setSoTimeout(5000);
  DatagramSocket 端点 = new DatagramSocket(9301); 端点.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket 连接 = 服务器值.accept(); 连接.setSoTimeout(5000);
  连接.getOutputStream().write(连接.getInputStream().read() + 1);
  连接.close(); 服务器值.close();
  byte[] 数据 = new byte[64]; DatagramPacket 数据报 = new DatagramPacket(数据, 数据.length);
  端点.receive(数据报); 端点.send(数据报); 端点.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for 名称, 源代码 in 源代码文件集.items():
        (输出 / (名称 + '.java')).write_text(源代码, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(输出)] +
                          [str(输出 / (名称 + '.java')) for 名称 in 源代码文件集])
    日志记录 = bytearray()
    def 空端口编号(类型分类=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, 类型分类) as 搜索值:
            搜索值.bind(('127.0.0.4', 0))
            return 搜索值.getsockname()[1]
    文件端口编号, TCP端口, UDP端口 = 空端口编号(), 空端口编号(), 空端口编号(socket.SOCK_DGRAM)
    进程值 = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 临时值, 网络桥接(
                文件端口编号, ['tcp:{}:9300'.format(TCP端口), 'udp:{}:9301'.format(UDP端口)],
                捕获=True, 宿主地址='127.0.0.4') as 桥接值:
            控制路径 = Path(临时值) / 'qmp.sock'
            进程值 = subprocess.Popen(命令() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(控制路径)] + 桥接值.已转发参数(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            选取条目 = selectors.DefaultSelector()
            选取条目.register(进程值.stdout, selectors.EVENT_READ)
            def 接收(显示值=b'jkoros-native> ', 初始项目=0, 限制值=60):
                结尾 = time.monotonic() + 限制值
                while 显示值 not in 日志记录[初始项目:]:
                    if time.monotonic() > 结尾 or 进程值.poll() is not None:
                        raise AssertionError('Missing ' + repr(显示值) + '\n' + 日志记录[初始项目:].decode('utf-8', 'replace'))
                    for 键值, _ in 选取条目.select(.05):
                        片段值 = 键值.fileobj.read(65536)
                        if 片段值:
                            日志记录.extend(片段值)
                return 日志记录[初始项目:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def 发送(数据):
                进程值.stdin.write(数据)
                进程值.stdin.flush()
            def 命令壳(文本):
                print(文本, flush=True)
                初始项目 = len(日志记录)
                发送((文本 + '\n').encode())
                return 接收(初始项目=初始项目)
            接收()
            with socket.socket(socket.AF_UNIX) as 控制值:
                控制值.settimeout(10)
                控制值.connect(str(控制路径))
                流值 = 控制值.makefile('rwb')
                json.loads(流值.readline())
                def 申请(指令值, 实参=None):
                    数据 = {'execute': 指令值}
                    if 实参 is not None:
                        数据['arguments'] = 实参
                    流值.write((json.dumps(数据) + '\n').encode())
                    流值.flush()
                    while True:
                        回复 = json.loads(流值.readline())
                        if 'error' in 回复:
                            raise AssertionError(回复)
                        if 'return' in 回复:
                            return 回复['return']
                申请('qmp_capabilities')
                def 读取权限():
                    申请('stop')
                    try:
                        return 申请('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        申请('cont')
                报告值['shell_cpu'] = 读取权限()
                assert 'EL1h' in 报告值['shell_cpu'], 报告值['shell_cpu']
                报告值['initial_ps'] = 命令壳('ps')
                assert 'kernel/shell' in 报告值['initial_ps']
                报告值['ipconfig'] = 命令壳('ipconfig')
                assert 'inet 10.0.2.15' in 报告值['ipconfig']
                报告值['gateway_ping'] = 命令壳('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in 报告值['gateway_ping']
                assert 'FTP listening' in 命令壳('ftpd start')
                with ftplib.FTP() as 传送值:
                    传送值.encoding = 'utf-8'
                    传送值.connect('127.0.0.4', 文件端口编号, timeout=20)
                    传送值.login()
                    for 名称 in 源代码文件集:
                        传送值.storbinary('STOR ' + 名称 + '.class', io.BytesIO((输出 / (名称 + '.class')).read_bytes()))
                初始项目 = len(日志记录)
                发送('java 特权检查\n'.encode())
                接收(b'EL0_PROBE_READY\r\n', 初始项目)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    报告值['java_cpu'] = 读取权限()
                    if 'EL0t' in 报告值['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in 报告值['java_cpu'], 报告值['java_cpu']
                接收(初始项目=初始项目)
                报告值['after_exit_ps'] = 命令壳('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', 报告值['after_exit_ps'])
                报告值['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 回显测试夹具() as 对端值:
                    文本 = 命令壳('java 网络检查 {} {}'.format(对端值.TCP端口, 对端值.UDP端口))
                    assert 'OUTBOUND_TCP_UDP_PASS' in 文本 and 'exit 0' in 文本, 文本
                    assert 对端值.拥有已接收 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, 对端值.拥有已接收
                    assert not 对端值.错误列, 对端值.错误列
                    报告值['outbound_peers'] = {种类值: 数据.decode() for 种类值, 数据 in 对端值.拥有已接收.items()}
                初始项目 = len(日志记录)
                发送('java 接收检查\n'.encode())
                接收(b'INBOUND_READY\r\n', 初始项目)
                with socket.create_connection(('127.0.0.4', TCP端口), timeout=5) as 对端值:
                    对端值.sendall(b'A')
                    assert 对端值.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 对端值:
                    对端值.settimeout(5)
                    对端值.sendto(b'UDP-IN', ('127.0.0.4', UDP端口))
                    assert 对端值.recvfrom(64)[0] == b'UDP-IN'
                文本 = 接收(初始项目=初始项目)
                assert 'INBOUND_TCP_UDP_PASS' in 文本 and 'exit 0' in 文本, 文本
                报告值['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in 命令壳('terminal')
                命令壳('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                初始项目 = len(日志记录)
                发送('java 窗口例\n'.encode())
                接收('GUI 用例 准备: 窗口例\r\n'.encode(), 初始项目)
                初始项目 = len(日志记录)
                发送(bytes([30, 2, 1, 0, 0, 0, 0]))
                接收(初始项目=初始项目)
                报告值['suspended_java_ps'] = 命令壳('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 窗口例', 报告值['suspended_java_ps']), 报告值['suspended_java_ps']
                报告值['top'] = 命令壳('top -n 1')
                assert 'java 窗口例' in 报告值['top'] and 'kernel/shell' in 报告值['top']
                报告值['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                报告值['network_trace'] = 桥接值.追踪日志
                assert not 桥接值.错误, 桥接值.错误
                发送(b'poweroff\n')
                assert 进程值.wait(timeout=15) == 0
                报告值['passed'] = True
            选取条目.close()
    except Exception as 错误:
        报告值['error'] = str(错误)
        raise
    finally:
        if 进程值 is not None and 进程值.poll() is None:
            进程值.terminate()
            try:
                进程值.wait(timeout=10)
            except subprocess.TimeoutExpired:
                进程值.kill()
                进程值.wait()
        (输出 / 'serial.log').write_bytes(日志记录)
        (输出 / 'report.json').write_text(json.dumps(报告值, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({键值: 报告值[键值] for 键值 in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    运行()
