#!/usr/bin/env python3
"""QEMU의 實際資料 CPU 權限值, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from 執行命令 import 項目根, 命令
from 網路橋接 import 網路橋接
from 回顯測試夾具 import 回顯測試夾具


def 運行():
    輸出 = 項目根 / 'build/verification/execution-network-review'
    輸出.mkdir(parents=True, exist_ok=True)
    報告值 = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((項目根 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    原始碼檔案集 = {
        '特權檢查': '''public class 特權檢查 {
 public static void main(String[] 實參) {
  System.out.println("EL0_PROBE_READY");
  int 數 = 0; while (true) { 數++; }
 }
}''',
        '網路檢查': '''import java.net.*;
public class 網路檢查 {
 public static void main(String[] 實參) throws Exception {
  Socket 連接 = new Socket("10.0.2.2", Integer.parseInt(實參[0]));
  連接.setSoTimeout(3000);
  byte[] 文本 = "TCP 한글\\n".getBytes("UTF-8");
  連接.getOutputStream().write(文本);
  for (int 位置索引 = 0; 位置索引 < 文本.length; 位置索引++)
   if (連接.getInputStream().read() != (文本[位置索引] & 255)) throw new RuntimeException("TCP mismatch");
  連接.close();
  DatagramSocket 端點 = new DatagramSocket(); 端點.setSoTimeout(3000);
  文本 = "UDP 한글".getBytes("UTF-8");
  端點.send(new DatagramPacket(文本, 文本.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(實參[1])));
  byte[] 回覆 = new byte[64]; DatagramPacket 數據報 = new DatagramPacket(回覆, 回覆.length);
  端點.receive(數據報);
  if (數據報.getLength() != 文本.length) throw new RuntimeException("UDP length");
  for (int 位置索引 = 0; 位置索引 < 文本.length; 位置索引++)
   if (回覆[位置索引] != 文本[位置索引]) throw new RuntimeException("UDP mismatch");
  端點.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '接收檢查': '''import java.net.*;
public class 接收檢查 {
 public static void main(String[] 實參) throws Exception {
  ServerSocket 服務器值 = new ServerSocket(9300); 服務器值.setSoTimeout(5000);
  DatagramSocket 端點 = new DatagramSocket(9301); 端點.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket 連接 = 服務器值.accept(); 連接.setSoTimeout(5000);
  連接.getOutputStream().write(連接.getInputStream().read() + 1);
  連接.close(); 服務器值.close();
  byte[] 資料 = new byte[64]; DatagramPacket 數據報 = new DatagramPacket(資料, 資料.length);
  端點.receive(數據報); 端點.send(數據報); 端點.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for 名稱, 原始碼 in 原始碼檔案集.items():
        (輸出 / (名稱 + '.java')).write_text(原始碼, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(輸出)] +
                          [str(輸出 / (名稱 + '.java')) for 名稱 in 原始碼檔案集])
    日誌記錄 = bytearray()
    def 空埠編號(類型分類=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, 類型分類) as 搜索值:
            搜索值.bind(('127.0.0.4', 0))
            return 搜索值.getsockname()[1]
    檔案埠編號, TCP埠, UDP埠 = 空埠編號(), 空埠編號(), 空埠編號(socket.SOCK_DGRAM)
    程序值 = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 臨時值, 網路橋接(
                檔案埠編號, ['tcp:{}:9300'.format(TCP埠), 'udp:{}:9301'.format(UDP埠)],
                捕獲=True, 宿主地址='127.0.0.4') as 橋接值:
            控制路徑 = Path(臨時值) / 'qmp.sock'
            程序值 = subprocess.Popen(命令() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(控制路徑)] + 橋接值.已轉發實際參數(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            選取條目 = selectors.DefaultSelector()
            選取條目.register(程序值.stdout, selectors.EVENT_READ)
            def 接收(顯示值=b'jkoros-native> ', 初始項目=0, 限制值=60):
                結尾 = time.monotonic() + 限制值
                while 顯示值 not in 日誌記錄[初始項目:]:
                    if time.monotonic() > 結尾 or 程序值.poll() is not None:
                        raise AssertionError('Missing ' + repr(顯示值) + '\n' + 日誌記錄[初始項目:].decode('utf-8', 'replace'))
                    for 鍵值, _ in 選取條目.select(.05):
                        片段值 = 鍵值.fileobj.read(65536)
                        if 片段值:
                            日誌記錄.extend(片段值)
                return 日誌記錄[初始項目:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def 發送(資料):
                程序值.stdin.write(資料)
                程序值.stdin.flush()
            def 命令殼(文本):
                print(文本, flush=True)
                初始項目 = len(日誌記錄)
                發送((文本 + '\n').encode())
                return 接收(初始項目=初始項目)
            接收()
            with socket.socket(socket.AF_UNIX) as 控制值:
                控制值.settimeout(10)
                控制值.connect(str(控制路徑))
                流值 = 控制值.makefile('rwb')
                json.loads(流值.readline())
                def 申請(指令值, 實參=None):
                    資料 = {'execute': 指令值}
                    if 實參 is not None:
                        資料['arguments'] = 實參
                    流值.write((json.dumps(資料) + '\n').encode())
                    流值.flush()
                    while True:
                        回覆 = json.loads(流值.readline())
                        if 'error' in 回覆:
                            raise AssertionError(回覆)
                        if 'return' in 回覆:
                            return 回覆['return']
                申請('qmp_capabilities')
                def 讀取權限():
                    申請('stop')
                    try:
                        return 申請('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        申請('cont')
                報告值['shell_cpu'] = 讀取權限()
                assert 'EL1h' in 報告值['shell_cpu'], 報告值['shell_cpu']
                報告值['initial_ps'] = 命令殼('ps')
                assert 'kernel/shell' in 報告值['initial_ps']
                報告值['ipconfig'] = 命令殼('ipconfig')
                assert 'inet 10.0.2.15' in 報告值['ipconfig']
                報告值['gateway_ping'] = 命令殼('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in 報告值['gateway_ping']
                assert 'FTP listening' in 命令殼('ftpd start')
                with ftplib.FTP() as 傳送值:
                    傳送值.encoding = 'utf-8'
                    傳送值.connect('127.0.0.4', 檔案埠編號, timeout=20)
                    傳送值.login()
                    for 名稱 in 原始碼檔案集:
                        傳送值.storbinary('STOR ' + 名稱 + '.class', io.BytesIO((輸出 / (名稱 + '.class')).read_bytes()))
                初始項目 = len(日誌記錄)
                發送('java 特權檢查\n'.encode())
                接收(b'EL0_PROBE_READY\r\n', 初始項目)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    報告值['java_cpu'] = 讀取權限()
                    if 'EL0t' in 報告值['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in 報告值['java_cpu'], 報告值['java_cpu']
                接收(初始項目=初始項目)
                報告值['after_exit_ps'] = 命令殼('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', 報告值['after_exit_ps'])
                報告值['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 回顯測試夾具() as 對端值:
                    文本 = 命令殼('java 網路檢查 {} {}'.format(對端值.TCP埠, 對端值.UDP埠))
                    assert 'OUTBOUND_TCP_UDP_PASS' in 文本 and 'exit 0' in 文本, 文本
                    assert 對端值.擁有已接收 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, 對端值.擁有已接收
                    assert not 對端值.錯誤列, 對端值.錯誤列
                    報告值['outbound_peers'] = {種類值: 資料.decode() for 種類值, 資料 in 對端值.擁有已接收.items()}
                初始項目 = len(日誌記錄)
                發送('java 接收檢查\n'.encode())
                接收(b'INBOUND_READY\r\n', 初始項目)
                with socket.create_connection(('127.0.0.4', TCP埠), timeout=5) as 對端值:
                    對端值.sendall(b'A')
                    assert 對端值.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 對端值:
                    對端值.settimeout(5)
                    對端值.sendto(b'UDP-IN', ('127.0.0.4', UDP埠))
                    assert 對端值.recvfrom(64)[0] == b'UDP-IN'
                文本 = 接收(初始項目=初始項目)
                assert 'INBOUND_TCP_UDP_PASS' in 文本 and 'exit 0' in 文本, 文本
                報告值['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in 命令殼('terminal')
                命令殼('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                初始項目 = len(日誌記錄)
                發送('java 窗口例\n'.encode())
                接收('GUI 範例 準備: 窗口例\r\n'.encode(), 初始項目)
                初始項目 = len(日誌記錄)
                發送(bytes([30, 2, 1, 0, 0, 0, 0]))
                接收(初始項目=初始項目)
                報告值['suspended_java_ps'] = 命令殼('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 窗口例', 報告值['suspended_java_ps']), 報告值['suspended_java_ps']
                報告值['top'] = 命令殼('top -n 1')
                assert 'java 窗口例' in 報告值['top'] and 'kernel/shell' in 報告值['top']
                報告值['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                報告值['network_trace'] = 橋接值.追蹤日誌
                assert not 橋接值.錯誤, 橋接值.錯誤
                發送(b'poweroff\n')
                assert 程序值.wait(timeout=15) == 0
                報告值['passed'] = True
            選取條目.close()
    except Exception as 錯誤:
        報告值['error'] = str(錯誤)
        raise
    finally:
        if 程序值 is not None and 程序值.poll() is None:
            程序值.terminate()
            try:
                程序值.wait(timeout=10)
            except subprocess.TimeoutExpired:
                程序值.kill()
                程序值.wait()
        (輸出 / 'serial.log').write_bytes(日誌記錄)
        (輸出 / 'report.json').write_text(json.dumps(報告值, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({鍵值: 報告值[鍵值] for 鍵值 in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    運行()
