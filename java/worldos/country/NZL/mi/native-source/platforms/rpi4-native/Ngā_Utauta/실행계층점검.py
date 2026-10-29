#!/usr/bin/env python3
"""QEMU의 tūturu_raraunga CPU mana_uru_uara, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from kawe_tono import whakaatu_pūtake, tono
from whatunga_arawhata import whatunga_arawhata
from 되돌림시험서버 import 되돌림시험서버


def whakahaere():
    출력 = whakaatu_pūtake / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    pūrongo_uara = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((whakaatu_pūtake / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    pūtake_Ngā_Kōnae = {
        'whakaaetanga_taki': '''public class whakaaetanga_taki {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'whatunga_taki': '''import java.net.*;
public class whatunga_taki {
 public static void main(String[] 인수) throws Exception {
  Socket TŪHONO = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  TŪHONO.setSoTimeout(3000);
  byte[] Ngā_kupu = "TCP 한글\\n".getBytes("UTF-8");
  TŪHONO.getOutputStream().write(Ngā_kupu);
  for (int tūranga_INDEX = 0; tūranga_INDEX < Ngā_kupu.length; tūranga_INDEX++)
   if (TŪHONO.getInputStream().read() != (Ngā_kupu[tūranga_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  TŪHONO.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Ngā_kupu = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Ngā_kupu, Ngā_kupu.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] whakautu = new byte[64]; DatagramPacket 전문 = new DatagramPacket(whakautu, whakautu.length);
  종단.receive(전문);
  if (전문.getLength() != Ngā_kupu.length) throw new RuntimeException("UDP length");
  for (int tūranga_INDEX = 0; tūranga_INDEX < Ngā_kupu.length; tūranga_INDEX++)
   if (whakautu[tūranga_INDEX] != Ngā_kupu[tūranga_INDEX]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket tūmau_uara = new ServerSocket(9300); tūmau_uara.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket TŪHONO = tūmau_uara.accept(); TŪHONO.setSoTimeout(5000);
  TŪHONO.getOutputStream().write(TŪHONO.getInputStream().read() + 1);
  TŪHONO.close(); tūmau_uara.close();
  byte[] raraunga = new byte[64]; DatagramPacket 전문 = new DatagramPacket(raraunga, raraunga.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Ingoa, pūtake in pūtake_Ngā_Kōnae.items():
        (출력 / (Ingoa + '.java')).write_text(pūtake, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Ingoa + '.java')) for Ingoa in pūtake_Ngā_Kōnae])
    LOG_RECORD = bytearray()
    def 빈접속번호(TYPE_kāwai=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_kāwai) as Rapu_uara:
            Rapu_uara.bind(('127.0.0.4', 0))
            return Rapu_uara.getsockname()[1]
    파일접속번호, TCP_kawe, UDP_kawe = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Hātepe_uara = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, whatunga_arawhata(
                파일접속번호, ['tcp:{}:9300'.format(TCP_kawe), 'udp:{}:9301'.format(UDP_kawe)],
                hopu=True, taurima_ADDRESS='127.0.0.4') as arawhata_uara:
            mana_ara = Path(임시) / 'qmp.sock'
            Hātepe_uara = subprocess.Popen(tono() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(mana_ara)] + arawhata_uara.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_tuemi = selectors.DefaultSelector()
            CHOOSE_tuemi.register(Hātepe_uara.stdout, selectors.EVENT_READ)
            def 받기(whakaatu_uara=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while whakaatu_uara not in LOG_RECORD[처음:]:
                    if time.monotonic() > 끝 or Hātepe_uara.poll() is not None:
                        raise AssertionError('Missing ' + repr(whakaatu_uara) + '\n' + LOG_RECORD[처음:].decode('utf-8', 'replace'))
                    for kī_uara, _ in CHOOSE_tuemi.select(.05):
                        조각 = kī_uara.fileobj.read(65536)
                        if 조각:
                            LOG_RECORD.extend(조각)
                return LOG_RECORD[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def tuku(raraunga):
                Hātepe_uara.stdin.write(raraunga)
                Hātepe_uara.stdin.flush()
            def anga(Ngā_kupu):
                print(Ngā_kupu, flush=True)
                처음 = len(LOG_RECORD)
                tuku((Ngā_kupu + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as mana_uara:
                mana_uara.settimeout(10)
                mana_uara.connect(str(mana_ara))
                roma_uara = mana_uara.makefile('rwb')
                json.loads(roma_uara.readline())
                def 요청(tohutohu_uara, 인수=None):
                    raraunga = {'execute': tohutohu_uara}
                    if 인수 is not None:
                        raraunga['arguments'] = 인수
                    roma_uara.write((json.dumps(raraunga) + '\n').encode())
                    roma_uara.flush()
                    while True:
                        whakautu = json.loads(roma_uara.readline())
                        if 'error' in whakautu:
                            raise AssertionError(whakautu)
                        if 'return' in whakautu:
                            return whakautu['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                pūrongo_uara['shell_cpu'] = 권한읽기()
                assert 'EL1h' in pūrongo_uara['shell_cpu'], pūrongo_uara['shell_cpu']
                pūrongo_uara['initial_ps'] = anga('ps')
                assert 'kernel/shell' in pūrongo_uara['initial_ps']
                pūrongo_uara['ipconfig'] = anga('ipconfig')
                assert 'inet 10.0.2.15' in pūrongo_uara['ipconfig']
                pūrongo_uara['gateway_ping'] = anga('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in pūrongo_uara['gateway_ping']
                assert 'FTP listening' in anga('ftpd start')
                with ftplib.FTP() as whakawhiti_uara_630ba093:
                    whakawhiti_uara_630ba093.encoding = 'utf-8'
                    whakawhiti_uara_630ba093.connect('127.0.0.4', 파일접속번호, timeout=20)
                    whakawhiti_uara_630ba093.login()
                    for Ingoa in pūtake_Ngā_Kōnae:
                        whakawhiti_uara_630ba093.storbinary('STOR ' + Ingoa + '.class', io.BytesIO((출력 / (Ingoa + '.class')).read_bytes()))
                처음 = len(LOG_RECORD)
                tuku('java whakaaetanga_taki\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    pūrongo_uara['java_cpu'] = 권한읽기()
                    if 'EL0t' in pūrongo_uara['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in pūrongo_uara['java_cpu'], pūrongo_uara['java_cpu']
                받기(처음=처음)
                pūrongo_uara['after_exit_ps'] = anga('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', pūrongo_uara['after_exit_ps'])
                pūrongo_uara['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as hoa_uara:
                    Ngā_kupu = anga('java whatunga_taki {} {}'.format(hoa_uara.TCP_kawe, hoa_uara.UDP_kawe))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Ngā_kupu and 'exit 0' in Ngā_kupu, Ngā_kupu
                    assert hoa_uara.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, hoa_uara.수신됨
                    assert not hoa_uara.오류들, hoa_uara.오류들
                    pūrongo_uara['outbound_peers'] = {종류: raraunga.decode() for 종류, raraunga in hoa_uara.수신됨.items()}
                처음 = len(LOG_RECORD)
                tuku('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_kawe), timeout=5) as hoa_uara:
                    hoa_uara.sendall(b'A')
                    assert hoa_uara.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as hoa_uara:
                    hoa_uara.settimeout(5)
                    hoa_uara.sendto(b'UDP-IN', ('127.0.0.4', UDP_kawe))
                    assert hoa_uara.recvfrom(64)[0] == b'UDP-IN'
                Ngā_kupu = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Ngā_kupu and 'exit 0' in Ngā_kupu, Ngā_kupu
                pūrongo_uara['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in anga('terminal')
                anga('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_RECORD)
                tuku('java 창예제\n'.encode())
                받기('GUI 예제 Whakarite: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_RECORD)
                tuku(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                pūrongo_uara['suspended_java_ps'] = anga('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', pūrongo_uara['suspended_java_ps']), pūrongo_uara['suspended_java_ps']
                pūrongo_uara['top'] = anga('top -n 1')
                assert 'java 창예제' in pūrongo_uara['top'] and 'kernel/shell' in pūrongo_uara['top']
                pūrongo_uara['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                pūrongo_uara['network_trace'] = arawhata_uara.tapeke_hauroki_LOG
                assert not arawhata_uara.Pōhēhē, arawhata_uara.Pōhēhē
                tuku(b'poweroff\n')
                assert Hātepe_uara.wait(timeout=15) == 0
                pūrongo_uara['passed'] = True
            CHOOSE_tuemi.close()
    except Exception as Pōhēhē:
        pūrongo_uara['error'] = str(Pōhēhē)
        raise
    finally:
        if Hātepe_uara is not None and Hātepe_uara.poll() is None:
            Hātepe_uara.terminate()
            try:
                Hātepe_uara.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Hātepe_uara.kill()
                Hātepe_uara.wait()
        (출력 / 'serial.log').write_bytes(LOG_RECORD)
        (출력 / 'report.json').write_text(json.dumps(pūrongo_uara, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({kī_uara: pūrongo_uara[kī_uara] for kī_uara in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    whakahaere()
