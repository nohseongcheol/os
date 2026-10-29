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
from Rhwydwaith_pont import Rhwydwaith_pont
from Gweithredu_gorchymyn import prosiect_gwraidd, Gorchymyn
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Gweithredu_2():
    mesur_data = prosiect_gwraidd / 'build/verification/ftp'; mesur_data.mkdir(parents=True, exist_ok=True)
    dilysu_adrodd = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((prosiect_gwraidd / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = mesur_data / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { Cymraeg.자체.Allbwn.ysgrifennu_llinell("JAR Gweithredu_gorchymyn: " + 인수[0]); Cymraeg.자체.Ffeil.Ysgrifennu("jar.txt", "자체 cnewyllyn_VALUE Ffeil"); Cymraeg.자체.Allbwn.ysgrifennu_llinell(Cymraeg.자체.Ffeil.Darllen("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(prosiect_gwraidd/'build/java-library/classes'), '-d', str(mesur_data), str(자바원문)])
    Archif = io.BytesIO()
    with zipfile.ZipFile(Archif, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(mesur_data/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); rhif_porth = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); gweinydd_ffrwd_porth = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Rhwydwaith_pont(rhif_porth, ['tcp:{}:9300'.format(gweinydd_ffrwd_porth), 'udp:{}:9301'.format(서버전문접속번호)], recordio=True) as pont:
        Proses = subprocess.Popen(Gorchymyn() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + pont.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        dewisydd = selectors.DefaultSelector(); dewisydd.register(Proses.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            data = bytearray(); gorffen_OFFSET = time.monotonic() + 시간제한
            while 확인표시 not in data:
                if time.monotonic() > gorffen_OFFSET or Proses.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + data.decode('utf-8', 'replace'))
                for 누름값, _ in dewisydd.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8', 'replace').replace('\r\n', '\n')
        def cragen(llinell):
            Proses.stdin.write(llinell.encode() + b'\n'); Proses.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in cragen('ftpd start')
            ffeil_trosglwyddo_cyswllt = ftplib.FTP(); ffeil_trosglwyddo_cyswllt.encoding = 'utf-8'; ffeil_trosglwyddo_cyswllt.connect('127.0.0.1', rhif_porth, timeout=20); ffeil_trosglwyddo_cyswllt.login()
            llwyth_uchaf_data = bytes(range(256)) * 32
            ffeil_trosglwyddo_cyswllt.storbinary('STOR binary.dat', io.BytesIO(llwyth_uchaf_data))
            mesur = bytearray(); ffeil_trosglwyddo_cyswllt.retrbinary('RETR binary.dat', mesur.extend)
            assert mesur == llwyth_uchaf_data; assert ffeil_trosglwyddo_cyswllt.size('binary.dat') == len(llwyth_uchaf_data)
            dilysu_adrodd['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ffeil_trosglwyddo_cyswllt.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in cragen('cat 한글.txt')
            assert '한글.txt' in ffeil_trosglwyddo_cyswllt.nlst()
            assert dict(ffeil_trosglwyddo_cyswllt.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            dilysu_adrodd['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ffeil_trosglwyddo_cyswllt.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            mesur = bytearray(); ffeil_trosglwyddo_cyswllt.retrbinary('RETR binary.dat', mesur.extend); assert mesur == llwyth_uchaf_data
            dilysu_adrodd['checks'].append('oversized replacement rejected; previous file preserved')
            with ffeil_trosglwyddo_cyswllt.transfercmd('STOR pending.txt') as Upload_Ffeil:
                # A control command must not change the active upload's destination.
                assert ffeil_trosglwyddo_cyswllt.size('binary.dat') == len(llwyth_uchaf_data)
                Upload_Ffeil.sendall(b'UPLOAD TARGET PRESERVED')
            assert ffeil_trosglwyddo_cyswllt.voidresp().startswith('226')
            mesur = bytearray(); ffeil_trosglwyddo_cyswllt.retrbinary('RETR pending.txt', mesur.extend)
            assert mesur == b'UPLOAD TARGET PRESERVED'
            mesur = bytearray(); ffeil_trosglwyddo_cyswllt.retrbinary('RETR binary.dat', mesur.extend)
            assert mesur == llwyth_uchaf_data
            ffeil_trosglwyddo_cyswllt.delete('pending.txt')
            dilysu_adrodd['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ffeil_trosglwyddo_cyswllt.storbinary('STOR 인사.jar', io.BytesIO(Archif.getvalue()))
            Testun = cragen('java -jar 인사.jar 누리')
            assert 'JAR Gweithredu_gorchymyn: 누리' in Testun and '자체 cnewyllyn_VALUE Ffeil' in Testun and 'exit 0' in Testun, Testun
            Testun = cragen('./인사.jar 세상')
            assert 'JAR Gweithredu_gorchymyn: 세상' in Testun and 'exit 0' in Testun, Testun
            dilysu_adrodd['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct data { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct data VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = agor_ffeil("cc.txt", darllen_ysgrifennu | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; ysgrifennu_ffeil_data(문서, 인사, sizeof(인사)-1); cau_ffeil(문서); ysgrifennu_ffeil_data(1, 인사, sizeof(인사)-1); return 0; }\n'
            ffeil_trosglwyddo_cyswllt.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Testun = cragen('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Testun and 'exit 0' in Testun, Testun
            Testun = cragen('run 한글.elf'); assert 'CC NATIVE PASS' in Testun and 'exit 0' in Testun, Testun
            assert 'CC NATIVE PASS' in cragen('cat cc.txt')
            실행파일 = bytearray(); ffeil_trosglwyddo_cyswllt.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ffeil_trosglwyddo_cyswllt.storbinary('STOR copïo_VALUE.elf', io.BytesIO(실행파일)); Testun = cragen('run copïo_VALUE.elf'); assert 'CC NATIVE PASS' in Testun and 'exit 0' in Testun, Testun
            ffeil_trosglwyddo_cyswllt.storbinary('STOR Gweithredu_gorchymyn', io.BytesIO(실행파일)); Testun=cragen('./Gweithredu_gorchymyn');assert 'CC NATIVE PASS' in Testun and 'exit 0' in Testun,Testun
            ffeil_trosglwyddo_cyswllt.storbinary('STOR Enw.txt', io.BytesIO(실행파일)); Testun=cragen('./Enw.txt');assert 'CC NATIVE PASS' in Testun and 'exit 0' in Testun,Testun
            cragen('rm Gweithredu_gorchymyn Enw.txt')
            dilysu_adrodd['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            cragen('rm binary.dat 한글.txt 한글.c 한글.elf copïo_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(mesur_data/'linux-reference')
            ffeil_trosglwyddo_cyswllt.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Testun=cragen('./리눅스인사');assert 'exit -8' in Testun,Testun
            Testun=cragen('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Testun,Testun
            assert 'LINUX ELF FILE IO' in cragen('cat linux.txt')
            ffeil_trosglwyddo_cyswllt.delete('리눅스인사');ffeil_trosglwyddo_cyswllt.delete('linux.txt')
            ffeil_trosglwyddo_cyswllt.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in cragen('./FALSE_VALUE.elf');ffeil_trosglwyddo_cyswllt.delete('FALSE_VALUE.elf')
            dilysu_adrodd['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = mesur_data/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Cysylltu = Cymraeg.자체.연결통신.Cysylltu("10.0.2.2", Integer.parseInt(args[0]));
 Cysylltu.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] FFYNHONNELL = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<FFYNHONNELL.length;i++) if (Cysylltu.getInputStream().read() != (FFYNHONNELL[i]&255)) throw new RuntimeException("TCP mismatch");
 Cysylltu.close();
 DatagramSocket 종단 = Cymraeg.자체.통신.Agor(0); Cymraeg.자체.통신.TIMEOUT(종단, 500);
 Cymraeg.자체.통신.anfon(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Cymraeg.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(prosiect_gwraidd/'build/java-library/classes'),'-d',str(mesur_data),str(통신원문)])
                ffeil_trosglwyddo_cyswllt.storbinary('STOR 바깥통신.class', io.BytesIO((mesur_data/'바깥통신.class').read_bytes()))
                Testun = cragen('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_porth, 되돌림서버항목.UDP_porth))
                assert 'EXTERNAL TCP UDP PASS' in Testun and '10.0.2.2' in Testun and 'exit 0' in Testun, Testun
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            dilysu_adrodd['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ffeil_trosglwyddo_cyswllt.delete('바깥통신.class')
            gweinydd_ffynhonnell=mesur_data/'서버시험.java'
            gweinydd_ffynhonnell.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket gweinydd_VALUE = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket gwestai_VALUE = gweinydd_VALUE.accept();
  gwestai_VALUE.getOutputStream().write(gwestai_VALUE.getInputStream().read()+1); gwestai_VALUE.close(); gweinydd_VALUE.close();
  byte[] Cynnwys_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Cynnwys_VALUE, Cynnwys_VALUE.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mesur_data),str(gweinydd_ffynhonnell)])
            ffeil_trosglwyddo_cyswllt.storbinary('STOR 서버시험.class',io.BytesIO((mesur_data/'서버시험.class').read_bytes()))
            Proses.stdin.write('java 서버시험\n'.encode());Proses.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',gweinydd_ffrwd_porth),timeout=5) as cymar_VALUE:
                cymar_VALUE.sendall(b'A');assert cymar_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as cymar_VALUE:
                cymar_VALUE.settimeout(5);cymar_VALUE.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert cymar_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Testun=수신하기();assert 'INBOUND TCP UDP PASS' in Testun and 'exit 0' in Testun,Testun
            dilysu_adrodd['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ffeil_trosglwyddo_cyswllt.delete('서버시험.class')
            cyfarwyddyd_SEQUENCE = 'public class 빛 { public static void main(String[] 인수) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } Cymraeg.자체.Allbwn.수쓰기(SUM_VALUE); Cymraeg.자체.Ffeil.Ysgrifennu("aot.txt", "한글 AOT Ffeil 😀"); Cymraeg.자체.Allbwn.ysgrifennu_llinell(Cymraeg.자체.Ffeil.Darllen("aot.txt")); } }'
            ffeil_trosglwyddo_cyswllt.storbinary('STOR 빛.java', io.BytesIO(cyfarwyddyd_SEQUENCE.encode()))
            Testun = cragen('javac 빛.java'); assert 'exit 0' in Testun and 'Compiled:' in Testun, Testun
            Testun = cragen('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Testun and 'exit 0' in Testun, Testun
            Testun = cragen('run 빛.elf'); assert '\n55\n' in Testun and '한글 AOT Ffeil 😀' in Testun and 'exit 0' in Testun, Testun
            자체실행파일 = bytearray(); ffeil_trosglwyddo_cyswllt.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Testun = cragen('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Testun and 'unsupported' in Testun, Testun
            보존자료 = bytearray(); ffeil_trosglwyddo_cyswllt.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ffeil_trosglwyddo_cyswllt.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ffeil_trosglwyddo_cyswllt.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Testun = cragen('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Testun and 'exit 0' in Testun, Testun
            Testun = cragen('run 빛.elf'); assert '\n55\n' in Testun and '한글 AOT Ffeil 😀' in Testun and 'exit 0' in Testun, Testun
            dilysu_adrodd['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            dilysu_adrodd['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statig_ffynhonnell=mesur_data/'정적시험.java'
            statig_ffynhonnell.write_text('''public class 정적시험 {
 static int prosiect_gwraidd = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] 인수) {
  int[] VALUE = new int[] {prosiect_gwraidd, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mesur_data),str(statig_ffynhonnell)])
            ffeil_trosglwyddo_cyswllt.storbinary('STOR 정적시험.class',io.BytesIO((mesur_data/'정적시험.class').read_bytes()))
            Testun=cragen('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Testun,Testun
            Testun=cragen('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Testun,Testun
            ffeil_trosglwyddo_cyswllt.delete('정적시험.class');ffeil_trosglwyddo_cyswllt.delete('정적시험.elf')
            dilysu_adrodd['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Archif.getvalue());손상자료[14]^=1
            ffeil_trosglwyddo_cyswllt.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Testun=cragen('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Testun,Testun
            dilysu_adrodd['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ffeil_trosglwyddo_cyswllt.quit(); assert 'FTP stopped' in cragen('ftpd stop')
            assert not pont.Gwall, pont.Gwall
            dilysu_adrodd.update(passed=True, frames_to_guest=pont.커널수신틀수, frames_from_guest=pont.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in dewisydd.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            pont.rhewi_digwyddiad.set()
            Proses.terminate()
            try: Proses.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
            dewisydd.close(); Proses.stdin.close(); Proses.stdout.close()
            dilysu_adrodd['bridge_error'] = pont.Gwall
            dilysu_adrodd['frames_to_guest'] = pont.커널수신틀수; dilysu_adrodd['frames_from_guest'] = pont.커널발신틀수
            (mesur_data/'packets.json').write_text(json.dumps(pont.olrhain_LOG,indent=2)+'\n')
            (mesur_data / 'serial.log').write_bytes(대화기록)
            (mesur_data / 'report.json').write_text(json.dumps(dilysu_adrodd, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Gweithredu_2()
