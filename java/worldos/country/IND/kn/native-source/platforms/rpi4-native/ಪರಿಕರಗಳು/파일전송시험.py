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
from ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ import ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ, ಆಜ್ಞೆ
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def ಚಲಾಯಿಸು_2():
    ಮಾಪನ_ಡೇಟಾ = ಬಿಂಬಿಸು_ಮೂಲ / 'build/verification/ftp'; ಮಾಪನ_ಡೇಟಾ.mkdir(parents=True, exist_ok=True)
    ದೃಢೀಕರಣ_ವರದಿ = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = ಮಾಪನ_ಡೇಟಾ / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { ಕನ್ನಡ.자체.ಔಟ್_ಪುಟ್.ಬರೆ_ಸಾಲು("JAR ಪೂರೈಸು_ಆದೇಶ: " + 인수[0]); ಕನ್ನಡ.자체.ಕಡತ.ಬರೆ("jar.txt", "자체 ಕರ್ನಲ್_ಮೌಲ್ಯ ಕಡತ"); ಕನ್ನಡ.자체.ಔಟ್_ಪುಟ್.ಬರೆ_ಸಾಲು(ಕನ್ನಡ.자체.ಕಡತ.ಓದು("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ಬಿಂಬಿಸು_ಮೂಲ/'build/java-library/classes'), '-d', str(ಮಾಪನ_ಡೇಟಾ), str(자바원문)])
    ಅರ್ಖೀವ್ = io.BytesIO()
    with zipfile.ZipFile(ಅರ್ಖೀವ್, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(ಮಾಪನ_ಡೇಟಾ/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); ಪೋರ್ಟ್_ಸಂಖ್ಯೆ = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); ಸರ್ವರ್_ಸ್ಟ್ರೀಮ್_ಪೋರ್ಟ್ = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ(ಪೋರ್ಟ್_ಸಂಖ್ಯೆ, ['tcp:{}:9300'.format(ಸರ್ವರ್_ಸ್ಟ್ರೀಮ್_ಪೋರ್ಟ್), 'udp:{}:9301'.format(서버전문접속번호)], ಸೆರೆಹಿಡಿ=True) as ಸೇತುವೆ:
        ಪ್ರಕ್ರಿಯೆ = subprocess.Popen(ಆಜ್ಞೆ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ಸೇತುವೆ.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        ಸೆಲೆಕ್ಟರ್ = selectors.DefaultSelector(); ಸೆಲೆಕ್ಟರ್.register(ಪ್ರಕ್ರಿಯೆ.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            ಡೇಟಾ = bytearray(); ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್ = time.monotonic() + 시간제한
            while 확인표시 not in ಡೇಟಾ:
                if time.monotonic() > ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್ or ಪ್ರಕ್ರಿಯೆ.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + ಡೇಟಾ.decode('utf-8', 'replace'))
                for 누름값, _ in ಸೆಲೆಕ್ಟರ್.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: ಡೇಟಾ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ಡೇಟಾ or b'FAIL ' in ಡೇಟಾ: raise AssertionError(ಡೇಟಾ)
            return ಡೇಟಾ.decode('utf-8', 'replace').replace('\r\n', '\n')
        def ಶೆಲ್(ಸಾಲು):
            ಪ್ರಕ್ರಿಯೆ.stdin.write(ಸಾಲು.encode() + b'\n'); ಪ್ರಕ್ರಿಯೆ.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in ಶೆಲ್('ftpd start')
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ = ftplib.FTP(); ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.encoding = 'utf-8'; ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.connect('127.0.0.1', ಪೋರ್ಟ್_ಸಂಖ್ಯೆ, timeout=20); ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.login()
            ಪೇಲೋಡ್_ಡೇಟಾ = bytes(range(256)) * 32
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR binary.dat', io.BytesIO(ಪೇಲೋಡ್_ಡೇಟಾ))
            ಮಾಪನ = bytearray(); ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.retrbinary('RETR binary.dat', ಮಾಪನ.extend)
            assert ಮಾಪನ == ಪೇಲೋಡ್_ಡೇಟಾ; assert ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.size('binary.dat') == len(ಪೇಲೋಡ್_ಡೇಟಾ)
            ದೃಢೀಕರಣ_ವರದಿ['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in ಶೆಲ್('cat 한글.txt')
            assert '한글.txt' in ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.nlst()
            assert dict(ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            ದೃಢೀಕರಣ_ವರದಿ['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            ಮಾಪನ = bytearray(); ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.retrbinary('RETR binary.dat', ಮಾಪನ.extend); assert ಮಾಪನ == ಪೇಲೋಡ್_ಡೇಟಾ
            ದೃಢೀಕರಣ_ವರದಿ['checks'].append('oversized replacement rejected; previous file preserved')
            with ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.transfercmd('STOR pending.txt') as ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು:
                # A control command must not change the active upload's destination.
                assert ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.size('binary.dat') == len(ಪೇಲೋಡ್_ಡೇಟಾ)
                ಅಪ್_ಲೋಡ್_ಫೈಲ್_ಗಳು.sendall(b'UPLOAD TARGET PRESERVED')
            assert ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.voidresp().startswith('226')
            ಮಾಪನ = bytearray(); ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.retrbinary('RETR pending.txt', ಮಾಪನ.extend)
            assert ಮಾಪನ == b'UPLOAD TARGET PRESERVED'
            ಮಾಪನ = bytearray(); ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.retrbinary('RETR binary.dat', ಮಾಪನ.extend)
            assert ಮಾಪನ == ಪೇಲೋಡ್_ಡೇಟಾ
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.delete('pending.txt')
            ದೃಢೀಕರಣ_ವರದಿ['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR 인사.jar', io.BytesIO(ಅರ್ಖೀವ್.getvalue()))
            ಪಠ್ಯ = ಶೆಲ್('java -jar 인사.jar 누리')
            assert 'JAR ಪೂರೈಸು_ಆದೇಶ: 누리' in ಪಠ್ಯ and '자체 ಕರ್ನಲ್_ಮೌಲ್ಯ ಕಡತ' in ಪಠ್ಯ and 'exit 0' in ಪಠ್ಯ, ಪಠ್ಯ
            ಪಠ್ಯ = ಶೆಲ್('./인사.jar 세상')
            assert 'JAR ಪೂರೈಸು_ಆದೇಶ: 세상' in ಪಠ್ಯ and 'exit 0' in ಪಠ್ಯ, ಪಠ್ಯ
            ದೃಢೀಕರಣ_ವರದಿ['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct ಡೇಟಾ { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct ಡೇಟಾ ಮೌಲ್ಯ = {합(10), 1.25}; if (ಮೌಲ್ಯ.수 != 55 || ಮೌಲ್ಯ.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = ರಚಿಸು_ಫೈಲ್("cc.txt", ಓದು_ಬರೆ | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; ಬರೆ_ಫೈಲ್_ಡೇಟಾ(문서, 인사, sizeof(인사)-1); ಮುಚ್ಚು_ಫೈಲ್(문서); ಬರೆ_ಫೈಲ್_ಡೇಟಾ(1, 인사, sizeof(인사)-1); return 0; }\n'
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            ಪಠ್ಯ = ಶೆಲ್('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in ಪಠ್ಯ and 'exit 0' in ಪಠ್ಯ, ಪಠ್ಯ
            ಪಠ್ಯ = ಶೆಲ್('run 한글.elf'); assert 'CC NATIVE PASS' in ಪಠ್ಯ and 'exit 0' in ಪಠ್ಯ, ಪಠ್ಯ
            assert 'CC NATIVE PASS' in ಶೆಲ್('cat cc.txt')
            실행파일 = bytearray(); ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR ನಕಲಿಸು_ಮೌಲ್ಯ.elf', io.BytesIO(실행파일)); ಪಠ್ಯ = ಶೆಲ್('run ನಕಲಿಸು_ಮೌಲ್ಯ.elf'); assert 'CC NATIVE PASS' in ಪಠ್ಯ and 'exit 0' in ಪಠ್ಯ, ಪಠ್ಯ
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR ಪೂರೈಸು_ಆದೇಶ', io.BytesIO(실행파일)); ಪಠ್ಯ=ಶೆಲ್('./ಪೂರೈಸು_ಆದೇಶ');assert 'CC NATIVE PASS' in ಪಠ್ಯ and 'exit 0' in ಪಠ್ಯ,ಪಠ್ಯ
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR ಹೆಸರು.txt', io.BytesIO(실행파일)); ಪಠ್ಯ=ಶೆಲ್('./ಹೆಸರು.txt');assert 'CC NATIVE PASS' in ಪಠ್ಯ and 'exit 0' in ಪಠ್ಯ,ಪಠ್ಯ
            ಶೆಲ್('rm ಪೂರೈಸು_ಆದೇಶ ಹೆಸರು.txt')
            ದೃಢೀಕರಣ_ವರದಿ['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            ಶೆಲ್('rm binary.dat 한글.txt 한글.c 한글.elf ನಕಲಿಸು_ಮೌಲ್ಯ.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(ಮಾಪನ_ಡೇಟಾ/'linux-reference')
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            ಪಠ್ಯ=ಶೆಲ್('./리눅스인사');assert 'exit -8' in ಪಠ್ಯ,ಪಠ್ಯ
            ಪಠ್ಯ=ಶೆಲ್('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in ಪಠ್ಯ,ಪಠ್ಯ
            assert 'LINUX ELF FILE IO' in ಶೆಲ್('cat linux.txt')
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.delete('리눅스인사');ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.delete('linux.txt')
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in ಶೆಲ್('./거짓.elf');ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.delete('거짓.elf')
            ದೃಢೀಕರಣ_ವರದಿ['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = ಮಾಪನ_ಡೇಟಾ/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು = ಕನ್ನಡ.자체.연결통신.ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು("10.0.2.2", Integer.parseInt(args[0]));
 ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ಮೂಲ = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ಮೂಲ.length;i++) if (ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.getInputStream().read() != (ಮೂಲ[i]&255)) throw new RuntimeException("TCP mismatch");
 ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.close();
 DatagramSocket 종단 = ಕನ್ನಡ.자체.통신.ತೆರೆ(0); ಕನ್ನಡ.자체.통신.대기시간(종단, 500);
 ಕನ್ನಡ.자체.통신.ಕಳುಹಿಸಿ(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!ಕನ್ನಡ.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(ಬಿಂಬಿಸು_ಮೂಲ/'build/java-library/classes'),'-d',str(ಮಾಪನ_ಡೇಟಾ),str(통신원문)])
                ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR 바깥통신.class', io.BytesIO((ಮಾಪನ_ಡೇಟಾ/'바깥통신.class').read_bytes()))
                ಪಠ್ಯ = ಶೆಲ್('java 바깥통신 {} {}'.format(되돌림서버항목.ಪ್ರಸಾರ_ನಿಯಂತ್ರಣ_ಪ್ರೊಟೋಕಾಲ್_ಪೋರ್ಟ್, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in ಪಠ್ಯ and '10.0.2.2' in ಪಠ್ಯ and 'exit 0' in ಪಠ್ಯ, ಪಠ್ಯ
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            ದೃಢೀಕರಣ_ವರದಿ['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.delete('바깥통신.class')
            ಸರ್ವರ್_ಮೂಲ=ಮಾಪನ_ಡೇಟಾ/'서버시험.java'
            ಸರ್ವರ್_ಮೂಲ.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket ಸರ್ವರ್_ಮೌಲ್ಯ = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket ಅತಿಥಿ_ಮೌಲ್ಯ = ಸರ್ವರ್_ಮೌಲ್ಯ.accept();
  ಅತಿಥಿ_ಮೌಲ್ಯ.getOutputStream().write(ಅತಿಥಿ_ಮೌಲ್ಯ.getInputStream().read()+1); ಅತಿಥಿ_ಮೌಲ್ಯ.close(); ಸರ್ವರ್_ಮೌಲ್ಯ.close();
  byte[] ವಿಷಯ_ಮೌಲ್ಯ = new byte[8]; DatagramPacket 전문 = new DatagramPacket(ವಿಷಯ_ಮೌಲ್ಯ, ವಿಷಯ_ಮೌಲ್ಯ.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ಮಾಪನ_ಡೇಟಾ),str(ಸರ್ವರ್_ಮೂಲ)])
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR 서버시험.class',io.BytesIO((ಮಾಪನ_ಡೇಟಾ/'서버시험.class').read_bytes()))
            ಪ್ರಕ್ರಿಯೆ.stdin.write('java 서버시험\n'.encode());ಪ್ರಕ್ರಿಯೆ.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',ಸರ್ವರ್_ಸ್ಟ್ರೀಮ್_ಪೋರ್ಟ್),timeout=5) as ಪೀರ್_ಮೌಲ್ಯ:
                ಪೀರ್_ಮೌಲ್ಯ.sendall(b'A');assert ಪೀರ್_ಮೌಲ್ಯ.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as ಪೀರ್_ಮೌಲ್ಯ:
                ಪೀರ್_ಮೌಲ್ಯ.settimeout(5);ಪೀರ್_ಮೌಲ್ಯ.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert ಪೀರ್_ಮೌಲ್ಯ.recvfrom(512)[0]==b'UDP-IN'
            ಪಠ್ಯ=수신하기();assert 'INBOUND TCP UDP PASS' in ಪಠ್ಯ and 'exit 0' in ಪಠ್ಯ,ಪಠ್ಯ
            ದೃಢೀಕರಣ_ವರದಿ['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } ಕನ್ನಡ.자체.ಔಟ್_ಪುಟ್.수쓰기(합); ಕನ್ನಡ.자체.ಕಡತ.ಬರೆ("aot.txt", "한글 AOT ಕಡತ 😀"); ಕನ್ನಡ.자체.ಔಟ್_ಪುಟ್.ಬರೆ_ಸಾಲು(ಕನ್ನಡ.자체.ಕಡತ.ಓದು("aot.txt")); } }'
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            ಪಠ್ಯ = ಶೆಲ್('javac 빛.java'); assert 'exit 0' in ಪಠ್ಯ and 'Compiled:' in ಪಠ್ಯ, ಪಠ್ಯ
            ಪಠ್ಯ = ಶೆಲ್('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ಪಠ್ಯ and 'exit 0' in ಪಠ್ಯ, ಪಠ್ಯ
            ಪಠ್ಯ = ಶೆಲ್('run 빛.elf'); assert '\n55\n' in ಪಠ್ಯ and '한글 AOT ಕಡತ 😀' in ಪಠ್ಯ and 'exit 0' in ಪಠ್ಯ, ಪಠ್ಯ
            자체실행파일 = bytearray(); ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            ಪಠ್ಯ = ಶೆಲ್('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in ಪಠ್ಯ and 'unsupported' in ಪಠ್ಯ, ಪಠ್ಯ
            보존자료 = bytearray(); ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            ಪಠ್ಯ = ಶೆಲ್('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ಪಠ್ಯ and 'exit 0' in ಪಠ್ಯ, ಪಠ್ಯ
            ಪಠ್ಯ = ಶೆಲ್('run 빛.elf'); assert '\n55\n' in ಪಠ್ಯ and '한글 AOT ಕಡತ 😀' in ಪಠ್ಯ and 'exit 0' in ಪಠ್ಯ, ಪಠ್ಯ
            ದೃಢೀಕರಣ_ವರದಿ['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            ದೃಢೀಕರಣ_ವರದಿ['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ಸ್ಥಾಯಿ_ಮೂಲ=ಮಾಪನ_ಡೇಟಾ/'정적시험.java'
            ಸ್ಥಾಯಿ_ಮೂಲ.write_text('''public class 정적시험 {
 static int ಬಿಂಬಿಸು_ಮೂಲ = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] ಮೌಲ್ಯ = new int[] {ಬಿಂಬಿಸು_ಮೂಲ, 합(10)};
  System.out.println(ಮೌಲ್ಯ[0] + ಮೌಲ್ಯ[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ಮಾಪನ_ಡೇಟಾ),str(ಸ್ಥಾಯಿ_ಮೂಲ)])
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR 정적시험.class',io.BytesIO((ಮಾಪನ_ಡೇಟಾ/'정적시험.class').read_bytes()))
            ಪಠ್ಯ=ಶೆಲ್('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in ಪಠ್ಯ,ಪಠ್ಯ
            ಪಠ್ಯ=ಶೆಲ್('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in ಪಠ್ಯ,ಪಠ್ಯ
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.delete('정적시험.class');ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.delete('정적시험.elf')
            ದೃಢೀಕರಣ_ವರದಿ['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(ಅರ್ಖೀವ್.getvalue());손상자료[14]^=1
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            ಪಠ್ಯ=ಶೆಲ್('java -jar 인사.jar');assert 'Main-Class\nexit 1' in ಪಠ್ಯ,ಪಠ್ಯ
            ದೃಢೀಕರಣ_ವರದಿ['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.quit(); assert 'FTP stopped' in ಶೆಲ್('ftpd stop')
            assert not ಸೇತುವೆ.ದೋಷ, ಸೇತುವೆ.ದೋಷ
            ದೃಢೀಕರಣ_ವರದಿ.update(passed=True, frames_to_guest=ಸೇತುವೆ.커널수신틀수, frames_from_guest=ಸೇತುವೆ.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in ಸೆಲೆಕ್ಟರ್.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            ಸೇತುವೆ.ವಿರಾಮ_ಸಂಗತಿ.set()
            ಪ್ರಕ್ರಿಯೆ.terminate()
            try: ಪ್ರಕ್ರಿಯೆ.wait(timeout=5)
            except subprocess.TimeoutExpired: ಪ್ರಕ್ರಿಯೆ.kill(); ಪ್ರಕ್ರಿಯೆ.wait()
            ಸೆಲೆಕ್ಟರ್.close(); ಪ್ರಕ್ರಿಯೆ.stdin.close(); ಪ್ರಕ್ರಿಯೆ.stdout.close()
            ದೃಢೀಕರಣ_ವರದಿ['bridge_error'] = ಸೇತುವೆ.ದೋಷ
            ದೃಢೀಕರಣ_ವರದಿ['frames_to_guest'] = ಸೇತುವೆ.커널수신틀수; ದೃಢೀಕರಣ_ವರದಿ['frames_from_guest'] = ಸೇತುವೆ.커널발신틀수
            (ಮಾಪನ_ಡೇಟಾ/'packets.json').write_text(json.dumps(ಸೇತುವೆ.ಟ್ರೇಸ್_ಲಾಗ್,indent=2)+'\n')
            (ಮಾಪನ_ಡೇಟಾ / 'serial.log').write_bytes(대화기록)
            (ಮಾಪನ_ಡೇಟಾ / 'report.json').write_text(json.dumps(ದೃಢೀಕರಣ_ವರದಿ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': ಚಲಾಯಿಸು_2()
