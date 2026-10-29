#!/usr/bin/env python3
"""QEMU의 ค่าจริง_ข้อมูล CPU สิทธิ์_ค่า, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from ดําเนินการ_คําสั่ง import แสดง_ราก, คําสั่ง
from บริดจ์_3de4fe3a import บริดจ์_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def เรียกใช้งาน():
    ข้อความออก = แสดง_ราก / 'build/verification/execution-network-review'
    ข้อความออก.mkdir(parents=True, exist_ok=True)
    รายงาน_ค่า = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((แสดง_ราก / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    แหล่ง_ไฟล์ = {
        'สิทธิ์_เช็ค': '''public class สิทธิ์_เช็ค {
 public static void main(String[] อาร์กิวเมนต์) {
  System.out.println("EL0_PROBE_READY");
  int หมายเลข = 0; while (true) { หมายเลข++; }
 }
}''',
        'เครือข่าย_เช็ค': '''import java.net.*;
public class เครือข่าย_เช็ค {
 public static void main(String[] อาร์กิวเมนต์) throws Exception {
  Socket เชื่อมต่อ = new Socket("10.0.2.2", Integer.parseInt(อาร์กิวเมนต์[0]));
  เชื่อมต่อ.setSoTimeout(3000);
  byte[] ข้อความ = "TCP 한글\\n".getBytes("UTF-8");
  เชื่อมต่อ.getOutputStream().write(ข้อความ);
  for (int ดัชนีชี้ตําแหน่ง = 0; ดัชนีชี้ตําแหน่ง < ข้อความ.length; ดัชนีชี้ตําแหน่ง++)
   if (เชื่อมต่อ.getInputStream().read() != (ข้อความ[ดัชนีชี้ตําแหน่ง] & 255)) throw new RuntimeException("TCP mismatch");
  เชื่อมต่อ.close();
  DatagramSocket ปลายทาง = new DatagramSocket(); ปลายทาง.setSoTimeout(3000);
  ข้อความ = "UDP 한글".getBytes("UTF-8");
  ปลายทาง.send(new DatagramPacket(ข้อความ, ข้อความ.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(อาร์กิวเมนต์[1])));
  byte[] ตอบกลับ = new byte[64]; DatagramPacket เดตาแกรม = new DatagramPacket(ตอบกลับ, ตอบกลับ.length);
  ปลายทาง.receive(เดตาแกรม);
  if (เดตาแกรม.getLength() != ข้อความ.length) throw new RuntimeException("UDP length");
  for (int ดัชนีชี้ตําแหน่ง = 0; ดัชนีชี้ตําแหน่ง < ข้อความ.length; ดัชนีชี้ตําแหน่ง++)
   if (ตอบกลับ[ดัชนีชี้ตําแหน่ง] != ข้อความ[ดัชนีชี้ตําแหน่ง]) throw new RuntimeException("UDP mismatch");
  ปลายทาง.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'รับ_เช็ค': '''import java.net.*;
public class รับ_เช็ค {
 public static void main(String[] อาร์กิวเมนต์) throws Exception {
  ServerSocket เซิร์ฟเวอร์_ค่า = new ServerSocket(9300); เซิร์ฟเวอร์_ค่า.setSoTimeout(5000);
  DatagramSocket ปลายทาง = new DatagramSocket(9301); ปลายทาง.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket เชื่อมต่อ = เซิร์ฟเวอร์_ค่า.accept(); เชื่อมต่อ.setSoTimeout(5000);
  เชื่อมต่อ.getOutputStream().write(เชื่อมต่อ.getInputStream().read() + 1);
  เชื่อมต่อ.close(); เซิร์ฟเวอร์_ค่า.close();
  byte[] ข้อมูล = new byte[64]; DatagramPacket เดตาแกรม = new DatagramPacket(ข้อมูล, ข้อมูล.length);
  ปลายทาง.receive(เดตาแกรม); ปลายทาง.send(เดตาแกรม); ปลายทาง.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for ชื่อ, รหัสต้นฉบับ in แหล่ง_ไฟล์.items():
        (ข้อความออก / (ชื่อ + '.java')).write_text(รหัสต้นฉบับ, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ข้อความออก)] +
                          [str(ข้อความออก / (ชื่อ + '.java')) for ชื่อ in แหล่ง_ไฟล์])
    บันทึก_สถิติ = bytearray()
    def 빈접속번호(ชนิด_ประเภท=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, ชนิด_ประเภท) as ค้นหา_ค่า:
            ค้นหา_ค่า.bind(('127.0.0.4', 0))
            return ค้นหา_ค่า.getsockname()[1]
    แฟ้ม_หมายเลขพอร์ต, 연결접속번호, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    กระบวนการ_ค่า = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, บริดจ์_3de4fe3a(
                แฟ้ม_หมายเลขพอร์ต, ['tcp:{}:9300'.format(연결접속번호), 'udp:{}:9301'.format(전문접속번호)],
                จับ=True, โฮสต์_อีเมล='127.0.0.4') as บริดจ์_ค่า:
            ควบคุม_พาธ = Path(임시) / 'qmp.sock'
            กระบวนการ_ค่า = subprocess.Popen(คําสั่ง() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(ควบคุม_พาธ)] + บริดจ์_ค่า.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            เลือก_รายการ = selectors.DefaultSelector()
            เลือก_รายการ.register(กระบวนการ_ค่า.stdout, selectors.EVENT_READ)
            def รับ(แสดง_ค่า=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while แสดง_ค่า not in บันทึก_สถิติ[처음:]:
                    if time.monotonic() > 끝 or กระบวนการ_ค่า.poll() is not None:
                        raise AssertionError('Missing ' + repr(แสดง_ค่า) + '\n' + บันทึก_สถิติ[처음:].decode('utf-8', 'replace'))
                    for คีย์_ค่า, _ in เลือก_รายการ.select(.05):
                        조각 = คีย์_ค่า.fileobj.read(65536)
                        if 조각:
                            บันทึก_สถิติ.extend(조각)
                return บันทึก_สถิติ[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ส่ง(ข้อมูล):
                กระบวนการ_ค่า.stdin.write(ข้อมูล)
                กระบวนการ_ค่า.stdin.flush()
            def เชลล์(ข้อความ):
                print(ข้อความ, flush=True)
                처음 = len(บันทึก_สถิติ)
                ส่ง((ข้อความ + '\n').encode())
                return รับ(처음=처음)
            รับ()
            with socket.socket(socket.AF_UNIX) as ควบคุม_ค่า:
                ควบคุม_ค่า.settimeout(10)
                ควบคุม_ค่า.connect(str(ควบคุม_พาธ))
                สตรีม_ค่า = ควบคุม_ค่า.makefile('rwb')
                json.loads(สตรีม_ค่า.readline())
                def คําขอ(명령어, อาร์กิวเมนต์=None):
                    ข้อมูล = {'execute': 명령어}
                    if อาร์กิวเมนต์ is not None:
                        ข้อมูล['arguments'] = อาร์กิวเมนต์
                    สตรีม_ค่า.write((json.dumps(ข้อมูล) + '\n').encode())
                    สตรีม_ค่า.flush()
                    while True:
                        ตอบกลับ = json.loads(สตรีม_ค่า.readline())
                        if 'error' in ตอบกลับ:
                            raise AssertionError(ตอบกลับ)
                        if 'return' in ตอบกลับ:
                            return ตอบกลับ['return']
                คําขอ('qmp_capabilities')
                def 권한읽기():
                    คําขอ('stop')
                    try:
                        return คําขอ('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        คําขอ('cont')
                รายงาน_ค่า['shell_cpu'] = 권한읽기()
                assert 'EL1h' in รายงาน_ค่า['shell_cpu'], รายงาน_ค่า['shell_cpu']
                รายงาน_ค่า['initial_ps'] = เชลล์('ps')
                assert 'kernel/shell' in รายงาน_ค่า['initial_ps']
                รายงาน_ค่า['ipconfig'] = เชลล์('ipconfig')
                assert 'inet 10.0.2.15' in รายงาน_ค่า['ipconfig']
                รายงาน_ค่า['gateway_ping'] = เชลล์('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in รายงาน_ค่า['gateway_ping']
                assert 'FTP listening' in เชลล์('ftpd start')
                with ftplib.FTP() as โอน_ค่า:
                    โอน_ค่า.encoding = 'utf-8'
                    โอน_ค่า.connect('127.0.0.4', แฟ้ม_หมายเลขพอร์ต, timeout=20)
                    โอน_ค่า.login()
                    for ชื่อ in แหล่ง_ไฟล์:
                        โอน_ค่า.storbinary('STOR ' + ชื่อ + '.class', io.BytesIO((ข้อความออก / (ชื่อ + '.class')).read_bytes()))
                처음 = len(บันทึก_สถิติ)
                ส่ง('java สิทธิ์_เช็ค\n'.encode())
                รับ(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    รายงาน_ค่า['java_cpu'] = 권한읽기()
                    if 'EL0t' in รายงาน_ค่า['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in รายงาน_ค่า['java_cpu'], รายงาน_ค่า['java_cpu']
                รับ(처음=처음)
                รายงาน_ค่า['after_exit_ps'] = เชลล์('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', รายงาน_ค่า['after_exit_ps'])
                รายงาน_ค่า['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as ชั้น_ค่า:
                    ข้อความ = เชลล์('java เครือข่าย_เช็ค {} {}'.format(ชั้น_ค่า.연결접속번호, ชั้น_ค่า.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in ข้อความ and 'exit 0' in ข้อความ, ข้อความ
                    assert ชั้น_ค่า.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, ชั้น_ค่า.수신됨
                    assert not ชั้น_ค่า.오류들, ชั้น_ค่า.오류들
                    รายงาน_ค่า['outbound_peers'] = {종류: ข้อมูล.decode() for 종류, ข้อมูล in ชั้น_ค่า.수신됨.items()}
                처음 = len(บันทึก_สถิติ)
                ส่ง('java รับ_เช็ค\n'.encode())
                รับ(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', 연결접속번호), timeout=5) as ชั้น_ค่า:
                    ชั้น_ค่า.sendall(b'A')
                    assert ชั้น_ค่า.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ชั้น_ค่า:
                    ชั้น_ค่า.settimeout(5)
                    ชั้น_ค่า.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert ชั้น_ค่า.recvfrom(64)[0] == b'UDP-IN'
                ข้อความ = รับ(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in ข้อความ and 'exit 0' in ข้อความ, ข้อความ
                รายงาน_ค่า['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in เชลล์('terminal')
                เชลล์('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(บันทึก_สถิติ)
                ส่ง('java 창예제\n'.encode())
                รับ('GUI 예제 จัดเตรียม: 창예제\r\n'.encode(), 처음)
                처음 = len(บันทึก_สถิติ)
                ส่ง(bytes([30, 2, 1, 0, 0, 0, 0]))
                รับ(처음=처음)
                รายงาน_ค่า['suspended_java_ps'] = เชลล์('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', รายงาน_ค่า['suspended_java_ps']), รายงาน_ค่า['suspended_java_ps']
                รายงาน_ค่า['top'] = เชลล์('top -n 1')
                assert 'java 창예제' in รายงาน_ค่า['top'] and 'kernel/shell' in รายงาน_ค่า['top']
                รายงาน_ค่า['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                รายงาน_ค่า['network_trace'] = บริดจ์_ค่า.แฟ้มบันทึกการติดตาม
                assert not บริดจ์_ค่า.ข้อผิดพลาด, บริดจ์_ค่า.ข้อผิดพลาด
                ส่ง(b'poweroff\n')
                assert กระบวนการ_ค่า.wait(timeout=15) == 0
                รายงาน_ค่า['passed'] = True
            เลือก_รายการ.close()
    except Exception as ข้อผิดพลาด:
        รายงาน_ค่า['error'] = str(ข้อผิดพลาด)
        raise
    finally:
        if กระบวนการ_ค่า is not None and กระบวนการ_ค่า.poll() is None:
            กระบวนการ_ค่า.terminate()
            try:
                กระบวนการ_ค่า.wait(timeout=10)
            except subprocess.TimeoutExpired:
                กระบวนการ_ค่า.kill()
                กระบวนการ_ค่า.wait()
        (ข้อความออก / 'serial.log').write_bytes(บันทึก_สถิติ)
        (ข้อความออก / 'report.json').write_text(json.dumps(รายงาน_ค่า, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({คีย์_ค่า: รายงาน_ค่า[คีย์_ค่า] for คีย์_ค่า in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    เรียกใช้งาน()
