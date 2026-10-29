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
from નેટવર્ક_બ્રિજ import નેટવર્ક_બ્રિજ
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ, આદેશ
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def ચલાવો_2():
    પરિમાણ_ડેટા = પ્રોજેક્ટ_રૂટ / 'build/verification/ftp'; પરિમાણ_ડેટા.mkdir(parents=True, exist_ok=True)
    માન્યતા_અહેવાલ = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((પ્રોજેક્ટ_રૂટ / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = પરિમાણ_ડેટા / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] દલીલો) throws Exception { ગુજરાતી.자체.આઉટપુટ.લખો_લાઇન("JAR અમલ_કરો_આદેશ: " + દલીલો[0]); ગુજરાતી.자체.ફાઈલ.લખો("jar.txt", "자체 કર્નેલ_મૂલ્ય ફાઈલ"); ગુજરાતી.자체.આઉટપુટ.લખો_લાઇન(ગુજરાતી.자체.ફાઈલ.વાંચો("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(પ્રોજેક્ટ_રૂટ/'build/java-library/classes'), '-d', str(પરિમાણ_ડેટા), str(자바원문)])
    સંગ્રહ = io.BytesIO()
    with zipfile.ZipFile(સંગ્રહ, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(પરિમાણ_ડેટા/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); પોર્ટ_નંબર = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); સર્વર_સ્ટ્રીમ_પૉર્ટ = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with નેટવર્ક_બ્રિજ(પોર્ટ_નંબર, ['tcp:{}:9300'.format(સર્વર_સ્ટ્રીમ_પૉર્ટ), 'udp:{}:9301'.format(서버전문접속번호)], કૅપ્ચર_કરો=True) as બ્રિજ:
        પ્રક્રિયા = subprocess.Popen(આદેશ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + બ્રિજ.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        પસંદકર્તા = selectors.DefaultSelector(); પસંદકર્તા.register(પ્રક્રિયા.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            ડેટા = bytearray(); અંત_કરો_ઑફસેટ = time.monotonic() + 시간제한
            while 확인표시 not in ડેટા:
                if time.monotonic() > અંત_કરો_ઑફસેટ or પ્રક્રિયા.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + ડેટા.decode('utf-8', 'replace'))
                for 누름값, _ in પસંદકર્તા.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: ડેટા.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ડેટા or b'FAIL ' in ડેટા: raise AssertionError(ડેટા)
            return ડેટા.decode('utf-8', 'replace').replace('\r\n', '\n')
        def શેલ(લાઇન):
            પ્રક્રિયા.stdin.write(લાઇન.encode() + b'\n'); પ્રક્રિયા.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in શેલ('ftpd start')
            ફાઇલ_સ્થાનાંતર_કનેક્શન = ftplib.FTP(); ફાઇલ_સ્થાનાંતર_કનેક્શન.encoding = 'utf-8'; ફાઇલ_સ્થાનાંતર_કનેક્શન.connect('127.0.0.1', પોર્ટ_નંબર, timeout=20); ફાઇલ_સ્થાનાંતર_કનેક્શન.login()
            પેલોડ_ડેટા = bytes(range(256)) * 32
            ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR binary.dat', io.BytesIO(પેલોડ_ડેટા))
            પરિમાણ = bytearray(); ફાઇલ_સ્થાનાંતર_કનેક્શન.retrbinary('RETR binary.dat', પરિમાણ.extend)
            assert પરિમાણ == પેલોડ_ડેટા; assert ફાઇલ_સ્થાનાંતર_કનેક્શન.size('binary.dat') == len(પેલોડ_ડેટા)
            માન્યતા_અહેવાલ['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in શેલ('cat 한글.txt')
            assert '한글.txt' in ફાઇલ_સ્થાનાંતર_કનેક્શન.nlst()
            assert dict(ફાઇલ_સ્થાનાંતર_કનેક્શન.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            માન્યતા_અહેવાલ['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            પરિમાણ = bytearray(); ફાઇલ_સ્થાનાંતર_કનેક્શન.retrbinary('RETR binary.dat', પરિમાણ.extend); assert પરિમાણ == પેલોડ_ડેટા
            માન્યતા_અહેવાલ['checks'].append('oversized replacement rejected; previous file preserved')
            with ફાઇલ_સ્થાનાંતર_કનેક્શન.transfercmd('STOR pending.txt') as અપલોડ_કરો_ફાઇલો:
                # A control command must not change the active upload's destination.
                assert ફાઇલ_સ્થાનાંતર_કનેક્શન.size('binary.dat') == len(પેલોડ_ડેટા)
                અપલોડ_કરો_ફાઇલો.sendall(b'UPLOAD TARGET PRESERVED')
            assert ફાઇલ_સ્થાનાંતર_કનેક્શન.voidresp().startswith('226')
            પરિમાણ = bytearray(); ફાઇલ_સ્થાનાંતર_કનેક્શન.retrbinary('RETR pending.txt', પરિમાણ.extend)
            assert પરિમાણ == b'UPLOAD TARGET PRESERVED'
            પરિમાણ = bytearray(); ફાઇલ_સ્થાનાંતર_કનેક્શન.retrbinary('RETR binary.dat', પરિમાણ.extend)
            assert પરિમાણ == પેલોડ_ડેટા
            ફાઇલ_સ્થાનાંતર_કનેક્શન.delete('pending.txt')
            માન્યતા_અહેવાલ['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR 인사.jar', io.BytesIO(સંગ્રહ.getvalue()))
            લખાણ = શેલ('java -jar 인사.jar 누리')
            assert 'JAR અમલ_કરો_આદેશ: 누리' in લખાણ and '자체 કર્નેલ_મૂલ્ય ફાઈલ' in લખાણ and 'exit 0' in લખાણ, લખાણ
            લખાણ = શેલ('./인사.jar 세상')
            assert 'JAR અમલ_કરો_આદેશ: 세상' in લખાણ and 'exit 0' in લખાણ, લખાણ
            માન્યતા_અહેવાલ['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct ડેટા { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct ડેટા મૂલ્ય = {합(10), 1.25}; if (મૂલ્ય.수 != 55 || મૂલ્ય.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = બનાવો_ફાઇલ("cc.txt", વાંચન_લેખન | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; લખો_ફાઇલ_ડેટા(문서, 인사, sizeof(인사)-1); બંધ_કરો_ફાઇલ(문서); લખો_ફાઇલ_ડેટા(1, 인사, sizeof(인사)-1); return 0; }\n'
            ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            લખાણ = શેલ('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in લખાણ and 'exit 0' in લખાણ, લખાણ
            લખાણ = શેલ('run 한글.elf'); assert 'CC NATIVE PASS' in લખાણ and 'exit 0' in લખાણ, લખાણ
            assert 'CC NATIVE PASS' in શેલ('cat cc.txt')
            실행파일 = bytearray(); ફાઇલ_સ્થાનાંતર_કનેક્શન.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR ઉદાહરણ_મૂલ્ય.elf', io.BytesIO(실행파일)); લખાણ = શેલ('run ઉદાહરણ_મૂલ્ય.elf'); assert 'CC NATIVE PASS' in લખાણ and 'exit 0' in લખાણ, લખાણ
            ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR અમલ_કરો_આદેશ', io.BytesIO(실행파일)); લખાણ=શેલ('./અમલ_કરો_આદેશ');assert 'CC NATIVE PASS' in લખાણ and 'exit 0' in લખાણ,લખાણ
            ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR નામ.txt', io.BytesIO(실행파일)); લખાણ=શેલ('./નામ.txt');assert 'CC NATIVE PASS' in લખાણ and 'exit 0' in લખાણ,લખાણ
            શેલ('rm અમલ_કરો_આદેશ નામ.txt')
            માન્યતા_અહેવાલ['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            શેલ('rm binary.dat 한글.txt 한글.c 한글.elf ઉદાહરણ_મૂલ્ય.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(પરિમાણ_ડેટા/'linux-reference')
            ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            લખાણ=શેલ('./리눅스인사');assert 'exit -8' in લખાણ,લખાણ
            લખાણ=શેલ('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in લખાણ,લખાણ
            assert 'LINUX ELF FILE IO' in શેલ('cat linux.txt')
            ફાઇલ_સ્થાનાંતર_કનેક્શન.delete('리눅스인사');ફાઇલ_સ્થાનાંતર_કનેક્શન.delete('linux.txt')
            ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in શેલ('./거짓.elf');ફાઇલ_સ્થાનાંતર_કનેક્શન.delete('거짓.elf')
            માન્યતા_અહેવાલ['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = પરિમાણ_ડેટા/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket સંપર્ક_કરો = ગુજરાતી.자체.연결통신.સંપર્ક_કરો("10.0.2.2", Integer.parseInt(args[0]));
 સંપર્ક_કરો.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] સ્રોત = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<સ્રોત.length;i++) if (સંપર્ક_કરો.getInputStream().read() != (સ્રોત[i]&255)) throw new RuntimeException("TCP mismatch");
 સંપર્ક_કરો.close();
 DatagramSocket 종단 = ગુજરાતી.자체.통신.ખોલો(0); ગુજરાતી.자체.통신.대기시간(종단, 500);
 ગુજરાતી.자체.통신.મોકલો(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!ગુજરાતી.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(પ્રોજેક્ટ_રૂટ/'build/java-library/classes'),'-d',str(પરિમાણ_ડેટા),str(통신원문)])
                ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR 바깥통신.class', io.BytesIO((પરિમાણ_ડેટા/'바깥통신.class').read_bytes()))
                લખાણ = શેલ('java 바깥통신 {} {}'.format(되돌림서버항목.પ્રસારણ_નિયંત્રણ_પ્રોટોકૉલ_પૉર્ટ, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in લખાણ and '10.0.2.2' in લખાણ and 'exit 0' in લખાણ, લખાણ
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            માન્યતા_અહેવાલ['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ફાઇલ_સ્થાનાંતર_કનેક્શન.delete('바깥통신.class')
            સર્વર_સ્રોત=પરિમાણ_ડેટા/'서버시험.java'
            સર્વર_સ્રોત.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket સર્વર_મૂલ્ય = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket અતિથિ_મૂલ્ય = સર્વર_મૂલ્ય.accept();
  અતિથિ_મૂલ્ય.getOutputStream().write(અતિથિ_મૂલ્ય.getInputStream().read()+1); અતિથિ_મૂલ્ય.close(); સર્વર_મૂલ્ય.close();
  byte[] સામગ્રી_મૂલ્ય = new byte[8]; DatagramPacket 전문 = new DatagramPacket(સામગ્રી_મૂલ્ય, સામગ્રી_મૂલ્ય.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(પરિમાણ_ડેટા),str(સર્વર_સ્રોત)])
            ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR 서버시험.class',io.BytesIO((પરિમાણ_ડેટા/'서버시험.class').read_bytes()))
            પ્રક્રિયા.stdin.write('java 서버시험\n'.encode());પ્રક્રિયા.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',સર્વર_સ્ટ્રીમ_પૉર્ટ),timeout=5) as પીઅર_મૂલ્ય:
                પીઅર_મૂલ્ય.sendall(b'A');assert પીઅર_મૂલ્ય.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as પીઅર_મૂલ્ય:
                પીઅર_મૂલ્ય.settimeout(5);પીઅર_મૂલ્ય.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert પીઅર_મૂલ્ય.recvfrom(512)[0]==b'UDP-IN'
            લખાણ=수신하기();assert 'INBOUND TCP UDP PASS' in લખાણ and 'exit 0' in લખાણ,લખાણ
            માન્યતા_અહેવાલ['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ફાઇલ_સ્થાનાંતર_કનેક્શન.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] દલીલો) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } ગુજરાતી.자체.આઉટપુટ.수쓰기(합); ગુજરાતી.자체.ફાઈલ.લખો("aot.txt", "한글 AOT ફાઈલ 😀"); ગુજરાતી.자체.આઉટપુટ.લખો_લાઇન(ગુજરાતી.자체.ફાઈલ.વાંચો("aot.txt")); } }'
            ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            લખાણ = શેલ('javac 빛.java'); assert 'exit 0' in લખાણ and 'Compiled:' in લખાણ, લખાણ
            લખાણ = શેલ('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in લખાણ and 'exit 0' in લખાણ, લખાણ
            લખાણ = શેલ('run 빛.elf'); assert '\n55\n' in લખાણ and '한글 AOT ફાઈલ 😀' in લખાણ and 'exit 0' in લખાણ, લખાણ
            자체실행파일 = bytearray(); ફાઇલ_સ્થાનાંતર_કનેક્શન.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            લખાણ = શેલ('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in લખાણ and 'unsupported' in લખાણ, લખાણ
            보존자료 = bytearray(); ફાઇલ_સ્થાનાંતર_કનેક્શન.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ફાઇલ_સ્થાનાંતર_કનેક્શન.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            લખાણ = શેલ('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in લખાણ and 'exit 0' in લખાણ, લખાણ
            લખાણ = શેલ('run 빛.elf'); assert '\n55\n' in લખાણ and '한글 AOT ફાઈલ 😀' in લખાણ and 'exit 0' in લખાણ, લખાણ
            માન્યતા_અહેવાલ['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            માન્યતા_અહેવાલ['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            સ્થિર_સ્રોત=પરિમાણ_ડેટા/'정적시험.java'
            સ્થિર_સ્રોત.write_text('''public class 정적시험 {
 static int પ્રોજેક્ટ_રૂટ = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] દલીલો) {
  int[] મૂલ્ય = new int[] {પ્રોજેક્ટ_રૂટ, 합(10)};
  System.out.println(મૂલ્ય[0] + મૂલ્ય[1]); System.out.println(દલીલો[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(પરિમાણ_ડેટા),str(સ્થિર_સ્રોત)])
            ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR 정적시험.class',io.BytesIO((પરિમાણ_ડેટા/'정적시험.class').read_bytes()))
            લખાણ=શેલ('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in લખાણ,લખાણ
            લખાણ=શેલ('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in લખાણ,લખાણ
            ફાઇલ_સ્થાનાંતર_કનેક્શન.delete('정적시험.class');ફાઇલ_સ્થાનાંતર_કનેક્શન.delete('정적시험.elf')
            માન્યતા_અહેવાલ['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(સંગ્રહ.getvalue());손상자료[14]^=1
            ફાઇલ_સ્થાનાંતર_કનેક્શન.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            લખાણ=શેલ('java -jar 인사.jar');assert 'Main-Class\nexit 1' in લખાણ,લખાણ
            માન્યતા_અહેવાલ['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ફાઇલ_સ્થાનાંતર_કનેક્શન.quit(); assert 'FTP stopped' in શેલ('ftpd stop')
            assert not બ્રિજ.ભૂલ, બ્રિજ.ભૂલ
            માન્યતા_અહેવાલ.update(passed=True, frames_to_guest=બ્રિજ.커널수신틀수, frames_from_guest=બ્રિજ.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in પસંદકર્તા.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            બ્રિજ.થોભો_ઇવેંટ.set()
            પ્રક્રિયા.terminate()
            try: પ્રક્રિયા.wait(timeout=5)
            except subprocess.TimeoutExpired: પ્રક્રિયા.kill(); પ્રક્રિયા.wait()
            પસંદકર્તા.close(); પ્રક્રિયા.stdin.close(); પ્રક્રિયા.stdout.close()
            માન્યતા_અહેવાલ['bridge_error'] = બ્રિજ.ભૂલ
            માન્યતા_અહેવાલ['frames_to_guest'] = બ્રિજ.커널수신틀수; માન્યતા_અહેવાલ['frames_from_guest'] = બ્રિજ.커널발신틀수
            (પરિમાણ_ડેટા/'packets.json').write_text(json.dumps(બ્રિજ.ટ્રૅસ_લૉગ,indent=2)+'\n')
            (પરિમાણ_ડેટા / 'serial.log').write_bytes(대화기록)
            (પરિમાણ_ડેટા / 'report.json').write_text(json.dumps(માન્યતા_અહેવાલ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': ચલાવો_2()
