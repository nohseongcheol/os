#!/usr/bin/env python3
"""QEMU의 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ CPU 권한, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import 기준, ᎤᏁᏤᎸᎩ
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def ᎠᎢᏎᏍᏗ():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    원문들 = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'ᏧᎾᏚᏓᎵ_ᎪᎯᏳᏔᏅ': '''import java.net.*;
public class ᏧᎾᏚᏓᎵ_ᎪᎯᏳᏔᏅ {
 public static void main(String[] 인수) throws Exception {
  Socket ᎫᏓᎳ = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  ᎫᏓᎳ.setSoTimeout(3000);
  byte[] ᎠᎪᎵᏰᏗ = "TCP 한글\\n".getBytes("UTF-8");
  ᎫᏓᎳ.getOutputStream().write(ᎠᎪᎵᏰᏗ);
  for (int 자리 = 0; 자리 < ᎠᎪᎵᏰᏗ.length; 자리++)
   if (ᎫᏓᎳ.getInputStream().read() != (ᎠᎪᎵᏰᏗ[자리] & 255)) throw new RuntimeException("TCP mismatch");
  ᎫᏓᎳ.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  ᎠᎪᎵᏰᏗ = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(ᎠᎪᎵᏰᏗ, ᎠᎪᎵᏰᏗ.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] 응답 = new byte[64]; DatagramPacket 전문 = new DatagramPacket(응답, 응답.length);
  종단.receive(전문);
  if (전문.getLength() != ᎠᎪᎵᏰᏗ.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < ᎠᎪᎵᏰᏗ.length; 자리++)
   if (응답[자리] != ᎠᎪᎵᏰᏗ[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ = new ServerSocket(9300); ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket ᎫᏓᎳ = ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.accept(); ᎫᏓᎳ.setSoTimeout(5000);
  ᎫᏓᎳ.getOutputStream().write(ᎫᏓᎳ.getInputStream().read() + 1);
  ᎫᏓᎳ.close(); ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.close();
  byte[] ᎦᏟᏌᏅᎯ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ᎦᏟᏌᏅᎯ, ᎦᏟᏌᏅᎯ.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for ᏚᏙᎥᎢ, ᎦᏟᏌᏅᎯ_0201f362 in 원문들.items():
        (출력 / (ᏚᏙᎥᎢ + '.java')).write_text(ᎦᏟᏌᏅᎯ_0201f362, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (ᏚᏙᎥᎢ + '.java')) for ᏚᏙᎥᎢ in 원문들])
    ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ = bytearray()
    def 빈접속번호(유형=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, 유형) as ᎠᏱᏍᏗ_ᏧᎬᏩᎶᏗᏯ:
            ᎠᏱᏍᏗ_ᏧᎬᏩᎶᏗᏯ.bind(('127.0.0.4', 0))
            return ᎠᏱᏍᏗ_ᏧᎬᏩᎶᏗᏯ.getsockname()[1]
    파일접속번호, TCP_ᎫᏓᎸᏗ, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                파일접속번호, ['tcp:{}:9300'.format(TCP_ᎫᏓᎸᏗ), 'udp:{}:9301'.format(전문접속번호)],
                포착여부=True, ᎠᏁᏢᏍᎩ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ='127.0.0.4') as 다리:
            ᎠᎯᎸᏍᏗ_ᎠᏍᏓᏩᏛᏍᏗ = Path(임시) / 'qmp.sock'
            ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ = subprocess.Popen(ᎤᏁᏤᎸᎩ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(ᎠᎯᎸᏍᏗ_ᎠᏍᏓᏩᏛᏍᏗ)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ᎭᏑᏯᎩ_ᏑᏓᎴᎩ_ᎪᏪᎸ = selectors.DefaultSelector()
            ᎭᏑᏯᎩ_ᏑᏓᎴᎩ_ᎪᏪᎸ.register(ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stdout, selectors.EVENT_READ)
            def 받기(ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ not in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[처음:]:
                    if time.monotonic() > 끝 or ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.poll() is not None:
                        raise AssertionError('Missing ' + repr(ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ) + '\n' + ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[처음:].decode('utf-8', 'replace'))
                    for ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ, _ in ᎭᏑᏯᎩ_ᏑᏓᎴᎩ_ᎪᏪᎸ.select(.05):
                        조각 = ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ.fileobj.read(65536)
                        if 조각:
                            ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.extend(조각)
                return ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ᏫᎦᏅᏗ(ᎦᏟᏌᏅᎯ):
                ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stdin.write(ᎦᏟᏌᏅᎯ)
                ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.stdin.flush()
            def ᎤᏯᏍᎦ(ᎠᎪᎵᏰᏗ):
                print(ᎠᎪᎵᏰᏗ, flush=True)
                처음 = len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                ᏫᎦᏅᏗ((ᎠᎪᎵᏰᏗ + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as ᎠᎯᎸᏍᏗ_ᏧᎬᏩᎶᏗᏯ:
                ᎠᎯᎸᏍᏗ_ᏧᎬᏩᎶᏗᏯ.settimeout(10)
                ᎠᎯᎸᏍᏗ_ᏧᎬᏩᎶᏗᏯ.connect(str(ᎠᎯᎸᏍᏗ_ᎠᏍᏓᏩᏛᏍᏗ))
                ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ = ᎠᎯᎸᏍᏗ_ᏧᎬᏩᎶᏗᏯ.makefile('rwb')
                json.loads(ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.readline())
                def 요청(ᏗᏕᏲᏗ_ᏧᎬᏩᎶᏗᏯ, 인수=None):
                    ᎦᏟᏌᏅᎯ = {'execute': ᏗᏕᏲᏗ_ᏧᎬᏩᎶᏗᏯ}
                    if 인수 is not None:
                        ᎦᏟᏌᏅᎯ['arguments'] = 인수
                    ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.write((json.dumps(ᎦᏟᏌᏅᎯ) + '\n').encode())
                    ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.flush()
                    while True:
                        응답 = json.loads(ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.readline())
                        if 'error' in 응답:
                            raise AssertionError(응답)
                        if 'return' in 응답:
                            return 응답['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['shell_cpu'] = 권한읽기()
                assert 'EL1h' in ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['shell_cpu'], ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['shell_cpu']
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['initial_ps'] = ᎤᏯᏍᎦ('ps')
                assert 'kernel/shell' in ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['initial_ps']
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['ipconfig'] = ᎤᏯᏍᎦ('ipconfig')
                assert 'inet 10.0.2.15' in ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['ipconfig']
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['gateway_ping'] = ᎤᏯᏍᎦ('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['gateway_ping']
                assert 'FTP listening' in ᎤᏯᏍᎦ('ftpd start')
                with ftplib.FTP() as ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ:
                    ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ.encoding = 'utf-8'
                    ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ.connect('127.0.0.4', 파일접속번호, timeout=20)
                    ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ.login()
                    for ᏚᏙᎥᎢ in 원문들:
                        ᎠᎲᏍᏗ_ᏧᎬᏩᎶᏗᏯ.storbinary('STOR ' + ᏚᏙᎥᎢ + '.class', io.BytesIO((출력 / (ᏚᏙᎥᎢ + '.class')).read_bytes()))
                처음 = len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                ᏫᎦᏅᏗ('java 권한점검\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['java_cpu'] = 권한읽기()
                    if 'EL0t' in ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['java_cpu'], ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['java_cpu']
                받기(처음=처음)
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['after_exit_ps'] = ᎤᏯᏍᎦ('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['after_exit_ps'])
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ:
                    ᎠᎪᎵᏰᏗ = ᎤᏯᏍᎦ('java ᏧᎾᏚᏓᎵ_ᎪᎯᏳᏔᏅ {} {}'.format(ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.TCP_ᎫᏓᎸᏗ, ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in ᎠᎪᎵᏰᏗ and 'exit 0' in ᎠᎪᎵᏰᏗ, ᎠᎪᎵᏰᏗ
                    assert ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.수신됨
                    assert not ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.오류들, ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.오류들
                    ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['outbound_peers'] = {종류: ᎦᏟᏌᏅᎯ.decode() for 종류, ᎦᏟᏌᏅᎯ in ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.수신됨.items()}
                처음 = len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                ᏫᎦᏅᏗ('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_ᎫᏓᎸᏗ), timeout=5) as ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ:
                    ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.sendall(b'A')
                    assert ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ:
                    ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.settimeout(5)
                    ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.recvfrom(64)[0] == b'UDP-IN'
                ᎠᎪᎵᏰᏗ = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in ᎠᎪᎵᏰᏗ and 'exit 0' in ᎠᎪᎵᏰᏗ, ᎠᎪᎵᏰᏗ
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in ᎤᏯᏍᎦ('terminal')
                ᎤᏯᏍᎦ('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                ᏫᎦᏅᏗ('java 창예제\n'.encode())
                받기('GUI 예제 ᎭᏛᏅᎢᏍᏓ: 창예제\r\n'.encode(), 처음)
                처음 = len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                ᏫᎦᏅᏗ(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['suspended_java_ps'] = ᎤᏯᏍᎦ('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['suspended_java_ps']), ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['suspended_java_ps']
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['top'] = ᎤᏯᏍᎦ('top -n 1')
                assert 'java 창예제' in ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['top'] and 'kernel/shell' in ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['top']
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['network_trace'] = 다리.추적기록
                assert not 다리.ᎦᎵᏓᏍᏔᏅ, 다리.ᎦᎵᏓᏍᏔᏅ
                ᏫᎦᏅᏗ(b'poweroff\n')
                assert ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait(timeout=15) == 0
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['passed'] = True
            ᎭᏑᏯᎩ_ᏑᏓᎴᎩ_ᎪᏪᎸ.close()
    except Exception as ᎦᎵᏓᏍᏔᏅ:
        ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['error'] = str(ᎦᎵᏓᏍᏔᏅ)
        raise
    finally:
        if ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ is not None and ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.poll() is None:
            ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.terminate()
            try:
                ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait(timeout=10)
            except subprocess.TimeoutExpired:
                ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.kill()
                ᎢᏯᏛᏁᎵᏓᏍᏗ_ᏧᎬᏩᎶᏗᏯ.wait()
        (출력 / 'serial.log').write_bytes(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
        (출력 / 'report.json').write_text(json.dumps(ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ: ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ[ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ] for ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ᎠᎢᏎᏍᏗ()
