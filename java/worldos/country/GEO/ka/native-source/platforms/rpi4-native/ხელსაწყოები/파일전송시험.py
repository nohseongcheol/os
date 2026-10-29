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
from ქსელი_ხიდი import ქსელი_ხიდი
from შესრულება_ბრძანება import პროეცირება_ფესვი, ბრძანება
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def გაშვება():
    გაზომვა_მონაცემები = პროეცირება_ფესვი / 'build/verification/ftp'; გაზომვა_მონაცემები.mkdir(parents=True, exist_ok=True)
    გადამოწმება_ანგარიში = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((პროეცირება_ფესვი / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = გაზომვა_მონაცემები / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.ჩაწერა_ხაზი("JAR შესრულება_ბრძანება: " + 인수[0]); 한국어.자체.ფაილი.ჩაწერა("jar.txt", "자체 ბირთვი_მნიშვნელობა ფაილი"); 한국어.자체.출력.ჩაწერა_ხაზი(한국어.자체.ფაილი.კითხვა("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(პროეცირება_ფესვი/'build/java-library/classes'), '-d', str(გაზომვა_მონაცემები), str(자바원문)])
    არქივი = io.BytesIO()
    with zipfile.ZipFile(არქივი, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(გაზომვა_მონაცემები/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); სერვერი_ნაკადი_პორტი = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with ქსელი_ხიდი(접속번호, ['tcp:{}:9300'.format(სერვერი_ნაკადი_პორტი), 'udp:{}:9301'.format(서버전문접속번호)], გადაღება=True) as ხიდი:
        პროცესი = subprocess.Popen(ბრძანება() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ხიდი.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        სელექტორი = selectors.DefaultSelector(); სელექტორი.register(პროცესი.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            მონაცემები = bytearray(); დასასრული_ოფსეტი = time.monotonic() + 시간제한
            while 확인표시 not in მონაცემები:
                if time.monotonic() > დასასრული_ოფსეტი or პროცესი.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + მონაცემები.decode('utf-8', 'replace'))
                for 누름값, _ in სელექტორი.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: მონაცემები.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in მონაცემები or b'FAIL ' in მონაცემები: raise AssertionError(მონაცემები)
            return მონაცემები.decode('utf-8', 'replace').replace('\r\n', '\n')
        def გარემო(ხაზი):
            პროცესი.stdin.write(ხაზი.encode() + b'\n'); პროცესი.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in გარემო('ftpd start')
            ფაილი_გადატანა_კავშირი = ftplib.FTP(); ფაილი_გადატანა_კავშირი.encoding = 'utf-8'; ფაილი_გადატანა_კავშირი.connect('127.0.0.1', 접속번호, timeout=20); ფაილი_გადატანა_კავშირი.login()
            დატვირთვა_მონაცემები = bytes(range(256)) * 32
            ფაილი_გადატანა_კავშირი.storbinary('STOR binary.dat', io.BytesIO(დატვირთვა_მონაცემები))
            გაზომვა = bytearray(); ფაილი_გადატანა_კავშირი.retrbinary('RETR binary.dat', გაზომვა.extend)
            assert გაზომვა == დატვირთვა_მონაცემები; assert ფაილი_გადატანა_კავშირი.size('binary.dat') == len(დატვირთვა_მონაცემები)
            გადამოწმება_ანგარიში['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ფაილი_გადატანა_კავშირი.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in გარემო('cat 한글.txt')
            assert '한글.txt' in ფაილი_გადატანა_კავშირი.nlst()
            assert dict(ფაილი_გადატანა_კავშირი.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            გადამოწმება_ანგარიში['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ფაილი_გადატანა_კავშირი.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            გაზომვა = bytearray(); ფაილი_გადატანა_კავშირი.retrbinary('RETR binary.dat', გაზომვა.extend); assert გაზომვა == დატვირთვა_მონაცემები
            გადამოწმება_ანგარიში['checks'].append('oversized replacement rejected; previous file preserved')
            with ფაილი_გადატანა_კავშირი.transfercmd('STOR pending.txt') as ატვირთვა_ფაილები:
                # A control command must not change the active upload's destination.
                assert ფაილი_გადატანა_კავშირი.size('binary.dat') == len(დატვირთვა_მონაცემები)
                ატვირთვა_ფაილები.sendall(b'UPLOAD TARGET PRESERVED')
            assert ფაილი_გადატანა_კავშირი.voidresp().startswith('226')
            გაზომვა = bytearray(); ფაილი_გადატანა_კავშირი.retrbinary('RETR pending.txt', გაზომვა.extend)
            assert გაზომვა == b'UPLOAD TARGET PRESERVED'
            გაზომვა = bytearray(); ფაილი_გადატანა_კავშირი.retrbinary('RETR binary.dat', გაზომვა.extend)
            assert გაზომვა == დატვირთვა_მონაცემები
            ფაილი_გადატანა_კავშირი.delete('pending.txt')
            გადამოწმება_ანგარიში['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ფაილი_გადატანა_კავშირი.storbinary('STOR 인사.jar', io.BytesIO(არქივი.getvalue()))
            ტექსტი = გარემო('java -jar 인사.jar 누리')
            assert 'JAR შესრულება_ბრძანება: 누리' in ტექსტი and '자체 ბირთვი_მნიშვნელობა ფაილი' in ტექსტი and 'exit 0' in ტექსტი, ტექსტი
            ტექსტი = გარემო('./인사.jar 세상')
            assert 'JAR შესრულება_ბრძანება: 세상' in ტექსტი and 'exit 0' in ტექსტი, ტექსტი
            გადამოწმება_ანგარიში['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct მონაცემები { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct მონაცემები მნიშვნელობა = {합(10), 1.25}; if (მნიშვნელობა.수 != 55 || მნიშვნელობა.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = გახსნა_ფაილი("cc.txt", ჩაწერა_წაკითხვა | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; ჩაწერა_ფაილი_მონაცემები(문서, 인사, sizeof(인사)-1); დახურვა_ფაილი(문서); ჩაწერა_ფაილი_მონაცემები(1, 인사, sizeof(인사)-1); return 0; }\n'
            ფაილი_გადატანა_კავშირი.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            ტექსტი = გარემო('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in ტექსტი and 'exit 0' in ტექსტი, ტექსტი
            ტექსტი = გარემო('run 한글.elf'); assert 'CC NATIVE PASS' in ტექსტი and 'exit 0' in ტექსტი, ტექსტი
            assert 'CC NATIVE PASS' in გარემო('cat cc.txt')
            실행파일 = bytearray(); ფაილი_გადატანა_კავშირი.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ფაილი_გადატანა_კავშირი.storbinary('STOR ასლი_მნიშვნელობა.elf', io.BytesIO(실행파일)); ტექსტი = გარემო('run ასლი_მნიშვნელობა.elf'); assert 'CC NATIVE PASS' in ტექსტი and 'exit 0' in ტექსტი, ტექსტი
            ფაილი_გადატანა_კავშირი.storbinary('STOR შესრულება_ბრძანება', io.BytesIO(실행파일)); ტექსტი=გარემო('./შესრულება_ბრძანება');assert 'CC NATIVE PASS' in ტექსტი and 'exit 0' in ტექსტი,ტექსტი
            ფაილი_გადატანა_კავშირი.storbinary('STOR სახელი.txt', io.BytesIO(실행파일)); ტექსტი=გარემო('./სახელი.txt');assert 'CC NATIVE PASS' in ტექსტი and 'exit 0' in ტექსტი,ტექსტი
            გარემო('rm შესრულება_ბრძანება სახელი.txt')
            გადამოწმება_ანგარიში['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            გარემო('rm binary.dat 한글.txt 한글.c 한글.elf ასლი_მნიშვნელობა.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(გაზომვა_მონაცემები/'linux-reference')
            ფაილი_გადატანა_კავშირი.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            ტექსტი=გარემო('./리눅스인사');assert 'exit -8' in ტექსტი,ტექსტი
            ტექსტი=გარემო('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in ტექსტი,ტექსტი
            assert 'LINUX ELF FILE IO' in გარემო('cat linux.txt')
            ფაილი_გადატანა_კავშირი.delete('리눅스인사');ფაილი_გადატანა_კავშირი.delete('linux.txt')
            ფაილი_გადატანა_კავშირი.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in გარემო('./거짓.elf');ფაილი_გადატანა_კავშირი.delete('거짓.elf')
            გადამოწმება_ანგარიში['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = გაზომვა_მონაცემები/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket დაკავშირება = 한국어.자체.연결통신.დაკავშირება("10.0.2.2", Integer.parseInt(args[0]));
 დაკავშირება.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] წყარო = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<წყარო.length;i++) if (დაკავშირება.getInputStream().read() != (წყარო[i]&255)) throw new RuntimeException("TCP mismatch");
 დაკავშირება.close();
 DatagramSocket 종단 = 한국어.자체.통신.გახსნა(0); 한국어.자체.통신.დრო_ამოიწურა(종단, 500);
 한국어.자체.통신.გაგზავნა(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(პროეცირება_ფესვი/'build/java-library/classes'),'-d',str(გაზომვა_მონაცემები),str(통신원문)])
                ფაილი_გადატანა_კავშირი.storbinary('STOR 바깥통신.class', io.BytesIO((გაზომვა_მონაცემები/'바깥통신.class').read_bytes()))
                ტექსტი = გარემო('java 바깥통신 {} {}'.format(되돌림서버항목.გადაცემის_მართვის_პროტოკოლი_პორტი, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in ტექსტი and '10.0.2.2' in ტექსტი and 'exit 0' in ტექსტი, ტექსტი
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            გადამოწმება_ანგარიში['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ფაილი_გადატანა_კავშირი.delete('바깥통신.class')
            სერვერი_წყარო=გაზომვა_მონაცემები/'서버시험.java'
            სერვერი_წყარო.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket სერვერი_მნიშვნელობა = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket სტუმარი_მნიშვნელობა = სერვერი_მნიშვნელობა.accept();
  სტუმარი_მნიშვნელობა.getOutputStream().write(სტუმარი_მნიშვნელობა.getInputStream().read()+1); სტუმარი_მნიშვნელობა.close(); სერვერი_მნიშვნელობა.close();
  byte[] შიგთავსი_მნიშვნელობა = new byte[8]; DatagramPacket 전문 = new DatagramPacket(შიგთავსი_მნიშვნელობა, შიგთავსი_მნიშვნელობა.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(გაზომვა_მონაცემები),str(სერვერი_წყარო)])
            ფაილი_გადატანა_კავშირი.storbinary('STOR 서버시험.class',io.BytesIO((გაზომვა_მონაცემები/'서버시험.class').read_bytes()))
            პროცესი.stdin.write('java 서버시험\n'.encode());პროცესი.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',სერვერი_ნაკადი_პორტი),timeout=5) as კვანძი_მნიშვნელობა_6a3b6fa7:
                კვანძი_მნიშვნელობა_6a3b6fa7.sendall(b'A');assert კვანძი_მნიშვნელობა_6a3b6fa7.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as კვანძი_მნიშვნელობა_6a3b6fa7:
                კვანძი_მნიშვნელობა_6a3b6fa7.settimeout(5);კვანძი_მნიშვნელობა_6a3b6fa7.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert კვანძი_მნიშვნელობა_6a3b6fa7.recvfrom(512)[0]==b'UDP-IN'
            ტექსტი=수신하기();assert 'INBOUND TCP UDP PASS' in ტექსტი and 'exit 0' in ტექსტი,ტექსტი
            გადამოწმება_ანგარიში['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ფაილი_გადატანა_კავშირი.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.ფაილი.ჩაწერა("aot.txt", "한글 AOT ფაილი 😀"); 한국어.자체.출력.ჩაწერა_ხაზი(한국어.자체.ფაილი.კითხვა("aot.txt")); } }'
            ფაილი_გადატანა_კავშირი.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            ტექსტი = გარემო('javac 빛.java'); assert 'exit 0' in ტექსტი and 'Compiled:' in ტექსტი, ტექსტი
            ტექსტი = გარემო('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ტექსტი and 'exit 0' in ტექსტი, ტექსტი
            ტექსტი = გარემო('run 빛.elf'); assert '\n55\n' in ტექსტი and '한글 AOT ფაილი 😀' in ტექსტი and 'exit 0' in ტექსტი, ტექსტი
            자체실행파일 = bytearray(); ფაილი_გადატანა_კავშირი.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            ტექსტი = გარემო('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in ტექსტი and 'unsupported' in ტექსტი, ტექსტი
            보존자료 = bytearray(); ფაილი_გადატანა_კავშირი.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ფაილი_გადატანა_კავშირი.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ფაილი_გადატანა_კავშირი.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            ტექსტი = გარემო('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ტექსტი and 'exit 0' in ტექსტი, ტექსტი
            ტექსტი = გარემო('run 빛.elf'); assert '\n55\n' in ტექსტი and '한글 AOT ფაილი 😀' in ტექსტი and 'exit 0' in ტექსტი, ტექსტი
            გადამოწმება_ანგარიში['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            გადამოწმება_ანგარიში['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            სტატიკური_წყარო=გაზომვა_მონაცემები/'정적시험.java'
            სტატიკური_წყარო.write_text('''public class 정적시험 {
 static int პროეცირება_ფესვი = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] მნიშვნელობა = new int[] {პროეცირება_ფესვი, 합(10)};
  System.out.println(მნიშვნელობა[0] + მნიშვნელობა[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(გაზომვა_მონაცემები),str(სტატიკური_წყარო)])
            ფაილი_გადატანა_კავშირი.storbinary('STOR 정적시험.class',io.BytesIO((გაზომვა_მონაცემები/'정적시험.class').read_bytes()))
            ტექსტი=გარემო('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in ტექსტი,ტექსტი
            ტექსტი=გარემო('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in ტექსტი,ტექსტი
            ფაილი_გადატანა_კავშირი.delete('정적시험.class');ფაილი_გადატანა_კავშირი.delete('정적시험.elf')
            გადამოწმება_ანგარიში['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(არქივი.getvalue());손상자료[14]^=1
            ფაილი_გადატანა_კავშირი.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            ტექსტი=გარემო('java -jar 인사.jar');assert 'Main-Class\nexit 1' in ტექსტი,ტექსტი
            გადამოწმება_ანგარიში['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ფაილი_გადატანა_კავშირი.quit(); assert 'FTP stopped' in გარემო('ftpd stop')
            assert not ხიდი.შეცდომა, ხიდი.შეცდომა
            გადამოწმება_ანგარიში.update(passed=True, frames_to_guest=ხიდი.커널수신틀수, frames_from_guest=ხიდი.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in სელექტორი.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            ხიდი.პაუზა_მოვლენა.set()
            პროცესი.terminate()
            try: პროცესი.wait(timeout=5)
            except subprocess.TimeoutExpired: პროცესი.kill(); პროცესი.wait()
            სელექტორი.close(); პროცესი.stdin.close(); პროცესი.stdout.close()
            გადამოწმება_ანგარიში['bridge_error'] = ხიდი.შეცდომა
            გადამოწმება_ანგარიში['frames_to_guest'] = ხიდი.커널수신틀수; გადამოწმება_ანგარიში['frames_from_guest'] = ხიდი.커널발신틀수
            (გაზომვა_მონაცემები/'packets.json').write_text(json.dumps(ხიდი.추적기록,indent=2)+'\n')
            (გაზომვა_მონაცემები / 'serial.log').write_bytes(대화기록)
            (გაზომვა_მონაცემები / 'report.json').write_text(json.dumps(გადამოწმება_ანგარიში, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': გაშვება()
