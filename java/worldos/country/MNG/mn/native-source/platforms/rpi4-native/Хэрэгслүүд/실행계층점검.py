#!/usr/bin/env python3
"""QEMU의 бодит_өгөгдөл CPU зөвшөөрөл_утга, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Гүйцэтгэх_команд import 기준, Тушаал
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def Ажиллуулах():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    тайлан_утга_ddf2aaf3 = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    эх_Файлууд = {
        'зөвшөөрөл_чек': '''public class зөвшөөрөл_чек {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Сүлжээ_чек': '''import java.net.*;
public class Сүлжээ_чек {
 public static void main(String[] 인수) throws Exception {
  Socket Холбох = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Холбох.setSoTimeout(3000);
  byte[] Бичвэр = "TCP 한글\\n".getBytes("UTF-8");
  Холбох.getOutputStream().write(Бичвэр);
  for (int 자리 = 0; 자리 < Бичвэр.length; 자리++)
   if (Холбох.getInputStream().read() != (Бичвэр[자리] & 255)) throw new RuntimeException("TCP mismatch");
  Холбох.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Бичвэр = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Бичвэр, Бичвэр.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] хариулах = new byte[64]; DatagramPacket 전문 = new DatagramPacket(хариулах, хариулах.length);
  종단.receive(전문);
  if (전문.getLength() != Бичвэр.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < Бичвэр.length; 자리++)
   if (хариулах[자리] != Бичвэр[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket сервер_утга = new ServerSocket(9300); сервер_утга.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Холбох = сервер_утга.accept(); Холбох.setSoTimeout(5000);
  Холбох.getOutputStream().write(Холбох.getInputStream().read() + 1);
  Холбох.close(); сервер_утга.close();
  byte[] өгөгдөл = new byte[64]; DatagramPacket 전문 = new DatagramPacket(өгөгдөл, өгөгдөл.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Нэр, ЭХ in эх_Файлууд.items():
        (출력 / (Нэр + '.java')).write_text(ЭХ, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Нэр + '.java')) for Нэр in эх_Файлууд])
    бичих_мөр_6e8b375a = bytearray()
    def 빈접속번호(бичих_ангилал=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, бичих_ангилал) as Хайх_утга:
            Хайх_утга.bind(('127.0.0.4', 0))
            return Хайх_утга.getsockname()[1]
    파일접속번호, Дамжууллын_хяналтын_протокол_порт, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    үйл_явц_утга = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                파일접속번호, ['tcp:{}:9300'.format(Дамжууллын_хяналтын_протокол_порт), 'udp:{}:9301'.format(전문접속번호)],
                авах=True, хост_хаяг='127.0.0.4') as 다리:
            хяналт_зам = Path(임시) / 'qmp.sock'
            үйл_явц_утга = subprocess.Popen(Тушаал() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(хяналт_зам)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            сонгох_зүйл = selectors.DefaultSelector()
            сонгох_зүйл.register(үйл_явц_утга.stdout, selectors.EVENT_READ)
            def 받기(үзүүлэх_утга=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while үзүүлэх_утга not in бичих_мөр_6e8b375a[처음:]:
                    if time.monotonic() > 끝 or үйл_явц_утга.poll() is not None:
                        raise AssertionError('Missing ' + repr(үзүүлэх_утга) + '\n' + бичих_мөр_6e8b375a[처음:].decode('utf-8', 'replace'))
                    for түлхүүр_утга, _ in сонгох_зүйл.select(.05):
                        조각 = түлхүүр_утга.fileobj.read(65536)
                        if 조각:
                            бичих_мөр_6e8b375a.extend(조각)
                return бичих_мөр_6e8b375a[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def илгээх(өгөгдөл):
                үйл_явц_утга.stdin.write(өгөгдөл)
                үйл_явц_утга.stdin.flush()
            def бүрхүүл(Бичвэр):
                print(Бичвэр, flush=True)
                처음 = len(бичих_мөр_6e8b375a)
                илгээх((Бичвэр + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as хяналт_утга:
                хяналт_утга.settimeout(10)
                хяналт_утга.connect(str(хяналт_зам))
                урсгал_утга = хяналт_утга.makefile('rwb')
                json.loads(урсгал_утга.readline())
                def 요청(заавар_утга, 인수=None):
                    өгөгдөл = {'execute': заавар_утга}
                    if 인수 is not None:
                        өгөгдөл['arguments'] = 인수
                    урсгал_утга.write((json.dumps(өгөгдөл) + '\n').encode())
                    урсгал_утга.flush()
                    while True:
                        хариулах = json.loads(урсгал_утга.readline())
                        if 'error' in хариулах:
                            raise AssertionError(хариулах)
                        if 'return' in хариулах:
                            return хариулах['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                тайлан_утга_ddf2aaf3['shell_cpu'] = 권한읽기()
                assert 'EL1h' in тайлан_утга_ddf2aaf3['shell_cpu'], тайлан_утга_ddf2aaf3['shell_cpu']
                тайлан_утга_ddf2aaf3['initial_ps'] = бүрхүүл('ps')
                assert 'kernel/shell' in тайлан_утга_ddf2aaf3['initial_ps']
                тайлан_утга_ddf2aaf3['ipconfig'] = бүрхүүл('ipconfig')
                assert 'inet 10.0.2.15' in тайлан_утга_ddf2aaf3['ipconfig']
                тайлан_утга_ddf2aaf3['gateway_ping'] = бүрхүүл('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in тайлан_утга_ddf2aaf3['gateway_ping']
                assert 'FTP listening' in бүрхүүл('ftpd start')
                with ftplib.FTP() as дамжуулах_утга:
                    дамжуулах_утга.encoding = 'utf-8'
                    дамжуулах_утга.connect('127.0.0.4', 파일접속번호, timeout=20)
                    дамжуулах_утга.login()
                    for Нэр in эх_Файлууд:
                        дамжуулах_утга.storbinary('STOR ' + Нэр + '.class', io.BytesIO((출력 / (Нэр + '.class')).read_bytes()))
                처음 = len(бичих_мөр_6e8b375a)
                илгээх('java зөвшөөрөл_чек\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    тайлан_утга_ddf2aaf3['java_cpu'] = 권한읽기()
                    if 'EL0t' in тайлан_утга_ddf2aaf3['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in тайлан_утга_ddf2aaf3['java_cpu'], тайлан_утга_ddf2aaf3['java_cpu']
                받기(처음=처음)
                тайлан_утга_ddf2aaf3['after_exit_ps'] = бүрхүүл('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', тайлан_утга_ddf2aaf3['after_exit_ps'])
                тайлан_утга_ddf2aaf3['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as ижил_түвшин_утга:
                    Бичвэр = бүрхүүл('java Сүлжээ_чек {} {}'.format(ижил_түвшин_утга.Дамжууллын_хяналтын_протокол_порт, ижил_түвшин_утга.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Бичвэр and 'exit 0' in Бичвэр, Бичвэр
                    assert ижил_түвшин_утга.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, ижил_түвшин_утга.수신됨
                    assert not ижил_түвшин_утга.오류들, ижил_түвшин_утга.오류들
                    тайлан_утга_ddf2aaf3['outbound_peers'] = {종류: өгөгдөл.decode() for 종류, өгөгдөл in ижил_түвшин_утга.수신됨.items()}
                처음 = len(бичих_мөр_6e8b375a)
                илгээх('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', Дамжууллын_хяналтын_протокол_порт), timeout=5) as ижил_түвшин_утга:
                    ижил_түвшин_утга.sendall(b'A')
                    assert ижил_түвшин_утга.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ижил_түвшин_утга:
                    ижил_түвшин_утга.settimeout(5)
                    ижил_түвшин_утга.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert ижил_түвшин_утга.recvfrom(64)[0] == b'UDP-IN'
                Бичвэр = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Бичвэр and 'exit 0' in Бичвэр, Бичвэр
                тайлан_утга_ddf2aaf3['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in бүрхүүл('terminal')
                бүрхүүл('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(бичих_мөр_6e8b375a)
                илгээх('java 창예제\n'.encode())
                받기('GUI 예제 Бэлтгэх: 창예제\r\n'.encode(), 처음)
                처음 = len(бичих_мөр_6e8b375a)
                илгээх(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                тайлан_утга_ddf2aaf3['suspended_java_ps'] = бүрхүүл('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', тайлан_утга_ddf2aaf3['suspended_java_ps']), тайлан_утга_ddf2aaf3['suspended_java_ps']
                тайлан_утга_ddf2aaf3['top'] = бүрхүүл('top -n 1')
                assert 'java 창예제' in тайлан_утга_ddf2aaf3['top'] and 'kernel/shell' in тайлан_утга_ddf2aaf3['top']
                тайлан_утга_ddf2aaf3['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                тайлан_утга_ddf2aaf3['network_trace'] = 다리.추적기록
                assert not 다리.Алдаа, 다리.Алдаа
                илгээх(b'poweroff\n')
                assert үйл_явц_утга.wait(timeout=15) == 0
                тайлан_утга_ddf2aaf3['passed'] = True
            сонгох_зүйл.close()
    except Exception as Алдаа:
        тайлан_утга_ddf2aaf3['error'] = str(Алдаа)
        raise
    finally:
        if үйл_явц_утга is not None and үйл_явц_утга.poll() is None:
            үйл_явц_утга.terminate()
            try:
                үйл_явц_утга.wait(timeout=10)
            except subprocess.TimeoutExpired:
                үйл_явц_утга.kill()
                үйл_явц_утга.wait()
        (출력 / 'serial.log').write_bytes(бичих_мөр_6e8b375a)
        (출력 / 'report.json').write_text(json.dumps(тайлан_утга_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({түлхүүр_утга: тайлан_утга_ddf2aaf3[түлхүүр_утга] for түлхүүр_утга in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Ажиллуулах()
