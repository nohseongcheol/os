#!/usr/bin/env python3
"""QEMU의 sebenar_data CPU keizinan_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from laksanakan_perintah import projek_akar, Perintah
from rangkaian_penghubung import rangkaian_penghubung
from 되돌림시험서버 import 되돌림시험서버


def Jalan():
    출력 = projek_akar / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    lapor_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((projek_akar / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    sumber_Fail = {
        'keizinan_cek': '''public class keizinan_cek {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'rangkaian_cek': '''import java.net.*;
public class rangkaian_cek {
 public static void main(String[] 인수) throws Exception {
  Socket Sambung = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Sambung.setSoTimeout(3000);
  byte[] Teks = "TCP 한글\\n".getBytes("UTF-8");
  Sambung.getOutputStream().write(Teks);
  for (int jawatan_INDEX = 0; jawatan_INDEX < Teks.length; jawatan_INDEX++)
   if (Sambung.getInputStream().read() != (Teks[jawatan_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  Sambung.close();
  DatagramSocket peserta = new DatagramSocket(); peserta.setSoTimeout(3000);
  Teks = "UDP 한글".getBytes("UTF-8");
  peserta.send(new DatagramPacket(Teks, Teks.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] balas = new byte[64]; DatagramPacket 전문 = new DatagramPacket(balas, balas.length);
  peserta.receive(전문);
  if (전문.getLength() != Teks.length) throw new RuntimeException("UDP length");
  for (int jawatan_INDEX = 0; jawatan_INDEX < Teks.length; jawatan_INDEX++)
   if (balas[jawatan_INDEX] != Teks[jawatan_INDEX]) throw new RuntimeException("UDP mismatch");
  peserta.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket pelayan_VALUE = new ServerSocket(9300); pelayan_VALUE.setSoTimeout(5000);
  DatagramSocket peserta = new DatagramSocket(9301); peserta.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Sambung = pelayan_VALUE.accept(); Sambung.setSoTimeout(5000);
  Sambung.getOutputStream().write(Sambung.getInputStream().read() + 1);
  Sambung.close(); pelayan_VALUE.close();
  byte[] data = new byte[64]; DatagramPacket 전문 = new DatagramPacket(data, data.length);
  peserta.receive(전문); peserta.send(전문); peserta.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Nama, SUMBER in sumber_Fail.items():
        (출력 / (Nama + '.java')).write_text(SUMBER, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Nama + '.java')) for Nama in sumber_Fail])
    LOG_baris = bytearray()
    def 빈접속번호(TYPE_bidang=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_bidang) as Cari_VALUE:
            Cari_VALUE.bind(('127.0.0.4', 0))
            return Cari_VALUE.getsockname()[1]
    fail_nombor_port, TCP_port, UDP_port = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Proses_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, rangkaian_penghubung(
                fail_nombor_port, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(UDP_port)],
                rakam=True, hos_e_mel='127.0.0.4') as penghubung_VALUE:
            kawalan_laluan = Path(임시) / 'qmp.sock'
            Proses_VALUE = subprocess.Popen(Perintah() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(kawalan_laluan)] + penghubung_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            pilih_item = selectors.DefaultSelector()
            pilih_item.register(Proses_VALUE.stdout, selectors.EVENT_READ)
            def 받기(tayang_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while tayang_VALUE not in LOG_baris[처음:]:
                    if time.monotonic() > 끝 or Proses_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(tayang_VALUE) + '\n' + LOG_baris[처음:].decode('utf-8', 'replace'))
                    for Kunci_VALUE, _ in pilih_item.select(.05):
                        조각 = Kunci_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_baris.extend(조각)
                return LOG_baris[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def e_mel_9aee63bd(data):
                Proses_VALUE.stdin.write(data)
                Proses_VALUE.stdin.flush()
            def cangkerang(Teks):
                print(Teks, flush=True)
                처음 = len(LOG_baris)
                e_mel_9aee63bd((Teks + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as kawalan_VALUE:
                kawalan_VALUE.settimeout(10)
                kawalan_VALUE.connect(str(kawalan_laluan))
                strim_VALUE = kawalan_VALUE.makefile('rwb')
                json.loads(strim_VALUE.readline())
                def permintaan(suruhan_VALUE, 인수=None):
                    data = {'execute': suruhan_VALUE}
                    if 인수 is not None:
                        data['arguments'] = 인수
                    strim_VALUE.write((json.dumps(data) + '\n').encode())
                    strim_VALUE.flush()
                    while True:
                        balas = json.loads(strim_VALUE.readline())
                        if 'error' in balas:
                            raise AssertionError(balas)
                        if 'return' in balas:
                            return balas['return']
                permintaan('qmp_capabilities')
                def 권한읽기():
                    permintaan('stop')
                    try:
                        return permintaan('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        permintaan('cont')
                lapor_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in lapor_VALUE['shell_cpu'], lapor_VALUE['shell_cpu']
                lapor_VALUE['initial_ps'] = cangkerang('ps')
                assert 'kernel/shell' in lapor_VALUE['initial_ps']
                lapor_VALUE['ipconfig'] = cangkerang('ipconfig')
                assert 'inet 10.0.2.15' in lapor_VALUE['ipconfig']
                lapor_VALUE['gateway_ping'] = cangkerang('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in lapor_VALUE['gateway_ping']
                assert 'FTP listening' in cangkerang('ftpd start')
                with ftplib.FTP() as pindah_VALUE:
                    pindah_VALUE.encoding = 'utf-8'
                    pindah_VALUE.connect('127.0.0.4', fail_nombor_port, timeout=20)
                    pindah_VALUE.login()
                    for Nama in sumber_Fail:
                        pindah_VALUE.storbinary('STOR ' + Nama + '.class', io.BytesIO((출력 / (Nama + '.class')).read_bytes()))
                처음 = len(LOG_baris)
                e_mel_9aee63bd('java keizinan_cek\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    lapor_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in lapor_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in lapor_VALUE['java_cpu'], lapor_VALUE['java_cpu']
                받기(처음=처음)
                lapor_VALUE['after_exit_ps'] = cangkerang('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', lapor_VALUE['after_exit_ps'])
                lapor_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as rakan_VALUE:
                    Teks = cangkerang('java rangkaian_cek {} {}'.format(rakan_VALUE.TCP_port, rakan_VALUE.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Teks and 'exit 0' in Teks, Teks
                    assert rakan_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, rakan_VALUE.수신됨
                    assert not rakan_VALUE.오류들, rakan_VALUE.오류들
                    lapor_VALUE['outbound_peers'] = {종류: data.decode() for 종류, data in rakan_VALUE.수신됨.items()}
                처음 = len(LOG_baris)
                e_mel_9aee63bd('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as rakan_VALUE:
                    rakan_VALUE.sendall(b'A')
                    assert rakan_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as rakan_VALUE:
                    rakan_VALUE.settimeout(5)
                    rakan_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert rakan_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Teks = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Teks and 'exit 0' in Teks, Teks
                lapor_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in cangkerang('terminal')
                cangkerang('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_baris)
                e_mel_9aee63bd('java ContohTetingkap\n'.encode())
                받기('GUI 예제 Sediakan: ContohTetingkap\r\n'.encode(), 처음)
                처음 = len(LOG_baris)
                e_mel_9aee63bd(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                lapor_VALUE['suspended_java_ps'] = cangkerang('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java ContohTetingkap', lapor_VALUE['suspended_java_ps']), lapor_VALUE['suspended_java_ps']
                lapor_VALUE['top'] = cangkerang('top -n 1')
                assert 'java ContohTetingkap' in lapor_VALUE['top'] and 'kernel/shell' in lapor_VALUE['top']
                lapor_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                lapor_VALUE['network_trace'] = penghubung_VALUE.jejak_LOG
                assert not penghubung_VALUE.RALAT, penghubung_VALUE.RALAT
                e_mel_9aee63bd(b'poweroff\n')
                assert Proses_VALUE.wait(timeout=15) == 0
                lapor_VALUE['passed'] = True
            pilih_item.close()
    except Exception as RALAT:
        lapor_VALUE['error'] = str(RALAT)
        raise
    finally:
        if Proses_VALUE is not None and Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try:
                Proses_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proses_VALUE.kill()
                Proses_VALUE.wait()
        (출력 / 'serial.log').write_bytes(LOG_baris)
        (출력 / 'report.json').write_text(json.dumps(lapor_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Kunci_VALUE: lapor_VALUE[Kunci_VALUE] for Kunci_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Jalan()
