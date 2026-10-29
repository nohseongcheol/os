#!/usr/bin/env python3
"""QEMU의 בפועל_נתונים CPU הרשאה_ערך, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from לבצע_פקודה import לשקף_בסיס, פקודה
from גשר_3de4fe3a import גשר_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def הפעלה():
    פלטטקסט = לשקף_בסיס / 'build/verification/execution-network-review'
    פלטטקסט.mkdir(parents=True, exist_ok=True)
    דוח_ערך_ddf2aaf3 = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((לשקף_בסיס / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    מקור_קבצים = {
        'הרשאה_שיק': '''public class הרשאה_שיק {
 public static void main(String[] ארגומנטים) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'רשת_שיק': '''import java.net.*;
public class רשת_שיק {
 public static void main(String[] ארגומנטים) throws Exception {
  Socket חיבור = new Socket("10.0.2.2", Integer.parseInt(ארגומנטים[0]));
  חיבור.setSoTimeout(3000);
  byte[] טקסט = "TCP 한글\\n".getBytes("UTF-8");
  חיבור.getOutputStream().write(טקסט);
  for (int עמדה_מדד = 0; עמדה_מדד < טקסט.length; עמדה_מדד++)
   if (חיבור.getInputStream().read() != (טקסט[עמדה_מדד] & 255)) throw new RuntimeException("TCP mismatch");
  חיבור.close();
  DatagramSocket משתתף = new DatagramSocket(); משתתף.setSoTimeout(3000);
  טקסט = "UDP 한글".getBytes("UTF-8");
  משתתף.send(new DatagramPacket(טקסט, טקסט.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(ארגומנטים[1])));
  byte[] מענה = new byte[64]; DatagramPacket יחידת_נתונים = new DatagramPacket(מענה, מענה.length);
  משתתף.receive(יחידת_נתונים);
  if (יחידת_נתונים.getLength() != טקסט.length) throw new RuntimeException("UDP length");
  for (int עמדה_מדד = 0; עמדה_מדד < טקסט.length; עמדה_מדד++)
   if (מענה[עמדה_מדד] != טקסט[עמדה_מדד]) throw new RuntimeException("UDP mismatch");
  משתתף.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'לקבל_שיק': '''import java.net.*;
public class לקבל_שיק {
 public static void main(String[] ארגומנטים) throws Exception {
  ServerSocket שרת_ערך = new ServerSocket(9300); שרת_ערך.setSoTimeout(5000);
  DatagramSocket משתתף = new DatagramSocket(9301); משתתף.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket חיבור = שרת_ערך.accept(); חיבור.setSoTimeout(5000);
  חיבור.getOutputStream().write(חיבור.getInputStream().read() + 1);
  חיבור.close(); שרת_ערך.close();
  byte[] נתונים = new byte[64]; DatagramPacket יחידת_נתונים = new DatagramPacket(נתונים, נתונים.length);
  משתתף.receive(יחידת_נתונים); משתתף.send(יחידת_נתונים); משתתף.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for שם, קודמקור in מקור_קבצים.items():
        (פלטטקסט / (שם + '.java')).write_text(קודמקור, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(פלטטקסט)] +
                          [str(פלטטקסט / (שם + '.java')) for שם in מקור_קבצים])
    לרשום_שיא = bytearray()
    def ריק_מספר_יציאה(כתב_אזור=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, כתב_אזור) as חפש_ערך:
            חפש_ערך.bind(('127.0.0.4', 0))
            return חפש_ערך.getsockname()[1]
    파일접속번호, יציאת_TCP, פרוטוקול_יחידת_נתונים_של_משתמש_הסב = ריק_מספר_יציאה(), ריק_מספר_יציאה(), ריק_מספר_יציאה(socket.SOCK_DGRAM)
    תהליך_ערך = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, גשר_3de4fe3a(
                파일접속번호, ['tcp:{}:9300'.format(יציאת_TCP), 'udp:{}:9301'.format(פרוטוקול_יחידת_נתונים_של_משתמש_הסב)],
                לכוד=True, ארח_למען='127.0.0.4') as גשר_ערך:
            פקד_נתיב = Path(임시) / 'qmp.sock'
            תהליך_ערך = subprocess.Popen(פקודה() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(פקד_נתיב)] + גשר_ערך.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            בחר_פריט = selectors.DefaultSelector()
            בחר_פריט.register(תהליך_ערך.stdout, selectors.EVENT_READ)
            def לקבל(הופעה_ערך=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while הופעה_ערך not in לרשום_שיא[처음:]:
                    if time.monotonic() > 끝 or תהליך_ערך.poll() is not None:
                        raise AssertionError('Missing ' + repr(הופעה_ערך) + '\n' + לרשום_שיא[처음:].decode('utf-8', 'replace'))
                    for מקש_ערך, _ in בחר_פריט.select(.05):
                        조각 = מקש_ערך.fileobj.read(65536)
                        if 조각:
                            לרשום_שיא.extend(조각)
                return לרשום_שיא[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def שלח(נתונים):
                תהליך_ערך.stdin.write(נתונים)
                תהליך_ערך.stdin.flush()
            def מעטפת(טקסט):
                print(טקסט, flush=True)
                처음 = len(לרשום_שיא)
                שלח((טקסט + '\n').encode())
                return לקבל(처음=처음)
            לקבל()
            with socket.socket(socket.AF_UNIX) as פקד_ערך:
                פקד_ערך.settimeout(10)
                פקד_ערך.connect(str(פקד_נתיב))
                זרם_ערך = פקד_ערך.makefile('rwb')
                json.loads(זרם_ערך.readline())
                def בקשה(הוראה_ערך, ארגומנטים=None):
                    נתונים = {'execute': הוראה_ערך}
                    if ארגומנטים is not None:
                        נתונים['arguments'] = ארגומנטים
                    זרם_ערך.write((json.dumps(נתונים) + '\n').encode())
                    זרם_ערך.flush()
                    while True:
                        מענה = json.loads(זרם_ערך.readline())
                        if 'error' in מענה:
                            raise AssertionError(מענה)
                        if 'return' in מענה:
                            return מענה['return']
                בקשה('qmp_capabilities')
                def הרשאת_קריאה():
                    בקשה('stop')
                    try:
                        return בקשה('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        בקשה('cont')
                דוח_ערך_ddf2aaf3['shell_cpu'] = הרשאת_קריאה()
                assert 'EL1h' in דוח_ערך_ddf2aaf3['shell_cpu'], דוח_ערך_ddf2aaf3['shell_cpu']
                דוח_ערך_ddf2aaf3['initial_ps'] = מעטפת('ps')
                assert 'kernel/shell' in דוח_ערך_ddf2aaf3['initial_ps']
                דוח_ערך_ddf2aaf3['ipconfig'] = מעטפת('ipconfig')
                assert 'inet 10.0.2.15' in דוח_ערך_ddf2aaf3['ipconfig']
                דוח_ערך_ddf2aaf3['gateway_ping'] = מעטפת('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in דוח_ערך_ddf2aaf3['gateway_ping']
                assert 'FTP listening' in מעטפת('ftpd start')
                with ftplib.FTP() as העבר_ערך:
                    העבר_ערך.encoding = 'utf-8'
                    העבר_ערך.connect('127.0.0.4', 파일접속번호, timeout=20)
                    העבר_ערך.login()
                    for שם in מקור_קבצים:
                        העבר_ערך.storbinary('STOR ' + שם + '.class', io.BytesIO((פלטטקסט / (שם + '.class')).read_bytes()))
                처음 = len(לרשום_שיא)
                שלח('java הרשאה_שיק\n'.encode())
                לקבל(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    דוח_ערך_ddf2aaf3['java_cpu'] = הרשאת_קריאה()
                    if 'EL0t' in דוח_ערך_ddf2aaf3['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in דוח_ערך_ddf2aaf3['java_cpu'], דוח_ערך_ddf2aaf3['java_cpu']
                לקבל(처음=처음)
                דוח_ערך_ddf2aaf3['after_exit_ps'] = מעטפת('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', דוח_ערך_ddf2aaf3['after_exit_ps'])
                דוח_ערך_ddf2aaf3['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as עמית_ערך:
                    טקסט = מעטפת('java רשת_שיק {} {}'.format(עמית_ערך.יציאת_TCP, עמית_ערך.פרוטוקול_יחידת_נתונים_של_משתמש_הסב))
                    assert 'OUTBOUND_TCP_UDP_PASS' in טקסט and 'exit 0' in טקסט, טקסט
                    assert עמית_ערך.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, עמית_ערך.수신됨
                    assert not עמית_ערך.오류들, עמית_ערך.오류들
                    דוח_ערך_ddf2aaf3['outbound_peers'] = {종류: נתונים.decode() for 종류, נתונים in עמית_ערך.수신됨.items()}
                처음 = len(לרשום_שיא)
                שלח('java לקבל_שיק\n'.encode())
                לקבל(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', יציאת_TCP), timeout=5) as עמית_ערך:
                    עמית_ערך.sendall(b'A')
                    assert עמית_ערך.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as עמית_ערך:
                    עמית_ערך.settimeout(5)
                    עמית_ערך.sendto(b'UDP-IN', ('127.0.0.4', פרוטוקול_יחידת_נתונים_של_משתמש_הסב))
                    assert עמית_ערך.recvfrom(64)[0] == b'UDP-IN'
                טקסט = לקבל(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in טקסט and 'exit 0' in טקסט, טקסט
                דוח_ערך_ddf2aaf3['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in מעטפת('terminal')
                מעטפת('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(לרשום_שיא)
                שלח('java דוגמתחלון\n'.encode())
                לקבל('GUI 예제 להכין: דוגמתחלון\r\n'.encode(), 처음)
                처음 = len(לרשום_שיא)
                שלח(bytes([30, 2, 1, 0, 0, 0, 0]))
                לקבל(처음=처음)
                דוח_ערך_ddf2aaf3['suspended_java_ps'] = מעטפת('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java דוגמתחלון', דוח_ערך_ddf2aaf3['suspended_java_ps']), דוח_ערך_ddf2aaf3['suspended_java_ps']
                דוח_ערך_ddf2aaf3['top'] = מעטפת('top -n 1')
                assert 'java דוגמתחלון' in דוח_ערך_ddf2aaf3['top'] and 'kernel/shell' in דוח_ערך_ddf2aaf3['top']
                דוח_ערך_ddf2aaf3['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                דוח_ערך_ddf2aaf3['network_trace'] = גשר_ערך.יומן_מעקב
                assert not גשר_ערך.שגיאה, גשר_ערך.שגיאה
                שלח(b'poweroff\n')
                assert תהליך_ערך.wait(timeout=15) == 0
                דוח_ערך_ddf2aaf3['passed'] = True
            בחר_פריט.close()
    except Exception as שגיאה:
        דוח_ערך_ddf2aaf3['error'] = str(שגיאה)
        raise
    finally:
        if תהליך_ערך is not None and תהליך_ערך.poll() is None:
            תהליך_ערך.terminate()
            try:
                תהליך_ערך.wait(timeout=10)
            except subprocess.TimeoutExpired:
                תהליך_ערך.kill()
                תהליך_ערך.wait()
        (פלטטקסט / 'serial.log').write_bytes(לרשום_שיא)
        (פלטטקסט / 'report.json').write_text(json.dumps(דוח_ערך_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({מקש_ערך: דוח_ערך_ddf2aaf3[מקש_ערך] for מקש_ערך in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    הפעלה()
