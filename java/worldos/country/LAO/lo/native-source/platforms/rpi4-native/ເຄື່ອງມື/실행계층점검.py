#!/usr/bin/env python3
"""QEMU의 ຕົວ_ຈິງ_ຂໍ້ມູນ CPU ການອະນຸຍາດ_ຄ່າ, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ, ຄໍາສັ່ງ_1f12b8e2
from ເຄືອຂ່າຍ_ຕົວເຊື່ອມ import ເຄືອຂ່າຍ_ຕົວເຊື່ອມ
from 되돌림시험서버 import 되돌림시험서버


def ແລ່ນ():
    출력 = ໂຄງ_ການ_ເລກຮາກ / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    ລາຍງານ_ຄ່າ = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    ແຫຼ່ງທີ່ມາ_ໄຟລ໌ = {
        'ການອະນຸຍາດ_ເຊັກເງິນ': '''public class ການອະນຸຍາດ_ເຊັກເງິນ {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'ເຄືອຂ່າຍ_ເຊັກເງິນ': '''import java.net.*;
public class ເຄືອຂ່າຍ_ເຊັກເງິນ {
 public static void main(String[] 인수) throws Exception {
  Socket ເຊື່ອມຕໍ່ = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  ເຊື່ອມຕໍ່.setSoTimeout(3000);
  byte[] ຂໍ້ຄວາມ = "TCP 한글\\n".getBytes("UTF-8");
  ເຊື່ອມຕໍ່.getOutputStream().write(ຂໍ້ຄວາມ);
  for (int ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ = 0; ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ < ຂໍ້ຄວາມ.length; ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ++)
   if (ເຊື່ອມຕໍ່.getInputStream().read() != (ຂໍ້ຄວາມ[ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ] & 255)) throw new RuntimeException("TCP mismatch");
  ເຊື່ອມຕໍ່.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  ຂໍ້ຄວາມ = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(ຂໍ້ຄວາມ, ຂໍ້ຄວາມ.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] ຕອບກັບ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ຕອບກັບ, ຕອບກັບ.length);
  종단.receive(전문);
  if (전문.getLength() != ຂໍ້ຄວາມ.length) throw new RuntimeException("UDP length");
  for (int ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ = 0; ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ < ຂໍ້ຄວາມ.length; ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ++)
   if (ຕອບກັບ[ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ] != ຂໍ້ຄວາມ[ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket 서버 = new ServerSocket(9300); 서버.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket ເຊື່ອມຕໍ່ = 서버.accept(); ເຊື່ອມຕໍ່.setSoTimeout(5000);
  ເຊື່ອມຕໍ່.getOutputStream().write(ເຊື່ອມຕໍ່.getInputStream().read() + 1);
  ເຊື່ອມຕໍ່.close(); 서버.close();
  byte[] ຂໍ້ມູນ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ຂໍ້ມູນ, ຂໍ້ມູນ.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for ຊື່, ແຫຼ່ງທີ່ມາ in ແຫຼ່ງທີ່ມາ_ໄຟລ໌.items():
        (출력 / (ຊື່ + '.java')).write_text(ແຫຼ່ງທີ່ມາ, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (ຊື່ + '.java')) for ຊື່ in ແຫຼ່ງທີ່ມາ_ໄຟລ໌])
    ບັນທຶກ_ແຖວ = bytearray()
    def ຫວ່າງ_ເປົ່າ_ຫມາຍເລກພອດ(ພິມ_ຫມວດ=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, ພິມ_ຫມວດ) as ຊອກຫາ_ຄ່າ:
            ຊອກຫາ_ຄ່າ.bind(('127.0.0.4', 0))
            return ຊອກຫາ_ຄ່າ.getsockname()[1]
    ຟາຍ_ຫມາຍເລກພອດ, ທີຊີພີ_ຜອດ, ຢູດີພີ_ຜອດ = ຫວ່າງ_ເປົ່າ_ຫມາຍເລກພອດ(), ຫວ່າງ_ເປົ່າ_ຫມາຍເລກພອດ(), ຫວ່າງ_ເປົ່າ_ຫມາຍເລກພອດ(socket.SOCK_DGRAM)
    ຂະ_ບວນ_ການ_ຄ່າ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, ເຄືອຂ່າຍ_ຕົວເຊື່ອມ(
                ຟາຍ_ຫມາຍເລກພອດ, ['tcp:{}:9300'.format(ທີຊີພີ_ຜອດ), 'udp:{}:9301'.format(ຢູດີພີ_ຜອດ)],
                ບັນທຶກ_ba7b8054=True, ໂຮສ_ອີເມວ='127.0.0.4') as ຕົວເຊື່ອມ_ຄ່າ:
            ຄວບຄຸມ_ທາງໂຄຈອນ = Path(임시) / 'qmp.sock'
            ຂະ_ບວນ_ການ_ຄ່າ = subprocess.Popen(ຄໍາສັ່ງ_1f12b8e2() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(ຄວບຄຸມ_ທາງໂຄຈອນ)] + ຕົວເຊື່ອມ_ຄ່າ.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ເລືອກ_ລາຍການ = selectors.DefaultSelector()
            ເລືອກ_ລາຍການ.register(ຂະ_ບວນ_ການ_ຄ່າ.stdout, selectors.EVENT_READ)
            def 받기(ລາຍການ_ຄ່າ=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ລາຍການ_ຄ່າ not in ບັນທຶກ_ແຖວ[처음:]:
                    if time.monotonic() > 끝 or ຂະ_ບວນ_ການ_ຄ່າ.poll() is not None:
                        raise AssertionError('Missing ' + repr(ລາຍການ_ຄ່າ) + '\n' + ບັນທຶກ_ແຖວ[처음:].decode('utf-8', 'replace'))
                    for ກະແຈ_ຄ່າ, _ in ເລືອກ_ລາຍການ.select(.05):
                        조각 = ກະແຈ_ຄ່າ.fileobj.read(65536)
                        if 조각:
                            ບັນທຶກ_ແຖວ.extend(조각)
                return ບັນທຶກ_ແຖວ[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ສົ່ງ(ຂໍ້ມູນ):
                ຂະ_ບວນ_ການ_ຄ່າ.stdin.write(ຂໍ້ມູນ)
                ຂະ_ບວນ_ການ_ຄ່າ.stdin.flush()
            def ເຊລ(ຂໍ້ຄວາມ):
                print(ຂໍ້ຄວາມ, flush=True)
                처음 = len(ບັນທຶກ_ແຖວ)
                ສົ່ງ((ຂໍ້ຄວາມ + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as ຄວບຄຸມ_ຄ່າ:
                ຄວບຄຸມ_ຄ່າ.settimeout(10)
                ຄວບຄຸມ_ຄ່າ.connect(str(ຄວບຄຸມ_ທາງໂຄຈອນ))
                ສະຕຣີມ_ຄ່າ = ຄວບຄຸມ_ຄ່າ.makefile('rwb')
                json.loads(ສະຕຣີມ_ຄ່າ.readline())
                def 요청(ຄໍາແນະນໍາ_ຄ່າ, 인수=None):
                    ຂໍ້ມູນ = {'execute': ຄໍາແນະນໍາ_ຄ່າ}
                    if 인수 is not None:
                        ຂໍ້ມູນ['arguments'] = 인수
                    ສະຕຣີມ_ຄ່າ.write((json.dumps(ຂໍ້ມູນ) + '\n').encode())
                    ສະຕຣີມ_ຄ່າ.flush()
                    while True:
                        ຕອບກັບ = json.loads(ສະຕຣີມ_ຄ່າ.readline())
                        if 'error' in ຕອບກັບ:
                            raise AssertionError(ຕອບກັບ)
                        if 'return' in ຕອບກັບ:
                            return ຕອບກັບ['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                ລາຍງານ_ຄ່າ['shell_cpu'] = 권한읽기()
                assert 'EL1h' in ລາຍງານ_ຄ່າ['shell_cpu'], ລາຍງານ_ຄ່າ['shell_cpu']
                ລາຍງານ_ຄ່າ['initial_ps'] = ເຊລ('ps')
                assert 'kernel/shell' in ລາຍງານ_ຄ່າ['initial_ps']
                ລາຍງານ_ຄ່າ['ipconfig'] = ເຊລ('ipconfig')
                assert 'inet 10.0.2.15' in ລາຍງານ_ຄ່າ['ipconfig']
                ລາຍງານ_ຄ່າ['gateway_ping'] = ເຊລ('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in ລາຍງານ_ຄ່າ['gateway_ping']
                assert 'FTP listening' in ເຊລ('ftpd start')
                with ftplib.FTP() as ໂອນ_ຄ່າ:
                    ໂອນ_ຄ່າ.encoding = 'utf-8'
                    ໂອນ_ຄ່າ.connect('127.0.0.4', ຟາຍ_ຫມາຍເລກພອດ, timeout=20)
                    ໂອນ_ຄ່າ.login()
                    for ຊື່ in ແຫຼ່ງທີ່ມາ_ໄຟລ໌:
                        ໂອນ_ຄ່າ.storbinary('STOR ' + ຊື່ + '.class', io.BytesIO((출력 / (ຊື່ + '.class')).read_bytes()))
                처음 = len(ບັນທຶກ_ແຖວ)
                ສົ່ງ('java ການອະນຸຍາດ_ເຊັກເງິນ\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    ລາຍງານ_ຄ່າ['java_cpu'] = 권한읽기()
                    if 'EL0t' in ລາຍງານ_ຄ່າ['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in ລາຍງານ_ຄ່າ['java_cpu'], ລາຍງານ_ຄ່າ['java_cpu']
                받기(처음=처음)
                ລາຍງານ_ຄ່າ['after_exit_ps'] = ເຊລ('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', ລາຍງານ_ຄ່າ['after_exit_ps'])
                ລາຍງານ_ຄ່າ['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as ລຸ້ນດຽວກັນ_ຄ່າ:
                    ຂໍ້ຄວາມ = ເຊລ('java ເຄືອຂ່າຍ_ເຊັກເງິນ {} {}'.format(ລຸ້ນດຽວກັນ_ຄ່າ.ທີຊີພີ_ຜອດ, ລຸ້ນດຽວກັນ_ຄ່າ.ຢູດີພີ_ຜອດ))
                    assert 'OUTBOUND_TCP_UDP_PASS' in ຂໍ້ຄວາມ and 'exit 0' in ຂໍ້ຄວາມ, ຂໍ້ຄວາມ
                    assert ລຸ້ນດຽວກັນ_ຄ່າ.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, ລຸ້ນດຽວກັນ_ຄ່າ.수신됨
                    assert not ລຸ້ນດຽວກັນ_ຄ່າ.오류들, ລຸ້ນດຽວກັນ_ຄ່າ.오류들
                    ລາຍງານ_ຄ່າ['outbound_peers'] = {종류: ຂໍ້ມູນ.decode() for 종류, ຂໍ້ມູນ in ລຸ້ນດຽວກັນ_ຄ່າ.수신됨.items()}
                처음 = len(ບັນທຶກ_ແຖວ)
                ສົ່ງ('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', ທີຊີພີ_ຜອດ), timeout=5) as ລຸ້ນດຽວກັນ_ຄ່າ:
                    ລຸ້ນດຽວກັນ_ຄ່າ.sendall(b'A')
                    assert ລຸ້ນດຽວກັນ_ຄ່າ.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ລຸ້ນດຽວກັນ_ຄ່າ:
                    ລຸ້ນດຽວກັນ_ຄ່າ.settimeout(5)
                    ລຸ້ນດຽວກັນ_ຄ່າ.sendto(b'UDP-IN', ('127.0.0.4', ຢູດີພີ_ຜອດ))
                    assert ລຸ້ນດຽວກັນ_ຄ່າ.recvfrom(64)[0] == b'UDP-IN'
                ຂໍ້ຄວາມ = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in ຂໍ້ຄວາມ and 'exit 0' in ຂໍ້ຄວາມ, ຂໍ້ຄວາມ
                ລາຍງານ_ຄ່າ['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in ເຊລ('terminal')
                ເຊລ('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(ບັນທຶກ_ແຖວ)
                ສົ່ງ('java 창예제\n'.encode())
                받기('GUI 예제 ກະ_ກຽມ: 창예제\r\n'.encode(), 처음)
                처음 = len(ບັນທຶກ_ແຖວ)
                ສົ່ງ(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                ລາຍງານ_ຄ່າ['suspended_java_ps'] = ເຊລ('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', ລາຍງານ_ຄ່າ['suspended_java_ps']), ລາຍງານ_ຄ່າ['suspended_java_ps']
                ລາຍງານ_ຄ່າ['top'] = ເຊລ('top -n 1')
                assert 'java 창예제' in ລາຍງານ_ຄ່າ['top'] and 'kernel/shell' in ລາຍງານ_ຄ່າ['top']
                ລາຍງານ_ຄ່າ['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                ລາຍງານ_ຄ່າ['network_trace'] = ຕົວເຊື່ອມ_ຄ່າ.추적기록
                assert not ຕົວເຊື່ອມ_ຄ່າ.ຂໍ້ຜິດພາດ, ຕົວເຊື່ອມ_ຄ່າ.ຂໍ້ຜິດພາດ
                ສົ່ງ(b'poweroff\n')
                assert ຂະ_ບວນ_ການ_ຄ່າ.wait(timeout=15) == 0
                ລາຍງານ_ຄ່າ['passed'] = True
            ເລືອກ_ລາຍການ.close()
    except Exception as ຂໍ້ຜິດພາດ:
        ລາຍງານ_ຄ່າ['error'] = str(ຂໍ້ຜິດພາດ)
        raise
    finally:
        if ຂະ_ບວນ_ການ_ຄ່າ is not None and ຂະ_ບວນ_ການ_ຄ່າ.poll() is None:
            ຂະ_ບວນ_ການ_ຄ່າ.terminate()
            try:
                ຂະ_ບວນ_ການ_ຄ່າ.wait(timeout=10)
            except subprocess.TimeoutExpired:
                ຂະ_ບວນ_ການ_ຄ່າ.kill()
                ຂະ_ບວນ_ການ_ຄ່າ.wait()
        (출력 / 'serial.log').write_bytes(ບັນທຶກ_ແຖວ)
        (출력 / 'report.json').write_text(json.dumps(ລາຍງານ_ຄ່າ, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({ກະແຈ_ຄ່າ: ລາຍງານ_ຄ່າ[ກະແຈ_ຄ່າ] for ກະແຈ_ຄ່າ in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ແລ່ນ()
