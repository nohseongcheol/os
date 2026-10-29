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
from 통신다리 import 통신다리
from ተግብር_ትእዛዝ import 기준, ትእዛዝ
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def ኣኺድ():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    ምርግጋፅ_ጸብጻብ = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { ትግርኛ.자체.출력.ጸሓፍ_መስመር("JAR ተግብር_ትእዛዝ: " + 인수[0]); ትግርኛ.자체.ፋይል.ጸሓፍ("jar.txt", "자체 ፍረ_ዋጋ ፋይል"); ትግርኛ.자체.출력.ጸሓፍ_መስመር(ትግርኛ.자체.ፋይል.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    ሰንድ = io.BytesIO()
    with zipfile.ZipFile(ሰንድ, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); ኣገልጋሊ_ወሓዚ_ወደብ = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with 통신다리(접속번호, ['tcp:{}:9300'.format(ኣገልጋሊ_ወሓዚ_ወደብ), 'udp:{}:9301'.format(서버전문접속번호)], ቕረጽ=True) as 연결다리:
        መስርሕ = subprocess.Popen(ትእዛዝ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 연결다리.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        መራፂ = selectors.DefaultSelector(); መራፂ.register(መስርሕ.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            ሓበሬታ = bytearray(); ኣቑም_ሽፋን = time.monotonic() + 시간제한
            while 확인표시 not in ሓበሬታ:
                if time.monotonic() > ኣቑም_ሽፋን or መስርሕ.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + ሓበሬታ.decode('utf-8', 'replace'))
                for 누름값, _ in መራፂ.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: ሓበሬታ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ሓበሬታ or b'FAIL ' in ሓበሬታ: raise AssertionError(ሓበሬታ)
            return ሓበሬታ.decode('utf-8', 'replace').replace('\r\n', '\n')
        def ሽፋን(መስመር):
            መስርሕ.stdin.write(መስመር.encode() + b'\n'); መስርሕ.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in ሽፋን('ftpd start')
            ፋይል_ምስጋር_ርክብ = ftplib.FTP(); ፋይል_ምስጋር_ርክብ.encoding = 'utf-8'; ፋይል_ምስጋር_ርክብ.connect('127.0.0.1', 접속번호, timeout=20); ፋይል_ምስጋር_ርክብ.login()
            ጽዕነት_ክፍሊት_ሓበሬታ = bytes(range(256)) * 32
            ፋይል_ምስጋር_ርክብ.storbinary('STOR binary.dat', io.BytesIO(ጽዕነት_ክፍሊት_ሓበሬታ))
            결과 = bytearray(); ፋይል_ምስጋር_ርክብ.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ጽዕነት_ክፍሊት_ሓበሬታ; assert ፋይል_ምስጋር_ርክብ.size('binary.dat') == len(ጽዕነት_ክፍሊት_ሓበሬታ)
            ምርግጋፅ_ጸብጻብ['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ፋይል_ምስጋር_ርክብ.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in ሽፋን('cat 한글.txt')
            assert '한글.txt' in ፋይል_ምስጋር_ርክብ.nlst()
            assert dict(ፋይል_ምስጋር_ርክብ.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            ምርግጋፅ_ጸብጻብ['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ፋይል_ምስጋር_ርክብ.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); ፋይል_ምስጋር_ርክብ.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == ጽዕነት_ክፍሊት_ሓበሬታ
            ምርግጋፅ_ጸብጻብ['checks'].append('oversized replacement rejected; previous file preserved')
            with ፋይል_ምስጋር_ርክብ.transfercmd('STOR pending.txt') as ስቐል_ፋይላት:
                # A control command must not change the active upload's destination.
                assert ፋይል_ምስጋር_ርክብ.size('binary.dat') == len(ጽዕነት_ክፍሊት_ሓበሬታ)
                ስቐል_ፋይላት.sendall(b'UPLOAD TARGET PRESERVED')
            assert ፋይል_ምስጋር_ርክብ.voidresp().startswith('226')
            결과 = bytearray(); ፋይል_ምስጋር_ርክብ.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); ፋይል_ምስጋር_ርክብ.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ጽዕነት_ክፍሊት_ሓበሬታ
            ፋይል_ምስጋር_ርክብ.delete('pending.txt')
            ምርግጋፅ_ጸብጻብ['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ፋይል_ምስጋር_ርክብ.storbinary('STOR 인사.jar', io.BytesIO(ሰንድ.getvalue()))
            ጽሑፍ = ሽፋን('java -jar 인사.jar 누리')
            assert 'JAR ተግብር_ትእዛዝ: 누리' in ጽሑፍ and '자체 ፍረ_ዋጋ ፋይል' in ጽሑፍ and 'exit 0' in ጽሑፍ, ጽሑፍ
            ጽሑፍ = ሽፋን('./인사.jar 세상')
            assert 'JAR ተግብር_ትእዛዝ: 세상' in ጽሑፍ and 'exit 0' in ጽሑፍ, ጽሑፍ
            ምርግጋፅ_ጸብጻብ['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct ሓበሬታ { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct ሓበሬታ ዋጋ = {합(10), 1.25}; if (ዋጋ.수 != 55 || ዋጋ.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = ክፈት_ፋይል("cc.txt", ኣንብብ_ጽሓፍ | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; ጸሓፍ_ፋይል_ሓበሬታ(문서, 인사, sizeof(인사)-1); ዕጸው_ፋይል(문서); ጸሓፍ_ፋይል_ሓበሬታ(1, 인사, sizeof(인사)-1); return 0; }\n'
            ፋይል_ምስጋር_ርክብ.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            ጽሑፍ = ሽፋን('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in ጽሑፍ and 'exit 0' in ጽሑፍ, ጽሑፍ
            ጽሑፍ = ሽፋን('run 한글.elf'); assert 'CC NATIVE PASS' in ጽሑፍ and 'exit 0' in ጽሑፍ, ጽሑፍ
            assert 'CC NATIVE PASS' in ሽፋን('cat cc.txt')
            실행파일 = bytearray(); ፋይል_ምስጋር_ርክብ.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ፋይል_ምስጋር_ርክብ.storbinary('STOR ቅዳሕ_ዋጋ.elf', io.BytesIO(실행파일)); ጽሑፍ = ሽፋን('run ቅዳሕ_ዋጋ.elf'); assert 'CC NATIVE PASS' in ጽሑፍ and 'exit 0' in ጽሑፍ, ጽሑፍ
            ፋይል_ምስጋር_ርክብ.storbinary('STOR ተግብር_ትእዛዝ', io.BytesIO(실행파일)); ጽሑፍ=ሽፋን('./ተግብር_ትእዛዝ');assert 'CC NATIVE PASS' in ጽሑፍ and 'exit 0' in ጽሑፍ,ጽሑፍ
            ፋይል_ምስጋር_ርክብ.storbinary('STOR ሽም.txt', io.BytesIO(실행파일)); ጽሑፍ=ሽፋን('./ሽም.txt');assert 'CC NATIVE PASS' in ጽሑፍ and 'exit 0' in ጽሑፍ,ጽሑፍ
            ሽፋን('rm ተግብር_ትእዛዝ ሽም.txt')
            ምርግጋፅ_ጸብጻብ['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            ሽፋን('rm binary.dat 한글.txt 한글.c 한글.elf ቅዳሕ_ዋጋ.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            ፋይል_ምስጋር_ርክብ.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            ጽሑፍ=ሽፋን('./리눅스인사');assert 'exit -8' in ጽሑፍ,ጽሑፍ
            ጽሑፍ=ሽፋን('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in ጽሑፍ,ጽሑፍ
            assert 'LINUX ELF FILE IO' in ሽፋን('cat linux.txt')
            ፋይል_ምስጋር_ርክብ.delete('리눅스인사');ፋይል_ምስጋር_ርክብ.delete('linux.txt')
            ፋይል_ምስጋር_ርክብ.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in ሽፋን('./거짓.elf');ፋይል_ምስጋር_ርክብ.delete('거짓.elf')
            ምርግጋፅ_ጸብጻብ['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket ኣላግብ = ትግርኛ.자체.연결통신.ኣላግብ("10.0.2.2", Integer.parseInt(args[0]));
 ኣላግብ.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ምንጪ = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ምንጪ.length;i++) if (ኣላግብ.getInputStream().read() != (ምንጪ[i]&255)) throw new RuntimeException("TCP mismatch");
 ኣላግብ.close();
 DatagramSocket 종단 = ትግርኛ.자체.통신.ክፈት(0); ትግርኛ.자체.통신.대기시간(종단, 500);
 ትግርኛ.자체.통신.ለኣኽ(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!ትግርኛ.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                ፋይል_ምስጋር_ርክብ.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                ጽሑፍ = ሽፋን('java 바깥통신 {} {}'.format(되돌림서버항목.ናይ_መተሓላላፊ_ተቖጻጻሪ_ፕሮቶኮል_ወደብ, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in ጽሑፍ and '10.0.2.2' in ጽሑፍ and 'exit 0' in ጽሑፍ, ጽሑፍ
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            ምርግጋፅ_ጸብጻብ['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ፋይል_ምስጋር_ርክብ.delete('바깥통신.class')
            ኣገልጋሊ_ምንጪ=결과자료/'서버시험.java'
            ኣገልጋሊ_ምንጪ.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket ኣገልጋሊ_ዋጋ = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket 손님 = ኣገልጋሊ_ዋጋ.accept();
  손님.getOutputStream().write(손님.getInputStream().read()+1); 손님.close(); ኣገልጋሊ_ዋጋ.close();
  byte[] ትሕዝቶ_ዋጋ = new byte[8]; DatagramPacket 전문 = new DatagramPacket(ትሕዝቶ_ዋጋ, ትሕዝቶ_ዋጋ.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(ኣገልጋሊ_ምንጪ)])
            ፋይል_ምስጋር_ርክብ.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            መስርሕ.stdin.write('java 서버시험\n'.encode());መስርሕ.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',ኣገልጋሊ_ወሓዚ_ወደብ),timeout=5) as መዘና_ዋጋ:
                መዘና_ዋጋ.sendall(b'A');assert መዘና_ዋጋ.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as መዘና_ዋጋ:
                መዘና_ዋጋ.settimeout(5);መዘና_ዋጋ.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert መዘና_ዋጋ.recvfrom(512)[0]==b'UDP-IN'
            ጽሑፍ=수신하기();assert 'INBOUND TCP UDP PASS' in ጽሑፍ and 'exit 0' in ጽሑፍ,ጽሑፍ
            ምርግጋፅ_ጸብጻብ['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ፋይል_ምስጋር_ርክብ.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } ትግርኛ.자체.출력.수쓰기(합); ትግርኛ.자체.ፋይል.ጸሓፍ("aot.txt", "한글 AOT ፋይል 😀"); ትግርኛ.자체.출력.ጸሓፍ_መስመር(ትግርኛ.자체.ፋይል.읽기("aot.txt")); } }'
            ፋይል_ምስጋር_ርክብ.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            ጽሑፍ = ሽፋን('javac 빛.java'); assert 'exit 0' in ጽሑፍ and 'Compiled:' in ጽሑፍ, ጽሑፍ
            ጽሑፍ = ሽፋን('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ጽሑፍ and 'exit 0' in ጽሑፍ, ጽሑፍ
            ጽሑፍ = ሽፋን('run 빛.elf'); assert '\n55\n' in ጽሑፍ and '한글 AOT ፋይል 😀' in ጽሑፍ and 'exit 0' in ጽሑፍ, ጽሑፍ
            자체실행파일 = bytearray(); ፋይል_ምስጋር_ርክብ.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            ጽሑፍ = ሽፋን('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in ጽሑፍ and 'unsupported' in ጽሑፍ, ጽሑፍ
            보존자료 = bytearray(); ፋይል_ምስጋር_ርክብ.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ፋይል_ምስጋር_ርክብ.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ፋይል_ምስጋር_ርክብ.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            ጽሑፍ = ሽፋን('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ጽሑፍ and 'exit 0' in ጽሑፍ, ጽሑፍ
            ጽሑፍ = ሽፋን('run 빛.elf'); assert '\n55\n' in ጽሑፍ and '한글 AOT ፋይል 😀' in ጽሑፍ and 'exit 0' in ጽሑፍ, ጽሑፍ
            ምርግጋፅ_ጸብጻብ['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            ምርግጋፅ_ጸብጻብ['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ቀዋሚ_ምንጪ=결과자료/'정적시험.java'
            ቀዋሚ_ምንጪ.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] ዋጋ = new int[] {기준, 합(10)};
  System.out.println(ዋጋ[0] + ዋጋ[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(ቀዋሚ_ምንጪ)])
            ፋይል_ምስጋር_ርክብ.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            ጽሑፍ=ሽፋን('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in ጽሑፍ,ጽሑፍ
            ጽሑፍ=ሽፋን('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in ጽሑፍ,ጽሑፍ
            ፋይል_ምስጋር_ርክብ.delete('정적시험.class');ፋይል_ምስጋር_ርክብ.delete('정적시험.elf')
            ምርግጋፅ_ጸብጻብ['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(ሰንድ.getvalue());손상자료[14]^=1
            ፋይል_ምስጋር_ርክብ.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            ጽሑፍ=ሽፋን('java -jar 인사.jar');assert 'Main-Class\nexit 1' in ጽሑፍ,ጽሑፍ
            ምርግጋፅ_ጸብጻብ['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ፋይል_ምስጋር_ርክብ.quit(); assert 'FTP stopped' in ሽፋን('ftpd stop')
            assert not 연결다리.ጌጋ, 연결다리.ጌጋ
            ምርግጋፅ_ጸብጻብ.update(passed=True, frames_to_guest=연결다리.커널수신틀수, frames_from_guest=연결다리.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in መራፂ.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            연결다리.ንግዚኡ_ደው_ኣብል_ፍጻመ.set()
            መስርሕ.terminate()
            try: መስርሕ.wait(timeout=5)
            except subprocess.TimeoutExpired: መስርሕ.kill(); መስርሕ.wait()
            መራፂ.close(); መስርሕ.stdin.close(); መስርሕ.stdout.close()
            ምርግጋፅ_ጸብጻብ['bridge_error'] = 연결다리.ጌጋ
            ምርግጋፅ_ጸብጻብ['frames_to_guest'] = 연결다리.커널수신틀수; ምርግጋፅ_ጸብጻብ['frames_from_guest'] = 연결다리.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(연결다리.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(ምርግጋፅ_ጸብጻብ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': ኣኺድ()
