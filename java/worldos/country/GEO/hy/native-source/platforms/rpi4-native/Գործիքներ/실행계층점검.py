#!/usr/bin/env python3
"""QEMU의 իրական_տվյալ CPU թույլտվություն_արժեք, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from կատարել_հրաման import արձակել_արմատ, Հրահանգ
from Ցանց_կամուրջ import Ցանց_կամուրջ
from 되돌림시험서버 import 되돌림시험서버


def Գործարկել():
    Ելք = արձակել_արմատ / 'build/verification/execution-network-review'
    Ելք.mkdir(parents=True, exist_ok=True)
    զեկույց_արժեք = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((արձակել_արմատ / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    աղբյուր_Նիշքեր = {
        'թույլտվություն_կտրոն': '''public class թույլտվություն_կտրոն {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Ցանց_կտրոն': '''import java.net.*;
public class Ցանց_կտրոն {
 public static void main(String[] 인수) throws Exception {
  Socket Միացնել = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Միացնել.setSoTimeout(3000);
  byte[] Տեքստ = "TCP 한글\\n".getBytes("UTF-8");
  Միացնել.getOutputStream().write(Տեքստ);
  for (int դիրք_դասիչ = 0; դիրք_դասիչ < Տեքստ.length; դիրք_դասիչ++)
   if (Միացնել.getInputStream().read() != (Տեքստ[դիրք_դասիչ] & 255)) throw new RuntimeException("TCP mismatch");
  Միացնել.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Տեքստ = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Տեքստ, Տեքստ.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] պատասխանել = new byte[64]; DatagramPacket 전문 = new DatagramPacket(պատասխանել, պատասխանել.length);
  종단.receive(전문);
  if (전문.getLength() != Տեքստ.length) throw new RuntimeException("UDP length");
  for (int դիրք_դասիչ = 0; դիրք_դասիչ < Տեքստ.length; դիրք_դասիչ++)
   if (պատասխանել[դիրք_դասիչ] != Տեքստ[դիրք_դասիչ]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket սպասարկիչ_արժեք = new ServerSocket(9300); սպասարկիչ_արժեք.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Միացնել = սպասարկիչ_արժեք.accept(); Միացնել.setSoTimeout(5000);
  Միացնել.getOutputStream().write(Միացնել.getInputStream().read() + 1);
  Միացնել.close(); սպասարկիչ_արժեք.close();
  byte[] տվյալ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(տվյալ, տվյալ.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Անուն, ԱՂԲՅՈՒՐ in աղբյուր_Նիշքեր.items():
        (Ելք / (Անուն + '.java')).write_text(ԱՂԲՅՈՒՐ, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Ելք)] +
                          [str(Ելք / (Անուն + '.java')) for Անուն in աղբյուր_Նիշքեր])
    մատյան_տող = bytearray()
    def 빈접속번호(մուտքագրել_անվանակարգ=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, մուտքագրել_անվանակարգ) as որոնել_արժեք:
            որոնել_արժեք.bind(('127.0.0.4', 0))
            return որոնել_արժեք.getsockname()[1]
    파일접속번호, Փոխանցման_կառավարման_հաղորդակարգ_միացք, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Ընթացք_արժեք = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Ցանց_կամուրջ(
                파일접속번호, ['tcp:{}:9300'.format(Փոխանցման_կառավարման_հաղորդակարգ_միացք), 'udp:{}:9301'.format(전문접속번호)],
                նկարահանել=True, հոստ_հասցե='127.0.0.4') as կամուրջ_արժեք:
            հսկում_ուղի = Path(임시) / 'qmp.sock'
            Ընթացք_արժեք = subprocess.Popen(Հրահանգ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(հսկում_ուղի)] + կամուրջ_արժեք.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ընտրել_միավոր = selectors.DefaultSelector()
            ընտրել_միավոր.register(Ընթացք_արժեք.stdout, selectors.EVENT_READ)
            def 받기(ցուցադրել_արժեք=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ցուցադրել_արժեք not in մատյան_տող[처음:]:
                    if time.monotonic() > 끝 or Ընթացք_արժեք.poll() is not None:
                        raise AssertionError('Missing ' + repr(ցուցադրել_արժեք) + '\n' + մատյան_տող[처음:].decode('utf-8', 'replace'))
                    for ստեղն_արժեք, _ in ընտրել_միավոր.select(.05):
                        조각 = ստեղն_արժեք.fileobj.read(65536)
                        if 조각:
                            մատյան_տող.extend(조각)
                return մատյան_տող[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ուղարկել(տվյալ):
                Ընթացք_արժեք.stdin.write(տվյալ)
                Ընթացք_արժեք.stdin.flush()
            def խեցի(Տեքստ):
                print(Տեքստ, flush=True)
                처음 = len(մատյան_տող)
                ուղարկել((Տեքստ + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as հսկում_արժեք:
                հսկում_արժեք.settimeout(10)
                հսկում_արժեք.connect(str(հսկում_ուղի))
                հոսք_արժեք = հսկում_արժեք.makefile('rwb')
                json.loads(հոսք_արժեք.readline())
                def 요청(հրահանգ_արժեք, 인수=None):
                    տվյալ = {'execute': հրահանգ_արժեք}
                    if 인수 is not None:
                        տվյալ['arguments'] = 인수
                    հոսք_արժեք.write((json.dumps(տվյալ) + '\n').encode())
                    հոսք_արժեք.flush()
                    while True:
                        պատասխանել = json.loads(հոսք_արժեք.readline())
                        if 'error' in պատասխանել:
                            raise AssertionError(պատասխանել)
                        if 'return' in պատասխանել:
                            return պատասխանել['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                զեկույց_արժեք['shell_cpu'] = 권한읽기()
                assert 'EL1h' in զեկույց_արժեք['shell_cpu'], զեկույց_արժեք['shell_cpu']
                զեկույց_արժեք['initial_ps'] = խեցի('ps')
                assert 'kernel/shell' in զեկույց_արժեք['initial_ps']
                զեկույց_արժեք['ipconfig'] = խեցի('ipconfig')
                assert 'inet 10.0.2.15' in զեկույց_արժեք['ipconfig']
                զեկույց_արժեք['gateway_ping'] = խեցի('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in զեկույց_արժեք['gateway_ping']
                assert 'FTP listening' in խեցի('ftpd start')
                with ftplib.FTP() as փոխանցել_արժեք:
                    փոխանցել_արժեք.encoding = 'utf-8'
                    փոխանցել_արժեք.connect('127.0.0.4', 파일접속번호, timeout=20)
                    փոխանցել_արժեք.login()
                    for Անուն in աղբյուր_Նիշքեր:
                        փոխանցել_արժեք.storbinary('STOR ' + Անուն + '.class', io.BytesIO((Ելք / (Անուն + '.class')).read_bytes()))
                처음 = len(մատյան_տող)
                ուղարկել('java թույլտվություն_կտրոն\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    զեկույց_արժեք['java_cpu'] = 권한읽기()
                    if 'EL0t' in զեկույց_արժեք['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in զեկույց_արժեք['java_cpu'], զեկույց_արժեք['java_cpu']
                받기(처음=처음)
                զեկույց_արժեք['after_exit_ps'] = խեցի('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', զեկույց_արժեք['after_exit_ps'])
                զեկույց_արժեք['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as հավասարազոր_սարք_արժեք:
                    Տեքստ = խեցի('java Ցանց_կտրոն {} {}'.format(հավասարազոր_սարք_արժեք.Փոխանցման_կառավարման_հաղորդակարգ_միացք, հավասարազոր_սարք_արժեք.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Տեքստ and 'exit 0' in Տեքստ, Տեքստ
                    assert հավասարազոր_սարք_արժեք.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, հավասարազոր_սարք_արժեք.수신됨
                    assert not հավասարազոր_սարք_արժեք.오류들, հավասարազոր_սարք_արժեք.오류들
                    զեկույց_արժեք['outbound_peers'] = {종류: տվյալ.decode() for 종류, տվյալ in հավասարազոր_սարք_արժեք.수신됨.items()}
                처음 = len(մատյան_տող)
                ուղարկել('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', Փոխանցման_կառավարման_հաղորդակարգ_միացք), timeout=5) as հավասարազոր_սարք_արժեք:
                    հավասարազոր_սարք_արժեք.sendall(b'A')
                    assert հավասարազոր_սարք_արժեք.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as հավասարազոր_սարք_արժեք:
                    հավասարազոր_սարք_արժեք.settimeout(5)
                    հավասարազոր_սարք_արժեք.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert հավասարազոր_սարք_արժեք.recvfrom(64)[0] == b'UDP-IN'
                Տեքստ = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Տեքստ and 'exit 0' in Տեքստ, Տեքստ
                զեկույց_արժեք['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in խեցի('terminal')
                խեցի('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(մատյան_տող)
                ուղարկել('java 창예제\n'.encode())
                받기('GUI 예제 Պատրաստել: 창예제\r\n'.encode(), 처음)
                처음 = len(մատյան_տող)
                ուղարկել(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                զեկույց_արժեք['suspended_java_ps'] = խեցի('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', զեկույց_արժեք['suspended_java_ps']), զեկույց_արժեք['suspended_java_ps']
                զեկույց_արժեք['top'] = խեցի('top -n 1')
                assert 'java 창예제' in զեկույց_արժեք['top'] and 'kernel/shell' in զեկույց_արժեք['top']
                զեկույց_արժեք['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                զեկույց_արժեք['network_trace'] = կամուրջ_արժեք.추적기록
                assert not կամուրջ_արժեք.Սխալ, կամուրջ_արժեք.Սխալ
                ուղարկել(b'poweroff\n')
                assert Ընթացք_արժեք.wait(timeout=15) == 0
                զեկույց_արժեք['passed'] = True
            ընտրել_միավոր.close()
    except Exception as Սխալ:
        զեկույց_արժեք['error'] = str(Սխալ)
        raise
    finally:
        if Ընթացք_արժեք is not None and Ընթացք_արժեք.poll() is None:
            Ընթացք_արժեք.terminate()
            try:
                Ընթացք_արժեք.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Ընթացք_արժեք.kill()
                Ընթացք_արժեք.wait()
        (Ելք / 'serial.log').write_bytes(մատյան_տող)
        (Ելք / 'report.json').write_text(json.dumps(զեկույց_արժեք, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({ստեղն_արժեք: զեկույց_արժեք[ստեղն_արժեք] for ստեղն_արժեք in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Գործարկել()
