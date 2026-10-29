#!/usr/bin/env python3
"""QEMU의 அசல்_தரவு CPU அனுமதி_மதிப்பு, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from இயக்கு_கட்டளை import திட்டப்பணி_மூலம், கட்டளை
from பிணையம்_பிரிட்ஜ் import பிணையம்_பிரிட்ஜ்
from 되돌림시험서버 import 되돌림시험서버


def செயல்படுத்துக():
    வெளியீட்டு_இடம் = திட்டப்பணி_மூலம் / 'build/verification/execution-network-review'
    வெளியீட்டு_இடம்.mkdir(parents=True, exist_ok=True)
    அறிக்கை_மதிப்பு = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((திட்டப்பணி_மூலம் / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    மூலம்_கோப்புகள் = {
        'அனுமதி_காசோலை': '''public class அனுமதி_காசோலை {
 public static void main(String[] செயலுருபுகள்) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'பிணையம்_காசோலை': '''import java.net.*;
public class பிணையம்_காசோலை {
 public static void main(String[] செயலுருபுகள்) throws Exception {
  Socket இணைக்க = new Socket("10.0.2.2", Integer.parseInt(செயலுருபுகள்[0]));
  இணைக்க.setSoTimeout(3000);
  byte[] உரை = "TCP 한글\\n".getBytes("UTF-8");
  இணைக்க.getOutputStream().write(உரை);
  for (int நிலை_அடைவு = 0; நிலை_அடைவு < உரை.length; நிலை_அடைவு++)
   if (இணைக்க.getInputStream().read() != (உரை[நிலை_அடைவு] & 255)) throw new RuntimeException("TCP mismatch");
  இணைக்க.close();
  DatagramSocket முடிவுப்_புள்ளி = new DatagramSocket(); முடிவுப்_புள்ளி.setSoTimeout(3000);
  உரை = "UDP 한글".getBytes("UTF-8");
  முடிவுப்_புள்ளி.send(new DatagramPacket(உரை, உரை.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(செயலுருபுகள்[1])));
  byte[] பதிலளி = new byte[64]; DatagramPacket 전문 = new DatagramPacket(பதிலளி, பதிலளி.length);
  முடிவுப்_புள்ளி.receive(전문);
  if (전문.getLength() != உரை.length) throw new RuntimeException("UDP length");
  for (int நிலை_அடைவு = 0; நிலை_அடைவு < உரை.length; நிலை_அடைவு++)
   if (பதிலளி[நிலை_அடைவு] != உரை[நிலை_அடைவு]) throw new RuntimeException("UDP mismatch");
  முடிவுப்_புள்ளி.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] செயலுருபுகள்) throws Exception {
  ServerSocket சேவையகம்_மதிப்பு = new ServerSocket(9300); சேவையகம்_மதிப்பு.setSoTimeout(5000);
  DatagramSocket முடிவுப்_புள்ளி = new DatagramSocket(9301); முடிவுப்_புள்ளி.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket இணைக்க = சேவையகம்_மதிப்பு.accept(); இணைக்க.setSoTimeout(5000);
  இணைக்க.getOutputStream().write(இணைக்க.getInputStream().read() + 1);
  இணைக்க.close(); சேவையகம்_மதிப்பு.close();
  byte[] தரவு = new byte[64]; DatagramPacket 전문 = new DatagramPacket(தரவு, தரவு.length);
  முடிவுப்_புள்ளி.receive(전문); முடிவுப்_புள்ளி.send(전문); முடிவுப்_புள்ளி.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for பெயர், மூலக்_கோப்பு in மூலம்_கோப்புகள்.items():
        (வெளியீட்டு_இடம் / (பெயர் + '.java')).write_text(மூலக்_கோப்பு, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(வெளியீட்டு_இடம்)] +
                          [str(வெளியீட்டு_இடம் / (பெயர் + '.java')) for பெயர் in மூலம்_கோப்புகள்])
    பதிவு_பதிவு = bytearray()
    def வெறுமை_முனைய_எண்(வகை_வகை=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, வகை_வகை) as தேடு_மதிப்பு:
            தேடு_மதிப்பு.bind(('127.0.0.4', 0))
            return தேடு_மதிப்பு.getsockname()[1]
    கோப்பு_முனைய_எண், டிரான்ஸ்மிஷன்_கண்ட்ரோல்_புரோட்டோகால்_முணையம், 전문접속번호 = வெறுமை_முனைய_எண்(), வெறுமை_முனைய_எண்(), வெறுமை_முனைய_எண்(socket.SOCK_DGRAM)
    செயலகம்_மதிப்பு = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, பிணையம்_பிரிட்ஜ்(
                கோப்பு_முனைய_எண், ['tcp:{}:9300'.format(டிரான்ஸ்மிஷன்_கண்ட்ரோல்_புரோட்டோகால்_முணையம்), 'udp:{}:9301'.format(전문접속번호)],
                பிடிப்பு=True, ஓம்பு_முகவரி='127.0.0.4') as பிரிட்ஜ்_மதிப்பு:
            கட்டுப்பாடு_பாதை = Path(임시) / 'qmp.sock'
            செயலகம்_மதிப்பு = subprocess.Popen(கட்டளை() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(கட்டுப்பாடு_பாதை)] + பிரிட்ஜ்_மதிப்பு.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            தேர்வுசெய்_உருப்படி = selectors.DefaultSelector()
            தேர்வுசெய்_உருப்படி.register(செயலகம்_மதிப்பு.stdout, selectors.EVENT_READ)
            def 받기(காட்சி_மதிப்பு_487749b8=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while காட்சி_மதிப்பு_487749b8 not in பதிவு_பதிவு[처음:]:
                    if time.monotonic() > 끝 or செயலகம்_மதிப்பு.poll() is not None:
                        raise AssertionError('Missing ' + repr(காட்சி_மதிப்பு_487749b8) + '\n' + பதிவு_பதிவு[처음:].decode('utf-8', 'replace'))
                    for சாவி_மதிப்பு, _ in தேர்வுசெய்_உருப்படி.select(.05):
                        조각 = சாவி_மதிப்பு.fileobj.read(65536)
                        if 조각:
                            பதிவு_பதிவு.extend(조각)
                return பதிவு_பதிவு[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def அனுப்பு(தரவு):
                செயலகம்_மதிப்பு.stdin.write(தரவு)
                செயலகம்_மதிப்பு.stdin.flush()
            def கூடு(உரை):
                print(உரை, flush=True)
                처음 = len(பதிவு_பதிவு)
                அனுப்பு((உரை + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as கட்டுப்பாடு_மதிப்பு:
                கட்டுப்பாடு_மதிப்பு.settimeout(10)
                கட்டுப்பாடு_மதிப்பு.connect(str(கட்டுப்பாடு_பாதை))
                தொடரோடி_மதிப்பு = கட்டுப்பாடு_மதிப்பு.makefile('rwb')
                json.loads(தொடரோடி_மதிப்பு.readline())
                def HTTP_வேண்டுதல்(ஆணை_மதிப்பு, செயலுருபுகள்=None):
                    தரவு = {'execute': ஆணை_மதிப்பு}
                    if செயலுருபுகள் is not None:
                        தரவு['arguments'] = செயலுருபுகள்
                    தொடரோடி_மதிப்பு.write((json.dumps(தரவு) + '\n').encode())
                    தொடரோடி_மதிப்பு.flush()
                    while True:
                        பதிலளி = json.loads(தொடரோடி_மதிப்பு.readline())
                        if 'error' in பதிலளி:
                            raise AssertionError(பதிலளி)
                        if 'return' in பதிலளி:
                            return பதிலளி['return']
                HTTP_வேண்டுதல்('qmp_capabilities')
                def 권한읽기():
                    HTTP_வேண்டுதல்('stop')
                    try:
                        return HTTP_வேண்டுதல்('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        HTTP_வேண்டுதல்('cont')
                அறிக்கை_மதிப்பு['shell_cpu'] = 권한읽기()
                assert 'EL1h' in அறிக்கை_மதிப்பு['shell_cpu'], அறிக்கை_மதிப்பு['shell_cpu']
                அறிக்கை_மதிப்பு['initial_ps'] = கூடு('ps')
                assert 'kernel/shell' in அறிக்கை_மதிப்பு['initial_ps']
                அறிக்கை_மதிப்பு['ipconfig'] = கூடு('ipconfig')
                assert 'inet 10.0.2.15' in அறிக்கை_மதிப்பு['ipconfig']
                அறிக்கை_மதிப்பு['gateway_ping'] = கூடு('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in அறிக்கை_மதிப்பு['gateway_ping']
                assert 'FTP listening' in கூடு('ftpd start')
                with ftplib.FTP() as இடமாற்று_மதிப்பு:
                    இடமாற்று_மதிப்பு.encoding = 'utf-8'
                    இடமாற்று_மதிப்பு.connect('127.0.0.4', கோப்பு_முனைய_எண், timeout=20)
                    இடமாற்று_மதிப்பு.login()
                    for பெயர் in மூலம்_கோப்புகள்:
                        இடமாற்று_மதிப்பு.storbinary('STOR ' + பெயர் + '.class', io.BytesIO((வெளியீட்டு_இடம் / (பெயர் + '.class')).read_bytes()))
                처음 = len(பதிவு_பதிவு)
                அனுப்பு('java அனுமதி_காசோலை\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    அறிக்கை_மதிப்பு['java_cpu'] = 권한읽기()
                    if 'EL0t' in அறிக்கை_மதிப்பு['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in அறிக்கை_மதிப்பு['java_cpu'], அறிக்கை_மதிப்பு['java_cpu']
                받기(처음=처음)
                அறிக்கை_மதிப்பு['after_exit_ps'] = கூடு('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', அறிக்கை_மதிப்பு['after_exit_ps'])
                அறிக்கை_மதிப்பு['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as பியர்_மதிப்பு:
                    உரை = கூடு('java பிணையம்_காசோலை {} {}'.format(பியர்_மதிப்பு.டிரான்ஸ்மிஷன்_கண்ட்ரோல்_புரோட்டோகால்_முணையம், பியர்_மதிப்பு.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in உரை and 'exit 0' in உரை, உரை
                    assert பியர்_மதிப்பு.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, பியர்_மதிப்பு.수신됨
                    assert not பியர்_மதிப்பு.오류들, பியர்_மதிப்பு.오류들
                    அறிக்கை_மதிப்பு['outbound_peers'] = {종류: தரவு.decode() for 종류, தரவு in பியர்_மதிப்பு.수신됨.items()}
                처음 = len(பதிவு_பதிவு)
                அனுப்பு('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', டிரான்ஸ்மிஷன்_கண்ட்ரோல்_புரோட்டோகால்_முணையம்), timeout=5) as பியர்_மதிப்பு:
                    பியர்_மதிப்பு.sendall(b'A')
                    assert பியர்_மதிப்பு.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as பியர்_மதிப்பு:
                    பியர்_மதிப்பு.settimeout(5)
                    பியர்_மதிப்பு.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert பியர்_மதிப்பு.recvfrom(64)[0] == b'UDP-IN'
                உரை = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in உரை and 'exit 0' in உரை, உரை
                அறிக்கை_மதிப்பு['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in கூடு('terminal')
                கூடு('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(பதிவு_பதிவு)
                அனுப்பு('java 창예제\n'.encode())
                받기('GUI 예제 தயார்படுத்த: 창예제\r\n'.encode(), 처음)
                처음 = len(பதிவு_பதிவு)
                அனுப்பு(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                அறிக்கை_மதிப்பு['suspended_java_ps'] = கூடு('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', அறிக்கை_மதிப்பு['suspended_java_ps']), அறிக்கை_மதிப்பு['suspended_java_ps']
                அறிக்கை_மதிப்பு['top'] = கூடு('top -n 1')
                assert 'java 창예제' in அறிக்கை_மதிப்பு['top'] and 'kernel/shell' in அறிக்கை_மதிப்பு['top']
                அறிக்கை_மதிப்பு['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                அறிக்கை_மதிப்பு['network_trace'] = பிரிட்ஜ்_மதிப்பு.சுவடு_பதிவு
                assert not பிரிட்ஜ்_மதிப்பு.பிழை, பிரிட்ஜ்_மதிப்பு.பிழை
                அனுப்பு(b'poweroff\n')
                assert செயலகம்_மதிப்பு.wait(timeout=15) == 0
                அறிக்கை_மதிப்பு['passed'] = True
            தேர்வுசெய்_உருப்படி.close()
    except Exception as பிழை:
        அறிக்கை_மதிப்பு['error'] = str(பிழை)
        raise
    finally:
        if செயலகம்_மதிப்பு is not None and செயலகம்_மதிப்பு.poll() is None:
            செயலகம்_மதிப்பு.terminate()
            try:
                செயலகம்_மதிப்பு.wait(timeout=10)
            except subprocess.TimeoutExpired:
                செயலகம்_மதிப்பு.kill()
                செயலகம்_மதிப்பு.wait()
        (வெளியீட்டு_இடம் / 'serial.log').write_bytes(பதிவு_பதிவு)
        (வெளியீட்டு_இடம் / 'report.json').write_text(json.dumps(அறிக்கை_மதிப்பு, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({சாவி_மதிப்பு: அறிக்கை_மதிப்பு[சாவி_மதிப்பு] for சாவி_மதிப்பு in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    செயல்படுத்துக()
