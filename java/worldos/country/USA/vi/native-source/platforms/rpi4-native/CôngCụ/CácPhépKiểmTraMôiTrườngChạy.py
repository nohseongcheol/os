#!/usr/bin/env python3
"""QEMU의 dữLiệuThựcTế CPU giáTrịQuyền, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from thựcThiLệnh import gốcCâyDựÁn, lệnh
from cầuNốiMạng import cầuNốiMạng
from MẫuThửVọngLại import MẫuThửVọngLại


def chạy():
    ĐầuRa = gốcCâyDựÁn / 'build/verification/execution-network-review'
    ĐầuRa.mkdir(parents=True, exist_ok=True)
    giáTrịBáoCáo = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((gốcCâyDựÁn / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    cácTệpNguồn = {
        'KiểmTraĐặcQuyền': '''public class KiểmTraĐặcQuyền {
 public static void main(String[] cácĐốiSố) {
  System.out.println("EL0_PROBE_READY");
  int trịSố = 0; while (true) { trịSố++; }
 }
}''',
        'KiểmTraMạng': '''import java.net.*;
public class KiểmTraMạng {
 public static void main(String[] cácĐốiSố) throws Exception {
  Socket nốiKết = new Socket("10.0.2.2", Integer.parseInt(cácĐốiSố[0]));
  nốiKết.setSoTimeout(3000);
  byte[] vănBản = "TCP 한글\\n".getBytes("UTF-8");
  nốiKết.getOutputStream().write(vănBản);
  for (int chỉSốVịTrí = 0; chỉSốVịTrí < vănBản.length; chỉSốVịTrí++)
   if (nốiKết.getInputStream().read() != (vănBản[chỉSốVịTrí] & 255)) throw new RuntimeException("TCP mismatch");
  nốiKết.close();
  DatagramSocket điểmCuối = new DatagramSocket(); điểmCuối.setSoTimeout(3000);
  vănBản = "UDP 한글".getBytes("UTF-8");
  điểmCuối.send(new DatagramPacket(vănBản, vănBản.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(cácĐốiSố[1])));
  byte[] lờiĐáp = new byte[64]; DatagramPacket điệnDữLiệu = new DatagramPacket(lờiĐáp, lờiĐáp.length);
  điểmCuối.receive(điệnDữLiệu);
  if (điệnDữLiệu.getLength() != vănBản.length) throw new RuntimeException("UDP length");
  for (int chỉSốVịTrí = 0; chỉSốVịTrí < vănBản.length; chỉSốVịTrí++)
   if (lờiĐáp[chỉSốVịTrí] != vănBản[chỉSốVịTrí]) throw new RuntimeException("UDP mismatch");
  điểmCuối.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'KiểmTraNhận': '''import java.net.*;
public class KiểmTraNhận {
 public static void main(String[] cácĐốiSố) throws Exception {
  ServerSocket giáTrịMáyChủ = new ServerSocket(9300); giáTrịMáyChủ.setSoTimeout(5000);
  DatagramSocket điểmCuối = new DatagramSocket(9301); điểmCuối.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket nốiKết = giáTrịMáyChủ.accept(); nốiKết.setSoTimeout(5000);
  nốiKết.getOutputStream().write(nốiKết.getInputStream().read() + 1);
  nốiKết.close(); giáTrịMáyChủ.close();
  byte[] DữLiệu = new byte[64]; DatagramPacket điệnDữLiệu = new DatagramPacket(DữLiệu, DữLiệu.length);
  điểmCuối.receive(điệnDữLiệu); điểmCuối.send(điệnDữLiệu); điểmCuối.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for tên, mãNguồn in cácTệpNguồn.items():
        (ĐầuRa / (tên + '.java')).write_text(mãNguồn, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ĐầuRa)] +
                          [str(ĐầuRa / (tên + '.java')) for tên in cácTệpNguồn])
    bảnGhiNhậtKý = bytearray()
    def sốCổngRỗng(loạiMụcKiểu=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, loạiMụcKiểu) as tìmKiếmGiáTrị:
            tìmKiếmGiáTrị.bind(('127.0.0.4', 0))
            return tìmKiếmGiáTrị.getsockname()[1]
    sốCổngTệp, cổngTCP, cổngUDP = sốCổngRỗng(), sốCổngRỗng(), sốCổngRỗng(socket.SOCK_DGRAM)
    giáTrịTiếnTrình = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as giáTrịTạm, cầuNốiMạng(
                sốCổngTệp, ['tcp:{}:9300'.format(cổngTCP), 'udp:{}:9301'.format(cổngUDP)],
                thuGiữ=True, địaChỉChủ='127.0.0.4') as giáTrịCầuNối:
            đườngDẫnĐiềuKhiển = Path(giáTrịTạm) / 'qmp.sock'
            giáTrịTiếnTrình = subprocess.Popen(lệnh() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(đườngDẫnĐiềuKhiển)] + giáTrịCầuNối.đốiSốĐãChuyểnTiếp(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            phầnMụcChọn = selectors.DefaultSelector()
            phầnMụcChọn.register(giáTrịTiếnTrình.stdout, selectors.EVENT_READ)
            def nhận(hiệnGiáTrị=b'jkoros-native> ', phầnMụcBanĐầu=0, giáTrịGiớiHạn=60):
                phầnKết = time.monotonic() + giáTrịGiớiHạn
                while hiệnGiáTrị not in bảnGhiNhậtKý[phầnMụcBanĐầu:]:
                    if time.monotonic() > phầnKết or giáTrịTiếnTrình.poll() is not None:
                        raise AssertionError('Missing ' + repr(hiệnGiáTrị) + '\n' + bảnGhiNhậtKý[phầnMụcBanĐầu:].decode('utf-8', 'replace'))
                    for giáTrịPhím, _ in phầnMụcChọn.select(.05):
                        giáTrịĐoạn = giáTrịPhím.fileobj.read(65536)
                        if giáTrịĐoạn:
                            bảnGhiNhậtKý.extend(giáTrịĐoạn)
                return bảnGhiNhậtKý[phầnMụcBanĐầu:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def gửi(DữLiệu):
                giáTrịTiếnTrình.stdin.write(DữLiệu)
                giáTrịTiếnTrình.stdin.flush()
            def vỏLệnh(vănBản):
                print(vănBản, flush=True)
                phầnMụcBanĐầu = len(bảnGhiNhậtKý)
                gửi((vănBản + '\n').encode())
                return nhận(phầnMụcBanĐầu=phầnMụcBanĐầu)
            nhận()
            with socket.socket(socket.AF_UNIX) as giáTrịĐiềuKhiển:
                giáTrịĐiềuKhiển.settimeout(10)
                giáTrịĐiềuKhiển.connect(str(đườngDẫnĐiềuKhiển))
                giáTrịLuồng = giáTrịĐiềuKhiển.makefile('rwb')
                json.loads(giáTrịLuồng.readline())
                def yêuCầu(giáTrịChỉLệnh, cácĐốiSố=None):
                    DữLiệu = {'execute': giáTrịChỉLệnh}
                    if cácĐốiSố is not None:
                        DữLiệu['arguments'] = cácĐốiSố
                    giáTrịLuồng.write((json.dumps(DữLiệu) + '\n').encode())
                    giáTrịLuồng.flush()
                    while True:
                        lờiĐáp = json.loads(giáTrịLuồng.readline())
                        if 'error' in lờiĐáp:
                            raise AssertionError(lờiĐáp)
                        if 'return' in lờiĐáp:
                            return lờiĐáp['return']
                yêuCầu('qmp_capabilities')
                def đọcQuyền():
                    yêuCầu('stop')
                    try:
                        return yêuCầu('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        yêuCầu('cont')
                giáTrịBáoCáo['shell_cpu'] = đọcQuyền()
                assert 'EL1h' in giáTrịBáoCáo['shell_cpu'], giáTrịBáoCáo['shell_cpu']
                giáTrịBáoCáo['initial_ps'] = vỏLệnh('ps')
                assert 'kernel/shell' in giáTrịBáoCáo['initial_ps']
                giáTrịBáoCáo['ipconfig'] = vỏLệnh('ipconfig')
                assert 'inet 10.0.2.15' in giáTrịBáoCáo['ipconfig']
                giáTrịBáoCáo['gateway_ping'] = vỏLệnh('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in giáTrịBáoCáo['gateway_ping']
                assert 'FTP listening' in vỏLệnh('ftpd start')
                with ftplib.FTP() as giáTrịChuyểnGiao:
                    giáTrịChuyểnGiao.encoding = 'utf-8'
                    giáTrịChuyểnGiao.connect('127.0.0.4', sốCổngTệp, timeout=20)
                    giáTrịChuyểnGiao.login()
                    for tên in cácTệpNguồn:
                        giáTrịChuyểnGiao.storbinary('STOR ' + tên + '.class', io.BytesIO((ĐầuRa / (tên + '.class')).read_bytes()))
                phầnMụcBanĐầu = len(bảnGhiNhậtKý)
                gửi('java KiểmTraĐặcQuyền\n'.encode())
                nhận(b'EL0_PROBE_READY\r\n', phầnMụcBanĐầu)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    giáTrịBáoCáo['java_cpu'] = đọcQuyền()
                    if 'EL0t' in giáTrịBáoCáo['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in giáTrịBáoCáo['java_cpu'], giáTrịBáoCáo['java_cpu']
                nhận(phầnMụcBanĐầu=phầnMụcBanĐầu)
                giáTrịBáoCáo['after_exit_ps'] = vỏLệnh('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', giáTrịBáoCáo['after_exit_ps'])
                giáTrịBáoCáo['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with MẫuThửVọngLại() as giáTrịĐốiTác:
                    vănBản = vỏLệnh('java KiểmTraMạng {} {}'.format(giáTrịĐốiTác.cổngTCP, giáTrịĐốiTác.cổngUDP))
                    assert 'OUTBOUND_TCP_UDP_PASS' in vănBản and 'exit 0' in vănBản, vănBản
                    assert giáTrịĐốiTác.cóĐãNhận == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, giáTrịĐốiTác.cóĐãNhận
                    assert not giáTrịĐốiTác.cácLỗi, giáTrịĐốiTác.cácLỗi
                    giáTrịBáoCáo['outbound_peers'] = {giáTrịLoại: DữLiệu.decode() for giáTrịLoại, DữLiệu in giáTrịĐốiTác.cóĐãNhận.items()}
                phầnMụcBanĐầu = len(bảnGhiNhậtKý)
                gửi('java KiểmTraNhận\n'.encode())
                nhận(b'INBOUND_READY\r\n', phầnMụcBanĐầu)
                with socket.create_connection(('127.0.0.4', cổngTCP), timeout=5) as giáTrịĐốiTác:
                    giáTrịĐốiTác.sendall(b'A')
                    assert giáTrịĐốiTác.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as giáTrịĐốiTác:
                    giáTrịĐốiTác.settimeout(5)
                    giáTrịĐốiTác.sendto(b'UDP-IN', ('127.0.0.4', cổngUDP))
                    assert giáTrịĐốiTác.recvfrom(64)[0] == b'UDP-IN'
                vănBản = nhận(phầnMụcBanĐầu=phầnMụcBanĐầu)
                assert 'INBOUND_TCP_UDP_PASS' in vănBản and 'exit 0' in vănBản, vănBản
                giáTrịBáoCáo['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in vỏLệnh('terminal')
                vỏLệnh('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                phầnMụcBanĐầu = len(bảnGhiNhậtKý)
                gửi('java VíDụCửaSổ\n'.encode())
                nhận('GUI VíDụ chuẩnBị: VíDụCửaSổ\r\n'.encode(), phầnMụcBanĐầu)
                phầnMụcBanĐầu = len(bảnGhiNhậtKý)
                gửi(bytes([30, 2, 1, 0, 0, 0, 0]))
                nhận(phầnMụcBanĐầu=phầnMụcBanĐầu)
                giáTrịBáoCáo['suspended_java_ps'] = vỏLệnh('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java VíDụCửaSổ', giáTrịBáoCáo['suspended_java_ps']), giáTrịBáoCáo['suspended_java_ps']
                giáTrịBáoCáo['top'] = vỏLệnh('top -n 1')
                assert 'java VíDụCửaSổ' in giáTrịBáoCáo['top'] and 'kernel/shell' in giáTrịBáoCáo['top']
                giáTrịBáoCáo['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                giáTrịBáoCáo['network_trace'] = giáTrịCầuNối.nhậtKýDấuVết
                assert not giáTrịCầuNối.lỗi, giáTrịCầuNối.lỗi
                gửi(b'poweroff\n')
                assert giáTrịTiếnTrình.wait(timeout=15) == 0
                giáTrịBáoCáo['passed'] = True
            phầnMụcChọn.close()
    except Exception as lỗi:
        giáTrịBáoCáo['error'] = str(lỗi)
        raise
    finally:
        if giáTrịTiếnTrình is not None and giáTrịTiếnTrình.poll() is None:
            giáTrịTiếnTrình.terminate()
            try:
                giáTrịTiếnTrình.wait(timeout=10)
            except subprocess.TimeoutExpired:
                giáTrịTiếnTrình.kill()
                giáTrịTiếnTrình.wait()
        (ĐầuRa / 'serial.log').write_bytes(bảnGhiNhậtKý)
        (ĐầuRa / 'report.json').write_text(json.dumps(giáTrịBáoCáo, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({giáTrịPhím: giáTrịBáoCáo[giáTrịPhím] for giáTrịPhím in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    chạy()
