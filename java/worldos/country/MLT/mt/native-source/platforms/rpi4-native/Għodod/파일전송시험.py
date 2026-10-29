#!/usr/bin/env python3
"""Real host TCP client -> SLIP -> bare-metal lwIP -> FTP -> Java VFS."""
import ftplib
import hashlib
import io
import json
import selectors
import socket
import subprocess
import time
import zipfile
from netwerk_pont import netwerk_pont
from eżegwixxa_kmand import pprojetta_għerq, kmand
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def serje():
    miżura_data = pprojetta_għerq / 'build/verification/ftp'; miżura_data.mkdir(parents=True, exist_ok=True)
    validazzjoni_rapport = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((pprojetta_għerq / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = miżura_data / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { Malti.자체.출력.kiteb_linja("JAR eżegwixxa_kmand: " + 인수[0]); Malti.자체.fajl.kiteb("jar.txt", "자체 kernel_VALUE fajl"); Malti.자체.출력.kiteb_linja(Malti.자체.fajl.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(pprojetta_għerq/'build/java-library/classes'), '-d', str(miżura_data), str(자바원문)])
    Arkivju = io.BytesIO()
    with zipfile.ZipFile(Arkivju, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(miżura_data/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_Stream_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with netwerk_pont(접속번호, ['tcp:{}:9300'.format(server_Stream_port), 'udp:{}:9301'.format(서버전문접속번호)], iġbed=True) as pont:
        Proċess = subprocess.Popen(kmand() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + pont.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selettur = selectors.DefaultSelector(); selettur.register(Proċess.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            data = bytearray(); ttermina_OFFSET = time.monotonic() + 시간제한
            while 확인표시 not in data:
                if time.monotonic() > ttermina_OFFSET or Proċess.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + data.decode('utf-8', 'replace'))
                for 누름값, _ in selettur.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8', 'replace').replace('\r\n', '\n')
        def shell(linja):
            Proċess.stdin.write(linja.encode() + b'\n'); Proċess.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in shell('ftpd start')
            fajl_trasferiment_konnessjoni = ftplib.FTP(); fajl_trasferiment_konnessjoni.encoding = 'utf-8'; fajl_trasferiment_konnessjoni.connect('127.0.0.1', 접속번호, timeout=20); fajl_trasferiment_konnessjoni.login()
            payload_data = bytes(range(256)) * 32
            fajl_trasferiment_konnessjoni.storbinary('STOR binary.dat', io.BytesIO(payload_data))
            miżura = bytearray(); fajl_trasferiment_konnessjoni.retrbinary('RETR binary.dat', miżura.extend)
            assert miżura == payload_data; assert fajl_trasferiment_konnessjoni.size('binary.dat') == len(payload_data)
            validazzjoni_rapport['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            fajl_trasferiment_konnessjoni.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in shell('cat 한글.txt')
            assert '한글.txt' in fajl_trasferiment_konnessjoni.nlst()
            assert dict(fajl_trasferiment_konnessjoni.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            validazzjoni_rapport['checks'].append('UTF-8 filename and content visible in guest shell')
            try: fajl_trasferiment_konnessjoni.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            miżura = bytearray(); fajl_trasferiment_konnessjoni.retrbinary('RETR binary.dat', miżura.extend); assert miżura == payload_data
            validazzjoni_rapport['checks'].append('oversized replacement rejected; previous file preserved')
            with fajl_trasferiment_konnessjoni.transfercmd('STOR pending.txt') as tella_Fajls:
                # A control command must not change the active upload's destination.
                assert fajl_trasferiment_konnessjoni.size('binary.dat') == len(payload_data)
                tella_Fajls.sendall(b'UPLOAD TARGET PRESERVED')
            assert fajl_trasferiment_konnessjoni.voidresp().startswith('226')
            miżura = bytearray(); fajl_trasferiment_konnessjoni.retrbinary('RETR pending.txt', miżura.extend)
            assert miżura == b'UPLOAD TARGET PRESERVED'
            miżura = bytearray(); fajl_trasferiment_konnessjoni.retrbinary('RETR binary.dat', miżura.extend)
            assert miżura == payload_data
            fajl_trasferiment_konnessjoni.delete('pending.txt')
            validazzjoni_rapport['checks'].append('interleaved SIZE cannot change the active STOR destination')
            fajl_trasferiment_konnessjoni.storbinary('STOR 인사.jar', io.BytesIO(Arkivju.getvalue()))
            SMS = shell('java -jar 인사.jar 누리')
            assert 'JAR eżegwixxa_kmand: 누리' in SMS and '자체 kernel_VALUE fajl' in SMS and 'exit 0' in SMS, SMS
            SMS = shell('./인사.jar 세상')
            assert 'JAR eżegwixxa_kmand: 세상' in SMS and 'exit 0' in SMS, SMS
            validazzjoni_rapport['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct data { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct data VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = fetaħ_fajl("cc.txt", qari_kitba | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; kiteb_fajl_data(문서, 인사, sizeof(인사)-1); agħlaq_fajl(문서); kiteb_fajl_data(1, 인사, sizeof(인사)-1); return 0; }\n'
            fajl_trasferiment_konnessjoni.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            SMS = shell('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = shell('run 한글.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            assert 'CC NATIVE PASS' in shell('cat cc.txt')
            실행파일 = bytearray(); fajl_trasferiment_konnessjoni.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            fajl_trasferiment_konnessjoni.storbinary('STOR kkopja_VALUE.elf', io.BytesIO(실행파일)); SMS = shell('run kkopja_VALUE.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            fajl_trasferiment_konnessjoni.storbinary('STOR eżegwixxa_kmand', io.BytesIO(실행파일)); SMS=shell('./eżegwixxa_kmand');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            fajl_trasferiment_konnessjoni.storbinary('STOR isem.txt', io.BytesIO(실행파일)); SMS=shell('./isem.txt');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            shell('rm eżegwixxa_kmand isem.txt')
            validazzjoni_rapport['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            shell('rm binary.dat 한글.txt 한글.c 한글.elf kkopja_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(miżura_data/'linux-reference')
            fajl_trasferiment_konnessjoni.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            SMS=shell('./리눅스인사');assert 'exit -8' in SMS,SMS
            SMS=shell('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in SMS,SMS
            assert 'LINUX ELF FILE IO' in shell('cat linux.txt')
            fajl_trasferiment_konnessjoni.delete('리눅스인사');fajl_trasferiment_konnessjoni.delete('linux.txt')
            fajl_trasferiment_konnessjoni.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in shell('./FALSE_VALUE.elf');fajl_trasferiment_konnessjoni.delete('FALSE_VALUE.elf')
            validazzjoni_rapport['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = miżura_data/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket AQBAD = Malti.자체.연결통신.AQBAD("10.0.2.2", Integer.parseInt(args[0]));
 AQBAD.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] sors = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<sors.length;i++) if (AQBAD.getInputStream().read() != (sors[i]&255)) throw new RuntimeException("TCP mismatch");
 AQBAD.close();
 DatagramSocket 종단 = Malti.자체.통신.fetaħ(0); Malti.자체.통신.TIMEOUT(종단, 500);
 Malti.자체.통신.bagħat(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Malti.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(pprojetta_għerq/'build/java-library/classes'),'-d',str(miżura_data),str(통신원문)])
                fajl_trasferiment_konnessjoni.storbinary('STOR 바깥통신.class', io.BytesIO((miżura_data/'바깥통신.class').read_bytes()))
                SMS = shell('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_port, 되돌림서버항목.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in SMS and '10.0.2.2' in SMS and 'exit 0' in SMS, SMS
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            validazzjoni_rapport['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            fajl_trasferiment_konnessjoni.delete('바깥통신.class')
            server_sors=miżura_data/'서버시험.java'
            server_sors.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket mistieden_VALUE = server_VALUE.accept();
  mistieden_VALUE.getOutputStream().write(mistieden_VALUE.getInputStream().read()+1); mistieden_VALUE.close(); server_VALUE.close();
  byte[] Kontenut_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Kontenut_VALUE, Kontenut_VALUE.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(miżura_data),str(server_sors)])
            fajl_trasferiment_konnessjoni.storbinary('STOR 서버시험.class',io.BytesIO((miżura_data/'서버시험.class').read_bytes()))
            Proċess.stdin.write('java 서버시험\n'.encode());Proċess.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_Stream_port),timeout=5) as peer_VALUE:
                peer_VALUE.sendall(b'A');assert peer_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as peer_VALUE:
                peer_VALUE.settimeout(5);peer_VALUE.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert peer_VALUE.recvfrom(512)[0]==b'UDP-IN'
            SMS=수신하기();assert 'INBOUND TCP UDP PASS' in SMS and 'exit 0' in SMS,SMS
            validazzjoni_rapport['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            fajl_trasferiment_konnessjoni.delete('서버시험.class')
            istruzzjoni_SEQUENCE = 'public class 빛 { public static void main(String[] 인수) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } Malti.자체.출력.수쓰기(SUM_VALUE); Malti.자체.fajl.kiteb("aot.txt", "한글 AOT fajl 😀"); Malti.자체.출력.kiteb_linja(Malti.자체.fajl.읽기("aot.txt")); } }'
            fajl_trasferiment_konnessjoni.storbinary('STOR 빛.java', io.BytesIO(istruzzjoni_SEQUENCE.encode()))
            SMS = shell('javac 빛.java'); assert 'exit 0' in SMS and 'Compiled:' in SMS, SMS
            SMS = shell('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = shell('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT fajl 😀' in SMS and 'exit 0' in SMS, SMS
            자체실행파일 = bytearray(); fajl_trasferiment_konnessjoni.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            SMS = shell('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in SMS and 'unsupported' in SMS, SMS
            보존자료 = bytearray(); fajl_trasferiment_konnessjoni.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); fajl_trasferiment_konnessjoni.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            fajl_trasferiment_konnessjoni.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            SMS = shell('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = shell('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT fajl 😀' in SMS and 'exit 0' in SMS, SMS
            validazzjoni_rapport['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            validazzjoni_rapport['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statiku_sors=miżura_data/'정적시험.java'
            statiku_sors.write_text('''public class 정적시험 {
 static int pprojetta_għerq = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] 인수) {
  int[] VALUE = new int[] {pprojetta_għerq, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(miżura_data),str(statiku_sors)])
            fajl_trasferiment_konnessjoni.storbinary('STOR 정적시험.class',io.BytesIO((miżura_data/'정적시험.class').read_bytes()))
            SMS=shell('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in SMS,SMS
            SMS=shell('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in SMS,SMS
            fajl_trasferiment_konnessjoni.delete('정적시험.class');fajl_trasferiment_konnessjoni.delete('정적시험.elf')
            validazzjoni_rapport['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arkivju.getvalue());손상자료[14]^=1
            fajl_trasferiment_konnessjoni.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            SMS=shell('java -jar 인사.jar');assert 'Main-Class\nexit 1' in SMS,SMS
            validazzjoni_rapport['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            fajl_trasferiment_konnessjoni.quit(); assert 'FTP stopped' in shell('ftpd stop')
            assert not pont.żball, pont.żball
            validazzjoni_rapport.update(passed=True, frames_to_guest=pont.커널수신틀수, frames_from_guest=pont.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in selettur.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            pont.pause_avveniment.set()
            Proċess.terminate()
            try: Proċess.wait(timeout=5)
            except subprocess.TimeoutExpired: Proċess.kill(); Proċess.wait()
            selettur.close(); Proċess.stdin.close(); Proċess.stdout.close()
            validazzjoni_rapport['bridge_error'] = pont.żball
            validazzjoni_rapport['frames_to_guest'] = pont.커널수신틀수; validazzjoni_rapport['frames_from_guest'] = pont.커널발신틀수
            (miżura_data/'packets.json').write_text(json.dumps(pont.traċċar_LOG,indent=2)+'\n')
            (miżura_data / 'serial.log').write_bytes(대화기록)
            (miżura_data / 'report.json').write_text(json.dumps(validazzjoni_rapport, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': serje()
