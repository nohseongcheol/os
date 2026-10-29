#!/usr/bin/env python3
"""QEMU의 real_ma_lumotlar CPU ruxsat_VALUE_a9fa0dfa, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from bajarmoq_buyruq import Project_ildiz, Buyruq
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def Bajarish():
    출력 = Project_ildiz / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    hisobot_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_ildiz / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    manba_Fayllar = {
        'ruxsat_chek': '''public class ruxsat_chek {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Tarmoq_chek': '''import java.net.*;
public class Tarmoq_chek {
 public static void main(String[] 인수) throws Exception {
  Socket Ulanish = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Ulanish.setSoTimeout(3000);
  byte[] Matn = "TCP 한글\\n".getBytes("UTF-8");
  Ulanish.getOutputStream().write(Matn);
  for (int holat_INDEX = 0; holat_INDEX < Matn.length; holat_INDEX++)
   if (Ulanish.getInputStream().read() != (Matn[holat_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  Ulanish.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Matn = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Matn, Matn.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] javob_berish = new byte[64]; DatagramPacket 전문 = new DatagramPacket(javob_berish, javob_berish.length);
  종단.receive(전문);
  if (전문.getLength() != Matn.length) throw new RuntimeException("UDP length");
  for (int holat_INDEX = 0; holat_INDEX < Matn.length; holat_INDEX++)
   if (javob_berish[holat_INDEX] != Matn[holat_INDEX]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); server_VALUE.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Ulanish = server_VALUE.accept(); Ulanish.setSoTimeout(5000);
  Ulanish.getOutputStream().write(Ulanish.getInputStream().read() + 1);
  Ulanish.close(); server_VALUE.close();
  byte[] ma_lumotlar = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ma_lumotlar, ma_lumotlar.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Nomi, manba in manba_Fayllar.items():
        (출력 / (Nomi + '.java')).write_text(manba, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Nomi + '.java')) for Nomi in manba_Fayllar])
    LOG_satr = bytearray()
    def 빈접속번호(TYPE_toifa=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_toifa) as Izlash_VALUE:
            Izlash_VALUE.bind(('127.0.0.4', 0))
            return Izlash_VALUE.getsockname()[1]
    파일접속번호, TCP_bayonnomasi_port, UDP_port = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Jarayon_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                파일접속번호, ['tcp:{}:9300'.format(TCP_bayonnomasi_port), 'udp:{}:9301'.format(UDP_port)],
                olish=True, tashkilotchi_manzil='127.0.0.4') as 다리:
            boshqaruv_yo_l = Path(임시) / 'qmp.sock'
            Jarayon_VALUE = subprocess.Popen(Buyruq() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(boshqaruv_yo_l)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_element = selectors.DefaultSelector()
            CHOOSE_element.register(Jarayon_VALUE.stdout, selectors.EVENT_READ)
            def 받기(ko_rsatmoq_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ko_rsatmoq_VALUE not in LOG_satr[처음:]:
                    if time.monotonic() > 끝 or Jarayon_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(ko_rsatmoq_VALUE) + '\n' + LOG_satr[처음:].decode('utf-8', 'replace'))
                    for Kalit_VALUE, _ in CHOOSE_element.select(.05):
                        조각 = Kalit_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_satr.extend(조각)
                return LOG_satr[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def yuborish(ma_lumotlar):
                Jarayon_VALUE.stdin.write(ma_lumotlar)
                Jarayon_VALUE.stdin.flush()
            def qobiq(Matn):
                print(Matn, flush=True)
                처음 = len(LOG_satr)
                yuborish((Matn + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as boshqaruv_VALUE:
                boshqaruv_VALUE.settimeout(10)
                boshqaruv_VALUE.connect(str(boshqaruv_yo_l))
                oqim_VALUE = boshqaruv_VALUE.makefile('rwb')
                json.loads(oqim_VALUE.readline())
                def 요청(qo_llanma_VALUE, 인수=None):
                    ma_lumotlar = {'execute': qo_llanma_VALUE}
                    if 인수 is not None:
                        ma_lumotlar['arguments'] = 인수
                    oqim_VALUE.write((json.dumps(ma_lumotlar) + '\n').encode())
                    oqim_VALUE.flush()
                    while True:
                        javob_berish = json.loads(oqim_VALUE.readline())
                        if 'error' in javob_berish:
                            raise AssertionError(javob_berish)
                        if 'return' in javob_berish:
                            return javob_berish['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                hisobot_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in hisobot_VALUE['shell_cpu'], hisobot_VALUE['shell_cpu']
                hisobot_VALUE['initial_ps'] = qobiq('ps')
                assert 'kernel/shell' in hisobot_VALUE['initial_ps']
                hisobot_VALUE['ipconfig'] = qobiq('ipconfig')
                assert 'inet 10.0.2.15' in hisobot_VALUE['ipconfig']
                hisobot_VALUE['gateway_ping'] = qobiq('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in hisobot_VALUE['gateway_ping']
                assert 'FTP listening' in qobiq('ftpd start')
                with ftplib.FTP() as uzatish_VALUE:
                    uzatish_VALUE.encoding = 'utf-8'
                    uzatish_VALUE.connect('127.0.0.4', 파일접속번호, timeout=20)
                    uzatish_VALUE.login()
                    for Nomi in manba_Fayllar:
                        uzatish_VALUE.storbinary('STOR ' + Nomi + '.class', io.BytesIO((출력 / (Nomi + '.class')).read_bytes()))
                처음 = len(LOG_satr)
                yuborish('java ruxsat_chek\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    hisobot_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in hisobot_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in hisobot_VALUE['java_cpu'], hisobot_VALUE['java_cpu']
                받기(처음=처음)
                hisobot_VALUE['after_exit_ps'] = qobiq('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', hisobot_VALUE['after_exit_ps'])
                hisobot_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as bir_rangli_VALUE:
                    Matn = qobiq('java Tarmoq_chek {} {}'.format(bir_rangli_VALUE.TCP_bayonnomasi_port, bir_rangli_VALUE.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Matn and 'exit 0' in Matn, Matn
                    assert bir_rangli_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, bir_rangli_VALUE.수신됨
                    assert not bir_rangli_VALUE.오류들, bir_rangli_VALUE.오류들
                    hisobot_VALUE['outbound_peers'] = {종류: ma_lumotlar.decode() for 종류, ma_lumotlar in bir_rangli_VALUE.수신됨.items()}
                처음 = len(LOG_satr)
                yuborish('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_bayonnomasi_port), timeout=5) as bir_rangli_VALUE:
                    bir_rangli_VALUE.sendall(b'A')
                    assert bir_rangli_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as bir_rangli_VALUE:
                    bir_rangli_VALUE.settimeout(5)
                    bir_rangli_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert bir_rangli_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Matn = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Matn and 'exit 0' in Matn, Matn
                hisobot_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in qobiq('terminal')
                qobiq('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_satr)
                yuborish('java 창예제\n'.encode())
                받기('GUI 예제 Tayyorlamoq: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_satr)
                yuborish(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                hisobot_VALUE['suspended_java_ps'] = qobiq('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', hisobot_VALUE['suspended_java_ps']), hisobot_VALUE['suspended_java_ps']
                hisobot_VALUE['top'] = qobiq('top -n 1')
                assert 'java 창예제' in hisobot_VALUE['top'] and 'kernel/shell' in hisobot_VALUE['top']
                hisobot_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                hisobot_VALUE['network_trace'] = 다리.iz_LOG
                assert not 다리.Xato, 다리.Xato
                yuborish(b'poweroff\n')
                assert Jarayon_VALUE.wait(timeout=15) == 0
                hisobot_VALUE['passed'] = True
            CHOOSE_element.close()
    except Exception as Xato:
        hisobot_VALUE['error'] = str(Xato)
        raise
    finally:
        if Jarayon_VALUE is not None and Jarayon_VALUE.poll() is None:
            Jarayon_VALUE.terminate()
            try:
                Jarayon_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Jarayon_VALUE.kill()
                Jarayon_VALUE.wait()
        (출력 / 'serial.log').write_bytes(LOG_satr)
        (출력 / 'report.json').write_text(json.dumps(hisobot_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Kalit_VALUE: hisobot_VALUE[Kalit_VALUE] for Kalit_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Bajarish()
