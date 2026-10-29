#!/usr/bin/env python3
"""QEMU의 fiili_veri CPU izin_değer, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from yürütmek_komut import işlem_kök, komut
from köprü_3de4fe3a import köprü_3de4fe3a
from yankı_düzen import yankı_düzen


def çalıştır():
    metinÇıktısı = işlem_kök / 'build/verification/execution-network-review'
    metinÇıktısı.mkdir(parents=True, exist_ok=True)
    Rapor_değer = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((işlem_kök / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    kaynak_Dosyalar = {
        'izin_çek': '''public class izin_çek {
 public static void main(String[] bağımsız_değişkenler) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'ağ_çek': '''import java.net.*;
public class ağ_çek {
 public static void main(String[] bağımsız_değişkenler) throws Exception {
  Socket Bağlan = new Socket("10.0.2.2", Integer.parseInt(bağımsız_değişkenler[0]));
  Bağlan.setSoTimeout(3000);
  byte[] metin = "TCP 한글\\n".getBytes("UTF-8");
  Bağlan.getOutputStream().write(metin);
  for (int konum_dizini = 0; konum_dizini < metin.length; konum_dizini++)
   if (Bağlan.getInputStream().read() != (metin[konum_dizini] & 255)) throw new RuntimeException("TCP mismatch");
  Bağlan.close();
  DatagramSocket uç_nokta = new DatagramSocket(); uç_nokta.setSoTimeout(3000);
  metin = "UDP 한글".getBytes("UTF-8");
  uç_nokta.send(new DatagramPacket(metin, metin.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(bağımsız_değişkenler[1])));
  byte[] yanıt = new byte[64]; DatagramPacket veri_birimi = new DatagramPacket(yanıt, yanıt.length);
  uç_nokta.receive(veri_birimi);
  if (veri_birimi.getLength() != metin.length) throw new RuntimeException("UDP length");
  for (int konum_dizini = 0; konum_dizini < metin.length; konum_dizini++)
   if (yanıt[konum_dizini] != metin[konum_dizini]) throw new RuntimeException("UDP mismatch");
  uç_nokta.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'almak_çek': '''import java.net.*;
public class almak_çek {
 public static void main(String[] bağımsız_değişkenler) throws Exception {
  ServerSocket sunucu_değer = new ServerSocket(9300); sunucu_değer.setSoTimeout(5000);
  DatagramSocket uç_nokta = new DatagramSocket(9301); uç_nokta.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Bağlan = sunucu_değer.accept(); Bağlan.setSoTimeout(5000);
  Bağlan.getOutputStream().write(Bağlan.getInputStream().read() + 1);
  Bağlan.close(); sunucu_değer.close();
  byte[] veri = new byte[64]; DatagramPacket veri_birimi = new DatagramPacket(veri, veri.length);
  uç_nokta.receive(veri_birimi); uç_nokta.send(veri_birimi); uç_nokta.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for İsim, kaynakKod in kaynak_Dosyalar.items():
        (metinÇıktısı / (İsim + '.java')).write_text(kaynakKod, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(metinÇıktısı)] +
                          [str(metinÇıktısı / (İsim + '.java')) for İsim in kaynak_Dosyalar])
    LOG_KAYIT = bytearray()
    def boş_bağlantı_noktası_numarası(TÜR_alan=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TÜR_alan) as Ara_değer:
            Ara_değer.bind(('127.0.0.4', 0))
            return Ara_değer.getsockname()[1]
    Dosya_bağlantı_noktası_numarası, TCP_bağlantı_noktası, UDP_taşımak = boş_bağlantı_noktası_numarası(), boş_bağlantı_noktası_numarası(), boş_bağlantı_noktası_numarası(socket.SOCK_DGRAM)
    işlem_değer = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, köprü_3de4fe3a(
                Dosya_bağlantı_noktası_numarası, ['tcp:{}:9300'.format(TCP_bağlantı_noktası), 'udp:{}:9301'.format(UDP_taşımak)],
                çekmek=True, konak_ADRES='127.0.0.4') as köprü_değer_982037b1:
            denetim_yol = Path(임시) / 'qmp.sock'
            işlem_değer = subprocess.Popen(komut() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(denetim_yol)] + köprü_değer_982037b1.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ELEMAN_öğe = selectors.DefaultSelector()
            ELEMAN_öğe.register(işlem_değer.stdout, selectors.EVENT_READ)
            def almak(şov_değer=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while şov_değer not in LOG_KAYIT[처음:]:
                    if time.monotonic() > 끝 or işlem_değer.poll() is not None:
                        raise AssertionError('Missing ' + repr(şov_değer) + '\n' + LOG_KAYIT[처음:].decode('utf-8', 'replace'))
                    for tuş_değer, _ in ELEMAN_öğe.select(.05):
                        parça_değer = tuş_değer.fileobj.read(65536)
                        if parça_değer:
                            LOG_KAYIT.extend(parça_değer)
                return LOG_KAYIT[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def göndermek(veri):
                işlem_değer.stdin.write(veri)
                işlem_değer.stdin.flush()
            def kabuk(metin):
                print(metin, flush=True)
                처음 = len(LOG_KAYIT)
                göndermek((metin + '\n').encode())
                return almak(처음=처음)
            almak()
            with socket.socket(socket.AF_UNIX) as denetim_değer:
                denetim_değer.settimeout(10)
                denetim_değer.connect(str(denetim_yol))
                akış_değer = denetim_değer.makefile('rwb')
                json.loads(akış_değer.readline())
                def istek(명령어, bağımsız_değişkenler=None):
                    veri = {'execute': 명령어}
                    if bağımsız_değişkenler is not None:
                        veri['arguments'] = bağımsız_değişkenler
                    akış_değer.write((json.dumps(veri) + '\n').encode())
                    akış_değer.flush()
                    while True:
                        yanıt = json.loads(akış_değer.readline())
                        if 'error' in yanıt:
                            raise AssertionError(yanıt)
                        if 'return' in yanıt:
                            return yanıt['return']
                istek('qmp_capabilities')
                def 권한읽기():
                    istek('stop')
                    try:
                        return istek('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        istek('cont')
                Rapor_değer['shell_cpu'] = 권한읽기()
                assert 'EL1h' in Rapor_değer['shell_cpu'], Rapor_değer['shell_cpu']
                Rapor_değer['initial_ps'] = kabuk('ps')
                assert 'kernel/shell' in Rapor_değer['initial_ps']
                Rapor_değer['ipconfig'] = kabuk('ipconfig')
                assert 'inet 10.0.2.15' in Rapor_değer['ipconfig']
                Rapor_değer['gateway_ping'] = kabuk('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in Rapor_değer['gateway_ping']
                assert 'FTP listening' in kabuk('ftpd start')
                with ftplib.FTP() as devir_değer:
                    devir_değer.encoding = 'utf-8'
                    devir_değer.connect('127.0.0.4', Dosya_bağlantı_noktası_numarası, timeout=20)
                    devir_değer.login()
                    for İsim in kaynak_Dosyalar:
                        devir_değer.storbinary('STOR ' + İsim + '.class', io.BytesIO((metinÇıktısı / (İsim + '.class')).read_bytes()))
                처음 = len(LOG_KAYIT)
                göndermek('java izin_çek\n'.encode())
                almak(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    Rapor_değer['java_cpu'] = 권한읽기()
                    if 'EL0t' in Rapor_değer['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in Rapor_değer['java_cpu'], Rapor_değer['java_cpu']
                almak(처음=처음)
                Rapor_değer['after_exit_ps'] = kabuk('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', Rapor_değer['after_exit_ps'])
                Rapor_değer['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with yankı_düzen() as eş_değer:
                    metin = kabuk('java ağ_çek {} {}'.format(eş_değer.TCP_bağlantı_noktası, eş_değer.UDP_taşımak))
                    assert 'OUTBOUND_TCP_UDP_PASS' in metin and 'exit 0' in metin, metin
                    assert eş_değer.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, eş_değer.수신됨
                    assert not eş_değer.오류들, eş_değer.오류들
                    Rapor_değer['outbound_peers'] = {Tip_değer: veri.decode() for Tip_değer, veri in eş_değer.수신됨.items()}
                처음 = len(LOG_KAYIT)
                göndermek('java almak_çek\n'.encode())
                almak(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_bağlantı_noktası), timeout=5) as eş_değer:
                    eş_değer.sendall(b'A')
                    assert eş_değer.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as eş_değer:
                    eş_değer.settimeout(5)
                    eş_değer.sendto(b'UDP-IN', ('127.0.0.4', UDP_taşımak))
                    assert eş_değer.recvfrom(64)[0] == b'UDP-IN'
                metin = almak(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in metin and 'exit 0' in metin, metin
                Rapor_değer['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in kabuk('terminal')
                kabuk('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_KAYIT)
                göndermek('java PencereÖrneği\n'.encode())
                almak('GUI 예제 Hazırlan: PencereÖrneği\r\n'.encode(), 처음)
                처음 = len(LOG_KAYIT)
                göndermek(bytes([30, 2, 1, 0, 0, 0, 0]))
                almak(처음=처음)
                Rapor_değer['suspended_java_ps'] = kabuk('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java PencereÖrneği', Rapor_değer['suspended_java_ps']), Rapor_değer['suspended_java_ps']
                Rapor_değer['top'] = kabuk('top -n 1')
                assert 'java PencereÖrneği' in Rapor_değer['top'] and 'kernel/shell' in Rapor_değer['top']
                Rapor_değer['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                Rapor_değer['network_trace'] = köprü_değer_982037b1.izleme_günlüğü
                assert not köprü_değer_982037b1.hata, köprü_değer_982037b1.hata
                göndermek(b'poweroff\n')
                assert işlem_değer.wait(timeout=15) == 0
                Rapor_değer['passed'] = True
            ELEMAN_öğe.close()
    except Exception as hata:
        Rapor_değer['error'] = str(hata)
        raise
    finally:
        if işlem_değer is not None and işlem_değer.poll() is None:
            işlem_değer.terminate()
            try:
                işlem_değer.wait(timeout=10)
            except subprocess.TimeoutExpired:
                işlem_değer.kill()
                işlem_değer.wait()
        (metinÇıktısı / 'serial.log').write_bytes(LOG_KAYIT)
        (metinÇıktısı / 'report.json').write_text(json.dumps(Rapor_değer, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({tuş_değer: Rapor_değer[tuş_değer] for tuş_değer in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    çalıştır()
