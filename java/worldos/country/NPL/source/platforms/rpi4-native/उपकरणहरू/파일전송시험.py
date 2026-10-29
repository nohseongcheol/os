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
from सञ्जाल_ब्रिज import सञ्जाल_ब्रिज
from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट, आदेश
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def चलाउनुहोस्():
    मापन_लगत = परियोजना_रूट / 'build/verification/ftp'; मापन_लगत.mkdir(parents=True, exist_ok=True)
    वैधानिकता_रिपोर्ट = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((परियोजना_रूट / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = मापन_लगत / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] तर्क) throws Exception { नेपाली.निज.출력.लेख्नुहोस्_रेखा("JAR कार्यान्वयन_गर्नुहोस्_आदेश: " + तर्क[0]); नेपाली.निज.फाइल.लेख्नुहोस्("jar.txt", "निज कर्णेल_मान फाइल"); नेपाली.निज.출력.लेख्नुहोस्_रेखा(नेपाली.निज.फाइल.पढनुहोस्("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(परियोजना_रूट/'build/java-library/classes'), '-d', str(मापन_लगत), str(자바원문)])
    सङ्ग्रह = io.BytesIO()
    with zipfile.ZipFile(सङ्ग्रह, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(मापन_लगत/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); सर्भर_प्रवाह_पोर्ट = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with सञ्जाल_ब्रिज(접속번호, ['tcp:{}:9300'.format(सर्भर_प्रवाह_पोर्ट), 'udp:{}:9301'.format(서버전문접속번호)], क्यापचर=True) as ब्रिज:
        प्रक्रिया = subprocess.Popen(आदेश() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ब्रिज.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        चयनकर्ता = selectors.DefaultSelector(); चयनकर्ता.register(प्रक्रिया.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            लगत = bytearray(); समाप्त_गर्नुहोस्_अफसेट = time.monotonic() + 시간제한
            while 확인표시 not in लगत:
                if time.monotonic() > समाप्त_गर्नुहोस्_अफसेट or प्रक्रिया.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + लगत.decode('utf-8', 'replace'))
                for 누름값, _ in चयनकर्ता.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: लगत.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in लगत or b'FAIL ' in लगत: raise AssertionError(लगत)
            return लगत.decode('utf-8', 'replace').replace('\r\n', '\n')
        def शेल(रेखा):
            प्रक्रिया.stdin.write(रेखा.encode() + b'\n'); प्रक्रिया.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in शेल('ftpd start')
            फाइल_ट्रान्सफर_जडान = ftplib.FTP(); फाइल_ट्रान्सफर_जडान.encoding = 'utf-8'; फाइल_ट्रान्सफर_जडान.connect('127.0.0.1', 접속번호, timeout=20); फाइल_ट्रान्सफर_जडान.login()
            पेलोड_लगत = bytes(range(256)) * 32
            फाइल_ट्रान्सफर_जडान.storbinary('STOR binary.dat', io.BytesIO(पेलोड_लगत))
            मापन = bytearray(); फाइल_ट्रान्सफर_जडान.retrbinary('RETR binary.dat', मापन.extend)
            assert मापन == पेलोड_लगत; assert फाइल_ट्रान्सफर_जडान.size('binary.dat') == len(पेलोड_लगत)
            वैधानिकता_रिपोर्ट['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            फाइल_ट्रान्सफर_जडान.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in शेल('cat 한글.txt')
            assert '한글.txt' in फाइल_ट्रान्सफर_जडान.nlst()
            assert dict(फाइल_ट्रान्सफर_जडान.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            वैधानिकता_रिपोर्ट['checks'].append('UTF-8 filename and content visible in guest shell')
            try: फाइल_ट्रान्सफर_जडान.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            मापन = bytearray(); फाइल_ट्रान्सफर_जडान.retrbinary('RETR binary.dat', मापन.extend); assert मापन == पेलोड_लगत
            वैधानिकता_रिपोर्ट['checks'].append('oversized replacement rejected; previous file preserved')
            with फाइल_ट्रान्सफर_जडान.transfercmd('STOR pending.txt') as अपलोड_गर्नुहोस्_फाइलहरू:
                # A control command must not change the active upload's destination.
                assert फाइल_ट्रान्सफर_जडान.size('binary.dat') == len(पेलोड_लगत)
                अपलोड_गर्नुहोस्_फाइलहरू.sendall(b'UPLOAD TARGET PRESERVED')
            assert फाइल_ट्रान्सफर_जडान.voidresp().startswith('226')
            मापन = bytearray(); फाइल_ट्रान्सफर_जडान.retrbinary('RETR pending.txt', मापन.extend)
            assert मापन == b'UPLOAD TARGET PRESERVED'
            मापन = bytearray(); फाइल_ट्रान्सफर_जडान.retrbinary('RETR binary.dat', मापन.extend)
            assert मापन == पेलोड_लगत
            फाइल_ट्रान्सफर_जडान.delete('pending.txt')
            वैधानिकता_रिपोर्ट['checks'].append('interleaved SIZE cannot change the active STOR destination')
            फाइल_ट्रान्सफर_जडान.storbinary('STOR 인사.jar', io.BytesIO(सङ्ग्रह.getvalue()))
            पाठ = शेल('java -jar 인사.jar 누리')
            assert 'JAR कार्यान्वयन_गर्नुहोस्_आदेश: 누리' in पाठ and 'निज कर्णेल_मान फाइल' in पाठ and 'exit 0' in पाठ, पाठ
            पाठ = शेल('./인사.jar 세상')
            assert 'JAR कार्यान्वयन_गर्नुहोस्_आदेश: 세상' in पाठ and 'exit 0' in पाठ, पाठ
            वैधानिकता_रिपोर्ट['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct लगत { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct लगत मान = {합(10), 1.25}; if (मान.수 != 55 || मान.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = सिर्जना_फाइल("cc.txt", पढ्न_लेख्_न | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; लेख्नुहोस्_फाइल_लगत(문서, 인사, sizeof(인사)-1); बन्द_गर्नुहोस्_फाइल(문서); लेख्नुहोस्_फाइल_लगत(1, 인사, sizeof(인사)-1); return 0; }\n'
            फाइल_ट्रान्सफर_जडान.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            पाठ = शेल('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in पाठ and 'exit 0' in पाठ, पाठ
            पाठ = शेल('run 한글.elf'); assert 'CC NATIVE PASS' in पाठ and 'exit 0' in पाठ, पाठ
            assert 'CC NATIVE PASS' in शेल('cat cc.txt')
            실행파일 = bytearray(); फाइल_ट्रान्सफर_जडान.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            फाइल_ट्रान्सफर_जडान.storbinary('STOR उद्धरण_मान_37b3d3b1.elf', io.BytesIO(실행파일)); पाठ = शेल('run उद्धरण_मान_37b3d3b1.elf'); assert 'CC NATIVE PASS' in पाठ and 'exit 0' in पाठ, पाठ
            फाइल_ट्रान्सफर_जडान.storbinary('STOR कार्यान्वयन_गर्नुहोस्_आदेश', io.BytesIO(실행파일)); पाठ=शेल('./कार्यान्वयन_गर्नुहोस्_आदेश');assert 'CC NATIVE PASS' in पाठ and 'exit 0' in पाठ,पाठ
            फाइल_ट्रान्सफर_जडान.storbinary('STOR नाम.txt', io.BytesIO(실행파일)); पाठ=शेल('./नाम.txt');assert 'CC NATIVE PASS' in पाठ and 'exit 0' in पाठ,पाठ
            शेल('rm कार्यान्वयन_गर्नुहोस्_आदेश नाम.txt')
            वैधानिकता_रिपोर्ट['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            शेल('rm binary.dat 한글.txt 한글.c 한글.elf उद्धरण_मान_37b3d3b1.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(मापन_लगत/'linux-reference')
            फाइल_ट्रान्सफर_जडान.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            पाठ=शेल('./리눅스인사');assert 'exit -8' in पाठ,पाठ
            पाठ=शेल('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in पाठ,पाठ
            assert 'LINUX ELF FILE IO' in शेल('cat linux.txt')
            फाइल_ट्रान्सफर_जडान.delete('리눅스인사');फाइल_ट्रान्सफर_जडान.delete('linux.txt')
            फाइल_ट्रान्सफर_जडान.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in शेल('./거짓.elf');फाइल_ट्रान्सफर_जडान.delete('거짓.elf')
            वैधानिकता_रिपोर्ट['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = मापन_लगत/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket जडान = नेपाली.निज.연결통신.जडान("10.0.2.2", Integer.parseInt(args[0]));
 जडान.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] स्रोत = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<स्रोत.length;i++) if (जडान.getInputStream().read() != (स्रोत[i]&255)) throw new RuntimeException("TCP mismatch");
 जडान.close();
 DatagramSocket 종단 = नेपाली.निज.통신.खोल्नुहोस्(0); नेपाली.निज.통신.समय_सकियो(종단, 500);
 नेपाली.निज.통신.पठाउनुहोस्(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!नेपाली.निज.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(परियोजना_रूट/'build/java-library/classes'),'-d',str(मापन_लगत),str(통신원문)])
                फाइल_ट्रान्सफर_जडान.storbinary('STOR 바깥통신.class', io.BytesIO((मापन_लगत/'바깥통신.class').read_bytes()))
                पाठ = शेल('java 바깥통신 {} {}'.format(되돌림서버항목.टिसिपी_पोर्ट, 되돌림서버항목.युडिपी_पोर्ट))
                assert 'EXTERNAL TCP UDP PASS' in पाठ and '10.0.2.2' in पाठ and 'exit 0' in पाठ, पाठ
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            वैधानिकता_रिपोर्ट['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            फाइल_ट्रान्सफर_जडान.delete('바깥통신.class')
            सर्भर_स्रोत=मापन_लगत/'서버시험.java'
            सर्भर_स्रोत.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket सर्भर_मान = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket अतिथि_मान = सर्भर_मान.accept();
  अतिथि_मान.getOutputStream().write(अतिथि_मान.getInputStream().read()+1); अतिथि_मान.close(); सर्भर_मान.close();
  byte[] सामग्री_मान = new byte[8]; DatagramPacket 전문 = new DatagramPacket(सामग्री_मान, सामग्री_मान.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(मापन_लगत),str(सर्भर_स्रोत)])
            फाइल_ट्रान्सफर_जडान.storbinary('STOR 서버시험.class',io.BytesIO((मापन_लगत/'서버시험.class').read_bytes()))
            प्रक्रिया.stdin.write('java 서버시험\n'.encode());प्रक्रिया.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',सर्भर_प्रवाह_पोर्ट),timeout=5) as समान_मान:
                समान_मान.sendall(b'A');assert समान_मान.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as समान_मान:
                समान_मान.settimeout(5);समान_मान.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert समान_मान.recvfrom(512)[0]==b'UDP-IN'
            पाठ=수신하기();assert 'INBOUND TCP UDP PASS' in पाठ and 'exit 0' in पाठ,पाठ
            वैधानिकता_रिपोर्ट['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            फाइल_ट्रान्सफर_जडान.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] तर्क) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } नेपाली.निज.출력.수쓰기(합); नेपाली.निज.फाइल.लेख्नुहोस्("aot.txt", "한글 AOT फाइल 😀"); नेपाली.निज.출력.लेख्नुहोस्_रेखा(नेपाली.निज.फाइल.पढनुहोस्("aot.txt")); } }'
            फाइल_ट्रान्सफर_जडान.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            पाठ = शेल('javac 빛.java'); assert 'exit 0' in पाठ and 'Compiled:' in पाठ, पाठ
            पाठ = शेल('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in पाठ and 'exit 0' in पाठ, पाठ
            पाठ = शेल('run 빛.elf'); assert '\n55\n' in पाठ and '한글 AOT फाइल 😀' in पाठ and 'exit 0' in पाठ, पाठ
            자체실행파일 = bytearray(); फाइल_ट्रान्सफर_जडान.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            पाठ = शेल('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in पाठ and 'unsupported' in पाठ, पाठ
            보존자료 = bytearray(); फाइल_ट्रान्सफर_जडान.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); फाइल_ट्रान्सफर_जडान.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            फाइल_ट्रान्सफर_जडान.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            पाठ = शेल('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in पाठ and 'exit 0' in पाठ, पाठ
            पाठ = शेल('run 빛.elf'); assert '\n55\n' in पाठ and '한글 AOT फाइल 😀' in पाठ and 'exit 0' in पाठ, पाठ
            वैधानिकता_रिपोर्ट['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            वैधानिकता_रिपोर्ट['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            तथ्याङ्कित_स्रोत=मापन_लगत/'정적시험.java'
            तथ्याङ्कित_स्रोत.write_text('''public class 정적시험 {
 static int परियोजना_रूट = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] तर्क) {
  int[] मान = new int[] {परियोजना_रूट, 합(10)};
  System.out.println(मान[0] + मान[1]); System.out.println(तर्क[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(मापन_लगत),str(तथ्याङ्कित_स्रोत)])
            फाइल_ट्रान्सफर_जडान.storbinary('STOR 정적시험.class',io.BytesIO((मापन_लगत/'정적시험.class').read_bytes()))
            पाठ=शेल('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in पाठ,पाठ
            पाठ=शेल('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in पाठ,पाठ
            फाइल_ट्रान्सफर_जडान.delete('정적시험.class');फाइल_ट्रान्सफर_जडान.delete('정적시험.elf')
            वैधानिकता_रिपोर्ट['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(सङ्ग्रह.getvalue());손상자료[14]^=1
            फाइल_ट्रान्सफर_जडान.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            पाठ=शेल('java -jar 인사.jar');assert 'Main-Class\nexit 1' in पाठ,पाठ
            वैधानिकता_रिपोर्ट['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            फाइल_ट्रान्सफर_जडान.quit(); assert 'FTP stopped' in शेल('ftpd stop')
            assert not ब्रिज.त्रुटि, ब्रिज.त्रुटि
            वैधानिकता_रिपोर्ट.update(passed=True, frames_to_guest=ब्रिज.커널수신틀수, frames_from_guest=ब्रिज.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in चयनकर्ता.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            ब्रिज.पज_घटना.set()
            प्रक्रिया.terminate()
            try: प्रक्रिया.wait(timeout=5)
            except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait()
            चयनकर्ता.close(); प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close()
            वैधानिकता_रिपोर्ट['bridge_error'] = ब्रिज.त्रुटि
            वैधानिकता_रिपोर्ट['frames_to_guest'] = ब्रिज.커널수신틀수; वैधानिकता_रिपोर्ट['frames_from_guest'] = ब्रिज.커널발신틀수
            (मापन_लगत/'packets.json').write_text(json.dumps(ब्रिज.추적기록,indent=2)+'\n')
            (मापन_लगत / 'serial.log').write_bytes(대화기록)
            (मापन_लगत / 'report.json').write_text(json.dumps(वैधानिकता_रिपोर्ट, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': चलाउनुहोस्()
