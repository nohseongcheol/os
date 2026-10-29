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
from ਨੈਟਵਰਕ_ਬਰਿਜ import ਨੈਟਵਰਕ_ਬਰਿਜ
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ, ਕਮਾਂਡ
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def ਚਲਾਓ_2():
    ਮਾਪ_ਸਮੱਗਰੀ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/verification/ftp'; ਮਾਪ_ਸਮੱਗਰੀ.mkdir(parents=True, exist_ok=True)
    ਮਾਨਤਾ_ਵਿਵਰਨ = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = ਮਾਪ_ਸਮੱਗਰੀ / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] ਆਰਗੂਮੈਂਟ) throws Exception { ਪੰਜਾਬੀ.자체.ਆਉਟਪੁੱਟ.ਲਿੱਖੋ_ਕਤਾਰ("JAR ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼: " + ਆਰਗੂਮੈਂਟ[0]); ਪੰਜਾਬੀ.자체.ਫਾਇਲ.ਲਿਖਣ("jar.txt", "자체 ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ ਫਾਇਲ"); ਪੰਜਾਬੀ.자체.ਆਉਟਪੁੱਟ.ਲਿੱਖੋ_ਕਤਾਰ(ਪੰਜਾਬੀ.자체.ਫਾਇਲ.ਪੜ੍ਹਨ("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/java-library/classes'), '-d', str(ਮਾਪ_ਸਮੱਗਰੀ), str(자바원문)])
    ਸੰਗ੍ਰਹਿ = io.BytesIO()
    with zipfile.ZipFile(ਸੰਗ੍ਰਹਿ, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(ਮਾਪ_ਸਮੱਗਰੀ/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); ਸਰਵਰ_ਸਟ੍ਰੀਮ_ਪੋਰਟ = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with ਨੈਟਵਰਕ_ਬਰਿਜ(접속번호, ['tcp:{}:9300'.format(ਸਰਵਰ_ਸਟ੍ਰੀਮ_ਪੋਰਟ), 'udp:{}:9301'.format(서버전문접속번호)], ਪਕੜਨਾ=True) as ਬਰਿਜ:
        ਪਰੋਸੈੱਸ = subprocess.Popen(ਕਮਾਂਡ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ਬਰਿਜ.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        ਚੋਣਕਰਤਾ = selectors.DefaultSelector(); ਚੋਣਕਰਤਾ.register(ਪਰੋਸੈੱਸ.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            ਸਮੱਗਰੀ = bytearray(); ਅੰਤ_ਔਫਸੈਟ = time.monotonic() + 시간제한
            while 확인표시 not in ਸਮੱਗਰੀ:
                if time.monotonic() > ਅੰਤ_ਔਫਸੈਟ or ਪਰੋਸੈੱਸ.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + ਸਮੱਗਰੀ.decode('utf-8', 'replace'))
                for 누름값, _ in ਚੋਣਕਰਤਾ.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: ਸਮੱਗਰੀ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ਸਮੱਗਰੀ or b'FAIL ' in ਸਮੱਗਰੀ: raise AssertionError(ਸਮੱਗਰੀ)
            return ਸਮੱਗਰੀ.decode('utf-8', 'replace').replace('\r\n', '\n')
        def ਸ਼ੈਲ(ਲਾਈਨ):
            ਪਰੋਸੈੱਸ.stdin.write(ਲਾਈਨ.encode() + b'\n'); ਪਰੋਸੈੱਸ.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in ਸ਼ੈਲ('ftpd start')
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ = ftplib.FTP(); ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.encoding = 'utf-8'; ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.connect('127.0.0.1', 접속번호, timeout=20); ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.login()
            ਪੇਲੋਡ_ਸਮੱਗਰੀ = bytes(range(256)) * 32
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR binary.dat', io.BytesIO(ਪੇਲੋਡ_ਸਮੱਗਰੀ))
            ਮਾਪ = bytearray(); ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.retrbinary('RETR binary.dat', ਮਾਪ.extend)
            assert ਮਾਪ == ਪੇਲੋਡ_ਸਮੱਗਰੀ; assert ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.size('binary.dat') == len(ਪੇਲੋਡ_ਸਮੱਗਰੀ)
            ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in ਸ਼ੈਲ('cat 한글.txt')
            assert '한글.txt' in ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.nlst()
            assert dict(ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            ਮਾਪ = bytearray(); ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.retrbinary('RETR binary.dat', ਮਾਪ.extend); assert ਮਾਪ == ਪੇਲੋਡ_ਸਮੱਗਰੀ
            ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('oversized replacement rejected; previous file preserved')
            with ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.transfercmd('STOR pending.txt') as ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ:
                # A control command must not change the active upload's destination.
                assert ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.size('binary.dat') == len(ਪੇਲੋਡ_ਸਮੱਗਰੀ)
                ਅਪਲੋਡ_ਕਰੋ_ਫ਼ਾਈਲਾਂ.sendall(b'UPLOAD TARGET PRESERVED')
            assert ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.voidresp().startswith('226')
            ਮਾਪ = bytearray(); ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.retrbinary('RETR pending.txt', ਮਾਪ.extend)
            assert ਮਾਪ == b'UPLOAD TARGET PRESERVED'
            ਮਾਪ = bytearray(); ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.retrbinary('RETR binary.dat', ਮਾਪ.extend)
            assert ਮਾਪ == ਪੇਲੋਡ_ਸਮੱਗਰੀ
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.delete('pending.txt')
            ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR 인사.jar', io.BytesIO(ਸੰਗ੍ਰਹਿ.getvalue()))
            ਟੈਕਸਟ = ਸ਼ੈਲ('java -jar 인사.jar 누리')
            assert 'JAR ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼: 누리' in ਟੈਕਸਟ and '자체 ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ ਫਾਇਲ' in ਟੈਕਸਟ and 'exit 0' in ਟੈਕਸਟ, ਟੈਕਸਟ
            ਟੈਕਸਟ = ਸ਼ੈਲ('./인사.jar 세상')
            assert 'JAR ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼: 세상' in ਟੈਕਸਟ and 'exit 0' in ਟੈਕਸਟ, ਟੈਕਸਟ
            ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct ਸਮੱਗਰੀ { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct ਸਮੱਗਰੀ ਕੀਮਤ = {합(10), 1.25}; if (ਕੀਮਤ.수 != 55 || ਕੀਮਤ.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = ਖੋਲੋ_ਲਿਖਤ_ਪੱਤਰ("cc.txt", ਪੜ੍ਹਨ_ਲਿਖਣ | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; ਲਿੱਖੋ_ਲਿਖਤ_ਪੱਤਰ_ਸਮੱਗਰੀ(문서, 인사, sizeof(인사)-1); ਬੰਦ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ(문서); ਲਿੱਖੋ_ਲਿਖਤ_ਪੱਤਰ_ਸਮੱਗਰੀ(1, 인사, sizeof(인사)-1); return 0; }\n'
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            ਟੈਕਸਟ = ਸ਼ੈਲ('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in ਟੈਕਸਟ and 'exit 0' in ਟੈਕਸਟ, ਟੈਕਸਟ
            ਟੈਕਸਟ = ਸ਼ੈਲ('run 한글.elf'); assert 'CC NATIVE PASS' in ਟੈਕਸਟ and 'exit 0' in ਟੈਕਸਟ, ਟੈਕਸਟ
            assert 'CC NATIVE PASS' in ਸ਼ੈਲ('cat cc.txt')
            실행파일 = bytearray(); ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR ਇਨਸਟੈਂਸ_ਕੀਮਤ.elf', io.BytesIO(실행파일)); ਟੈਕਸਟ = ਸ਼ੈਲ('run ਇਨਸਟੈਂਸ_ਕੀਮਤ.elf'); assert 'CC NATIVE PASS' in ਟੈਕਸਟ and 'exit 0' in ਟੈਕਸਟ, ਟੈਕਸਟ
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼', io.BytesIO(실행파일)); ਟੈਕਸਟ=ਸ਼ੈਲ('./ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼');assert 'CC NATIVE PASS' in ਟੈਕਸਟ and 'exit 0' in ਟੈਕਸਟ,ਟੈਕਸਟ
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR ਨਾਂ.txt', io.BytesIO(실행파일)); ਟੈਕਸਟ=ਸ਼ੈਲ('./ਨਾਂ.txt');assert 'CC NATIVE PASS' in ਟੈਕਸਟ and 'exit 0' in ਟੈਕਸਟ,ਟੈਕਸਟ
            ਸ਼ੈਲ('rm ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ ਨਾਂ.txt')
            ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            ਸ਼ੈਲ('rm binary.dat 한글.txt 한글.c 한글.elf ਇਨਸਟੈਂਸ_ਕੀਮਤ.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(ਮਾਪ_ਸਮੱਗਰੀ/'linux-reference')
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            ਟੈਕਸਟ=ਸ਼ੈਲ('./리눅스인사');assert 'exit -8' in ਟੈਕਸਟ,ਟੈਕਸਟ
            ਟੈਕਸਟ=ਸ਼ੈਲ('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in ਟੈਕਸਟ,ਟੈਕਸਟ
            assert 'LINUX ELF FILE IO' in ਸ਼ੈਲ('cat linux.txt')
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.delete('리눅스인사');ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.delete('linux.txt')
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in ਸ਼ੈਲ('./거짓.elf');ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.delete('거짓.elf')
            ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = ਮਾਪ_ਸਮੱਗਰੀ/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket ਕੁਨੈਕਸ਼ਨ_ਕਰੋ = ਪੰਜਾਬੀ.자체.연결통신.ਕੁਨੈਕਸ਼ਨ_ਕਰੋ("10.0.2.2", Integer.parseInt(args[0]));
 ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ਸਰੋਤ = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ਸਰੋਤ.length;i++) if (ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.getInputStream().read() != (ਸਰੋਤ[i]&255)) throw new RuntimeException("TCP mismatch");
 ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.close();
 DatagramSocket 종단 = ਪੰਜਾਬੀ.자체.통신.ਖੋਲ੍ਹੋ(0); ਪੰਜਾਬੀ.자체.통신.ਸਮਾਂ_ਸਮਾਪਤ(종단, 500);
 ਪੰਜਾਬੀ.자체.통신.ਈਮੇਲ(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!ਪੰਜਾਬੀ.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/java-library/classes'),'-d',str(ਮਾਪ_ਸਮੱਗਰੀ),str(통신원문)])
                ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR 바깥통신.class', io.BytesIO((ਮਾਪ_ਸਮੱਗਰੀ/'바깥통신.class').read_bytes()))
                ਟੈਕਸਟ = ਸ਼ੈਲ('java 바깥통신 {} {}'.format(되돌림서버항목.ਸੰਚਾਰ_ਰੋਕ_ਤਰੀਕਾ_ਪੋਰਟ, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in ਟੈਕਸਟ and '10.0.2.2' in ਟੈਕਸਟ and 'exit 0' in ਟੈਕਸਟ, ਟੈਕਸਟ
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.delete('바깥통신.class')
            ਸਰਵਰ_ਸਰੋਤ=ਮਾਪ_ਸਮੱਗਰੀ/'서버시험.java'
            ਸਰਵਰ_ਸਰੋਤ.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket ਸਰਵਰ_ਕੀਮਤ = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket ਗੈਸਟ_ਕੀਮਤ = ਸਰਵਰ_ਕੀਮਤ.accept();
  ਗੈਸਟ_ਕੀਮਤ.getOutputStream().write(ਗੈਸਟ_ਕੀਮਤ.getInputStream().read()+1); ਗੈਸਟ_ਕੀਮਤ.close(); ਸਰਵਰ_ਕੀਮਤ.close();
  byte[] ਤਤਕਰਾ_ਕੀਮਤ = new byte[8]; DatagramPacket 전문 = new DatagramPacket(ਤਤਕਰਾ_ਕੀਮਤ, ਤਤਕਰਾ_ਕੀਮਤ.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ਮਾਪ_ਸਮੱਗਰੀ),str(ਸਰਵਰ_ਸਰੋਤ)])
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR 서버시험.class',io.BytesIO((ਮਾਪ_ਸਮੱਗਰੀ/'서버시험.class').read_bytes()))
            ਪਰੋਸੈੱਸ.stdin.write('java 서버시험\n'.encode());ਪਰੋਸੈੱਸ.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',ਸਰਵਰ_ਸਟ੍ਰੀਮ_ਪੋਰਟ),timeout=5) as ਪਿਅਰ_ਕੀਮਤ:
                ਪਿਅਰ_ਕੀਮਤ.sendall(b'A');assert ਪਿਅਰ_ਕੀਮਤ.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as ਪਿਅਰ_ਕੀਮਤ:
                ਪਿਅਰ_ਕੀਮਤ.settimeout(5);ਪਿਅਰ_ਕੀਮਤ.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert ਪਿਅਰ_ਕੀਮਤ.recvfrom(512)[0]==b'UDP-IN'
            ਟੈਕਸਟ=수신하기();assert 'INBOUND TCP UDP PASS' in ਟੈਕਸਟ and 'exit 0' in ਟੈਕਸਟ,ਟੈਕਸਟ
            ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] ਆਰਗੂਮੈਂਟ) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } ਪੰਜਾਬੀ.자체.ਆਉਟਪੁੱਟ.수쓰기(합); ਪੰਜਾਬੀ.자체.ਫਾਇਲ.ਲਿਖਣ("aot.txt", "한글 AOT ਫਾਇਲ 😀"); ਪੰਜਾਬੀ.자체.ਆਉਟਪੁੱਟ.ਲਿੱਖੋ_ਕਤਾਰ(ਪੰਜਾਬੀ.자체.ਫਾਇਲ.ਪੜ੍ਹਨ("aot.txt")); } }'
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            ਟੈਕਸਟ = ਸ਼ੈਲ('javac 빛.java'); assert 'exit 0' in ਟੈਕਸਟ and 'Compiled:' in ਟੈਕਸਟ, ਟੈਕਸਟ
            ਟੈਕਸਟ = ਸ਼ੈਲ('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ਟੈਕਸਟ and 'exit 0' in ਟੈਕਸਟ, ਟੈਕਸਟ
            ਟੈਕਸਟ = ਸ਼ੈਲ('run 빛.elf'); assert '\n55\n' in ਟੈਕਸਟ and '한글 AOT ਫਾਇਲ 😀' in ਟੈਕਸਟ and 'exit 0' in ਟੈਕਸਟ, ਟੈਕਸਟ
            자체실행파일 = bytearray(); ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            ਟੈਕਸਟ = ਸ਼ੈਲ('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in ਟੈਕਸਟ and 'unsupported' in ਟੈਕਸਟ, ਟੈਕਸਟ
            보존자료 = bytearray(); ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            ਟੈਕਸਟ = ਸ਼ੈਲ('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ਟੈਕਸਟ and 'exit 0' in ਟੈਕਸਟ, ਟੈਕਸਟ
            ਟੈਕਸਟ = ਸ਼ੈਲ('run 빛.elf'); assert '\n55\n' in ਟੈਕਸਟ and '한글 AOT ਫਾਇਲ 😀' in ਟੈਕਸਟ and 'exit 0' in ਟੈਕਸਟ, ਟੈਕਸਟ
            ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ਸਥਾਈ_ਸਰੋਤ=ਮਾਪ_ਸਮੱਗਰੀ/'정적시험.java'
            ਸਥਾਈ_ਸਰੋਤ.write_text('''public class 정적시험 {
 static int ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] ਆਰਗੂਮੈਂਟ) {
  int[] ਕੀਮਤ = new int[] {ਪ੍ਰੋਜੈਕਟ_ਰੂਟ, 합(10)};
  System.out.println(ਕੀਮਤ[0] + ਕੀਮਤ[1]); System.out.println(ਆਰਗੂਮੈਂਟ[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ਮਾਪ_ਸਮੱਗਰੀ),str(ਸਥਾਈ_ਸਰੋਤ)])
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR 정적시험.class',io.BytesIO((ਮਾਪ_ਸਮੱਗਰੀ/'정적시험.class').read_bytes()))
            ਟੈਕਸਟ=ਸ਼ੈਲ('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in ਟੈਕਸਟ,ਟੈਕਸਟ
            ਟੈਕਸਟ=ਸ਼ੈਲ('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in ਟੈਕਸਟ,ਟੈਕਸਟ
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.delete('정적시험.class');ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.delete('정적시험.elf')
            ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(ਸੰਗ੍ਰਹਿ.getvalue());손상자료[14]^=1
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            ਟੈਕਸਟ=ਸ਼ੈਲ('java -jar 인사.jar');assert 'Main-Class\nexit 1' in ਟੈਕਸਟ,ਟੈਕਸਟ
            ਮਾਨਤਾ_ਵਿਵਰਨ['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.quit(); assert 'FTP stopped' in ਸ਼ੈਲ('ftpd stop')
            assert not ਬਰਿਜ.ਗਲਤੀ, ਬਰਿਜ.ਗਲਤੀ
            ਮਾਨਤਾ_ਵਿਵਰਨ.update(passed=True, frames_to_guest=ਬਰਿਜ.커널수신틀수, frames_from_guest=ਬਰਿਜ.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in ਚੋਣਕਰਤਾ.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            ਬਰਿਜ.ਰੁਕਣਾ_ਇਵੈਂਟ.set()
            ਪਰੋਸੈੱਸ.terminate()
            try: ਪਰੋਸੈੱਸ.wait(timeout=5)
            except subprocess.TimeoutExpired: ਪਰੋਸੈੱਸ.kill(); ਪਰੋਸੈੱਸ.wait()
            ਚੋਣਕਰਤਾ.close(); ਪਰੋਸੈੱਸ.stdin.close(); ਪਰੋਸੈੱਸ.stdout.close()
            ਮਾਨਤਾ_ਵਿਵਰਨ['bridge_error'] = ਬਰਿਜ.ਗਲਤੀ
            ਮਾਨਤਾ_ਵਿਵਰਨ['frames_to_guest'] = ਬਰਿਜ.커널수신틀수; ਮਾਨਤਾ_ਵਿਵਰਨ['frames_from_guest'] = ਬਰਿਜ.커널발신틀수
            (ਮਾਪ_ਸਮੱਗਰੀ/'packets.json').write_text(json.dumps(ਬਰਿਜ.ਟਰੇਸ_ਲੌਗ,indent=2)+'\n')
            (ਮਾਪ_ਸਮੱਗਰੀ / 'serial.log').write_bytes(대화기록)
            (ਮਾਪ_ਸਮੱਗਰੀ / 'report.json').write_text(json.dumps(ਮਾਨਤਾ_ਵਿਵਰਨ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': ਚਲਾਓ_2()
