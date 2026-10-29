#!/usr/bin/env python3
"""QEMU의 တကယ့်ဒေတာ CPU ခွင့်ပြုချက်တန်ဖိုး, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from စက်မောင်း import စီမံကိန်းအမြစ်, အမိန့်
from ကွန်ရက်တံတား import ကွန်ရက်တံတား
from 되돌림시험서버 import 되돌림시험서버


def လုပ်ဆောင်():
    အထွက် = စီမံကိန်းအမြစ် / 'build/verification/execution-network-review'
    အထွက်.mkdir(parents=True, exist_ok=True)
    အစီရင်ခံစာတန်ဖိုး = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((စီမံကိန်းအမြစ် / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    မူရင်းကုဒ်ဖိုင်များ = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] အချက်များ) {
  System.out.println("EL0_PROBE_READY");
  int ကိန်းတန်ဖိုး = 0; while (true) { ကိန်းတန်ဖိုး++; }
 }
}''',
        'ကွန်ရက်စစ်': '''import java.net.*;
public class ကွန်ရက်စစ် {
 public static void main(String[] အချက်များ) throws Exception {
  Socket ချိတ်ဆက် = new Socket("10.0.2.2", Integer.parseInt(အချက်များ[0]));
  ချိတ်ဆက်.setSoTimeout(3000);
  byte[] စာသား = "TCP 한글\\n".getBytes("UTF-8");
  ချိတ်ဆက်.getOutputStream().write(စာသား);
  for (int နေရာအညွှန်းကိန်း = 0; နေရာအညွှန်းကိန်း < စာသား.length; နေရာအညွှန်းကိန်း++)
   if (ချိတ်ဆက်.getInputStream().read() != (စာသား[နေရာအညွှန်းကိန်း] & 255)) throw new RuntimeException("TCP mismatch");
  ချိတ်ဆက်.close();
  DatagramSocket ဆုံးမှတ် = new DatagramSocket(); ဆုံးမှတ်.setSoTimeout(3000);
  စာသား = "UDP 한글".getBytes("UTF-8");
  ဆုံးမှတ်.send(new DatagramPacket(စာသား, စာသား.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(အချက်များ[1])));
  byte[] အကြောင်းပြန်ချက် = new byte[64]; DatagramPacket ဒေတာစာ = new DatagramPacket(အကြောင်းပြန်ချက်, အကြောင်းပြန်ချက်.length);
  ဆုံးမှတ်.receive(ဒေတာစာ);
  if (ဒေတာစာ.getLength() != စာသား.length) throw new RuntimeException("UDP length");
  for (int နေရာအညွှန်းကိန်း = 0; နေရာအညွှန်းကိန်း < စာသား.length; နေရာအညွှန်းကိန်း++)
   if (အကြောင်းပြန်ချက်[နေရာအညွှန်းကိန်း] != စာသား[နေရာအညွှန်းကိန်း]) throw new RuntimeException("UDP mismatch");
  ဆုံးမှတ်.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'လက်ခံရယူစစ်': '''import java.net.*;
public class လက်ခံရယူစစ် {
 public static void main(String[] အချက်များ) throws Exception {
  ServerSocket ဝန်ဆောင်စက်တန်ဖိုး = new ServerSocket(9300); ဝန်ဆောင်စက်တန်ဖိုး.setSoTimeout(5000);
  DatagramSocket ဆုံးမှတ် = new DatagramSocket(9301); ဆုံးမှတ်.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket ချိတ်ဆက် = ဝန်ဆောင်စက်တန်ဖိုး.accept(); ချိတ်ဆက်.setSoTimeout(5000);
  ချိတ်ဆက်.getOutputStream().write(ချိတ်ဆက်.getInputStream().read() + 1);
  ချိတ်ဆက်.close(); ဝန်ဆောင်စက်တန်ဖိုး.close();
  byte[] ဒေတာ = new byte[64]; DatagramPacket ဒေတာစာ = new DatagramPacket(ဒေတာ, ဒေတာ.length);
  ဆုံးမှတ်.receive(ဒေတာစာ); ဆုံးမှတ်.send(ဒေတာစာ); ဆုံးမှတ်.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for အမည်, မူရင်းကုဒ် in မူရင်းကုဒ်ဖိုင်များ.items():
        (အထွက် / (အမည် + '.java')).write_text(မူရင်းကုဒ်, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(အထွက်)] +
                          [str(အထွက် / (အမည် + '.java')) for အမည် in မူရင်းကုဒ်ဖိုင်များ])
    မှတ်တမ်းမှတ်တမ်းတစ်ခု = bytearray()
    def အလွတ်ဆက်သွယ်ပေါက်ကိန်း(ပုံစံအမျိုးအစား=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, ပုံစံအမျိုးအစား) as တန်ဖိုးရှာဖွေ:
            တန်ဖိုးရှာဖွေ.bind(('127.0.0.4', 0))
            return တန်ဖိုးရှာဖွေ.getsockname()[1]
    ဖိုင်ဆက်သွယ်ပေါက်ကိန်း, TCPဆက်သွယ်ပေါက်, UDPဆက်သွယ်ပေါက် = အလွတ်ဆက်သွယ်ပေါက်ကိန်း(), အလွတ်ဆက်သွယ်ပေါက်ကိန်း(), အလွတ်ဆက်သွယ်ပေါက်ကိန်း(socket.SOCK_DGRAM)
    လုပ်ငန်းစဉ် = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as ယာယီတန်ဖိုး, ကွန်ရက်တံတား(
                ဖိုင်ဆက်သွယ်ပေါက်ကိန်း, ['tcp:{}:9300'.format(TCPဆက်သွယ်ပေါက်), 'udp:{}:9301'.format(UDPဆက်သွယ်ပေါက်)],
                포착여부=True, အိမ်ရှင်လိပ်စာ='127.0.0.4') as တံတားတန်ဖိုး:
            ထိန်းချုပ်လမ်းကြောင်း = Path(ယာယီတန်ဖိုး) / 'qmp.sock'
            လုပ်ငန်းစဉ် = subprocess.Popen(အမိန့်() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(ထိန်းချုပ်လမ်းကြောင်း)] + တံတားတန်ဖိုး.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ရွေးအချက်အလက်တစ်ခု = selectors.DefaultSelector()
            ရွေးအချက်အလက်တစ်ခု.register(လုပ်ငန်းစဉ်.stdout, selectors.EVENT_READ)
            def လက်ခံ(တန်ဖိုးပြသ=b'jkoros-native> ', အစဦးအချက်အလက်တစ်ခု=0, ကန့်သတ်ချက်တန်ဖိုး=60):
                အဆုံး = time.monotonic() + ကန့်သတ်ချက်တန်ဖိုး
                while တန်ဖိုးပြသ not in မှတ်တမ်းမှတ်တမ်းတစ်ခု[အစဦးအချက်အလက်တစ်ခု:]:
                    if time.monotonic() > အဆုံး or လုပ်ငန်းစဉ်.poll() is not None:
                        raise AssertionError('Missing ' + repr(တန်ဖိုးပြသ) + '\n' + မှတ်တမ်းမှတ်တမ်းတစ်ခု[အစဦးအချက်အလက်တစ်ခု:].decode('utf-8', 'replace'))
                    for သော့တန်ဖိုး, _ in ရွေးအချက်အလက်တစ်ခု.select(.05):
                        အစိတ်အပိုင်း = သော့တန်ဖိုး.fileobj.read(65536)
                        if အစိတ်အပိုင်း:
                            မှတ်တမ်းမှတ်တမ်းတစ်ခု.extend(အစိတ်အပိုင်း)
                return မှတ်တမ်းမှတ်တမ်းတစ်ခု[အစဦးအချက်အလက်တစ်ခု:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ပို့(ဒေတာ):
                လုပ်ငန်းစဉ်.stdin.write(ဒေတာ)
                လုပ်ငန်းစဉ်.stdin.flush()
            def အမိန့်ဝင်း(စာသား):
                print(စာသား, flush=True)
                အစဦးအချက်အလက်တစ်ခု = len(မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                ပို့((စာသား + '\n').encode())
                return လက်ခံ(အစဦးအချက်အလက်တစ်ခု=အစဦးအချက်အလက်တစ်ခု)
            လက်ခံ()
            with socket.socket(socket.AF_UNIX) as ထိန်းချုပ်တန်ဖိုး:
                ထိန်းချုပ်တန်ဖိုး.settimeout(10)
                ထိန်းချုပ်တန်ဖိုး.connect(str(ထိန်းချုပ်လမ်းကြောင်း))
                စီးကြောင်းတန်ဖိုး = ထိန်းချုပ်တန်ဖိုး.makefile('rwb')
                json.loads(စီးကြောင်းတန်ဖိုး.readline())
                def တောင်းဆိုချက်(စက်ညွှန်ကြားချက်တန်ဖိုး, အချက်များ=None):
                    ဒေတာ = {'execute': စက်ညွှန်ကြားချက်တန်ဖိုး}
                    if အချက်များ is not None:
                        ဒေတာ['arguments'] = အချက်များ
                    စီးကြောင်းတန်ဖိုး.write((json.dumps(ဒေတာ) + '\n').encode())
                    စီးကြောင်းတန်ဖိုး.flush()
                    while True:
                        အကြောင်းပြန်ချက် = json.loads(စီးကြောင်းတန်ဖိုး.readline())
                        if 'error' in အကြောင်းပြန်ချက်:
                            raise AssertionError(အကြောင်းပြန်ချက်)
                        if 'return' in အကြောင်းပြန်ချက်:
                            return အကြောင်းပြန်ချက်['return']
                တောင်းဆိုချက်('qmp_capabilities')
                def ခွင့်ပြုချက်ဖတ်():
                    တောင်းဆိုချက်('stop')
                    try:
                        return တောင်းဆိုချက်('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        တောင်းဆိုချက်('cont')
                အစီရင်ခံစာတန်ဖိုး['shell_cpu'] = ခွင့်ပြုချက်ဖတ်()
                assert 'EL1h' in အစီရင်ခံစာတန်ဖိုး['shell_cpu'], အစီရင်ခံစာတန်ဖိုး['shell_cpu']
                အစီရင်ခံစာတန်ဖိုး['initial_ps'] = အမိန့်ဝင်း('ps')
                assert 'kernel/shell' in အစီရင်ခံစာတန်ဖိုး['initial_ps']
                အစီရင်ခံစာတန်ဖိုး['ipconfig'] = အမိန့်ဝင်း('ipconfig')
                assert 'inet 10.0.2.15' in အစီရင်ခံစာတန်ဖိုး['ipconfig']
                အစီရင်ခံစာတန်ဖိုး['gateway_ping'] = အမိန့်ဝင်း('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in အစီရင်ခံစာတန်ဖိုး['gateway_ping']
                assert 'FTP listening' in အမိန့်ဝင်း('ftpd start')
                with ftplib.FTP() as လွှဲပြောင်းတန်ဖိုး:
                    လွှဲပြောင်းတန်ဖိုး.encoding = 'utf-8'
                    လွှဲပြောင်းတန်ဖိုး.connect('127.0.0.4', ဖိုင်ဆက်သွယ်ပေါက်ကိန်း, timeout=20)
                    လွှဲပြောင်းတန်ဖိုး.login()
                    for အမည် in မူရင်းကုဒ်ဖိုင်များ:
                        လွှဲပြောင်းတန်ဖိုး.storbinary('STOR ' + အမည် + '.class', io.BytesIO((အထွက် / (အမည် + '.class')).read_bytes()))
                အစဦးအချက်အလက်တစ်ခု = len(မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                ပို့('java 권한점검\n'.encode())
                လက်ခံ(b'EL0_PROBE_READY\r\n', အစဦးအချက်အလက်တစ်ခု)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    အစီရင်ခံစာတန်ဖိုး['java_cpu'] = ခွင့်ပြုချက်ဖတ်()
                    if 'EL0t' in အစီရင်ခံစာတန်ဖိုး['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in အစီရင်ခံစာတန်ဖိုး['java_cpu'], အစီရင်ခံစာတန်ဖိုး['java_cpu']
                လက်ခံ(အစဦးအချက်အလက်တစ်ခု=အစဦးအချက်အလက်တစ်ခု)
                အစီရင်ခံစာတန်ဖိုး['after_exit_ps'] = အမိန့်ဝင်း('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', အစီရင်ခံစာတန်ဖိုး['after_exit_ps'])
                အစီရင်ခံစာတန်ဖိုး['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as တစ်ဖက်တန်ဖိုး:
                    စာသား = အမိန့်ဝင်း('java ကွန်ရက်စစ် {} {}'.format(တစ်ဖက်တန်ဖိုး.TCPဆက်သွယ်ပေါက်, တစ်ဖက်တန်ဖိုး.UDPဆက်သွယ်ပေါက်))
                    assert 'OUTBOUND_TCP_UDP_PASS' in စာသား and 'exit 0' in စာသား, စာသား
                    assert တစ်ဖက်တန်ဖိုး.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, တစ်ဖက်တန်ဖိုး.수신됨
                    assert not တစ်ဖက်တန်ဖိုး.အမှားများ, တစ်ဖက်တန်ဖိုး.အမှားများ
                    အစီရင်ခံစာတန်ဖိုး['outbound_peers'] = {အမျိုးအစားတန်ဖိုး: ဒေတာ.decode() for အမျိုးအစားတန်ဖိုး, ဒေတာ in တစ်ဖက်တန်ဖိုး.수신됨.items()}
                အစဦးအချက်အလက်တစ်ခု = len(မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                ပို့('java လက်ခံရယူစစ်\n'.encode())
                လက်ခံ(b'INBOUND_READY\r\n', အစဦးအချက်အလက်တစ်ခု)
                with socket.create_connection(('127.0.0.4', TCPဆက်သွယ်ပေါက်), timeout=5) as တစ်ဖက်တန်ဖိုး:
                    တစ်ဖက်တန်ဖိုး.sendall(b'A')
                    assert တစ်ဖက်တန်ဖိုး.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as တစ်ဖက်တန်ဖိုး:
                    တစ်ဖက်တန်ဖိုး.settimeout(5)
                    တစ်ဖက်တန်ဖိုး.sendto(b'UDP-IN', ('127.0.0.4', UDPဆက်သွယ်ပေါက်))
                    assert တစ်ဖက်တန်ဖိုး.recvfrom(64)[0] == b'UDP-IN'
                စာသား = လက်ခံ(အစဦးအချက်အလက်တစ်ခု=အစဦးအချက်အလက်တစ်ခု)
                assert 'INBOUND_TCP_UDP_PASS' in စာသား and 'exit 0' in စာသား, စာသား
                အစီရင်ခံစာတန်ဖိုး['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in အမိန့်ဝင်း('terminal')
                အမိန့်ဝင်း('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                အစဦးအချက်အလက်တစ်ခု = len(မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                ပို့('java ဝင်းဥပမာ\n'.encode())
                လက်ခံ('GUI ဥပမာ ပြင်ဆင်: ဝင်းဥပမာ\r\n'.encode(), အစဦးအချက်အလက်တစ်ခု)
                အစဦးအချက်အလက်တစ်ခု = len(မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                ပို့(bytes([30, 2, 1, 0, 0, 0, 0]))
                လက်ခံ(အစဦးအချက်အလက်တစ်ခု=အစဦးအချက်အလက်တစ်ခု)
                အစီရင်ခံစာတန်ဖိုး['suspended_java_ps'] = အမိန့်ဝင်း('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java ဝင်းဥပမာ', အစီရင်ခံစာတန်ဖိုး['suspended_java_ps']), အစီရင်ခံစာတန်ဖိုး['suspended_java_ps']
                အစီရင်ခံစာတန်ဖိုး['top'] = အမိန့်ဝင်း('top -n 1')
                assert 'java ဝင်းဥပမာ' in အစီရင်ခံစာတန်ဖိုး['top'] and 'kernel/shell' in အစီရင်ခံစာတန်ဖိုး['top']
                အစီရင်ခံစာတန်ဖိုး['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                အစီရင်ခံစာတန်ဖိုး['network_trace'] = တံတားတန်ဖိုး.ခြေရာမှတ်တမ်း
                assert not တံတားတန်ဖိုး.အမှား, တံတားတန်ဖိုး.အမှား
                ပို့(b'poweroff\n')
                assert လုပ်ငန်းစဉ်.wait(timeout=15) == 0
                အစီရင်ခံစာတန်ဖိုး['passed'] = True
            ရွေးအချက်အလက်တစ်ခု.close()
    except Exception as အမှား:
        အစီရင်ခံစာတန်ဖိုး['error'] = str(အမှား)
        raise
    finally:
        if လုပ်ငန်းစဉ် is not None and လုပ်ငန်းစဉ်.poll() is None:
            လုပ်ငန်းစဉ်.terminate()
            try:
                လုပ်ငန်းစဉ်.wait(timeout=10)
            except subprocess.TimeoutExpired:
                လုပ်ငန်းစဉ်.kill()
                လုပ်ငန်းစဉ်.wait()
        (အထွက် / 'serial.log').write_bytes(မှတ်တမ်းမှတ်တမ်းတစ်ခု)
        (အထွက် / 'report.json').write_text(json.dumps(အစီရင်ခံစာတန်ဖိုး, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({သော့တန်ဖိုး: အစီရင်ခံစာတန်ဖိုး[သော့တန်ဖိုး] for သော့တန်ဖိုး in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    လုပ်ဆောင်()
