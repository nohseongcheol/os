#!/usr/bin/env python3
"""QEMU의 aktual_data CPU izin_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Jalankan_perintah import Tugas_akar, perintah
from jaringan_bridge import jaringan_bridge
from 되돌림시험서버 import 되돌림시험서버


def jalankan():
    keluaranTeks = Tugas_akar / 'build/verification/execution-network-review'
    keluaranTeks.mkdir(parents=True, exist_ok=True)
    lapor_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Tugas_akar / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    sumber_File = {
        'izin_cek': '''public class izin_cek {
 public static void main(String[] argumen) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'jaringan_cek': '''import java.net.*;
public class jaringan_cek {
 public static void main(String[] argumen) throws Exception {
  Socket Sambung = new Socket("10.0.2.2", Integer.parseInt(argumen[0]));
  Sambung.setSoTimeout(3000);
  byte[] teks = "TCP 한글\\n".getBytes("UTF-8");
  Sambung.getOutputStream().write(teks);
  for (int posisi_INDEX = 0; posisi_INDEX < teks.length; posisi_INDEX++)
   if (Sambung.getInputStream().read() != (teks[posisi_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  Sambung.close();
  DatagramSocket peserta = new DatagramSocket(); peserta.setSoTimeout(3000);
  teks = "UDP 한글".getBytes("UTF-8");
  peserta.send(new DatagramPacket(teks, teks.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(argumen[1])));
  byte[] balas = new byte[64]; DatagramPacket 전문 = new DatagramPacket(balas, balas.length);
  peserta.receive(전문);
  if (전문.getLength() != teks.length) throw new RuntimeException("UDP length");
  for (int posisi_INDEX = 0; posisi_INDEX < teks.length; posisi_INDEX++)
   if (balas[posisi_INDEX] != teks[posisi_INDEX]) throw new RuntimeException("UDP mismatch");
  peserta.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'terima_cek': '''import java.net.*;
public class terima_cek {
 public static void main(String[] argumen) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); server_VALUE.setSoTimeout(5000);
  DatagramSocket peserta = new DatagramSocket(9301); peserta.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Sambung = server_VALUE.accept(); Sambung.setSoTimeout(5000);
  Sambung.getOutputStream().write(Sambung.getInputStream().read() + 1);
  Sambung.close(); server_VALUE.close();
  byte[] data = new byte[64]; DatagramPacket 전문 = new DatagramPacket(data, data.length);
  peserta.receive(전문); peserta.send(전문); peserta.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Nama_2, kodeSumber in sumber_File.items():
        (keluaranTeks / (Nama_2 + '.java')).write_text(kodeSumber, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(keluaranTeks)] +
                          [str(keluaranTeks / (Nama_2 + '.java')) for Nama_2 in sumber_File])
    LOG_baris = bytearray()
    def kosong_nomor_port(TYPE_area=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_area) as Cari_VALUE:
            Cari_VALUE.bind(('127.0.0.4', 0))
            return Cari_VALUE.getsockname()[1]
    file_nomor_port, TCP_port, UDP_port = kosong_nomor_port(), kosong_nomor_port(), kosong_nomor_port(socket.SOCK_DGRAM)
    Proses_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, jaringan_bridge(
                file_nomor_port, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(UDP_port)],
                ambil=True, host_surel='127.0.0.4') as bridge_VALUE:
            kontrol_jalur = Path(임시) / 'qmp.sock'
            Proses_VALUE = subprocess.Popen(perintah() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(kontrol_jalur)] + bridge_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            pilih_item = selectors.DefaultSelector()
            pilih_item.register(Proses_VALUE.stdout, selectors.EVENT_READ)
            def terima(show_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while show_VALUE not in LOG_baris[처음:]:
                    if time.monotonic() > 끝 or Proses_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(show_VALUE) + '\n' + LOG_baris[처음:].decode('utf-8', 'replace'))
                    for Kunci_VALUE, _ in pilih_item.select(.05):
                        조각 = Kunci_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_baris.extend(조각)
                return LOG_baris[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def kirim(data):
                Proses_VALUE.stdin.write(data)
                Proses_VALUE.stdin.flush()
            def shell(teks):
                print(teks, flush=True)
                처음 = len(LOG_baris)
                kirim((teks + '\n').encode())
                return terima(처음=처음)
            terima()
            with socket.socket(socket.AF_UNIX) as kontrol_VALUE:
                kontrol_VALUE.settimeout(10)
                kontrol_VALUE.connect(str(kontrol_jalur))
                Stream_VALUE = kontrol_VALUE.makefile('rwb')
                json.loads(Stream_VALUE.readline())
                def permintaan(instruksi_VALUE, argumen=None):
                    data = {'execute': instruksi_VALUE}
                    if argumen is not None:
                        data['arguments'] = argumen
                    Stream_VALUE.write((json.dumps(data) + '\n').encode())
                    Stream_VALUE.flush()
                    while True:
                        balas = json.loads(Stream_VALUE.readline())
                        if 'error' in balas:
                            raise AssertionError(balas)
                        if 'return' in balas:
                            return balas['return']
                permintaan('qmp_capabilities')
                def Izin_baca():
                    permintaan('stop')
                    try:
                        return permintaan('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        permintaan('cont')
                lapor_VALUE['shell_cpu'] = Izin_baca()
                assert 'EL1h' in lapor_VALUE['shell_cpu'], lapor_VALUE['shell_cpu']
                lapor_VALUE['initial_ps'] = shell('ps')
                assert 'kernel/shell' in lapor_VALUE['initial_ps']
                lapor_VALUE['ipconfig'] = shell('ipconfig')
                assert 'inet 10.0.2.15' in lapor_VALUE['ipconfig']
                lapor_VALUE['gateway_ping'] = shell('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in lapor_VALUE['gateway_ping']
                assert 'FTP listening' in shell('ftpd start')
                with ftplib.FTP() as Transfer_VALUE:
                    Transfer_VALUE.encoding = 'utf-8'
                    Transfer_VALUE.connect('127.0.0.4', file_nomor_port, timeout=20)
                    Transfer_VALUE.login()
                    for Nama_2 in sumber_File:
                        Transfer_VALUE.storbinary('STOR ' + Nama_2 + '.class', io.BytesIO((keluaranTeks / (Nama_2 + '.class')).read_bytes()))
                처음 = len(LOG_baris)
                kirim('java izin_cek\n'.encode())
                terima(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    lapor_VALUE['java_cpu'] = Izin_baca()
                    if 'EL0t' in lapor_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in lapor_VALUE['java_cpu'], lapor_VALUE['java_cpu']
                terima(처음=처음)
                lapor_VALUE['after_exit_ps'] = shell('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', lapor_VALUE['after_exit_ps'])
                lapor_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as serekan_VALUE:
                    teks = shell('java jaringan_cek {} {}'.format(serekan_VALUE.TCP_port, serekan_VALUE.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in teks and 'exit 0' in teks, teks
                    assert serekan_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, serekan_VALUE.수신됨
                    assert not serekan_VALUE.오류들, serekan_VALUE.오류들
                    lapor_VALUE['outbound_peers'] = {종류: data.decode() for 종류, data in serekan_VALUE.수신됨.items()}
                처음 = len(LOG_baris)
                kirim('java terima_cek\n'.encode())
                terima(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as serekan_VALUE:
                    serekan_VALUE.sendall(b'A')
                    assert serekan_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as serekan_VALUE:
                    serekan_VALUE.settimeout(5)
                    serekan_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert serekan_VALUE.recvfrom(64)[0] == b'UDP-IN'
                teks = terima(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in teks and 'exit 0' in teks, teks
                lapor_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in shell('terminal')
                shell('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_baris)
                kirim('java ContohJendela\n'.encode())
                terima('GUI 예제 Siapkan: ContohJendela\r\n'.encode(), 처음)
                처음 = len(LOG_baris)
                kirim(bytes([30, 2, 1, 0, 0, 0, 0]))
                terima(처음=처음)
                lapor_VALUE['suspended_java_ps'] = shell('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java ContohJendela', lapor_VALUE['suspended_java_ps']), lapor_VALUE['suspended_java_ps']
                lapor_VALUE['top'] = shell('top -n 1')
                assert 'java ContohJendela' in lapor_VALUE['top'] and 'kernel/shell' in lapor_VALUE['top']
                lapor_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                lapor_VALUE['network_trace'] = bridge_VALUE.log_jejak
                assert not bridge_VALUE.galat, bridge_VALUE.galat
                kirim(b'poweroff\n')
                assert Proses_VALUE.wait(timeout=15) == 0
                lapor_VALUE['passed'] = True
            pilih_item.close()
    except Exception as galat:
        lapor_VALUE['error'] = str(galat)
        raise
    finally:
        if Proses_VALUE is not None and Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try:
                Proses_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proses_VALUE.kill()
                Proses_VALUE.wait()
        (keluaranTeks / 'serial.log').write_bytes(LOG_baris)
        (keluaranTeks / 'report.json').write_text(json.dumps(lapor_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Kunci_VALUE: lapor_VALUE[Kunci_VALUE] for Kunci_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    jalankan()
