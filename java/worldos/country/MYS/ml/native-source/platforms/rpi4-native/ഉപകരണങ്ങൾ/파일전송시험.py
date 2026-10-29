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
from നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ് import നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം, ആജ്ഞ
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def നടപ്പിലാക്കുക():
    അളവ്_ഡാറ്റാ = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/verification/ftp'; അളവ്_ഡാറ്റാ.mkdir(parents=True, exist_ok=True)
    నిర్ధారణ_నివేదిక = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = അളവ്_ഡാറ്റാ / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.ഫലം.റൈറ്റ്_ചെയ്യുക_ലൈൻ("JAR നടപ്പാക്കുക_കമാന്_ഡ്: " + 인수[0]); 한국어.자체.ഫയല്.എഴുത്തു്("jar.txt", "자체 കെര്_ണല്_മൂല്യം ഫയല്"); 한국어.자체.ഫലം.റൈറ്റ്_ചെയ്യുക_ലൈൻ(한국어.자체.ഫയല്.വായന("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/java-library/classes'), '-d', str(അളവ്_ഡാറ്റാ), str(자바원문)])
    ശേഖരം = io.BytesIO()
    with zipfile.ZipFile(ശേഖരം, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(അളവ്_ഡാറ്റാ/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); പോര്_ട്ട്_നമ്പര് = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); സെര്_വര്_സ്ട്രീം_പോര്_ട്ട് = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്(പോര്_ട്ട്_നമ്പര്, ['tcp:{}:9300'.format(സെര്_വര്_സ്ട്രീം_പോര്_ട്ട്), 'udp:{}:9301'.format(서버전문접속번호)], ക്യാപ്_ചർ_ചെയ്യുക=True) as ബ്രിഡ്_ജ്:
        പ്രക്രിയ = subprocess.Popen(ആജ്ഞ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ബ്രിഡ്_ജ്.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        సెలక్టర్ = selectors.DefaultSelector(); సెలక్టర్.register(പ്രക്രിയ.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            ഡാറ്റാ = bytearray(); അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ് = time.monotonic() + 시간제한
            while 확인표시 not in ഡാറ്റാ:
                if time.monotonic() > അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ് or പ്രക്രിയ.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + ഡാറ്റാ.decode('utf-8', 'replace'))
                for 누름값, _ in సెలక్టర్.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: ഡാറ്റാ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ഡാറ്റാ or b'FAIL ' in ഡാറ്റാ: raise AssertionError(ഡാറ്റാ)
            return ഡാറ്റാ.decode('utf-8', 'replace').replace('\r\n', '\n')
        def ഷെല്(ലൈൻ):
            പ്രക്രിയ.stdin.write(ലൈൻ.encode() + b'\n'); പ്രക്രിയ.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in ഷെല്('ftpd start')
            ഫയല്_കൈമാറുക_കണക്ഷൻ = ftplib.FTP(); ഫയല്_കൈമാറുക_കണക്ഷൻ.encoding = 'utf-8'; ഫയല്_കൈമാറുക_കണക്ഷൻ.connect('127.0.0.1', പോര്_ട്ട്_നമ്പര്, timeout=20); ഫയല്_കൈമാറുക_കണക്ഷൻ.login()
            പേലോഡ്_ഡാറ്റാ = bytes(range(256)) * 32
            ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR binary.dat', io.BytesIO(പേലോഡ്_ഡാറ്റാ))
            അളവ് = bytearray(); ഫയല്_കൈമാറുക_കണക്ഷൻ.retrbinary('RETR binary.dat', അളവ്.extend)
            assert അളവ് == പേലോഡ്_ഡാറ്റാ; assert ഫയല്_കൈമാറുക_കണക്ഷൻ.size('binary.dat') == len(പേലോഡ്_ഡാറ്റാ)
            నిర్ధారణ_నివేదిక['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in ഷെല്('cat 한글.txt')
            assert '한글.txt' in ഫയല്_കൈമാറുക_കണക്ഷൻ.nlst()
            assert dict(ഫയല്_കൈമാറുക_കണക്ഷൻ.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            నిర్ధారణ_నివేదిక['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            അളവ് = bytearray(); ഫയല്_കൈമാറുക_കണക്ഷൻ.retrbinary('RETR binary.dat', അളവ്.extend); assert അളവ് == പേലോഡ്_ഡാറ്റാ
            నిర్ధారణ_నివేదిక['checks'].append('oversized replacement rejected; previous file preserved')
            with ഫയല്_കൈമാറുക_കണക്ഷൻ.transfercmd('STOR pending.txt') as അപ്_ലോഡ്_ഫയലുകൾ:
                # A control command must not change the active upload's destination.
                assert ഫയല്_കൈമാറുക_കണക്ഷൻ.size('binary.dat') == len(പേലോഡ്_ഡാറ്റാ)
                അപ്_ലോഡ്_ഫയലുകൾ.sendall(b'UPLOAD TARGET PRESERVED')
            assert ഫയല്_കൈമാറുക_കണക്ഷൻ.voidresp().startswith('226')
            അളവ് = bytearray(); ഫയല്_കൈമാറുക_കണക്ഷൻ.retrbinary('RETR pending.txt', അളവ്.extend)
            assert അളവ് == b'UPLOAD TARGET PRESERVED'
            അളവ് = bytearray(); ഫയല്_കൈമാറുക_കണക്ഷൻ.retrbinary('RETR binary.dat', അളവ്.extend)
            assert അളവ് == പേലോഡ്_ഡാറ്റാ
            ഫയല്_കൈമാറുക_കണക്ഷൻ.delete('pending.txt')
            నిర్ధారణ_నివేదిక['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR 인사.jar', io.BytesIO(ശേഖരം.getvalue()))
            പദാവലി = ഷെല്('java -jar 인사.jar 누리')
            assert 'JAR നടപ്പാക്കുക_കമാന്_ഡ്: 누리' in പദാവലി and '자체 കെര്_ണല്_മൂല്യം ഫയല്' in പദാവലി and 'exit 0' in പദാവലി, പദാവലി
            പദാവലി = ഷെല്('./인사.jar 세상')
            assert 'JAR നടപ്പാക്കുക_കമാന്_ഡ്: 세상' in പദാവലി and 'exit 0' in പദാവലി, പദാവലി
            నిర్ధారణ_నివేదిక['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct ഡാറ്റാ { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct ഡാറ്റാ മൂല്യം = {합(10), 1.25}; if (മൂല്യം.수 != 55 || മൂല്യം.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = തുറക്കുക_ഫയല്("cc.txt", വായനാ_റൈറ്റ് | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; റൈറ്റ്_ചെയ്യുക_ഫയല്_ഡാറ്റാ(문서, 인사, sizeof(인사)-1); അടയ്ക്കുക_ഫയല്(문서); റൈറ്റ്_ചെയ്യുക_ഫയല്_ഡാറ്റാ(1, 인사, sizeof(인사)-1); return 0; }\n'
            ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            പദാവലി = ഷെല്('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in പദാവലി and 'exit 0' in പദാവലി, പദാവലി
            പദാവലി = ഷെല്('run 한글.elf'); assert 'CC NATIVE PASS' in പദാവലി and 'exit 0' in പദാവലി, പദാവലി
            assert 'CC NATIVE PASS' in ഷെല്('cat cc.txt')
            നിര്_വ്വഹണക്ഷമമായ_ഫയല് = bytearray(); ഫയല്_കൈമാറുക_കണക്ഷൻ.retrbinary('RETR 한글.elf', നിര്_വ്വഹണക്ഷമമായ_ഫയല്.extend)
            assert നിര്_വ്വഹണക്ഷമമായ_ഫയല്[:4] == b'\x7fELF' and നിര്_വ്വഹണക്ഷമമായ_ഫയല്[18:20] == b'\xb7\x00'
            ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR ദൃഷ്ടാന്തം_മൂല്യം.elf', io.BytesIO(നിര്_വ്വഹണക്ഷമമായ_ഫയല്)); പദാവലി = ഷെല്('run ദൃഷ്ടാന്തം_മൂല്യം.elf'); assert 'CC NATIVE PASS' in പദാവലി and 'exit 0' in പദാവലി, പദാവലി
            ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR നടപ്പാക്കുക_കമാന്_ഡ്', io.BytesIO(നിര്_വ്വഹണക്ഷമമായ_ഫയല്)); പദാവലി=ഷെല്('./നടപ്പാക്കുക_കമാന്_ഡ്');assert 'CC NATIVE PASS' in പദാവലി and 'exit 0' in പദാവലി,പദാവലി
            ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR പേരു്.txt', io.BytesIO(നിര്_വ്വഹണക്ഷമമായ_ഫയല്)); പദാവലി=ഷെല്('./പേരു്.txt');assert 'CC NATIVE PASS' in പദാവലി and 'exit 0' in പദാവലി,പദാവലി
            ഷെല്('rm നടപ്പാക്കുക_കമാന്_ഡ് പേരു്.txt')
            నిర్ధారణ_నివేదిక['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            ഷെല്('rm binary.dat 한글.txt 한글.c 한글.elf ദൃഷ്ടാന്തം_മൂല്യം.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(അളവ്_ഡാറ്റാ/'linux-reference')
            ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            പദാവലി=ഷെല്('./리눅스인사');assert 'exit -8' in പദാവലി,പദാവലി
            പദാവലി=ഷെല്('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in പദാവലി,പദാവലി
            assert 'LINUX ELF FILE IO' in ഷെല്('cat linux.txt')
            ഫയല്_കൈമാറുക_കണക്ഷൻ.delete('리눅스인사');ഫയല്_കൈമാറുക_കണക്ഷൻ.delete('linux.txt')
            ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in ഷെല്('./거짓.elf');ഫയല്_കൈമാറുക_കണക്ഷൻ.delete('거짓.elf')
            నిర్ధారణ_నివేదిక['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = അളവ്_ഡാറ്റാ/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket കണക്ടു്_ചെയ്യുക = 한국어.자체.연결통신.കണക്ടു്_ചെയ്യുക("10.0.2.2", Integer.parseInt(args[0]));
 കണക്ടു്_ചെയ്യുക.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ഉറവിടം = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ഉറവിടം.length;i++) if (കണക്ടു്_ചെയ്യുക.getInputStream().read() != (ഉറവിടം[i]&255)) throw new RuntimeException("TCP mismatch");
 കണക്ടു്_ചെയ്യുക.close();
 DatagramSocket അവസാനബിന്ദു = 한국어.자체.통신.തുറക്കുക(0); 한국어.자체.통신.ടൈംഔട്ട്(അവസാനബിന്ദു, 500);
 한국어.자체.통신.അയയ്ക്കുക(അവസാനബിന്ദു, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(അവസാനബിന്ദു).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 അവസാനബിന്ദു.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/java-library/classes'),'-d',str(അളവ്_ഡാറ്റാ),str(통신원문)])
                ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR 바깥통신.class', io.BytesIO((അളവ്_ഡാറ്റാ/'바깥통신.class').read_bytes()))
                പദാവലി = ഷെല്('java 바깥통신 {} {}'.format(되돌림서버항목.ട്രാന്_സ്_മിഷന്_കണ്_ട്രോള്_പ്രോട്ടോക്കോള്_പോര്_ട്ട്, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in പദാവലി and '10.0.2.2' in പദാവലി and 'exit 0' in പദാവലി, പദാവലി
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            నిర్ధారణ_నివేదిక['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ഫയല്_കൈമാറുക_കണക്ഷൻ.delete('바깥통신.class')
            സെര്_വര്_ഉറവിടം=അളവ്_ഡാറ്റാ/'서버시험.java'
            സെര്_വര്_ഉറവിടം.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket സെര്_വര്_മൂല്യം = new ServerSocket(9300); DatagramSocket അവസാനബിന്ദു = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket അതിഥി_മൂല്യം = സെര്_വര്_മൂല്യം.accept();
  അതിഥി_മൂല്യം.getOutputStream().write(അതിഥി_മൂല്യം.getInputStream().read()+1); അതിഥി_മൂല്യം.close(); സെര്_വര്_മൂല്യം.close();
  byte[] ഉള്ളടക്കം_മൂല്യം = new byte[8]; DatagramPacket 전문 = new DatagramPacket(ഉള്ളടക്കം_മൂല്യം, ഉള്ളടക്കം_മൂല്യം.length); അവസാനബിന്ദു.receive(전문);
  അവസാനബിന്ദു.send(전문); അവസാനബിന്ദു.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(അളവ്_ഡാറ്റാ),str(സെര്_വര്_ഉറവിടം)])
            ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR 서버시험.class',io.BytesIO((അളവ്_ഡാറ്റാ/'서버시험.class').read_bytes()))
            പ്രക്രിയ.stdin.write('java 서버시험\n'.encode());പ്രക്രിയ.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',സെര്_വര്_സ്ട്രീം_പോര്_ട്ട്),timeout=5) as പീര്_മൂല്യം:
                പീര്_മൂല്യം.sendall(b'A');assert പീര്_മൂല്യം.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as പീര്_മൂല്യം:
                പീര്_മൂല്യം.settimeout(5);പീര്_മൂല്യം.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert പീര്_മൂല്യം.recvfrom(512)[0]==b'UDP-IN'
            പദാവലി=수신하기();assert 'INBOUND TCP UDP PASS' in പദാവലി and 'exit 0' in പദാവലി,പദാവലി
            నిర్ధారణ_నివేదిక['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ഫയല്_കൈമാറുക_കണക്ഷൻ.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.ഫലം.수쓰기(합); 한국어.자체.ഫയല്.എഴുത്തു്("aot.txt", "한글 AOT ഫയല് 😀"); 한국어.자체.ഫലം.റൈറ്റ്_ചെയ്യുക_ലൈൻ(한국어.자체.ഫയല്.വായന("aot.txt")); } }'
            ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            പദാവലി = ഷെല്('javac 빛.java'); assert 'exit 0' in പദാവലി and 'Compiled:' in പദാവലി, പദാവലി
            പദാവലി = ഷെല്('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in പദാവലി and 'exit 0' in പദാവലി, പദാവലി
            പദാവലി = ഷെല്('run 빛.elf'); assert '\n55\n' in പദാവലി and '한글 AOT ഫയല് 😀' in പദാവലി and 'exit 0' in പദാവലി, പദാവലി
            자체실행파일 = bytearray(); ഫയല്_കൈമാറുക_കണക്ഷൻ.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            പദാവലി = ഷെല്('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in പദാവലി and 'unsupported' in പദാവലി, പദാവലി
            보존자료 = bytearray(); ഫയല്_കൈമാറുക_കണക്ഷൻ.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ഫയല്_കൈമാറുക_കണക്ഷൻ.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            പദാവലി = ഷെല്('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in പദാവലി and 'exit 0' in പദാവലി, പദാവലി
            പദാവലി = ഷെല്('run 빛.elf'); assert '\n55\n' in പദാവലി and '한글 AOT ഫയല് 😀' in പദാവലി and 'exit 0' in പദാവലി, പദാവലി
            నిర్ధారణ_నివేదిక['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            నిర్ధారణ_నివేదిక['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            സ്ഥിരമായ_ഉറവിടം=അളവ്_ഡാറ്റാ/'정적시험.java'
            സ്ഥിരമായ_ഉറവിടം.write_text('''public class 정적시험 {
 static int പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] മൂല്യം = new int[] {പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം, 합(10)};
  System.out.println(മൂല്യം[0] + മൂല്യം[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(അളവ്_ഡാറ്റാ),str(സ്ഥിരമായ_ഉറവിടം)])
            ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR 정적시험.class',io.BytesIO((അളവ്_ഡാറ്റാ/'정적시험.class').read_bytes()))
            പദാവലി=ഷെല്('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in പദാവലി,പദാവലി
            പദാവലി=ഷെല്('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in പദാവലി,പദാവലി
            ഫയല്_കൈമാറുക_കണക്ഷൻ.delete('정적시험.class');ഫയല്_കൈമാറുക_കണക്ഷൻ.delete('정적시험.elf')
            నిర్ధారణ_నివేదిక['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(ശേഖരം.getvalue());손상자료[14]^=1
            ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            പദാവലി=ഷെല്('java -jar 인사.jar');assert 'Main-Class\nexit 1' in പദാവലി,പദാവലി
            నిర్ధారణ_నివేదిక['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ഫയല്_കൈമാറുക_കണക്ഷൻ.quit(); assert 'FTP stopped' in ഷെല്('ftpd stop')
            assert not ബ്രിഡ്_ജ്.പിശക്, ബ്രിഡ്_ജ്.പിശക്
            నిర్ధారణ_నివేదిక.update(passed=True, frames_to_guest=ബ്രിഡ്_ജ്.커널수신틀수, frames_from_guest=ബ്രിഡ്_ജ്.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in సెలక్టర్.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            ബ്രിഡ്_ജ്.അല്_പം_നിര്_ത്തുക_ഇവന്റ്.set()
            പ്രക്രിയ.terminate()
            try: പ്രക്രിയ.wait(timeout=5)
            except subprocess.TimeoutExpired: പ്രക്രിയ.kill(); പ്രക്രിയ.wait()
            సెలక్టర్.close(); പ്രക്രിയ.stdin.close(); പ്രക്രിയ.stdout.close()
            నిర్ధారణ_నివేదిక['bridge_error'] = ബ്രിഡ്_ജ്.പിശക്
            నిర్ధారణ_నివేదిక['frames_to_guest'] = ബ്രിഡ്_ജ്.커널수신틀수; నిర్ధారణ_నివేదిక['frames_from_guest'] = ബ്രിഡ്_ജ്.커널발신틀수
            (അളവ്_ഡാറ്റാ/'packets.json').write_text(json.dumps(ബ്രിഡ്_ജ്.ട്രെയ്സ്_ലോഗ്,indent=2)+'\n')
            (അളവ്_ഡാറ്റാ / 'serial.log').write_bytes(대화기록)
            (അളവ്_ഡാറ്റാ / 'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': നടപ്പിലാക്കുക()
