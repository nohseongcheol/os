#!/usr/bin/env python3
"""QEMU의 ትክክለኛ_ውሂብ CPU ፈቃድ_እሴት, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from ፈጽም_ትእዛዝ import አሳይ_ስር, ትእዛዝ
from መረብ_ድልድይ import መረብ_ድልድይ
from 되돌림시험서버 import 되돌림시험서버


def ማስኬጃ():
    ውጤት = አሳይ_ስር / 'build/verification/execution-network-review'
    ውጤት.mkdir(parents=True, exist_ok=True)
    ዘገባ_እሴት = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((አሳይ_ስር / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    ምንጭ_ፋይሎች = {
        'ፈቃድ_ቼክ': '''public class ፈቃድ_ቼክ {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'መረብ_ቼክ': '''import java.net.*;
public class መረብ_ቼክ {
 public static void main(String[] 인수) throws Exception {
  Socket መገናኛ = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  መገናኛ.setSoTimeout(3000);
  byte[] ጽሁፍ = "TCP 한글\\n".getBytes("UTF-8");
  መገናኛ.getOutputStream().write(ጽሁፍ);
  for (int በቦታ_አስቀመጠ_መረጃ_ጠቆመ = 0; በቦታ_አስቀመጠ_መረጃ_ጠቆመ < ጽሁፍ.length; በቦታ_አስቀመጠ_መረጃ_ጠቆመ++)
   if (መገናኛ.getInputStream().read() != (ጽሁፍ[በቦታ_አስቀመጠ_መረጃ_ጠቆመ] & 255)) throw new RuntimeException("TCP mismatch");
  መገናኛ.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  ጽሁፍ = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(ጽሁፍ, ጽሁፍ.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] መልስ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(መልስ, መልስ.length);
  종단.receive(전문);
  if (전문.getLength() != ጽሁፍ.length) throw new RuntimeException("UDP length");
  for (int በቦታ_አስቀመጠ_መረጃ_ጠቆመ = 0; በቦታ_አስቀመጠ_መረጃ_ጠቆመ < ጽሁፍ.length; በቦታ_አስቀመጠ_መረጃ_ጠቆመ++)
   if (መልስ[በቦታ_አስቀመጠ_መረጃ_ጠቆመ] != ጽሁፍ[በቦታ_አስቀመጠ_መረጃ_ጠቆመ]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket አገልጋይ_እሴት = new ServerSocket(9300); አገልጋይ_እሴት.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket መገናኛ = አገልጋይ_እሴት.accept(); መገናኛ.setSoTimeout(5000);
  መገናኛ.getOutputStream().write(መገናኛ.getInputStream().read() + 1);
  መገናኛ.close(); አገልጋይ_እሴት.close();
  byte[] ውሂብ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ውሂብ, ውሂብ.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for ስም, ምንጭ in ምንጭ_ፋይሎች.items():
        (ውጤት / (ስም + '.java')).write_text(ምንጭ, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ውጤት)] +
                          [str(ውጤት / (ስም + '.java')) for ስም in ምንጭ_ፋይሎች])
    መዝግብ_ረድፍ = bytearray()
    def ባዶ_የወደብ_ቁጥር(ተይብ_ምድብ=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, ተይብ_ምድብ) as ፈልግ_እሴት:
            ፈልግ_እሴት.bind(('127.0.0.4', 0))
            return ፈልግ_እሴት.getsockname()[1]
    ፋይል_የወደብ_ቁጥር, የትልልፍ_ቁጥጥር_ፕሮቶኮል_ወደብ, 전문접속번호 = ባዶ_የወደብ_ቁጥር(), ባዶ_የወደብ_ቁጥር(), ባዶ_የወደብ_ቁጥር(socket.SOCK_DGRAM)
    ሂደት_እሴት = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, መረብ_ድልድይ(
                ፋይል_የወደብ_ቁጥር, ['tcp:{}:9300'.format(የትልልፍ_ቁጥጥር_ፕሮቶኮል_ወደብ), 'udp:{}:9301'.format(전문접속번호)],
                መያዝ=True, አዘጋጅ_አድራሻ='127.0.0.4') as ድልድይ_እሴት:
            ቁጥጥር_ዱካ = Path(임시) / 'qmp.sock'
            ሂደት_እሴት = subprocess.Popen(ትእዛዝ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(ቁጥጥር_ዱካ)] + ድልድይ_እሴት.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ምረጥ_ንጥል_ነገር = selectors.DefaultSelector()
            ምረጥ_ንጥል_ነገር.register(ሂደት_እሴት.stdout, selectors.EVENT_READ)
            def 받기(አሳይ_እሴት=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while አሳይ_እሴት not in መዝግብ_ረድፍ[처음:]:
                    if time.monotonic() > 끝 or ሂደት_እሴት.poll() is not None:
                        raise AssertionError('Missing ' + repr(አሳይ_እሴት) + '\n' + መዝግብ_ረድፍ[처음:].decode('utf-8', 'replace'))
                    for ቁልፍ_እሴት, _ in ምረጥ_ንጥል_ነገር.select(.05):
                        조각 = ቁልፍ_እሴት.fileobj.read(65536)
                        if 조각:
                            መዝግብ_ረድፍ.extend(조각)
                return መዝግብ_ረድፍ[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ላክ(ውሂብ):
                ሂደት_እሴት.stdin.write(ውሂብ)
                ሂደት_እሴት.stdin.flush()
            def ሼል(ጽሁፍ):
                print(ጽሁፍ, flush=True)
                처음 = len(መዝግብ_ረድፍ)
                ላክ((ጽሁፍ + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as ቁጥጥር_እሴት:
                ቁጥጥር_እሴት.settimeout(10)
                ቁጥጥር_እሴት.connect(str(ቁጥጥር_ዱካ))
                ልቀቅ_እሴት = ቁጥጥር_እሴት.makefile('rwb')
                json.loads(ልቀቅ_እሴት.readline())
                def 요청(መምሪያ_እሴት, 인수=None):
                    ውሂብ = {'execute': መምሪያ_እሴት}
                    if 인수 is not None:
                        ውሂብ['arguments'] = 인수
                    ልቀቅ_እሴት.write((json.dumps(ውሂብ) + '\n').encode())
                    ልቀቅ_እሴት.flush()
                    while True:
                        መልስ = json.loads(ልቀቅ_እሴት.readline())
                        if 'error' in መልስ:
                            raise AssertionError(መልስ)
                        if 'return' in መልስ:
                            return መልስ['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                ዘገባ_እሴት['shell_cpu'] = 권한읽기()
                assert 'EL1h' in ዘገባ_እሴት['shell_cpu'], ዘገባ_እሴት['shell_cpu']
                ዘገባ_እሴት['initial_ps'] = ሼል('ps')
                assert 'kernel/shell' in ዘገባ_እሴት['initial_ps']
                ዘገባ_እሴት['ipconfig'] = ሼል('ipconfig')
                assert 'inet 10.0.2.15' in ዘገባ_እሴት['ipconfig']
                ዘገባ_እሴት['gateway_ping'] = ሼል('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in ዘገባ_እሴት['gateway_ping']
                assert 'FTP listening' in ሼል('ftpd start')
                with ftplib.FTP() as ትልልፍ_እሴት:
                    ትልልፍ_እሴት.encoding = 'utf-8'
                    ትልልፍ_እሴት.connect('127.0.0.4', ፋይል_የወደብ_ቁጥር, timeout=20)
                    ትልልፍ_እሴት.login()
                    for ስም in ምንጭ_ፋይሎች:
                        ትልልፍ_እሴት.storbinary('STOR ' + ስም + '.class', io.BytesIO((ውጤት / (ስም + '.class')).read_bytes()))
                처음 = len(መዝግብ_ረድፍ)
                ላክ('java ፈቃድ_ቼክ\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    ዘገባ_እሴት['java_cpu'] = 권한읽기()
                    if 'EL0t' in ዘገባ_እሴት['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in ዘገባ_እሴት['java_cpu'], ዘገባ_እሴት['java_cpu']
                받기(처음=처음)
                ዘገባ_እሴት['after_exit_ps'] = ሼል('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', ዘገባ_እሴት['after_exit_ps'])
                ዘገባ_እሴት['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as አቻ_እሴት:
                    ጽሁፍ = ሼል('java መረብ_ቼክ {} {}'.format(አቻ_እሴት.የትልልፍ_ቁጥጥር_ፕሮቶኮል_ወደብ, አቻ_እሴት.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in ጽሁፍ and 'exit 0' in ጽሁፍ, ጽሁፍ
                    assert አቻ_እሴት.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, አቻ_እሴት.수신됨
                    assert not አቻ_እሴት.오류들, አቻ_እሴት.오류들
                    ዘገባ_እሴት['outbound_peers'] = {종류: ውሂብ.decode() for 종류, ውሂብ in አቻ_እሴት.수신됨.items()}
                처음 = len(መዝግብ_ረድፍ)
                ላክ('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', የትልልፍ_ቁጥጥር_ፕሮቶኮል_ወደብ), timeout=5) as አቻ_እሴት:
                    አቻ_እሴት.sendall(b'A')
                    assert አቻ_እሴት.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as አቻ_እሴት:
                    አቻ_እሴት.settimeout(5)
                    አቻ_እሴት.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert አቻ_እሴት.recvfrom(64)[0] == b'UDP-IN'
                ጽሁፍ = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in ጽሁፍ and 'exit 0' in ጽሁፍ, ጽሁፍ
                ዘገባ_እሴት['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in ሼል('terminal')
                ሼል('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(መዝግብ_ረድፍ)
                ላክ('java 창예제\n'.encode())
                받기('GUI 예제 አዘጋጅ_9ce364fc: 창예제\r\n'.encode(), 처음)
                처음 = len(መዝግብ_ረድፍ)
                ላክ(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                ዘገባ_እሴት['suspended_java_ps'] = ሼል('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', ዘገባ_እሴት['suspended_java_ps']), ዘገባ_እሴት['suspended_java_ps']
                ዘገባ_እሴት['top'] = ሼል('top -n 1')
                assert 'java 창예제' in ዘገባ_እሴት['top'] and 'kernel/shell' in ዘገባ_እሴት['top']
                ዘገባ_እሴት['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                ዘገባ_እሴት['network_trace'] = ድልድይ_እሴት.ዱካ_መዝግብ
                assert not ድልድይ_እሴት.ስህተት, ድልድይ_እሴት.ስህተት
                ላክ(b'poweroff\n')
                assert ሂደት_እሴት.wait(timeout=15) == 0
                ዘገባ_እሴት['passed'] = True
            ምረጥ_ንጥል_ነገር.close()
    except Exception as ስህተት:
        ዘገባ_እሴት['error'] = str(ስህተት)
        raise
    finally:
        if ሂደት_እሴት is not None and ሂደት_እሴት.poll() is None:
            ሂደት_እሴት.terminate()
            try:
                ሂደት_እሴት.wait(timeout=10)
            except subprocess.TimeoutExpired:
                ሂደት_እሴት.kill()
                ሂደት_እሴት.wait()
        (ውጤት / 'serial.log').write_bytes(መዝግብ_ረድፍ)
        (ውጤት / 'report.json').write_text(json.dumps(ዘገባ_እሴት, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({ቁልፍ_እሴት: ዘገባ_እሴት[ቁልፍ_እሴት] for ቁልፍ_እሴት in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ማስኬጃ()
