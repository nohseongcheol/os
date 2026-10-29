#!/usr/bin/env python3
"""QEMU의 実際データ CPU 許可値, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from 命令実行 import 計画根, 命令
from 通信網橋渡し import 通信網橋渡し
from 復唱試験資料 import 復唱試験資料


def 起動処理():
    出力 = 計画根 / 'build/verification/execution-network-review'
    出力.mkdir(parents=True, exist_ok=True)
    報告値 = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((計画根 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    ソースファイル群 = {
        '特権検査': '''public class 特権検査 {
 public static void main(String[] 引数) {
  System.out.println("EL0_PROBE_READY");
  int 数 = 0; while (true) { 数++; }
 }
}''',
        '通信網検査': '''import java.net.*;
public class 通信網検査 {
 public static void main(String[] 引数) throws Exception {
  Socket 接続 = new Socket("10.0.2.2", Integer.parseInt(引数[0]));
  接続.setSoTimeout(3000);
  byte[] 文 = "TCP 한글\\n".getBytes("UTF-8");
  接続.getOutputStream().write(文);
  for (int 位置添字 = 0; 位置添字 < 文.length; 位置添字++)
   if (接続.getInputStream().read() != (文[位置添字] & 255)) throw new RuntimeException("TCP mismatch");
  接続.close();
  DatagramSocket 通信端点 = new DatagramSocket(); 通信端点.setSoTimeout(3000);
  文 = "UDP 한글".getBytes("UTF-8");
  通信端点.send(new DatagramPacket(文, 文.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(引数[1])));
  byte[] 返答 = new byte[64]; DatagramPacket データグラム = new DatagramPacket(返答, 返答.length);
  通信端点.receive(データグラム);
  if (データグラム.getLength() != 文.length) throw new RuntimeException("UDP length");
  for (int 位置添字 = 0; 位置添字 < 文.length; 位置添字++)
   if (返答[位置添字] != 文[位置添字]) throw new RuntimeException("UDP mismatch");
  通信端点.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '受取検査': '''import java.net.*;
public class 受取検査 {
 public static void main(String[] 引数) throws Exception {
  ServerSocket サーバー値 = new ServerSocket(9300); サーバー値.setSoTimeout(5000);
  DatagramSocket 通信端点 = new DatagramSocket(9301); 通信端点.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket 接続 = サーバー値.accept(); 接続.setSoTimeout(5000);
  接続.getOutputStream().write(接続.getInputStream().read() + 1);
  接続.close(); サーバー値.close();
  byte[] データ = new byte[64]; DatagramPacket データグラム = new DatagramPacket(データ, データ.length);
  通信端点.receive(データグラム); 通信端点.send(データグラム); 通信端点.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for 名前, ソース in ソースファイル群.items():
        (出力 / (名前 + '.java')).write_text(ソース, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(出力)] +
                          [str(出力 / (名前 + '.java')) for 名前 in ソースファイル群])
    履歴記録記録 = bytearray()
    def 空ポート番号(型分類=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, 型分類) as 値捜索:
            値捜索.bind(('127.0.0.4', 0))
            return 値捜索.getsockname()[1]
    ファイルポート番号, TCPポート, UDPポート = 空ポート番号(), 空ポート番号(), 空ポート番号(socket.SOCK_DGRAM)
    プロセス値 = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 一時値, 通信網橋渡し(
                ファイルポート番号, ['tcp:{}:9300'.format(TCPポート), 'udp:{}:9301'.format(UDPポート)],
                捕獲=True, ホスト番地='127.0.0.4') as 橋渡し値:
            制御経路 = Path(一時値) / 'qmp.sock'
            プロセス値 = subprocess.Popen(命令() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(制御経路)] + 橋渡し値.転送済み引数(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            項目選択 = selectors.DefaultSelector()
            項目選択.register(プロセス値.stdout, selectors.EVENT_READ)
            def 受取(値表示=b'jkoros-native> ', 初期項目=0, 上限値=60):
                終端 = time.monotonic() + 上限値
                while 値表示 not in 履歴記録記録[初期項目:]:
                    if time.monotonic() > 終端 or プロセス値.poll() is not None:
                        raise AssertionError('Missing ' + repr(値表示) + '\n' + 履歴記録記録[初期項目:].decode('utf-8', 'replace'))
                    for キー値, _ in 項目選択.select(.05):
                        断片値 = キー値.fileobj.read(65536)
                        if 断片値:
                            履歴記録記録.extend(断片値)
                return 履歴記録記録[初期項目:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def 送信(データ):
                プロセス値.stdin.write(データ)
                プロセス値.stdin.flush()
            def シェル(文):
                print(文, flush=True)
                初期項目 = len(履歴記録記録)
                送信((文 + '\n').encode())
                return 受取(初期項目=初期項目)
            受取()
            with socket.socket(socket.AF_UNIX) as 制御値:
                制御値.settimeout(10)
                制御値.connect(str(制御経路))
                ストリーム値 = 制御値.makefile('rwb')
                json.loads(ストリーム値.readline())
                def 要求(命令語値, 引数=None):
                    データ = {'execute': 命令語値}
                    if 引数 is not None:
                        データ['arguments'] = 引数
                    ストリーム値.write((json.dumps(データ) + '\n').encode())
                    ストリーム値.flush()
                    while True:
                        返答 = json.loads(ストリーム値.readline())
                        if 'error' in 返答:
                            raise AssertionError(返答)
                        if 'return' in 返答:
                            return 返答['return']
                要求('qmp_capabilities')
                def 許可読取():
                    要求('stop')
                    try:
                        return 要求('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        要求('cont')
                報告値['shell_cpu'] = 許可読取()
                assert 'EL1h' in 報告値['shell_cpu'], 報告値['shell_cpu']
                報告値['initial_ps'] = シェル('ps')
                assert 'kernel/shell' in 報告値['initial_ps']
                報告値['ipconfig'] = シェル('ipconfig')
                assert 'inet 10.0.2.15' in 報告値['ipconfig']
                報告値['gateway_ping'] = シェル('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in 報告値['gateway_ping']
                assert 'FTP listening' in シェル('ftpd start')
                with ftplib.FTP() as 転送値:
                    転送値.encoding = 'utf-8'
                    転送値.connect('127.0.0.4', ファイルポート番号, timeout=20)
                    転送値.login()
                    for 名前 in ソースファイル群:
                        転送値.storbinary('STOR ' + 名前 + '.class', io.BytesIO((出力 / (名前 + '.class')).read_bytes()))
                初期項目 = len(履歴記録記録)
                送信('java 特権検査\n'.encode())
                受取(b'EL0_PROBE_READY\r\n', 初期項目)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    報告値['java_cpu'] = 許可読取()
                    if 'EL0t' in 報告値['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in 報告値['java_cpu'], 報告値['java_cpu']
                受取(初期項目=初期項目)
                報告値['after_exit_ps'] = シェル('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', 報告値['after_exit_ps'])
                報告値['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 復唱試験資料() as 通信相手値:
                    文 = シェル('java 通信網検査 {} {}'.format(通信相手値.TCPポート, 通信相手値.UDPポート))
                    assert 'OUTBOUND_TCP_UDP_PASS' in 文 and 'exit 0' in 文, 文
                    assert 通信相手値.保有受信済み == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, 通信相手値.保有受信済み
                    assert not 通信相手値.エラー一覧, 通信相手値.エラー一覧
                    報告値['outbound_peers'] = {種別値: データ.decode() for 種別値, データ in 通信相手値.保有受信済み.items()}
                初期項目 = len(履歴記録記録)
                送信('java 受取検査\n'.encode())
                受取(b'INBOUND_READY\r\n', 初期項目)
                with socket.create_connection(('127.0.0.4', TCPポート), timeout=5) as 通信相手値:
                    通信相手値.sendall(b'A')
                    assert 通信相手値.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 通信相手値:
                    通信相手値.settimeout(5)
                    通信相手値.sendto(b'UDP-IN', ('127.0.0.4', UDPポート))
                    assert 通信相手値.recvfrom(64)[0] == b'UDP-IN'
                文 = 受取(初期項目=初期項目)
                assert 'INBOUND_TCP_UDP_PASS' in 文 and 'exit 0' in 文, 文
                報告値['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in シェル('terminal')
                シェル('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                初期項目 = len(履歴記録記録)
                送信('java 窓例\n'.encode())
                受取('GUI 用例 用意: 窓例\r\n'.encode(), 初期項目)
                初期項目 = len(履歴記録記録)
                送信(bytes([30, 2, 1, 0, 0, 0, 0]))
                受取(初期項目=初期項目)
                報告値['suspended_java_ps'] = シェル('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 窓例', 報告値['suspended_java_ps']), 報告値['suspended_java_ps']
                報告値['top'] = シェル('top -n 1')
                assert 'java 窓例' in 報告値['top'] and 'kernel/shell' in 報告値['top']
                報告値['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                報告値['network_trace'] = 橋渡し値.追跡履歴記録
                assert not 橋渡し値.エラー, 橋渡し値.エラー
                送信(b'poweroff\n')
                assert プロセス値.wait(timeout=15) == 0
                報告値['passed'] = True
            項目選択.close()
    except Exception as エラー:
        報告値['error'] = str(エラー)
        raise
    finally:
        if プロセス値 is not None and プロセス値.poll() is None:
            プロセス値.terminate()
            try:
                プロセス値.wait(timeout=10)
            except subprocess.TimeoutExpired:
                プロセス値.kill()
                プロセス値.wait()
        (出力 / 'serial.log').write_bytes(履歴記録記録)
        (出力 / 'report.json').write_text(json.dumps(報告値, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({キー値: 報告値[キー値] for キー値 in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    起動処理()
