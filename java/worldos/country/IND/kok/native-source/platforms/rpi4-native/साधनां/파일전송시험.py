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
from नॅटवर्क_ब्रिज import नॅटवर्क_ब्रिज
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट, आदेश
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def चलोवप():
    मेजप_डेटा = प्रॉजॅक्ट_रूट / 'build/verification/ftp'; मेजप_डेटा.mkdir(parents=True, exist_ok=True)
    वैधताय_अहवाल = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((प्रॉजॅक्ट_रूट / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = मेजप_डेटा / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.बरोवचें_रेग("JAR पाळो_दिवचो_आदेश: " + 인수[0]); 한국어.자체.फायल.बरोवचें("jar.txt", "자체 कर्नेल_मोल फायल"); 한국어.자체.출력.बरोवचें_रेग(한국어.자체.फायल.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(प्रॉजॅक्ट_रूट/'build/java-library/classes'), '-d', str(मेजप_डेटा), str(자바원문)])
    संग्रह = io.BytesIO()
    with zipfile.ZipFile(संग्रह, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(मेजप_डेटा/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); सर्वर_Stream_पोर्ट = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with नॅटवर्क_ब्रिज(접속번호, ['tcp:{}:9300'.format(सर्वर_Stream_पोर्ट), 'udp:{}:9301'.format(서버전문접속번호)], कॅप्चर=True) as ब्रिज:
        प्रक्रिया = subprocess.Popen(आदेश() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ब्रिज.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        वेंचक = selectors.DefaultSelector(); वेंचक.register(प्रक्रिया.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            डेटा = bytearray(); सोपोवचें_ऑफसॅट = time.monotonic() + 시간제한
            while 확인표시 not in डेटा:
                if time.monotonic() > सोपोवचें_ऑफसॅट or प्रक्रिया.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + डेटा.decode('utf-8', 'replace'))
                for 누름값, _ in वेंचक.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: डेटा.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in डेटा or b'FAIL ' in डेटा: raise AssertionError(डेटा)
            return डेटा.decode('utf-8', 'replace').replace('\r\n', '\n')
        def शॅल(रेग):
            प्रक्रिया.stdin.write(रेग.encode() + b'\n'); प्रक्रिया.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in शॅल('ftpd start')
            फायल_ट्रान्सफर_कनॅक्शन = ftplib.FTP(); फायल_ट्रान्सफर_कनॅक्शन.encoding = 'utf-8'; फायल_ट्रान्सफर_कनॅक्शन.connect('127.0.0.1', 접속번호, timeout=20); फायल_ट्रान्सफर_कनॅक्शन.login()
            पेलोड_डेटा = bytes(range(256)) * 32
            फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR binary.dat', io.BytesIO(पेलोड_डेटा))
            मेजप = bytearray(); फायल_ट्रान्सफर_कनॅक्शन.retrbinary('RETR binary.dat', मेजप.extend)
            assert मेजप == पेलोड_डेटा; assert फायल_ट्रान्सफर_कनॅक्शन.size('binary.dat') == len(पेलोड_डेटा)
            वैधताय_अहवाल['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in शॅल('cat 한글.txt')
            assert '한글.txt' in फायल_ट्रान्सफर_कनॅक्शन.nlst()
            assert dict(फायल_ट्रान्सफर_कनॅक्शन.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            वैधताय_अहवाल['checks'].append('UTF-8 filename and content visible in guest shell')
            try: फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            मेजप = bytearray(); फायल_ट्रान्सफर_कनॅक्शन.retrbinary('RETR binary.dat', मेजप.extend); assert मेजप == पेलोड_डेटा
            वैधताय_अहवाल['checks'].append('oversized replacement rejected; previous file preserved')
            with फायल_ट्रान्सफर_कनॅक्शन.transfercmd('STOR pending.txt') as अपलोड_करचें_फायली:
                # A control command must not change the active upload's destination.
                assert फायल_ट्रान्सफर_कनॅक्शन.size('binary.dat') == len(पेलोड_डेटा)
                अपलोड_करचें_फायली.sendall(b'UPLOAD TARGET PRESERVED')
            assert फायल_ट्रान्सफर_कनॅक्शन.voidresp().startswith('226')
            मेजप = bytearray(); फायल_ट्रान्सफर_कनॅक्शन.retrbinary('RETR pending.txt', मेजप.extend)
            assert मेजप == b'UPLOAD TARGET PRESERVED'
            मेजप = bytearray(); फायल_ट्रान्सफर_कनॅक्शन.retrbinary('RETR binary.dat', मेजप.extend)
            assert मेजप == पेलोड_डेटा
            फायल_ट्रान्सफर_कनॅक्शन.delete('pending.txt')
            वैधताय_अहवाल['checks'].append('interleaved SIZE cannot change the active STOR destination')
            फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR 인사.jar', io.BytesIO(संग्रह.getvalue()))
            SMS = शॅल('java -jar 인사.jar 누리')
            assert 'JAR पाळो_दिवचो_आदेश: 누리' in SMS and '자체 कर्नेल_मोल फायल' in SMS and 'exit 0' in SMS, SMS
            SMS = शॅल('./인사.jar 세상')
            assert 'JAR पाळो_दिवचो_आदेश: 세상' in SMS and 'exit 0' in SMS, SMS
            वैधताय_अहवाल['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct डेटा { int 수; double 비율; };\nint SUM_मोल(int n) { return n ? n + SUM_मोल(n-1) : 0; }\nint main(void) { struct डेटा मोल = {SUM_मोल(10), 1.25}; if (मोल.수 != 55 || मोल.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = उगडचें_फायल("cc.txt", वाचन_बरप | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; बरोवचें_फायल_डेटा(문서, 인사, sizeof(인사)-1); शेवट_फायल(문서); बरोवचें_फायल_डेटा(1, 인사, sizeof(인사)-1); return 0; }\n'
            फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            SMS = शॅल('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = शॅल('run 한글.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            assert 'CC NATIVE PASS' in शॅल('cat cc.txt')
            실행파일 = bytearray(); फायल_ट्रान्सफर_कनॅक्शन.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR इन्सटन्स_मोल.elf', io.BytesIO(실행파일)); SMS = शॅल('run इन्सटन्स_मोल.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR पाळो_दिवचो_आदेश', io.BytesIO(실행파일)); SMS=शॅल('./पाळो_दिवचो_आदेश');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR नांव.txt', io.BytesIO(실행파일)); SMS=शॅल('./नांव.txt');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            शॅल('rm पाळो_दिवचो_आदेश नांव.txt')
            वैधताय_अहवाल['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            शॅल('rm binary.dat 한글.txt 한글.c 한글.elf इन्सटन्स_मोल.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(मेजप_डेटा/'linux-reference')
            फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            SMS=शॅल('./리눅스인사');assert 'exit -8' in SMS,SMS
            SMS=शॅल('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in SMS,SMS
            assert 'LINUX ELF FILE IO' in शॅल('cat linux.txt')
            फायल_ट्रान्सफर_कनॅक्शन.delete('리눅스인사');फायल_ट्रान्सफर_कनॅक्शन.delete('linux.txt')
            फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR FALSE_मोल.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in शॅल('./FALSE_मोल.elf');फायल_ट्रान्सफर_कनॅक्शन.delete('FALSE_मोल.elf')
            वैधताय_अहवाल['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = मेजप_डेटा/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket कनॅक्ट = 한국어.자체.연결통신.कनॅक्ट("10.0.2.2", Integer.parseInt(args[0]));
 कनॅक्ट.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] स्त्रोत = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<स्त्रोत.length;i++) if (कनॅक्ट.getInputStream().read() != (स्त्रोत[i]&255)) throw new RuntimeException("TCP mismatch");
 कनॅक्ट.close();
 DatagramSocket 종단 = 한국어.자체.통신.उगडचें(0); 한국어.자체.통신.कालबाह्य(종단, 500);
 한국어.자체.통신.धाडचें(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(प्रॉजॅक्ट_रूट/'build/java-library/classes'),'-d',str(मेजप_डेटा),str(통신원문)])
                फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR 바깥통신.class', io.BytesIO((मेजप_डेटा/'바깥통신.class').read_bytes()))
                SMS = शॅल('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_पोर्ट, 되돌림서버항목.UDP_पोर्ट))
                assert 'EXTERNAL TCP UDP PASS' in SMS and '10.0.2.2' in SMS and 'exit 0' in SMS, SMS
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            वैधताय_अहवाल['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            फायल_ट्रान्सफर_कनॅक्शन.delete('바깥통신.class')
            सर्वर_स्त्रोत=मेजप_डेटा/'서버시험.java'
            सर्वर_स्त्रोत.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket सर्वर_मोल = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket सोयरो_मोल = सर्वर_मोल.accept();
  सोयरो_मोल.getOutputStream().write(सोयरो_मोल.getInputStream().read()+1); सोयरो_मोल.close(); सर्वर_मोल.close();
  byte[] अनुक्रमणिका_मोल = new byte[8]; DatagramPacket 전문 = new DatagramPacket(अनुक्रमणिका_मोल, अनुक्रमणिका_मोल.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(मेजप_डेटा),str(सर्वर_स्त्रोत)])
            फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR 서버시험.class',io.BytesIO((मेजप_डेटा/'서버시험.class').read_bytes()))
            प्रक्रिया.stdin.write('java 서버시험\n'.encode());प्रक्रिया.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',सर्वर_Stream_पोर्ट),timeout=5) as पीयर_मोल:
                पीयर_मोल.sendall(b'A');assert पीयर_मोल.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as पीयर_मोल:
                पीयर_मोल.settimeout(5);पीयर_मोल.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert पीयर_मोल.recvfrom(512)[0]==b'UDP-IN'
            SMS=수신하기();assert 'INBOUND TCP UDP PASS' in SMS and 'exit 0' in SMS,SMS
            वैधताय_अहवाल['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            फायल_ट्रान्सफर_कनॅक्शन.delete('서버시험.class')
            समजावणी_SEQUENCE = 'public class 빛 { public static void main(String[] 인수) throws Exception { int SUM_मोल = 0; int 수 = 1; while (수 <= 10) { SUM_मोल = SUM_मोल + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(SUM_मोल); 한국어.자체.फायल.बरोवचें("aot.txt", "한글 AOT फायल 😀"); 한국어.자체.출력.बरोवचें_रेग(한국어.자체.फायल.읽기("aot.txt")); } }'
            फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR 빛.java', io.BytesIO(समजावणी_SEQUENCE.encode()))
            SMS = शॅल('javac 빛.java'); assert 'exit 0' in SMS and 'Compiled:' in SMS, SMS
            SMS = शॅल('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = शॅल('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT फायल 😀' in SMS and 'exit 0' in SMS, SMS
            자체실행파일 = bytearray(); फायल_ट्रान्सफर_कनॅक्शन.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            SMS = शॅल('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in SMS and 'unsupported' in SMS, SMS
            보존자료 = bytearray(); फायल_ट्रान्सफर_कनॅक्शन.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); फायल_ट्रान्सफर_कनॅक्शन.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            SMS = शॅल('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = शॅल('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT फायल 😀' in SMS and 'exit 0' in SMS, SMS
            वैधताय_अहवाल['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            वैधताय_अहवाल['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            थीर_स्त्रोत=मेजप_डेटा/'정적시험.java'
            थीर_स्त्रोत.write_text('''public class 정적시험 {
 static int प्रॉजॅक्ट_रूट = 3;
 static int SUM_मोल(int n) { return n == 0 ? 0 : n + SUM_मोल(n-1); }
 public static void main(String[] 인수) {
  int[] मोल = new int[] {प्रॉजॅक्ट_रूट, SUM_मोल(10)};
  System.out.println(मोल[0] + मोल[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(मेजप_डेटा),str(थीर_स्त्रोत)])
            फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR 정적시험.class',io.BytesIO((मेजप_डेटा/'정적시험.class').read_bytes()))
            SMS=शॅल('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in SMS,SMS
            SMS=शॅल('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in SMS,SMS
            फायल_ट्रान्सफर_कनॅक्शन.delete('정적시험.class');फायल_ट्रान्सफर_कनॅक्शन.delete('정적시험.elf')
            वैधताय_अहवाल['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(संग्रह.getvalue());손상자료[14]^=1
            फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            SMS=शॅल('java -jar 인사.jar');assert 'Main-Class\nexit 1' in SMS,SMS
            वैधताय_अहवाल['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            फायल_ट्रान्सफर_कनॅक्शन.quit(); assert 'FTP stopped' in शॅल('ftpd stop')
            assert not ब्रिज.चूक, ब्रिज.चूक
            वैधताय_अहवाल.update(passed=True, frames_to_guest=ब्रिज.커널수신틀수, frames_from_guest=ब्रिज.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in वेंचक.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            ब्रिज.थांबणी_प्रसंग.set()
            प्रक्रिया.terminate()
            try: प्रक्रिया.wait(timeout=5)
            except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait()
            वेंचक.close(); प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close()
            वैधताय_अहवाल['bridge_error'] = ब्रिज.चूक
            वैधताय_अहवाल['frames_to_guest'] = ब्रिज.커널수신틀수; वैधताय_अहवाल['frames_from_guest'] = ब्रिज.커널발신틀수
            (मेजप_डेटा/'packets.json').write_text(json.dumps(ब्रिज.추적기록,indent=2)+'\n')
            (मेजप_डेटा / 'serial.log').write_bytes(대화기록)
            (मेजप_डेटा / 'report.json').write_text(json.dumps(वैधताय_अहवाल, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': चलोवप()
